#!/usr/bin/env
from flask import Flask, render_template
from config import config_map
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
if not os.path.exists("download"):
    os.makedirs("download")

db = SQLAlchemy()
loginmanager=LoginManager()

# 工厂模式


def creat_app(config_name):
    """
    创建flask的应用对象
    :param config_name: str 配置模式的名字 ("develop","product")
    :return:app
    """
    app = Flask(__name__)
    # 根据配置模式的名字获取配置参数的类
    config_class = config_map.get(config_name)
    app.config.from_object(config_class)

    register_logging(app)  # 加载日志处理器
    register_extensions(app)  # 注册扩展
    register_api(app)		# 注册API或者蓝图
    register_commands(app)  # 注册click或script命令
    register_shell_context(app)  # 注册shell上下文
    register_template_context(app)  # 注册模板上下文

    return app


def register_logging(app):
    pass


def register_extensions(app):
    db.init_app(app)  # 初始化SQLAlchemy , 本质就是将以上的配置读取出来
    loginmanager.init_app(app)
    from .models import User
    @loginmanager.user_loader
    def load_user(id):
        return User.query.get(id)
def register_api(app):
    from .admin import admin
    from .visitor import visitor
    from .supplier import supplier
    from .machinepart import machinepart
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(supplier, url_prefix='/supplier')
    app.register_blueprint(machinepart, url_prefix='/machinepart')
    app.register_blueprint(visitor)

    


def register_commands(app):
    pass


def register_shell_context(app):
    pass


def register_template_context(app):
    pass

