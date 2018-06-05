# coding: utf-8
"""
注入配置
author:CallMeE
date:2018-06-01
"""
# 此处插入所需注入的类
from controller import ShopGoodsController

# 此处构建注入列表
obj_list = {'_SGCobj': ShopGoodsController.ShopGoodsController}
