# -*- coding: UTF-8 -*-
from flask import session, redirect, url_for
from functools import wraps
import config
"""
存放常用的装饰器函数
"""


# 检查是否登录的装饰器
def login_required(func):
    @wraps(func)
    def inner(*args, **kwarg):
        if config.CMS_USER_ID in session:
            return func(*args, **kwarg)
        else:
            return redirect(url_for('cms.login'))
    return inner



