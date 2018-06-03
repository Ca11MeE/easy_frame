from mysql.binlog import ZipBinLog

class BinCache():

    _bin=''
    _file=''

    def __init__(self,file):
        # 初始化原始bin对象
        self._bin=ZipBinLog.zip_as_bin(file)
        self._file=file

    def chk_diff(self):
        print('check--->'+ self._file)
        return self._bin==ZipBinLog.zip_as_bin(self._file)