# -*- coding: UTF-8 -*-

"""
这个文件主要放一些基类的表单方法
"""

from wtforms import Form


class BaseForm(Form):
    def get_error(self):
        message = self.errors.popitem()[1][0]
        return message

    def validate(self, extra_validators=None):
        return super(BaseForm, self).validate()
