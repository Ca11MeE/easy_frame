def a_b():
    def method(f):
        def args(*args,**kwargs):
            print('a_b执行')
            print('a_b无参参数',args)
            print('a_b关键字参数',kwargs)
            result=f(*args,**kwargs)
            print('a_b执行完毕')
            return result
        return args
    return method

def a_a(c,d):
    def method(f):
        @a_b()
        def args(*args,**kwargs):
            print('a_a执行')
            print('a_a无参参数',args)
            print('a_a关键字参数',kwargs)
            result=f(*args,**kwargs)
            print('a_a执行完毕')
            return result
        return args
    return method


@a_a(3,4)
def a(a,b):
    print('方法a执行')

a(1,2)