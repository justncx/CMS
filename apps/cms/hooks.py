# -*- coding: UTF-8 -*-
from .views import bp
from flask import session, g
import config
from .models import CMSUser, CMSPermission

"""
这个文件用来存放钩子函数
"""

# 这个钩子函数用来东一个全局cms_user变量
@bp.before_request
def before_request():
    if config.CMS_USER_ID in session:
        user_id = session.get(config.CMS_USER_ID)
        user = CMSUser.query.get(user_id)
        if user:
            g.cms_user = user


# 这个钩子函数用来给模板传入CMSPermission, 使用上下文处理器，所有返回模板的时候
# 都会传入CMSPermission
@bp.context_processor
def cms_context_permission():
    return {'CMSPermission': CMSPermission, 'CMSUser': CMSUser}