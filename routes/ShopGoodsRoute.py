# coding: utf-8
# 启动类
from flask import request, Blueprint
import annotation
import boot
# from controller import ShopGoodsController
from annotation import AutoWired
from properties import IOCProp

"""
蓝图DEMO
author:CallMeE
date:2018-06-01
"""

# 此处定义蓝图前缀
url_prefix = None
app = Blueprint('app', __name__, url_prefix=url_prefix)

shop_good_rou = IOCProp.shop_good_rou

_SGCobj = None
_SGBobj=None


# 注入对象
# @AutoWired.InnerWired([ShopGoodsController.ShopGoodsController],a_w_list=['_SGCobj'],g=globals())
@AutoWired.OuterWired(shop_good_rou, g=globals())
def inject_obj():
    # for name in obj_list.keys():
    #     globals()[name]=AutoWired.get_obj(name)
    pass


inject_obj()


# 获取顶部标题栏
# @app.route('/tabs', methods=['GET', 'POST'])
@annotation.RequestMapping(app=app,path='/tabs',methods=['GET', 'POST'])
# @annotation.AutoParam()
@annotation.ResponseBody()
def hello():
    # print(a)
    # print(b)
    result = _SGCobj.getHeadTitle()
    return result


# 获取商品列表
@app.route('/shop/goods/list', methods=['post'])
@annotation.AutoParam()
@annotation.ResponseBody()
def getShopGoodsList(storeId):
    result = [_SGCobj.findGoodsList(cay_name='桶装水',store_id=storeId),_SGCobj.findGoodsList(cay_name='支装水',store_id=storeId),_SGCobj.findGoodsList(cay_name='空桶',store_id=storeId),_SGCobj.findGoodsList(cay_name='其他',store_id=storeId)]
    return result


# 获取商品详细信息
@app.route('/shop/goods/detail', methods=['post'])
@annotation.AutoParam()
@annotation.ResponseBody()
def getGoodDetail(id):
    result = _SGCobj.findGoodDetail(id)
    return result


# 获取商品描述
@app.route('/shop/goods/introduction', methods=['post'])
@annotation.AutoParam()
@annotation.ResponseBody()
def getGoodIntroduction(id):
    result = _SGCobj.findGoodIntroduction(id)
    return result


@app.route('/', methods=['get'])
def index():
    return '<button>点击一下吧</button>'

@app.route('/test', methods=['POST'])
@annotation.FullParam(kwarg_list=['args'])
@annotation.ResponseBody()
def test(args):
    return 'hello'+str(args)
