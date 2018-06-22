# coding: utf-8
# 商品列表
import mysql


class ShopGoodsBarrelController:
    def __init__(self):
        self.cursor = mysql.getDbObj(mysql.project_path + '/mappers/ShopGoodsBarrelMapper.xml',debug=False)

    def findUserByCode(self,code):
        result=self.cursor.exe_sql(methodName='findUserByCode',args=(code),pageInfo=None)
        return result