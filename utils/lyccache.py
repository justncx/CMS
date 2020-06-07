# -*- coding: UTF-8 -*-

import memcache

cache = memcache.Client(['127.0.0.1:11211'], debug=True)


def set(key, value, timeout=60):
    # 在这里我们重新封装set方法，而不去使用原先自带的set方法的好处是我们以后修改的话
    # 可以直接在这里
    # 添加其他代码
    return cache.set(key, value, timeout)

def get(key):
    return cache.get(key)

def delete(key):
    return cache.delete(key)

