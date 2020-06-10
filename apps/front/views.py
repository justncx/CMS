# -*- coding: UTF-8 -*-

from flask import Blueprint, views, render_template, redirect, make_response
from utils.captcha import Captcha
from io import BytesIO

bp = Blueprint('front', __name__)


@bp.route('/')
def index():
    return 'front index'


class SginupView(views.MethodView):
    def get(såelf):
        return render_template('front/front_signup.html')


bp.add_url_rule('/signup/', view_func=SginupView.as_view('signup'))


@bp.route('/captcha/')
def graph_captcha():
    text, image = Captcha.gene_graph_captcha()
    out = BytesIO()
    image.save(out, 'png')
    out.seek(0)
    resp = make_response(out.read())
    resp.content_type = 'image/png'
    return resp
