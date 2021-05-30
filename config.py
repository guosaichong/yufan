
import pymysql


# app配置


class Config(object):
    """配置信息"""

    SECRET_KEY = "tianjin"
    # mysql配置
    # SQLALCHEMY_DATABASE_URI = "mysql+pymysql://用户名:密码@主机地址/数据库名?charset=utf8mb4"
    
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_POOL_SIZE = 10
    # 设定连接池的连接超时时间。默认是 10 。
    SQLALCHEMY_POOL_TIMEOUT = 10
    # 多少秒后自动回收连接。这对 MySQL 是必要的， 它默认移除闲置多于 8 小时的连接。注意如果 使用了 MySQL ， Flask-SQLALchemy 自动设定这个值为 2 小时。
    SQLALCHEMY_POOL_RECYCLE = 7200
    SESSION_PROTECTION='strong'
    LOGIN_VIEW='visitor.login'


class DevelopmentConfig(Config):
    """开发模式的配置信息"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = ""

class ProductionConfig(Config):
    """生产环境的配置信息"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = ""

config_map = {
    "develop": DevelopmentConfig,
    "product": ProductionConfig
}

# 新浪邮箱设置
HOST='smtp.sina.com'
PORT=465
ACCOUNT='gsc21@sina.com'
PASSWORD=''
