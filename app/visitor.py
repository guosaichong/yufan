#!/usr/bin/env
from flask import Blueprint, render_template, request, jsonify, send_file
from sqlalchemy.sql.functions import func
from . import db
from .models import Visitor, User
import datetime
import math
from flask_login import login_required, login_user, logout_user
visitor = Blueprint('visitor', __name__)
import sys
sys.path.append("..")

@visitor.route("/", methods=["GET", "POST"])
def access():
    if request.method == "GET":
        # db.create_all()
        return render_template("access.html")
    else:
        # POST提交数据
        try:
            visitor_info = request.form.to_dict()
            # print(visitor_info)
            new_visitor = Visitor(name=visitor_info.get("visitor_name"), phone=visitor_info.get("phone"), license_number=visitor_info.get(
                "license_number"), supplier=visitor_info.get("supplier"), logistics_company=visitor_info.get("logistics_company"))
            db.session.add(new_visitor)
            db.session.commit()
            RET = {
                "code": 0,
                "msg": "上传成功！"
            }
            return jsonify(RET)
        except:
            RET = {
                "code": 1,
                "msg": "上传失败，请重新提交！"
            }
            return jsonify(RET)


@visitor.route('/visitor', methods=["GET", "POST"])
def visitor_info():
    if request.method == "GET":
        

        return render_template("visitor_info.html")
    else:
        search_date = request.form.get("search_date")
        # print(search_date)
        quantity = db.session.query(func.count(Visitor.id)).filter(
            db.cast(Visitor.create_time, db.DATE) == db.cast(search_date, db.DATE)).scalar()
        # print(quantity)
        page_total = math.ceil(quantity/15)
        # print(page_total)
        ret = db.session.query(Visitor.name, Visitor.phone, Visitor.license_number, Visitor.supplier, Visitor.logistics_company, Visitor.create_time).filter(
            db.cast(Visitor.create_time, db.DATE) == db.cast(search_date, db.DATE)).paginate(1,15).items
        # print(ret)
        RET={
            "quantity":quantity,
            "page_total":page_total,
            "ret":ret
        }
        # print(RET)
        return jsonify(RET)


@visitor.route('/visitor/<search_date>/<page_number>', methods=["POST"])
def get_data(search_date, page_number):
    search_date = request.form.get("search_date")
    page_number = request.form.get("page_number")
    # print(page_number)
    quantity = db.session.query(func.count(Visitor.id)).filter(
            db.cast(Visitor.create_time, db.DATE) == db.cast(search_date, db.DATE)).scalar()
    # print(quantity)
    page_total = math.ceil(quantity/15)
    # print(page_total)
    ret = db.session.query(Visitor.name, Visitor.phone, Visitor.license_number, Visitor.supplier, Visitor.logistics_company, Visitor.create_time).filter(
        db.cast(Visitor.create_time, db.DATE) == db.cast(search_date, db.DATE)).paginate(int(page_number),15).items
    # print(ret)
    RET={
            "page_total":page_total,
            "ret":ret
        }
    # print(RET)
    return jsonify(RET)

@visitor.route("/favicon.ico", methods=["GET"])
def favicon_ico():
    return send_file("favicon.ico")



@visitor.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('login.html')
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        # print(user)
        if not user:
            RET = {
                "code": 1,
                "msg": "用户尚未注册！"
            }

            return jsonify(RET)

        if not user.password == password:
            RET = {
                "code": 2,
                "msg": "密码错误！"
            }

            return jsonify(RET)
        login_user(user)
        RET = {
            "code": 0,
            "msg": "登录成功！"
        }
        return jsonify(RET)


@visitor.route('/wms_index', methods=['GET', 'POST'])
def wms_index():

    return render_template("wms_index.html")

@visitor.route('/forget', methods=["GET", "POST"])
def forget():
    if request.method == "GET":
        return render_template('forget.html')
    else:
        username = request.form.get("username")
        email = request.form.get("email")
        user = User.query.filter_by(username=username).first()
        # print(user.email)
        if not user:
            RET = {
                "code": 1,
                "msg": "用户尚未注册！"
            }

            return jsonify(RET)
        if user.email!=email:
            RET = {
                "code": 2,
                "msg": "邮箱地址不正确！"
            }

            return jsonify(RET)
        # 生成随机8个字符作为新密码
        import string,random
        goal = ''.join(random.sample(string.ascii_letters+string.digits,8))
        # print(goal)
        # 将新密码通过邮件发给用户
        from utils.email_serve import mail

        if mail(email,"忘记密码","请使用如下密码登录："+goal):
            import hashlib
            
            password_md5=hashlib.md5(goal.encode(encoding="utf-8")).hexdigest()
            # print(password_md5)
            User.query.filter_by(username=username).update({"password":password_md5})
            db.session.commit()
            RET = {
                "code": 0,
                "msg": "更改成功！"
            }
            return jsonify(RET)
@visitor.route('/success', methods=["GET", "POST"])
def success():
    
    return render_template('success.html')

@visitor.route('/register', methods=["GET", "POST"])
def register():
    if request.method=="GET":
        return render_template('register.html')
    else:
        pass        