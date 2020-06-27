# -*- coding: UTF-8 -*-


from wtforms import Form, StringField, IntegerField, ValidationError
from wtforms.validators import Email, InputRequired, Length, EqualTo
from ..forms import BaseForm
from utils import lyccache
from flask import g
from exts import db
from .models import CMSUser


class LoginForm(BaseForm):
    email = StringField(validators=[Email(message='请输入正确的有邮箱格式'),
                                    InputRequired(message='请输入邮箱')])
    password = StringField(validators=[Length(6, 20, message='请输入正确的密码')])
    remember = IntegerField()


class ResetPassworldForm(BaseForm):
    oldpwd = StringField(validators=[Length(6, 20, message='请输入正确的密码')])
    newpwd = StringField(validators=[Length(6, 20, message='请输入正确的密码')])
    newpwd2 = StringField(validators=[EqualTo('newpwd', message='两次输入的密码不一致')])


class ResetEmailForm(BaseForm):
    email = StringField(validators=[Email(message='请输入正确的有效格式')])
    captcha = StringField(validators=[Length(6, 6, message='请输入正确长度的验证码')])

    # 从memcached中获取邮箱和验证码，判断验证码是否正确
    def validate_captcha(self, field):
        print('field is %s' % field)
        # 这个地方的filed就代表的是captcha
        captcha = field.data
        email = self.email.data
        captcha_cacha = lyccache.get(email)
        print('email is %s' % email)
        print('captcha is %s' % captcha)
        print('captcha_cacha is %s' % captcha_cacha)
        if not captcha_cacha or captcha.lower() != captcha_cacha.lower():
            raise ValidationError('邮箱验证码错误！')

    # 验证邮箱是不是和原来的相同, 还需要判断更改的邮箱不能被其他人使用过
    def validate_email(self, field):
        email = field.data
        # 这个g.cms_user 是在钩子函数中定义的
        user = g.cms_user
        if user.email == email:
            raise ValidationError('不能和原来的邮箱相同！')
        if db.session.query(CMSUser).filter_by(email=email).first():
            raise ValidationError('该邮箱已注册！')


class AddBannerForm(BaseForm):
    name = StringField(validators=[InputRequired(message='请输入轮播图名称')])
    image_url = StringField(validators=[InputRequired(message='请输入轮播图的url')])
    link_url = StringField(validators=[InputRequired(message='请输入轮播图的跳转url')])
    priority = IntegerField(validators=[InputRequired(message='请输入轮播图的优先级')])


class UpdateBannerForm(AddBannerForm):
    banner_id = IntegerField(validators=[InputRequired(message='请输入轮播图的ID')])


class AddBoardForm(BaseForm):
    name = StringField(validators=[InputRequired(message='请输入板块名称')])


class UpdateBoardForm(AddBoardForm):
    board_id = IntegerField(validators=[InputRequired(message='请输入板块ID')])
