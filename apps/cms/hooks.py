# -*- coding: UTF-8 -*-
from .views import bp
from flask import session, g
import config
from .models import CMSUser

"""
这个文件用来存放钩子函数
"""


@bp.before_request
def before_request():
    if config.CMS_USER_ID in session:
        user_id = session.get(config.CMS_USER_ID)
        user = CMSUser.query.get(user_id)
        if user:
            g.cms_user = user

