from flask import Flask
from config import config_map
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_wtf import CSRFProtect
import redis
from . import api_1_0

# 数据库
db=SQLAlchemy()

# 创建redis连接对象
redis_store=None

# 工厂模式
def creat_app(config_name):
    """
    创建flask的应用对象
    :param config_name: str 配置模式的名字 ("develop","product")
    :return:
    """
    app = Flask(__name__)
    # 根据配置模式的名字获取配置参数的类
    config_class=config_map.get(config_name)
    app.config.from_object(config_class)
    # 使用app初始化db
    db.init_app(app)
    # 初始化redis对象
    global redis_store
    redis_store=redis.StrictReids(host=config_class.REDIS_HOST,port=config_class.REDIS_PORT)
    # 利用flask_session，将session数据保存到redis中
    Session(app)
    # 为flask补充csrf防护
    CSRFProtect(app)
    # 注册蓝图
    app.register_blueprint(api_1_0.api,url_prefix="/api/v1.0")
    return app