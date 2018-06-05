# coding: utf-8
from flask import jsonify
import functools

"""
注解集合(部分)
author:CallMeE
date:2018-06-01


json形式返回数据修饰器(跳过视图解析器)
"""


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
