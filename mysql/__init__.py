# coding: utf-8
import reader
from mysql import Pool, Connection, PageHelper
import os
import re
import mysql.binlog
from mysql.binlog import Schued

"""
后续开发;
(完成)1.远程读取mapperxml
(完成)2.语句对象定时更新暂定为本地xml文件增量binlog更新,后续开发远程增量更新(流程未定)
    (完成)2.1本地binlog处理对比
    (完成)2.2远程binlog处理对比
(半完成)3.binlog生成算法以及对比算法以及增量写入
(完成)4.细粒度事务控制
5.配置文件配置连接数


单条语句执行demo:
# obj = getDbObj(project_path + '/mappers/ShopGoodsMapper.xml')
# setObjUpdateRound(obj, '2')
# obj.exe_sql("findGoodsList")

批量语句执行DEMO:
# obj=getDbObj(path=project_path +'/mysql/test.xml',debug=True)
# obj.exe_sql_obj_queue(queue_obj={"test":(1,2),"test":(2,3)})
或者
# obj.exe_sql_queue(method_queue=['test','test','test_s','test','test'],args_queue=[('1','2'),('2','3'),(),('3','4'),('3','4')])
"""
# 定义连接池实例
pool = None

# 定义项目路径
project_path = os.path.dirname(os.path.dirname(__file__))


