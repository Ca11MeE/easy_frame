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

obj_list = IOCProp.obj_list

_SGCobj = None


# 注入对象
# @AutoWired.InnerWired([ShopGoodsController.ShopGoodsController],a_w_list=['_SGCobj'],g=globals())
@AutoWired.OuterWired(obj_list, g=globals())
def inject_obj():
    # for name in obj_list.keys():
    #     globals()[name]=AutoWired.get_obj(name)
    pass


inject_obj()


# 获取顶部标题栏
@app.route('/tabs', methods=['GET', 'POST'])
@annotation.AutoParam()
@annotation.ResponseBody()
def hello(a, b):
    result = _SGCobj.getHeadTitle()
    return result


# 获取商品列表
@app.route('/shop/goods/list', methods=['post'])
@annotation.AutoParam()
@annotation.ResponseBody()
def getShopGoodsList(page, pageSize):
    result = _SGCobj.findGoodsList(page, pageSize)
    return result


# 获取商品详细信息
@app.route('/shop/goods/detail', methods=['post'])
@annotation.ResponseBody()
def getGoodDetail():
    result = _SGCobj.findGoodDetail(request.json['id'])
    return result


# 获取商品描述
@app.route('/shop/goods/introduction', methods=['post'])
@annotation.ResponseBody()
def getGoodIntroduction():
    result = _SGCobj.findGoodIntroduction(request.json['id'])
    return result


@app.route('/', methods=['get'])
def index():
    return '<button>点击一下吧</button>'
