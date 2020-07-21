from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, DateTime, UniqueConstraint, Index, Time, Date, ForeignKey, Table,Enum
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy.orm import sessionmaker, relationship
from config import engine
Base = declarative_base()


class BaseModel(object):
    create_time = Column(DateTime, default=datetime.datetime.now)
    update_time = Column(
        DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)


class Run(Base, BaseModel):
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


user_to_role = Table("user_to_role",Base.metadata, Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
                     Column('role_id', Integer, ForeignKey('role.rid'), primary_key=True))


class User(UserMixin, Base, BaseModel):
    __tablename__ = "user"

    # 字段
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    username = Column(String(18), nullable=False, unique=True, index=True)
    password_hash = Column(String(128), nullable=False)

    role = relationship('Role', secondary=user_to_role, backref='user')

    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username


class Role(Base, BaseModel):
    __tablename__ = "role"

    rid = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    rname = Column(String(18), nullable=False, unique=True, index=True)

supplier_to_machinepart=Table("supplier_to_machinepart",Base.metadata, Column('supplier_id', Integer, ForeignKey('supplier.id'), primary_key=True),
                     Column('machinepart_id', Integer, ForeignKey('machinepart.id'), primary_key=True))

class Supplier(BaseModel,Base):
    __tablename__="supplier"
    id = Column(Integer, primary_key=True, autoincrement=True)
    supplier_number=Column(String(20),nullable=False, index=True)
    supplier_name=Column(String(30),nullable=False)
    machinepart=relationship("Machinepart",secondary=supplier_to_machinepart, backref='supplier')

class Machinepart(BaseModel,Base):
    __tablename__="machinepart"
    id = Column(Integer, primary_key=True, autoincrement=True)
    part_number=Column(String(20),nullable=False, index=True)
    part_name=Column(String(30),nullable=False)
    part_state=Column(Enum('合格','不合格'),default='合格')
    amount=Column(Integer,default=0)
    quantifier=Column(String(2),nullable=False)

Base.metadata.create_all(engine)
