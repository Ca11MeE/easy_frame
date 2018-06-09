# coding: utf-8
from flask import jsonify
import functools

"""
注解集合(部分)
author:CallMeE
date:2018-06-01


"""

# 响应返回数据修饰器(跳过视图解析器)
# 响应体形式返回
def ResponseBody():
    def method(f):
        @functools.wraps(f)
        def arg(*args, **kwargs):
            # print(args)
            # print(kwargs)
            result = jsonify(f(*args, **kwargs))
            # print(result)
            # print(jsonify(result))
            return result

        return arg

    return method

# 处理请求参数装饰器
# 表单形式数据
def as_form():
    pass

# json形式数据
def as_json():
    pass