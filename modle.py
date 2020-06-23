from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, DateTime, UniqueConstraint, Index, Time, Date
import datetime
# from config import engine,session

Base = declarative_base()


class Run(Base):
    # 表名
    __tablename__ = "test"
    # 字段

    id = Column(Integer, primary_key=True, nullable=False)
    car_number = Column(String(7), nullable=False, index=True)
    supplier = Column(String(20), nullable=False)
    contacts = Column(String(4), nullable=False)
    phone = Column(String(11), nullable=False)
    unloading_contacts = Column(String(4), nullable=False)
    unloading_site = Column(String(11), nullable=False)
    appointment_date = Column(Date, nullable=False)
    unloading_time = Column(Time, nullable=False)
    create_time = Column(DateTime, default=datetime.datetime.now, nullable=False)

# Base.metadata.create_all(engine)
# num=Run(car_number='津A12345',supplier='纳铁福',contacts='张三',phone='13512345678',unloading_contacts='王乐乐',unloading_site=25,appointment_date='2020-06-23',unloading_time='08:30:00')
# session.add(num)
# session.commit()