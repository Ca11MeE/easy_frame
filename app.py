# coding: utf-8
# 启动类
import json
from flask import Flask
from flask import jsonify
from flask import request
import mysql
from mysql import Pool
from annotation import AutoWired
from properties import IOCProp

_app=Flask(__name__)
_app.config['JSON_AS_ASCII']=False

_SGCobj=None

obj_list=IOCProp.obj_list

# 注入对象
# @AutoWired.Wired([ShopGoodsController.ShopGoodsController],a_w_list=['_SGCobj'])
@AutoWired.AutoWired(obj_list)
def inject_obj():
    pass

#
# # 获取顶部标题栏
# @_app.route('/tabs',methods=['GET'])
# def hello():
#     result=TestData.getHeadTitle()
#     return jsonify(result)

# 获取商品列表
@_app.route('/shop/goods/list',methods=['post'])
def getShopGoodsList():
    result=_SGCobj.findGoodsList(request.json['page'],request.json['pageSize'])
    return jsonify(result)

# 获取商品详细信息
@_app.route('/shop/goods/detail',methods=['post'])
def getGoodDetail():
    result=_SGCobj.findGoodDetail(request.json['id'])
    return jsonify(result)

# 获取商品描述
@_app.route('/shop/goods/introduction',methods=['post'])
def getGoodIntroduction():
    result=_SGCobj.findGoodIntroduction(request.json['id'])
    return jsonify(result)



# 启动服务器
if '__main__'==__name__:
    print('加载数据库模块')
    mysql.pool=Pool.Pool()
    print('加载完毕')
    _app.run(host='0.0.0.0',port=443,ssl_context=(mysql.project_path+'/sslContext/1_zxyzt.cn_bundle.crt',mysql.project_path+'/sslContext/2_zxyzt.cn.key'))
    # _app.run(host='0.0.0.0',port=443,ssl_context='adhoc')
