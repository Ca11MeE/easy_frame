# coding: utf-8
# 启动类
from flask import Flask,jsonify,request
import mysql
import annotation
# from controller import ShopGoodsController
from mysql import Pool
from annotation import AutoWired
from properties import IOCProp

_app = Flask(__name__)
_app.config['JSON_AS_ASCII'] = False

obj_list = IOCProp.obj_list

_SGCobj=None

# 注入对象
# @AutoWired.InnerWired([ShopGoodsController.ShopGoodsController],a_w_list=['_SGCobj'],g=globals())
@AutoWired.OuterWired(obj_list,g=globals())
def inject_obj():
    # for name in obj_list.keys():
    #     globals()[name]=AutoWired.get_obj(name)
    pass


#
# # 获取顶部标题栏
@_app.route('/tabs', methods=['GET'])
@annotation.ResponseBody()
def hello():
    result = _SGCobj.getHeadTitle()
    return result


# 获取商品列表
@_app.route('/shop/goods/list', methods=['post'])
@annotation.ResponseBody()
def getShopGoodsList():
    result = _SGCobj.findGoodsList(request.json['page'], request.json['pageSize'])
    return result


# 获取商品详细信息
@_app.route('/shop/goods/detail', methods=['post'])
@annotation.ResponseBody()
def getGoodDetail():
    result = _SGCobj.findGoodDetail(request.json['id'])
    return result


# 获取商品描述
@_app.route('/shop/goods/introduction', methods=['post'])
@annotation.ResponseBody()
def getGoodIntroduction():
    result = _SGCobj.findGoodIntroduction(request.json['id'])
    return result


# 启动服务器
if '__main__' == __name__:
    # print('加载数据库模块')
    mysql.pool = Pool.Pool()
    # print('加载完毕')
    inject_obj()
    _app.run(host='0.0.0.0', port=443, ssl_context=(mysql.project_path + '/sslContext/1_zxyzt.cn_bundle.crt', mysql.project_path + '/sslContext/2_zxyzt.cn.key'))
    # _app.run(host='127.0.0.1', port=443, ssl_context=(mysql.project_path + '/sslContext/1_zxyzt.cn_bundle.crt', mysql.project_path + '/sslContext/2_zxyzt.cn.key'))


    # _app.run(host='0.0.0.0',port=443,ssl_context='adhoc')
