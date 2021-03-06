# coding: utf-8
# 商品列表
import mysql
from mysql import PageHelper


class ShopGoodsController:
    def __init__(self):
        self.cursor = mysql.getDbObj(mysql.project_path + '/mappers/ShopGoodsMapper.xml',debug=False)
        self.head_title_cursor = mysql.getDbObj(mysql.project_path + '/mappers/HeadTitle.xml')
        mysql.setObjUpdateRound(self.cursor, 1)
        mysql.setObjUpdateRound(self.head_title_cursor, 1)

    def findGoodsList(self, cay_name,store_id):
        return self.cursor.exe_sql(methodName='findGoodsList', args=(cay_name,store_id),pageInfo=None)

    def findGoodDetail(self, id):
        return self.cursor.exe_sql(methodName='findGoodDetail', args=(id), pageInfo=None)

    def findGoodIntroduction(self, id):
        return self.cursor.exe_sql(methodName='findGoodIntroduction', args=(id), pageInfo=None)

    def getHeadTitle(self):
        data = self.head_title_cursor.exe_sql(methodName='findHeadTitle', pageInfo=None)
        result = {}
        result['tabs'] = data
        return result

        # if '__main__'==__name__:
        #     print('加载数据库模块')
        #     mysql.pool = Pool.Pool()
        #     print('加载完毕')
        #     obj=ShopGoodsController()
        #     obj.findGoodsList('1','2')
        #     obj.findGoodDetail(('00531f90-2020-11e8-bfad-00163e0435bc'))
        #     obj.findGoodsList('1','2')
        #     obj.findGoodDetail(('00531f90-2020-11e8-bfad-00163e0435bc'))
