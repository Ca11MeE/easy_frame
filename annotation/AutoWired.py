# 自动注入修饰器



'''
定义修饰器
'''
def Wired(clz,a_w_list=[],g):
    # print(locals())
    # 注入实例
    def wn(f):
        # print(len(args))
        def inner_function(*args,**dic_args):
            # 获取数组
            # print(args)
            # print(dic_args)
            if a_w_list is not None and 0<len(a_w_list):
                # 装饰器参数查找赋值
                a_name=a_w_list
            else:
                if dic_args['a_w_list'] is not None and 0<dic_args['a_w_list']:
                    # 被装饰函数关键字参数查找赋值
                    a_name=dic_args['a_w_list']
                else:
                    if 0>=len(args):
                        raise Exception('动态形参为空!!')
                    # 被装饰函数位置参数查找赋值
                    a_name=args[0]
            # for index in range(len(arg)):
            #     # print(str(id(arg[index])) + "初始化赋值为")
            #     print(str((arg[index])))
            #     arg[index] = clz[index]()
            #     # print(str(clz[index]))
            # for a in arg:
            #     print(id(a))
            for index in range(len(a_name)):
                # globals()[a_name[index]]=clz[index]()
                g[a_name[index]]=clz[index]()
            # return arg
            return f()
        return inner_function
        # print("解释器参数a:"+str(self))
        # print("解释器参数b:"+str(clz))
        # return f

    return wn

def AutoWired(obj_obj,g):
    # 前期准备
    clz=[]
    a_w_list=[]
    for key in obj_obj.keys():
        a_w_list.append(key)
        clz.append(obj_obj[key])
    # print(globals())
    # 注入实例
    def wn(f):
        # print(len(args))
        def inner_function(*args,**dic_args):
            # 获取数组
            # print(args)
            # print(dic_args)
            if a_w_list is not None and 0<len(a_w_list):
                # 装饰器参数查找赋值
                a_name=a_w_list
            else:
                if dic_args['a_w_list'] is not None and 0<dic_args['a_w_list']:
                    # 被装饰函数关键字参数查找赋值
                    a_name=dic_args['a_w_list']
                else:
                    if 0>=len(args):
                        raise Exception('动态形参为空!!')
                    # 被装饰函数位置参数查找赋值
                    a_name=args[0]
            # for index in range(len(arg)):
            #     # print(str(id(arg[index])) + "初始化赋值为")
            #     print(str((arg[index])))
            #     arg[index] = clz[index]()
            #     # print(str(clz[index]))
            # for a in arg:
            #     print(id(a))
            for index in range(len(a_name)):
                # globals()[a_name[index]]=clz[index]()
                print(str(a_name[index]),"注入"+str(clz[index]))
                g[a_name[index]] = clz[index]()
            # return arg
            # print(globals())
            return f()
        return inner_function
        # print("解释器参数a:"+str(self))
        # print("解释器参数b:"+str(clz))
        # return f

    return wn

def get_obj(name):
    print(globals())
    try:
        return globals()[name]
    except:
        return None;

# # @AutoWired(6,6)
# @AutoWired([A,B,C,D,E],a_w_list=['AA','BB','CC','DD','EE'])
# def a():
#     pass
#
#
# # print(globals())
# a()
# # print(globals())
#
# print(CC)


