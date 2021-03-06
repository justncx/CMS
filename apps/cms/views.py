# -*- coding: UTF-8 -*-

from flask import Blueprint, render_template, views, request, session, redirect,\
    url_for, g, jsonify
from .forms import LoginForm, ResetPassworldForm, ResetEmailForm, AddBannerForm,\
    UpdateBannerForm, AddBoardForm, UpdateBoardForm
from .models import CMSUser, CMSPermission
from .decorates import login_required, permission_required
import config
from exts import db, mail
from flask_mail import Message
from utils import restful, lyccache
import string
import random
from ..models import BannerModel, BorderModel


bp = Blueprint('cms', __name__, url_prefix='/cms')


@bp.route('/aboard/', methods=['POST'])
@login_required
@permission_required(CMSPermission.BOARDER)
def add_board():
    form = AddBoardForm(request.form)
    if form.validate():
        name = form.name.data
        board = BorderModel(name=name)
        db.session.add(board)
        db.session.commit()
        return restful.success()
    else:
        return restful.paramerror(message=form.get_error())


@bp.route('/uboard/', methods=['POST'])
@login_required
@permission_required(CMSPermission.BOARDER)
def update_board():
    form = UpdateBoardForm(request.form)
    if form.validate():
        board_id = form.board_id.data
        name = form.name.data
        print(name)
        board = BorderModel.query.get(board_id)
        if board:
            board.name = name
            db.session.commit()
            return restful.success()
        else:
            return restful.paramerror(message='没有这个板块')
    else:
        return restful.paramerror(form.get_error())


@bp.route('/dboard/', methods=['POST'])
@login_required
@permission_required(CMSPermission.BOARDER)
def delete_board():
    board_id = request.form.get('board_id')
    print(board_id)
    if not board_id:
        return restful.paramerror(message='请输入板块ID')
    board = BorderModel.query.get(board_id)
    if board:
        db.session.delete(board)
        db.session.commit()
        print('123132')
        return restful.success()
    else:
        return restful.paramerror(message='没有这个板块')


@bp.route('/dbanner/', methods=['GET', 'POST'])
@login_required
def delete_banner():
    banner_id = request.form.get('banner_id')
    if not banner_id:
        return restful.paramerror(message='请传入轮播图ID')
    banner = BannerModel.query.get(banner_id)
    if not banner:
        return restful.paramerror(message='没有这个轮播图')
    db.session.delete(banner)
    db.session.commit()
    return restful.success()


@bp.route('/ubanner/', methods=['GET', 'POST'])
@login_required
def update_banner():
    form = UpdateBannerForm(request.form)
    if form.validate():
        banner_id = form.banner_id.data
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        banner = BannerModel.query.get(banner_id)
        if banner:
            banner.name = name
            banner.image_url = image_url
            banner.link_url = link_url
            banner.priority = priority
            db.session.commit()
            return restful.success()
        else:
            return restful.paramerror(message='没有这个轮播图')
    else:
        return restful.paramerror(message=form.get_error())


@bp.route('/abanner/', methods=['GET', 'POST'])
# @bp.route('/abanner/')
@login_required
def add_banner():
    form = AddBannerForm(request.form)
    if form.validate():
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        banner = BannerModel(name=name, image_url=image_url, link_url=link_url, priority=priority)
        db.session.add(banner)
        db.session.commit()
        return restful.success()
    else:
        return restful.paramerror(message=form.get_error())


class ResetEmailView(views.MethodView):
    decorators = [login_required]
    def get(self):
        return render_template('cms/cms_resetemail.html')
    def post(self):
        form = ResetEmailForm(request.form)
        if form.validate():
            email = form.email.data
            g.cms_user.email = email
            db.session.commit()
            return restful.success()
        else:
            return restful.paramerror(form.get_error())


@bp.route('/email_captcha/')
def email_captcha():
    # 通过查询字符串的方式将邮箱传递进去
    # /email_captcha/?email=xxx@qq.com
    email = request.args.get('email')
    if not email:
        return restful.paramerror('请传递邮箱参数!')
    # 生成验证码
    source = list(string.ascii_letters)
    # source.extend(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])
    source.extend(map(lambda x: str(x), range(0, 10)))
    # 随机采样
    captcha = "".join(random.sample(source, 6))
    # 发送验证码
    message = Message(subject='验证码', recipients=[email], body='您的验证码是%s' % captcha)
    try:
        mail.send(message)
    except:
        return restful.servererror()
    lyccache.set(email, captcha)
    return restful.success(message='邮件发送成功')


