from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import mysql.connector

# 数据库配置
engine = create_engine("mysql+mysqlconnector://test:123456@47.105.166.136/yufan?charset=utf8",
                       max_overflow=0,  # 超过连接池大小外最多创建的连接
                       pool_size=50,  # 连接池大小
                       pool_timeout=30,  # 池中没有线程最多等待的时间，否则报错
                       pool_recycle=-1  # 多久之后对线程池中的线程进行一次连接的回收（重置）
                       )

