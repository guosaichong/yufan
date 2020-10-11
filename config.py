from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import mysql
import redis

class Config(object):
    """配置信息"""
    
    SECRET_KEY="tianjin"

    # 数据库配置
    engine = create_engine("mysql://test:123456@39.102.200.61/yufan?charset=utf8",
                        max_overflow=0,  # 超过连接池大小外最多创建的连接
                        pool_size=20,  # 连接池大小
                        pool_pre_ping=True,  # 预检测链接是否有效
                        pool_timeout=30,  # 池中没有线程最多等待的时间，否则报错
                        pool_recycle=-1  # 多久之后对线程池中的线程进行一次连接的回收（重置）
                        )
    # redis
    REDIS_HOST="39.102.200.61"
    REDIS_PORT=6379

    # flask-session配置
    SESSION_TYPE="redis"
    SESSION_REDIS=redis.StrictRedis(host=REDIS_HOST,port=REDIS_PORT)
    SESSION_USE_SIGNER=True # 对cookie中的session_id进行隐蔽处理
    PERMANENT_SESSION_LIFETIME=86400 # session数据的有效期，单位秒

class DevelopmentConfig(Config):
    """开发模式的配置信息"""
    DEBUG=True
class ProductionConfig(Config):
    """生产环境的配置信息"""
    pass

config_map={
    "develop":DevelopmentConfig,
    "product":ProductionConfig
}

