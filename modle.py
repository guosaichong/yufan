from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, DateTime, UniqueConstraint, Index, Time, Date
import datetime
from config import engine

Base = declarative_base()


class Run(Base):
    # 表名
    __tablename__ = "run"
    # 字段

    ID = Column(Integer, primary_key=True, nullable=False)
    car = Column(String(10), nullable=False, index=True)
    supplier = Column(String(20), nullable=False)
    name = Column(String(4), nullable=False)
    tel = Column(String(11), nullable=False)
    unloading = Column(String(4), nullable=False)
    position = Column(Integer, nullable=False)
    app_time = Column(Date, nullable=False)
    dis_time = Column(Time, nullable=False)
    sub_time = Column(DateTime, default=datetime.datetime.now, nullable=False)

# Base.metadata.create_all(engine)
