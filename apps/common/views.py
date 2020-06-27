# -*- coding: UTF-8 -*-

from flask import Blueprint, request, make_response, jsonify
from utils import restful, lyccache
import string
import random
import qiniu
from flask_mail import Message
from exts import mail
from ..common.forms import EmailForm
from utils.captcha import Captcha
from io import BytesIO


bp = Blueprint('common', __name__, url_prefix='/common')


@bp.route('/uptoken/', methods=['GET', 'POST'])
def uptoken():
    ak = 'NRZ2Haj_cLFZ8jQLwGibPjx2MmlUppRonEOB9hZR'
    sk = '8AkbHHu048eDLLgwLQRTMACl5wnRhv859UUDOhMC'
    q = qiniu.Auth(access_key=ak, secret_key=sk)
    bucket = 'flask-new'
    # print(qiniu.getUploadUrl())
    token = q.upload_token(bucket)
    print(token)
    return jsonify({'uptoken': token})


# 图形验证码
@bp.route('/captcha/')
def graph_captcha():
    text, image = Captcha.gene_graph_captcha()
    lyccache.set(text.lower(), text.lower())
    out = BytesIO()
    image.save(out, 'png')
    out.seek(0)
    resp = make_response(out.read())
    resp.content_type = 'image/png'
    return resp


@bp.route('/')
def index():
    return 'common index'


@bp.route('/email_captcha/', methods=['POST'])
def email_captcha():
    # email
    # timestamp
    # md5(email + timestamp + salt)
    form = EmailForm(request.form)
    if form.validate():
        email = form.email.data
        source = list(string.ascii_letters)
        # source.extend(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])
        source.extend(map(lambda x: str(x), range(0, 10)))
        # 随机采样
        captcha = "".join(random.sample(source, 6))
        # 发送验证码
        print('发送了短信验证码: %s' % captcha)
        message = Message(subject='验证码', recipients=[email], body='您的验证码是%s' % captcha)
        try:
            mail.send(message)
        except:
            return restful.servererror()
        lyccache.set(email, captcha)
        return restful.success(message='邮件发送成功')
    else:
        return restful.paramerror(message='参数错误')

# @bp.route('/email_captcha/')
# def email_captcha():
#     # 通过查询字符串的方式将邮箱传递进去
#     # /email_captcha/?email=xxx@qq.com
#     email = request.args.get('email')
#     print(email)
#     if not email:
#         return restful.paramerror('请传递邮箱参数!')
#     # 生成验证码
#     source = list(string.ascii_letters)
#     # source.extend(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])
#     source.extend(map(lambda x: str(x), range(0, 10)))
#     # 随机采样
#     captcha = "".join(random.sample(source, 6))
#     # 发送验证码
#     message = Message(subject='验证码', recipients=[email], body='您的验证码是%s' % captcha)
#     try:
#         mail.send(message)
#     except:
#         return restful.servererror()
#     lyccache.set(email, captcha)
#     return restful.success(message='邮件发送成功')
