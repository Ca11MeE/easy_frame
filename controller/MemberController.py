# coding: utf-8
# 商品列表
import mysql
import hashlib


class MemberController:
    def __init__(self):
        self.cursor = mysql.getDbObj(mysql.project_path + '/mappers/MemberMapper.xml', debug=False)

    def findUserByCode(self, code):
        result = self.cursor.exe_sql(methodName='findUserByCode', args=(code), pageInfo=None)
        return result

    def login(self, args):
        account = args['mobile']
        result = self.cursor.exe_sql(methodName='findUserByAccount', args=(account))
        # 对比密码
        return comparePassword(args, result[0]['password']) if 0 < len(result) else False

    def getUserByAccount(self,args):
        result=self.cursor.exe_sql(methodName='findOneByAccount',args=args)
        return result[0]

    def saveUserWxId(self,args):
        result=self.cursor.exe_sql(methodName='saveWxIdByAccount',args={'wechat_id':args['wx_id'],'id':args['member_id']})
        return 0<result


def comparePassword(args, pwd):
    # 对比
    b = hashlib.sha1(args['password'].encode('utf8'))
    b.update(args['mobile'].encode('utf8'))
    return str(b.hexdigest()) == pwd