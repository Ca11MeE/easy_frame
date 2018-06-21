# coding: utf-8
"""
注入配置
author:CallMeE
date:2018-06-01
"""
# 此处插入所需注入的类
from controller import ShopGoodsController, MemberController,ShopGoodsBarrelController

# 此处构建注入列表
shop_good_rou = {
    '_SGCobj': ShopGoodsController.ShopGoodsController,
    '_SGBobj':ShopGoodsBarrelController.ShopGoodsBarrelController
}
member_rou={
    '_memberObj': MemberController.MemberController
}
