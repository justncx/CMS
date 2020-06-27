# -*- coding: UTF-8 -*-

from .views import bp
from flask import session, g, render_template
import config
from .models import FrontUser


@bp.before_request
def my_before_request():
    if config.FRONT_USER_ID in session:
        user_id = session.get(config.FRONT_USER_ID)
        user = FrontUser.query.get(user_id)
        if user:
            g.front_user = user


@bp.errorhandler(404)
def page_not_found(error):
    return render_template('front/front_404.html'), 404
