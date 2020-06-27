# -*- coding: UTF-8 -*-
from flask import session, redirect, url_for, g
from functools import wraps
import config


# 检查是否登录的装饰器
def login_required(func):
    print('%s 我是login_required' % func.__name__)
    @wraps(func)
    def inner(*args, **kwarg):
        print('%s 执行login_required' % func.__name__)
        if config.FRONT_USER_ID in session:
            return func(*args, **kwarg)
        else:
            return redirect(url_for('front.signin'))
    return inner
