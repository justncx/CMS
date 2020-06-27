# -*- coding: UTF-8 -*-

from ..forms import BaseForm
from wtforms import StringField, ValidationError, IntegerField
from wtforms.validators import Regexp, Email, EqualTo, InputRequired
from utils import lyccache


class SignupForm(BaseForm):
    telephone = StringField(validators=[Email(message='请输入正确的邮箱')])
    # sms_captcha = StringField(validators=[Regexp(r'\w{6}', message='请输入正确格式的验证码')])
    sms_captcha = StringField(validators=[InputRequired(message='请输入正确格式的验证码')])
    # sms_captcha = StringField(validators=[Regexp(r"\w{4}",message='请输入正确格式的短信验证码！')])
    username = StringField(validators=[Regexp(r".{2,20}", message='请输入正确格式的用户名')])
    password1 = StringField(validators=[Regexp(r'[0-9a-zA-Z_\.]{6,20}', message='请输入正确格式的密码')])
    # password1 = StringField(validators=[InputRequired(message='请输入正确格式的密码')])
    password2 = StringField(validators=[EqualTo('password1', message='两次输入的密码不一致')])
    graph_captcha = StringField(validators=[Regexp(r'\w{4}', message='请输入正确格式图形验证码')])

    def validate_sms_captcha(self, field):
        smscaptcha = field.data
        telephone = self.telephone.data
        smscaptcha_mem = lyccache.get(telephone)
        print('smscaptcha_mem is %s' % smscaptcha_mem)
        if not smscaptcha_mem or smscaptcha_mem.lower() != smscaptcha.lower():
            raise ValidationError(message='短信验证码验证错误')

    def validate_graph_captcha(self, field):
        graph_captcha = field.data
        graph_captcha_mem = lyccache.get(graph_captcha.lower())
        if not graph_captcha_mem:
            raise ValidationError(message='图形验证码错误')


class SignInForm(BaseForm):
    telephone = StringField(validators=[Email(message='请输入正确的邮箱')])
    password = StringField(validators=[Regexp(r'[0-9a-zA-Z_\.]{6,20}', message='请输入正确格式的密码')])
    remember = StringField()


class AddPostForm(BaseForm):
    title = StringField(validators=[InputRequired(message='请输入标题')])
    content = StringField(validators=[InputRequired(message='请输入内容')])
    board_id = IntegerField(validators=[InputRequired(message='请输入板块ID')])


class AddCommentForm(BaseForm):
    content = StringField(validators=[InputRequired(message='请输入内容')])
    post_id = IntegerField(validators=[InputRequired(message='请输入帖子ID')])

