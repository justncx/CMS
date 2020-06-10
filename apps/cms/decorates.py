# -*- coding: UTF-8 -*-
from flask import session, redirect, url_for, g
from functools import wraps
import config
"""
存放常用的装饰器函数
"""


# 检查是否登录的装饰器
def login_required(func):
    print('%s 我是login_required' % func.__name__)
    @wraps(func)
    def inner(*args, **kwarg):
        print('%s 执行login_required' % func.__name__)
        if config.CMS_USER_ID in session:
            return func(*args, **kwarg)
        else:
            return redirect(url_for('cms.login'))
    return inner


# 判断用户权限的装饰器
def permission_required(permission):
    def outter(func):
        print('%s 我是permission_required' % func.__name__)
        @wraps(func)
        def inner(*args, **kwargs):
            print('%s 执行permission_required' % func.__name__)
            user = g.cms_user
            # print(user.roles)
            if user.has_permission(permission):
                return func(*args, **kwargs)
            else:
                return redirect(url_for('cms.index'))
        return inner
    return outter