class curObj:
    _page = False
    _db = None
    _cursor = None
    _conn = None
    _debug = False
    _cursor=None
    sql = reader.Mapper()

    def __init__(self, db, path, poolFlag, debug):
        self._debug = debug
        self._poolFlag = poolFlag
        if poolFlag:
            # 连接池实例化
            self._pool = db
        else:
            self._db = db
        self.sql.openDom(path)
        self._path = path
        self._sqls = self.sql.getTree()

    def refreash_sqls(self):
        global sql
        print(self._sqls)
        self.sql.openDom(self._path)
        self._sqls = self.sql.getTree()
        print(self._sqls)

    def check_conn(self,transaction=False):
        # if self._pool is not None:
        #     __conn = self._pool.getConn()
        # else:
        #     __conn = self._db
        # self._conn = __conn
        # self._db = __conn.getConnect()
        try:
            if not self._db:
                # 无连接,需要获取连接
                # print('没有发现连接,尝试获取连接')
                if self._poolFlag:
                    # 连接池
                    self._conn = self._pool.getConn()
                    self._db = self._conn.getConnect()
                else:
                    # 单个连接理论上只执行一次,过后直接关闭
                    self._db = Connection()
        except Exception as e:
            print(e)
            raise Exception('检查连接失败')

    # def setConn(self):
    #     if self._poolFlag:
    #         # 连接池实例化
    #         db =self._pool
    #     else:
    #         db = self._db
    #     __conn = db.getConn()
    #     self._conn = __conn
    #     self._db = __conn.getConnect()
    #
    #     # 单独连接实例化
    #     # 初始化指针
    #     self._cursor = self._db.cursor()

    def set_cursor(self):
        # 初始化指针(如果不存在指针)
        if not self._cursor:
            self._cursor = self._db.cursor()

    # 获取sql语句(包含处理)
    def get_sql(self, methodName, pageInfo, args=()):
        # 单独连接实例化
        # 判断是否存在子节点
        if methodName not in self._sqls:
            raise Exception('没有该方法!!!')
        _sql = self._sqls[methodName]
        # 判断是否分页(总开关)
        # 开启之后该实例所有语句都认为是 需要分页
        # 慎用!!!!
        if self._page:
            # 分页
            _sql = _sql + 'limit ' + str((self._pageNum - 1) * self._pageSize) + ',' + str(self._pageSize)
        if pageInfo:
            # print(pageInfo)
            # print(pageInfo['pageNum'])
            # print(pageInfo['pageSize'])
            # 分页
            _sql = _sql + PageHelper.depkg_page_info(pageInfo)
        # print(_sql)
        # 判断是否骨架拼接
        if args:
            _sql = _sql % args[:]
        # 去除注释与空格,换行等
        __sql = re.sub('\\s+', ' ', re.sub('<!--.*-->', ' ', _sql))
        return __sql

    # 设定分页信息
    def set_page(self, pageNum, pageSize):
        self._pageNum = pageNum
        self._pageSize = pageSize
        self._page = True

    def initial_page(self):
        self._page = False


    # 批量执行语句(整体版)
    """
    queue_obj中key为方法名,value为参数
    注意!!!!
    对于一个业务来说,一个sql方法只使用一次(因为有内部数据缓存)
    若其中有重复方法,建议用分割版
    """
    def exe_sql_obj_queue(self,queue_obj={}):
        if queue_obj:
            methods=list(queue_obj.keys())
            args=list(queue_obj.values())
            self.exe_sql_queue(method_queue=methods,args_queue=args)
        else:
            raise Exception('queue_obj参数不正确')

    # 批量执行语句(拆分版)
    """
    method_queue中存放顺序执行的sql方法名[str]
    args_queue中存放对应下标方法的参数元组[()]
    若其中包含select无条件参数语句,请用空元组()占位
    """
    def exe_sql_queue(self,method_queue=[],args_queue=[]):
        # 参数检查
        if not method_queue:
            raise Exception('语句方法为空')
            return
        if not args_queue:
            raise Exception('语句参数列表为空')
            return
        self.check_conn()
        self.set_cursor()
        try:
            # 开启事务
            # self._db.begin()
            # 批量取语句(以方法名为准,多于参数队列元素将丢弃)
            while method_queue:
                method=method_queue.pop(0)
                args=args_queue.pop(0)
                """
                对于增改查来说,并不需要分页,参数列表是必须的
                """
                _sql=self.get_sql(methodName=method,args=args,pageInfo=None)
                print(self._cursor)
                # 执行sql语句
                self._cursor.execute(_sql)
                # 调试模式打印语句
                if self._debug:
                    print_debug(methodName=method, args=args, sql=_sql, result=self._cursor.rowcount)
            # 事务提交(pymysql要求除查询外所有语句必须手动提交)
        except Exception as e:
            print(e)
            self._db.rollback()
            print('事务回滚'+str(method_queue))
        else:
            self._db.commit()
            print('事务提交' + str(method_queue))

        # 关闭连接
        self.close()


    # 执行单条语句
    # 防报错参数设定默认值
    def exe_sql(self, methodName='', pageInfo=None, args=()):
        # 参数检查
        if not re.sub('\s+','',methodName):
            raise Exception('语句方法为空')
            return
        self.check_conn()
        self.set_cursor()
        # 定义返回结果集
        result = []
        try:
            # print(pageInfo)
            if pageInfo and type(pageInfo) is type({}):
                _sql = self.get_sql(methodName=methodName, pageInfo=pageInfo, args=args)
            else:
                _sql = self.get_sql(methodName=methodName, args=args, pageInfo=None)
        except Exception as ex:
            print(ex)
            return result
        try:
            # 试执行语句
            self._cursor.execute(_sql)
            # 为了保障新增以及修改的操作可以生效而提交事务
            if 'select' not in _sql and 'SELECT' not in _sql:
                # print('不是查询!!')
                self._db.commit()
            else:
                # 回复分页状态
                self.initial_page()
        except Exception as e:
            self._db.rollback()
            print("执行出错,错误信息为:", e)
            return result
        # cursor.execute('select * from mw_system_member_level')

        data = self._cursor.fetchall()

        # print(data)

        description = self._cursor.description

        # print(description)

        result = sort_result(data, description, result)

        # print(data)
        # print(result)
        # 关闭连接
        self.close()
        # 调试模式语句执行信息打印
        if self._debug:
            print_debug(methodName=methodName, args=args, sql=_sql, result=result)
        return result

    def close(self):
        # print('关闭连接')
        self._cursor.close()
        if self._poolFlag:
            # 为连接池定义
            pool.closeConn(self._conn)
            # 归还连接后清除指针
            self._cursor = None
            self._db = None
            self._conn = None
        else:
            # 为单独连接定义
            self._db.close()

    # 定义插入更新器方法
    def insert_to_update_dispacther(self, millionSecond):
        if isinstance(millionSecond, int):
            w_time = millionSecond
            pass
        else:
            try:
                w_time = int(millionSecond)
            except Exception as e:
                print(e)

        # 此处为增量更新代码
        '''
        临时思路
        1.设定定时间隔
        2.传入当前语句对象
        3.内部压缩保存binlog
        4.定时完毕重新获取语句,获取新语句对象binlog
        5.对比binlog
            5.1若更新后binog无差异则不作处理
            5.2若存在差异,替换语句对象
        '''
        self._bin_cache = mysql.binlog.BinCache(self._path)
        # 添加变更处理
        self._bin_cache.set_false_fun(self.refreash_sqls)
        # 调度器添加任务
        Schued.sech_obj(fun=self._bin_cache.chk_diff, delay=w_time).enter()


