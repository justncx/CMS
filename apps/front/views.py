# -*- coding: UTF-8 -*-

from flask import Blueprint, views, render_template,\
    redirect, make_response, request, session, url_for, g, abort
from utils.captcha import Captcha
from utils import restful, safeutils
from io import BytesIO
from .models import FrontUser
from .forms import SignupForm, SignInForm, AddPostForm, AddCommentForm
from exts import db
from ..models import BannerModel, BorderModel, PostModel, CommentModel
import config
from .decorates import login_required
from flask_paginate import Pagination, get_page_parameter


bp = Blueprint('front', __name__)


@bp.route('/acomment', methods=['GET', 'POST'])
@login_required
def add_comment():
    form = AddCommentForm(request.form)
    if form.validate():
        content = form.content.data
        post_id = form.post_id.data
        post = PostModel.query.get(post_id)
        if post:
            comment = CommentModel(content=content)
            comment.post = post
            comment.author = g.front_user
            db.session.add(comment)
            db.session.commit()
            return restful.success()
        else:
            return restful.paramerror(message='没有这篇帖子')
    else:
        return restful.paramerror(form.get_error())


@bp.route('/p/<post_id>')
def post_detail(post_id):
    post = PostModel.query.get(post_id)
    if not post:
        abort(404)
    return render_template('front/front_pdetail.html', post=post)


@bp.route('/apost/', methods=['GET', 'POST'])
@login_required
def add_post():
    if request.method == 'GET':
        boards = BorderModel.query.all()
        return render_template('front/front_apost.html', boards=boards)
    else:
        form = AddPostForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            board_id = form.board_id.data
            board = BorderModel.query.get(board_id)
            if not board:
                return restful.paramerror(message='没找到该板块')
            post = PostModel(title=title, content=content)
            post.board = board
            post.author = g.front_user
            db.session.add(post)
            db.session.commit()
            return restful.success()
        else:
            return restful.paramerror(message=form.get_error())


@bp.route('/', strict_slashes=False)
def index():
    board_id = request.args.get('bd', type=int, default=None)
    page = request.args.get(get_page_parameter(), type=int, default=1)
    print(type(page))
    print(page)

    banners = BannerModel.query.order_by(BannerModel.priority).limit(4)
    # banners = BannerModel.query.order_by(BannerModel.priority.desc()).limit(4)
    boards = BorderModel.query.all()
    start = (page-1) * config.PER_PAGE
    end = start + config.PER_PAGE
    # ports = None
    # total = 0
    if board_id:
        total = PostModel.query.filter_by(board_id=board_id).slice(start, end).count()
        posts = PostModel.query.filter_by(board_id=board_id).slice(start, end)
    else:
        posts = PostModel.query.slice(start, end)
        total = PostModel.query.count()
    pagination = Pagination(bs_version=3, page=page, total=total,
                            outer_window=1, inner_window=2)
    context = {
        'banners': banners,
        'boards': boards,
        'posts': posts,
        'pagination': pagination,
        'current_board': board_id
    }
    return render_template('front/front_index.html', **context)


@bp.route('/test/', strict_slashes=False)
def test():
    return render_template('front/test.html')


class SingInView(views.MethodView):
    def get(self):
        return_to = request.referrer
        if return_to and return_to != url_for('front.signup') and\
                safeutils.is_safe_url(return_to) and return_to != request.url:
            return render_template('front/front_signin.html', return_to=return_to)
        else:
            return render_template('front/front_signin.html')

    def post(self):
        form = SignInForm(request.form)
        if form.validate():
            telephone = form.telephone.data
            password = form.password.data
            remember = form.remember.data
            user = FrontUser.query.filter_by(telephone=telephone).first()
            if user and user.check_password(password):
                session[config.FRONT_USER_ID] = user.id
                if remember:
                    session.permanent = True
                return restful.success()
            else:
                return restful.paramerror(message='手机号码或者密码错误')
        else:
            return restful.paramerror(message=form.get_error())


class SginupView(views.MethodView):
    def get(self):
        # 获取上个页面的url
        return_to = request.referrer
        if return_to and return_to != request.url and safeutils.is_safe_url(return_to):
            return render_template('front/front_signup.html', return_to=return_to)
        else:
            return render_template('front/front_signup.html')

    def post(self):
        form = SignupForm(request.form)
        if form.validate():
            telephone = form.telephone.data
            username = form.username.data
            password = form.password2.data
            user = FrontUser(telephone=telephone, username=username, password=password)
            db.session.add(user)
            db.session.commit()
            return restful.success(message='注册成功')
        else:
            print(form.get_error())
            return restful.paramerror(message=form.get_error())


bp.add_url_rule('/signup/', view_func=SginupView.as_view('signup'))
bp.add_url_rule('/signin/', view_func=SingInView.as_view('signin'))