# 测试邮件发送
@bp.route('/email/')
def send_email():
    print(db.session.query(CMSUser).filter_by(email='xuptwgl@163.com').first().email)
    print(type((db.session.query(CMSUser).filter_by(email='xuptwgl@163.com').first())))
    return "%s" % db.session.query(CMSUser).filter_by(email='xuptwgl@163.com').first().email
    message = Message(subject='test邮件发送', recipients=['xuptwgl@163.com'], body='测试1')
    mail.send(message)
    return '邮件发送成功！！！'


@bp.route('/')
@login_required
def index():
    return render_template('cms/cms_index.html')

@bp.route('/logout/')
@login_required
def logout():
    # session.clear()
    del session[config.CMS_USER_ID]
    return redirect(url_for('cms.login'))

@bp.route('/profile/')
@login_required
def profile():
    return render_template('cms/cms_profile.html')


class ResetPwdView(views.MethodView):
    # 在类视图中使用装饰器
    decorators = [login_required]
    def get(self):
        return render_template('cms/cms_resetpwd.html')
    def post(self):
        form = ResetPassworldForm(request.form)
        if form.validate():
            user_id = session.get(config.CMS_USER_ID)
            user = CMSUser.query.get(user_id)
            old_passwd = form.oldpwd.data
            print(old_passwd)
            if user.check_password(old_passwd):
                new_passwd = form.newpwds
                print(user)
                print(user.password)
                print(new_passwd.data)
                # 注意这里需要.data
                user.password = new_passwd.data
                db.session.commit()
                # return '修改成功'
                # return jsonify({
                #     'code': 200,
                #     'message': ''
                # })
                return restful.success()

            else:
                print('输入的原密码错误')
                # return '输入的原密码错误'
                # return jsonify({
                #     'code': 400,
                #     'message': '原密码输入错误'
                # })
                return restful.paramerror(message='原密码输入错误')
                # return restful.paramerror()
        else:
            print(form.errors)
            # return jsonify({
            #     'code': 400,
            #     'message': form.get_error()
            # })
            return restful.paramerror(form.get_error())
            # return restful.paramerror()


# 先判断登录，再判断权限
# bp.route('/posts/') 这个要写在上边。为什么？？？
"""
多重装饰器，在调用的时候从下往上，在执行内函数的时候从上往下
"""
@bp.route('/posts/')
@login_required
@permission_required(CMSPermission.POSTER)
def posts():
    return render_template('cms/cms_posts.html')


@bp.route('/banners')
@login_required
def banners():
    banners = BannerModel.query.order_by(BannerModel.priority.desc()).all()
    return render_template('cms/cms_banners.html', banners=banners)


@bp.route('/comments/')
@login_required
@permission_required(CMSPermission.COMMENTER)
def comments():
    return render_template('cms/cms_comments.html')


@bp.route('/boards/')
@login_required
@permission_required(CMSPermission.BOARDER)
def boards():
    board_models = BorderModel.query.all()
    context = {
        'boards': board_models
    }
    return render_template('cms/cms_boards.html', **context)


@bp.route('/fusers/')
@login_required
@permission_required(CMSPermission.FRONTER)
def fusers():
    return render_template('cms/cms_fusers.html')

@bp.route('/cusers/')
@login_required
@permission_required(CMSPermission.ADMINER)
def cusers():
    return render_template('cms/cms_cusers.html')


@login_required
@permission_required(CMSPermission.ALL_PERMISSION)
@bp.route('/croles/')
def croles():
    return render_template('cms/cms_croles.html')


# 这里使用类视图
class LoginView(views.MethodView):

    def get(self, message=None):
        return render_template('cms/cms_login.html', message=message)

    def post(self):
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data
            user = CMSUser.query.filter_by(email=email).first()
            if user and user.check_password(password):
                # 这里我们定义一个常量CMS_USER_ID,这样的话在使用的时候就不需要去写字符串，
                # 避免出错和与其他名字冲突
                session[config.CMS_USER_ID] = user.id
                # 如果选择了记住我，则长时间保存session
                if remember:
                    # 设置为True，默认为31天过期
                    session.permanent = True
                # 注意这里使用了蓝图，所以这里使用url反转的时候需要加蓝图.xx
                return redirect(url_for('cms.index'))
            else:
                return self.get(message='登录失败，邮箱或者密码错误')
                # return restful.paramerror(message='登录失败，邮箱或者密码错误')
                # return restful.paramerror()

        else:
            print(form.errors)
            # 避免代码冗余，使用self.get()
            return self.get(message='%s' % form.get_error())


bp.add_url_rule('/login/', view_func=LoginView.as_view('login'))
bp.add_url_rule('/resetpwd/', view_func=ResetPwdView.as_view('resetpwd'))
bp.add_url_rule('/resetemail/', view_func=ResetEmailView.as_view('resetemail'))

