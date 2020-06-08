# -*- coding: UTF-8 -*-
import datetime
import os

HOSTNAME = 'localhost'
PORT = 3306
DATABASE = 'cms'
USERNAME = 'root'
PASSWORD = '11111'

# dialect+driver://username:password@host:port/database
DB_URL = 'mysql+pymysql://{username}:{password}@{host}:{port}/{db}?' \
         'charset=utf8'.format(username=USERNAME,
                               password=PASSWORD,
                               host=HOSTNAME,
                               port=PORT,
                               db=DATABASE)

SQLALCHEMY_DATABASE_URI = DB_URL
SQLALCHEMY_TRACK_MODIFICATIONS = False

PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=31)
SECRET_KEY = os.urandom(100)

CMS_USER_ID = 'dadqdadwvsk'

# 发送者邮箱的服务器地址
MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = '465'
# MAIL_PORT = '587'
# MAIL_USE_TLS = True
MAIL_USE_SSL = True
MAIL_DEBUG = True
MAIL_USERNAME = '1322312@qq.com'
MAIL_PASSWORD = 'novhaifjorsqdjgg'
MAIL_DEFAULT_SENDER = '12313211@qq.com'
