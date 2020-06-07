# -*- coding: UTF-8 -*-

# 在主app中导入cms的时候，会执行这个init文件

from .views import bp
# 注意这里要导入hooks才能被执行
import apps.cms.hooks
