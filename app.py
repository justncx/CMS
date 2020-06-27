from flask import Flask
from apps.cms import bp as cms_bp
from apps.front import bp as front_bp
from apps.common import bp as common_bp
from apps.ueditor import bp as ueditor_bp
import config
from exts import db, mail
from flask_wtf import CSRFProtect
from utils.captcha import Captcha


def create_app():
    app = Flask(__name__)
    # 加载配置文件
    app.config.from_object(config)
    # 注册db
    db.init_app(app)
    # 注册mail
    mail.init_app(app)
    CSRFProtect(app)
    # 注册蓝图
    app.register_blueprint(cms_bp)
    app.register_blueprint(front_bp)
    app.register_blueprint(common_bp)
    app.register_blueprint(ueditor_bp)
    return app

Captcha.gene_graph_captcha()


if __name__ == '__main__':
    app = create_app()
    app.run()
