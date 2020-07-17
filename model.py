from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, DateTime, UniqueConstraint, Index, Time, Date,ForeignKey
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy.orm import sessionmaker,relationship
from config import engine
Base = declarative_base()


class Run(Base):
    # 表名
    __tablename__ = "test"
    # 字段

    id = Column(Integer, primary_key=True, nullable=False)
    car_number = Column(String(7), nullable=False, index=True)
    car_model = Column(String(10))
    supplier = Column(String(20), nullable=False)
    contacts = Column(String(4), nullable=False)
    phone = Column(String(11), nullable=False)
    unloading_contacts = Column(String(4), nullable=False)
    unloading_site = Column(String(11), nullable=False)
    appointment_date = Column(Date, nullable=False)
    unloading_time = Column(Time, nullable=False)
    create_time = Column(DateTime, default=datetime.datetime.now, nullable=False)
class User(UserMixin, Base):
    __tablename__ = "user"
   
    # 字段
    id = Column(Integer, primary_key=True, nullable=False,autoincrement=True)
    username = Column(String(18), nullable=False, unique=True, index=True)
    password_hash = Column(String(128), nullable=False)
    create_time = Column(
        DateTime, default=datetime.datetime.now, nullable=False)

    # role=relationship('Role',backref='user')

    def hash_password(self,password):
        self.password_hash=generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)
    

    def __repr__(self):
        return '<User %r>' % self.username
class Role(Base):
    __tablename__="role"
    
    rid=Column(Integer, primary_key=True, nullable=False,autoincrement=True)
    rname=Column(String(18), nullable=False, unique=True, index=True)
class UserToRole(Base):
    __tablename__ = 'user_to_role'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    role_id = Column(Integer, ForeignKey('role.rid'))
# Base.metadata.create_all(engine)
