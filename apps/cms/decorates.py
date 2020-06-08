# -*- coding: UTF-8 -*-
from flask import session, redirect, url_for, g
from functools import wraps
import config
"""
存放常用的装饰器函数
"""


# 检查是否登录的装饰器
def login_required(func):
    @wraps(func)
    def inner(*args, **kwarg):
        print('login'*12)
        if config.CMS_USER_ID in session:
            return func(*args, **kwarg)
        else:
            return redirect(url_for('cms.login'))
    return inner


# 判断用户权限的装饰器
def permission_required(permission):
    print('12313123123123131313131231312')
    def outter(func):
        @wraps(func)
        def inner(*args, **kwargs):
            user = g.cms_user
            # print(user.roles)
            if user.has_permission(permission):
                return func(*args, **kwargs)
            else:
                return redirect(url_for('cms.index'))
        return inner
    return outter
