from urllib import request
import uuid,os,mysql
import mysql.binlog.Schued as schued


class cell():

    def __init__(self,file_name='',remote_path=''):
        self._file_name=file_name
        self._remote_path=remote_path
        self._uid = uuid.uuid5(uuid.NAMESPACE_DNS, file_name)
        # 创建临时文件夹
        self._file_path=mysql.project_path + '/'+str(self._uid)
        # 检查路径
        if os.path.exists(self._file_path):
            pass
        else:
            os.mkdir(self._file_path)
        # 下载远程文件
        response=request.urlretrieve(url=remote_path,filename=self._file_path+'/'+self._file_name)
        print(response[0])
        # 放置路径
        self._abs_path=response[0]

    # 重新加载文件
    def reload_file(self):
        response = request.urlretrieve(url=self._remote_path, filename=self._file_path + '/' + self._file_name)
        print(response[0])
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


# 工厂模式获取实例
def get_cell(file_name,remote_path):
    return cell(file_name=file_name,remote_path=remote_path)