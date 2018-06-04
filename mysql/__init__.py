import pymysql
import reader
from mysql import Pool, Connection, PageHelper
import os
import re
import mysql.binlog
from mysql.binlog import Schued

"""
后续开发;
1.远程读取mapperxm
2.语句对象定时更新暂定为本地xml文件增量binlog更新,后续开发远程增量更新(流程未定)
    2.1本地binlog处理对比
    2.2远程binlog处理对比
3.binlog生成算法以及对比算法以及增量写入
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

    def checkConn(self):
        # if self._pool is not None:
        #     __conn = self._pool.getConn()
        # else:
        #     __conn = self._db
        # self._conn = __conn
        # self._db = __conn.getConnect()
        try:
            if self._db is None:
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

    # 获取sql语句(包含处理)
    def getSQL(self, methodName, pageInfo, args=()):
        self.checkConn()
        # 单独连接实例化
        # 初始化指针
        self._cursor = self._db.cursor()
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
        if pageInfo is not None:
            # print(pageInfo)
            # print(pageInfo['pageNum'])
            # print(pageInfo['pageSize'])
            # 分页
            _sql = _sql + PageHelper.depkg_page_info(pageInfo)
        # print(_sql)
        # 判断是否骨架拼接
        if args is not None and 0 < len(args):
            _sql = _sql % args[:]
        # 去除注释与空格,换行等
        __sql = re.sub('\\s+', ' ', re.sub('<!--.*-->', ' ', _sql))
        return __sql

    # 设定分页信息
    def setPage(self, pageNum, pageSize):
        self._pageNum = pageNum
        self._pageSize = pageSize
        self._page = True

    def initialPage(self):
        self._page = False

    def exeSQL(self, methodName, pageInfo=None, args=()):
        # 定义返回结果集
        result = []
        try:
            # print(pageInfo)
            if pageInfo is not None and type(pageInfo) is type({}):
                _sql = self.getSQL(methodName=methodName, pageInfo=pageInfo, args=args)
            else:
                _sql = self.getSQL(methodName=methodName, args=args, pageInfo=None)
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
                self.initialPage()
        except Exception as e:
            print("执行出错,错误信息为:", e)
            return result
        # cursor.execute('select * from mw_system_member_level')

        data = self._cursor.fetchall()

        # print(data)

        description = self._cursor.description

        # print(description)

        result = sortResult(data, description, result)

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
        if self._poolFlag:
            # 为连接池定义
            pool.closeConn(self._conn)
            # 归还连接后清除指针
            self._db = None
            self._conn = None
        else:
            # 为单独连接定义
            self._db.close()

    # 定义插入更新器方法
    def insertToUpdateDispacther(self, millionSecond):
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
def sortResult(data, description, result):
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
        pool.initPool(5, Connection.Connection)
    return curObj(pool, path, True, debug)


def setObjUpdateRound(obj, milllionSecond):
    if isinstance(obj, curObj):
        obj.insertToUpdateDispacther(milllionSecond)
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


import mysql.remote as remote

if '__main__' == __name__:
    print('加载数据库模块')
    pool = Pool.Pool()
    print('加载完毕')
    obj = getDbObj(project_path + '/mappers/ShopGoodsMapper.xml')
    # setObjUpdateRound(obj, '2')
    obj.exeSQL("findGoodsList")

    remote_cell = remote.getCell('ShopGoodsMapper.xml',
                                 remote_path='http://127.0.0.1:8400/member/export/xml/ShopGoodsMapper.xml')
    remote_cell.reload_file_round(1)
    obj1 = getDbObj(remote_cell.getPath(), debug=True)
    obj1.insertToUpdateDispacther(3)
    obj1.exeSQL("findGoodsList")

    # a=obj.exeSQL(methodName='findGoodIntroduction', args=('111'), pageInfo=None)
