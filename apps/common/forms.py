# -*- coding: UTF-8 -*-

from apps.forms import BaseForm
from wtforms import StringField
from wtforms.validators import Email, InputRequired, Length, EqualTo, regexp
import hashlib


class EmailForm(BaseForm):
    salt = 'dasdadqweqamvoaksmf1231'
    email = StringField(validators=[Email('请输入正确的邮箱')])
    timestamp = StringField(validators=[regexp(r'\d{13}')])
    sign = StringField(validators=[InputRequired()])

    def validate(self, extra_validators=None):
        result = super(EmailForm, self).validate()
        if not result:
            return False

        email = self.email.data
        timestamp = self.timestamp.data
        sign = self.sign.data

        # md5(timestamp+email+salt)
        # md5函数必须传递一个bytes类型的字符串进去
        sign2 = hashlib.md5((timestamp+email+self.salt).encode('utf-8')).hexdigest()
        print('客户端的md5 %s' % sign)
        print('服务器生产的的md5 %s' % sign2)
        if sign == sign2:
            return True
        else:
            return False