# 整理结果集并返回
def sort_result(data, description, result):
    for index in range(len(data)):
        item = data[index]
        r_item = {}
        for i in range(len(item)):
            colName = description[i][0]
            val = item[i]
            # print(type(val))
            value = 'none'
            if type(val) is not type(None):
                value = str(val)
            # print(type(value))
            # print(colName + ':' + value +',')
            # 组装data
            r_item[colName] = value
            # print(description[i][0])
            # print(r_item)
        # print('\n')
        # 组装结果集
        result.append(r_item)
    return result


def getDbObj(path, debug=False):
    if pool is None:
        raise Exception('连接池未定义')
    if 0 >= pool.size():
        # 配置属性生命周期过短,拟用__import__导入减轻内存废址
        prop = __import__('properties')
        if hasattr(prop,'pool_conn_num'):
            pool.initPool(getattr(prop,'pool_conn_num'), Connection.Connection)
        else:
            # 初始5个连接
            pool.initPool(5, Connection.Connection)

    return curObj(pool, path, True, debug)


def setObjUpdateRound(obj, milllionSecond):
    if isinstance(obj, curObj):
        obj.insert_to_update_dispacther(milllionSecond)
    else:
        raise Exception('类型错误!!!!')

# 调试模式下的打印
def print_debug(methodName, sql, args, result):
    print('METHOD:==>' + methodName)
    print('SQL:=====>' + sql)
    print('PARAMS:==>' + str(args))
    # 拿出列名
    print('ROWS:====>' + str(list(result[0].keys())))
    print('RESULT:==>' + str(list(result[0].values())))
    for r in result[1:]:
        print('=========>' + str(list(r.values())))


from mysql import remote

if '__main__' == __name__:
    # print('加载数据库模块')
    pool = Pool.Pool()
    # print('加载完毕')
    obj=getDbObj(path=project_path +'/mysql/test.xml',debug=True)
    obj.exe_sql_obj_queue(queue_obj={"test":(1,2),"test":(2,3)})
    obj.exe_sql_queue(method_queue=['test','test','test_s','test','test'],args_queue=[('1','2'),('2','3'),(),('3','4'),('3','4')])
    obj = getDbObj(project_path + '/mappers/ShopGoodsMapper.xml')
    setObjUpdateRound(obj, '2')
    obj.exe_sql("findGoodsList")

    remote_cell = remote.getCell('ShopGoodsMapper.xml',
                                 remote_path='http://127.0.0.1:8400/member/export/xml/ShopGoodsMapper.xml')
    remote_cell.reload_file_round(1)
    obj1 = getDbObj(remote_cell.getPath(), debug=True)
    obj1.insert_to_update_dispacther(3)
    obj1.exe_sql("findGoodsList")

    # a=obj.exe_sql(methodName='findGoodIntroduction', args=('111'), pageInfo=None)
