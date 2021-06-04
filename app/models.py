#!/usr/bin/env
# mysql 日期设置默认值必须使用timestamp类型
from sqlalchemy.sql.sqltypes import Boolean, Integer, TIMESTAMP
from sqlalchemy.sql import func
from . import db
import datetime
from sqlalchemy import text
from flask_login import UserMixin

class Visitor(db.Model):
    __tablename__ = 'visitor'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(16), nullable=False)
    phone = db.Column(db.String(16), nullable=False, index=True)
    license_number = db.Column(db.String(10), nullable=False)
    supplier = db.Column(db.String(30), nullable=False)
    logistics_company = db.Column(db.String(30), nullable=False)
    create_time = db.Column(TIMESTAMP, server_default=func.now())

    def __init__(self, name, phone, license_number, supplier, logistics_company):
        self.name = name
        self.phone = phone
        self.license_number = license_number
        self.supplier = supplier
        self.logistics_company = logistics_company

    def __repr__(self):
        return "<Visitor(name:%s,phone:%s,license_number:%s,supplier:%s,logistics_company:%s)>" % (self.name, self.phone, self.license_number, self.supplier, self.logistics_company)
# 角色用户表，一个角色对应多个用户，一个用户只能有一个角色（一对多）


class Role(db.Model):
    __tablename__ = "role"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(18), nullable=False, unique=True, index=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Role(name:%s)>" % self.name
# 外键要在多的一方，关系可以在任一方


class User(db.Model,UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(16), nullable=False, unique=True)
    password = db.Column(db.String(64), nullable=False)
    cellphone = db.Column(db.String(20), unique=True,
                          nullable=False, index=True)
    email = db.Column(db.String(60), unique=True, nullable=False)

    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    create_time = db.Column(
        TIMESTAMP, server_default=func.now(), nullable=False)

    role = db.relationship("Role", backref="users")

    def __init__(self, username, password, cellphone, email,):
        self.username = username
        self.password = password
        self.cellphone = cellphone
        self.email = email

    def __repr__(self):
        return "<User(username: %s,password:%s,cellphone:%s,email:%s)>" % (self.username, self.password, self.cellphone, self.email)


# 供应商和零件表，一个供应商可以供应多个零件，一个零件可以由多个供应商供应，多对多的关系，多对多需要第三张表
supplier_to_machinepart = db.Table("supplier_to_machinepart", db.Column('supplier_id', db.Integer, db.ForeignKey('supplier.id'), primary_key=True),
                                   db.Column('machinepart_id', db.Integer, db.ForeignKey('machinepart.id'), primary_key=True))


class Supplier(db.Model):
    __tablename__ = "supplier"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    supplier_number = db.Column(
        db.String(20), nullable=False, index=True, unique=True)
    supplier_name = db.Column(db.String(30), nullable=False, unique=True)
    machineparts = db.relationship(
        "Machinepart", secondary=supplier_to_machinepart, backref='suppliers')

    def __init__(self, supplier_number, supplier_name):
        self.supplier_number = supplier_number
        self.supplier_name = supplier_name

    def __repr__(self):
        return "<Supplier(supplier_number:%s,supplier_name:%s)>" % (self.supplier_number, self.supplier_name)


class Machinepart(db.Model):
    __tablename__ = "machinepart"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    part_number = db.Column(
        db.String(20), nullable=False, index=True, unique=True)
    part_name = db.Column(db.String(30), nullable=False)
    # Integer,Boolean类型设置默认值需要from sqlalchemy import text text("字符串")
    amount = db.Column(db.Integer, server_default=text("0"), nullable=False)
    quantifier = db.Column(db.String(2), nullable=False)

    def __init__(self, part_number, part_name, amount, quantifier):
        self.part_number = part_number
        self.part_name = part_name
        self.amount = amount
        self.quantifier = quantifier

    def __repr__(self):
        return "<Machinepart(part_number:%s,part_name:%s,amount:%d,quantifier:%s)>" % (self.part_number, self.part_name, self.amount, self.quantifier)

# 部门和办公设备的关系 一个部门可以使用多个办公设备 一个办公设备只能被一个部门使用 一对多的关系
class Department(db.Model):
    __tablename__ = "department"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False, index=True, unique=True)
    leader = db.Column(db.String(10), nullable=False, index=True)

    def __init__(self, name, leader):
        self.name = name
        self.leader = leader

    def __repr__(self):
        return "<Department(name:%s,leader:%s)>" % (self.name, self.leader)
# 类别和办公设备的关系 一个类别可以有多个办公设备 一个办公设备只能属于一个类别 一对多的关系
class Category(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False, index=True, unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Category(name:%s)>" % (self.name)
# 存放位置和办公设备的关系 一对多的关系
class Location(db.Model):
    __tablename__ = "location"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False, index=True, unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Location(name:%s)>" % (self.name)

class Equipment(db.Model):
    __tablename__ = "equipment"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(10), nullable=False, index=True)
    model = db.Column(db.String(20))
    user=db.Column(db.String(10))
    IPaddress=db.Column(db.String(20))
    asset_number = db.Column(db.String(20), nullable=False, unique=True)
    asset_status = db.Column(db.Enum("在用", "闲置", "报废"), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    department = db.relationship("Department", backref="equipments")
    category = db.relationship("Category", backref="equipments")
    location = db.relationship("Location", backref="equipments")

    def __init__(self, name, model, user, IPaddress,asset_number, asset_status,department_id,category_id,location_id):
        self.name = name
        self.model = model
        self.user=user
        self.IPaddress=IPaddress
        
        self.asset_number = asset_number
        self.asset_status = asset_status
        self.department_id=department_id
        self.category_id=category_id
        self.location_id = location_id

    def __repr__(self):
        return "<Equipment(name:%s,model:%s,asset_number:%s,asset_status:%s)>" % (self.name, self.model, self.asset_number, self.asset_status)
