# coding: utf-8
#  连接
from mysql import Connection

"""
连接池
author:CallMeE
date:2018-06-01
"""


class Pool():
    _size = 0

    # 初始化连接池
    def initPool(self, num, Conn):
        _pool = []
        self._Conn = Conn
        for item_c in range(num):
            # 遍历定义连接放入连接池
            conn = Conn()
            _pool.append(conn)
        self._pool = _pool
        self._size = num
        # print(_pool)
        # print(self)

    def __init__(self):
        print('初始化连接池')

    # 定义取出连接
    def getConn(self):
        __pool = self._pool
        if __pool:
            currConn = __pool.pop(0)
            if currConn.testConn():
                # 连接有效
                # print('连接有效')
                # 不作处理
                pass
            else:
                print('连接无效')
                currConn.reConn()

            return currConn
        else:
            # 连接数不足则新增连接
            conn = Connection.Connection()
            self._pool.append(conn)

    # 定义归还连接
    def closeConn(self, conn):
        # print(self._pool)
        self._pool.append(conn)
        # print(self._pool)

    # 定义查询连接池连接数
    def size(self):
        return self._size
