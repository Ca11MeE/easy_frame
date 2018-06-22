# coding: utf-8
# 启动类
from flask import Blueprint
import annotation
import boot
# from controller import ShopGoodsController
from annotation import AutoWired
from properties import IOCProp
from urllib import request, response

"""
蓝图DEMO
author:CallMeE
date:2018-06-01
"""

# 此处定义蓝图前缀
url_prefix = None
app = Blueprint('member', __name__, url_prefix=url_prefix)

member_rou = IOCProp.member_rou

_memberObj = None


# 注入对象
# @AutoWired.InnerWired([ShopGoodsController.ShopGoodsController],a_w_list=['_SGCobj'],g=globals())
@AutoWired.OuterWired(member_rou, g=globals())
def inject_obj():
    # for name in obj_list.keys():
    #     globals()[name]=AutoWired.get_obj(name)
    pass


inject_obj()


@annotation.RequestMapping(app=app, path='/check/member/code', methods=['Post'])
@annotation.AutoParam(kwarg_list=['wxCode', 'appId', 'secCode'])
@annotation.ResponseBody()
def checkUserCode(wxCode, appId, secCode):
    print(locals())
    re_wx_url = 'https://api.weixin.qq.com/sns/jscode2session?appid=' + appId + '&secret=' + secCode + '&js_code=' + wxCode + '&grant_type=authorization_code'
    req = request.Request(re_wx_url)
    res = request.urlopen(req)
    res = eval(res.read())
    print(res)
    if 'openid' in res:
        result = _memberObj.findUserByCode(code=res['openid'])
        if result:
            result[0]['open_id']=res['openid']
        else:
            return res
        return result
    else:
        return res


@annotation.RequestMapping(app, '/login', ['post'])
@annotation.FullParam()
@annotation.ResponseBody()
def login(args):
    result = _memberObj.login(args)
    return {'event': 200, 'data': _memberObj.getUserByAccount(args), 'msg': '登陆成功'} if result else {'event': 500,
                                                                                                    'msg': '登陆失败'}


@annotation.RequestMapping(app, '/login/bind/wx', ['post'])
@annotation.FullParam()
@annotation.ResponseBody()
def bindWx(args):
    result = _memberObj.saveUserWxId(args)
    return {'event': 200,'data':_memberObj.findUserByCode(code=args['wx_id']), 'msg': '绑定成功'} if result else {'event': 500, 'msg': '绑定失败,请勿重复绑定'}
