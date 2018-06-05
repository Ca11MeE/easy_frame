# coding: utf-8
# 连接包装类
import pymysql

"""
mysql连接实例(半成品)

待实现:;
1.配置文件配置连接属性
author:CallMeE
date:2018-06-01
"""


class Connection:
    _host = 'bdm238721578.my3w.com'
    _user = 'bdm238721578'
    _pwd = 'ealohu31841'
    _db = 'bdm238721578_db'

    def __init__(self, __host=_host, __user=_user, __pwd=_pwd, __db=_db):
        # print('初始化连接')
        self._db = pymysql.connect(__host, __user, __pwd, __db, charset='utf8')
        # self._db = pymysql.connect('localhost', 'root', 'wo4ce4kumima', 'agymall_db', charset='utf8')

    def getConnect(self):
        return self._db

    def testConn(self):
        try:
            self._db.ping()
            return True
        except:
            return False

    def reConn(self):
        # print('重连接')
        self._db = pymysql.connect(self._host, self._user, self._pwd, self._db, charset='utf8')
