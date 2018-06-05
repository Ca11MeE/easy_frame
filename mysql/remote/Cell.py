from urllib import request
import uuid,os,mysql,time
import mysql.binlog.Schued as schued


class cell():

    def __init__(self,file_name='',remote_path=''):
        self._file_name=file_name
        self._remote_path=remote_path
        self._uid = uuid.uuid5(uuid.NAMESPACE_DNS, file_name)
        # 创建临时文件夹(安全性考虑，采用多层目录)
        self._file_path=mysql.project_path + sort_path(self._uid)
        # 检查路径
        if os.path.exists(self._file_path):
            pass
        else:
            os.makedirs(self._file_path)
        while True:
            # 下载远程文件
            try:
                response=request.urlretrieve(url=remote_path,filename=self._file_path+'/'+self._file_name)
                print('加载远程mapper：' + response[0])
                # 放置路径
                self._abs_path = response[0]
                break
            except:
                print('连接远程计算机失败,请检查连接,3秒后重试('+str(id(self))+')')
                time.sleep(3)


    # 重新加载文件
    def reload_file(self):
        response = request.urlretrieve(url=self._remote_path, filename=self._file_path + '/' + self._file_name)
        print('加载远程mapper：' + response[0])
        # 放置路径
        self._abs_path = response[0]
        # 链式调用（非必需）
        return self

    # 进入调度定时更新文件
    def reload_file_round(self,minute):
        schued.sech_obj(self.reload_file,minute*60).enter()
        # 链式调用（非必需）
        return self

    # 获取下载文件路径
    def getPath(self):
        return self._abs_path

    # 另一种方式获取路径
    def __str__(self):
        return self.getPath()


def sort_path(path_str):
    result='/.mapper'
    for s in str(path_str):
        result=result+'/'+s
    return result


# 工厂模式获取实例
def get_cell(file_name,remote_path):
    return cell(file_name=file_name,remote_path=remote_path)