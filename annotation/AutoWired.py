# 自动注入修饰器
import mysql.Connection

'''
定义修饰器
'''
def AutoWired(self,clz):
    # 注入实例
    def wn(f):
        # print(len(args))
        return f
    return wn

@AutoWired(6,6)
def a(aa,bb):
    print('result:',aa,bb)


a(1,2)

print(a(3,4))