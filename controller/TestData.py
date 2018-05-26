# coding: utf-8
# 测试数据返回
import mysql

import os

def data():
    data = {"tabs": [{"name": "首页", "id": "1"},{"name": "首页", "id": "1"},{"name": "首页", "id": "1"},{"name": "首页", "id": "1"},{"name": "首页", "id": "1"},
                     {"name": "首页", "id": "1"},{"name": "首页", "id": "1"},{"name": "首页", "id": "1"},{"name": "首页", "id": "1"},{"name": "首页", "id": "1"},
                     {"name": "首页", "id": "1"},{"name": "首页", "id": "1"},{"name": "首页", "id": "1"},{"name": "首页", "id": "1"},{"name": "首页", "id": "1"},{"name": "首页", "id": "1"},
                     {"name": "首页", "id": "1"},{"name": "首页", "id": "1"},{"name": "首页", "id": "1"},{"name": "首页", "id": "1"},{"name": "首页", "id": "1"},{"name": "首页", "id": "1"},
                     {"name": "首页", "id": "1"}]}
    return data

def getHeadTitle():
    cursor=mysql.getDbObj(mysql.project_path+'/mappers/HeadTitle.xml')
    data=cursor.exeSQL(methodName='findHeadTitle',pageInfo=None)
    result={}
    result['tabs']=data
    return result


if'__main__'==__name__:
    getHeadTitle()