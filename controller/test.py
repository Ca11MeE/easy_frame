# 路由类

class a:
    def square_sum(fn):
        def square(*args):
            print(args)
            return fn(*args)
        return square


@a.square_sum
def sum_a(a,b):
    print("3=", a)
    print("4=", b)


sum_a(10,11)