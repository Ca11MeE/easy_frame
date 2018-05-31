# 商品列表
import mysql
from mysql import Pool


class ShopGoodsController:

    def __init__(self):

        self.cursor=mysql.getDbObj(mysql.project_path+'/mappers/ShopGoodsMapper.xml')
        self.head_title_cursor = mysql.getDbObj(mysql.project_path + '/mappers/HeadTitle.xml')


    def findGoodsList(self,page,pageSize):
        pageInfo={}
        pageInfo['pageNum']=int(page)
        pageInfo['pageSize']=int(pageSize)
        return self.cursor.exeSQL('findGoodsList',pageInfo=pageInfo)

    def findGoodDetail(self,id):
        return self.cursor.exeSQL('findGoodDetail',args=(id),pageInfo=None)

    def findGoodIntroduction(self,id):
        return self.cursor.exeSQL('findGoodIntroduction',args=(id),pageInfo=None)

    def getHeadTitle(self):
        data = self.head_title_cursor.exeSQL(methodName='findHeadTitle', pageInfo=None)
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