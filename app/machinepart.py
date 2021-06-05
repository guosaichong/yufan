#!/usr/bin/env
import math
from flask import Blueprint, render_template, request, jsonify, url_for, redirect
import os

from flask.helpers import flash
from .models import db, Supplier, Machinepart
from sqlalchemy import and_, func, or_

machinepart = Blueprint('machinepart', __name__)


@machinepart.route('/management', methods=["GET"])
def management():
    return render_template("machinepart/management.html")


@machinepart.route('/add', methods=["GET", "POST"])
def add():
    # 查询零部件所属的供应商

    suppliers = Supplier.query.all()
    print(suppliers)

    if request.method == "GET":

        return render_template('machinepart/add.html', suppliers=suppliers)
    elif request.method == "POST":
        input_supplier = request.form.get("supplier")
        input_part_name = request.form.get('part_name')
        input_part_number = request.form.get('part_number')
        input_amount = request.form.get("amount")
        input_quantifier = request.form.get("quantifier")

        supplier = Supplier.query.filter(
            Supplier.supplier_number == input_supplier).first()

        # print(supplier)
        part = Machinepart.query.filter(
            Machinepart.part_number == input_part_number).first()
        
        if part:
            supplier.machineparts.append(part)
            db.session.commit()
            flash("添加成功")
            return render_template('machinepart/add.html', suppliers=suppliers)
        new_part = Machinepart(
            part_number=input_part_number, part_name=input_part_name, amount=0, quantifier=input_quantifier)
        
        supplier.machineparts.append(new_part)

        db.session.commit()
        flash("添加成功")
        return render_template('machinepart/add.html', suppliers=suppliers)

@machinepart.route('/query_part', methods=[ "POST"])
def query_part():
    input_part_number=request.form.get("part_number")
    part = Machinepart.query.filter(Machinepart.part_number == input_part_number).first()
    if part:
        RET={
            "part_name":part.part_name,
            "quantifier":part.quantifier,
            "readonly":True,
        }
        return jsonify(RET)
    RET={"readonly":False}
    return jsonify(RET)
# 删除零部件


@machinepart.route('/del_machinepart_index', methods=['GET', 'POST'])
def del_machinepart_index():

    if request.method == "GET":

        part_members = db.session.query(Machinepart).all()
        print(part_members)
        return render_template('machinepart/del_machinepart_index.html', part_members=part_members)
    elif request.method == "POST":

        input_machinepart = request.form.get('machinepart')

        input_machinepart = db.session.query(Machinepart).filter(or_(Machinepart.part_number.like(
            '%'+input_machinepart+'%'), Machinepart.part_name.like('%'+input_machinepart+'%')))
        # print(input_supplier.count())
        if input_machinepart.count():

            return render_template('machinepart/del_machinepart_index.html', part_members=input_machinepart)
        else:
            flash('没有找到')

            part_numbers = db.session.query(Machinepart).all()
            return render_template('machinepart/del_machinepart_index.html', part_members=part_numbers)

# 删除零部件


@machinepart.route("/del_machinepart/<del_part_number>")
def del_machinepart(del_part_number):

    # 查询
    machinepart = db.session.query(Machinepart).filter_by(
        part_number=del_part_number).first()
    # 有就删除
    if machinepart:
        try:
            # # 先删除supplier_to_machinepart中machinepart_id为machinepart.id的所有记录
            # dbsession.query(Supplier_To_Machinepart).filter_by(machinepart_id=machinepart.id).delete()
            db.session.delete(machinepart)
            db.session.commit()

            flash("已删除")
        except Exception as e:
            print(e)
            flash("删除零部件出错")
            db.session.rollback()
    else:
        flash("供应商找不到")
    return redirect(url_for("machinepart.del_machinepart_index"))
# 展示零件信息


@machinepart.route('/machinepart_info', methods=["GET", "POST"])
def machinepart_info():
    if request.method == "GET":
        return render_template("machinepart/machinepart_info.html")
    else:
        # 零件种类数
        machinepart_amount = Machinepart.query.count()
        # print(machinepart_amount)
        # 每页显示15条，共有多少页
        page_total = math.ceil(machinepart_amount/15)
        # 前15条数据
        ret = Machinepart.query.limit(15).all()
        # print(ret)
        part_list=[]
        for r in ret:
            obj={"part_number":r.part_number,"part_name":r.part_name,"amount":r.amount,"quantifier":r.quantifier}
            # print(obj)
            supplier_list=[]
            for s in r.suppliers:
                
                supplier_list.append(s.supplier_name)
            # print(supplier_list)
            obj["suppliers"]=supplier_list    
            
            # print(obj)
            part_list.append(obj)
        # print(part_list)
        
        RET = {
            "machinepart_amount": machinepart_amount,
            "page_total":page_total,
            "part_list":part_list
        }
        return jsonify(RET)
# 修改零件信息
@machinepart.route('/mod_machinepart_index', methods=["GET", "POST"])
def mod_machinepart_index():
    if request.method == "GET":
        machinepart_numbers = db.session.query(Machinepart).all()
        return render_template('machinepart/mod_machinepart_index.html', machinepart_numbers=machinepart_numbers)
    elif request.method == "POST":

        input_part_number = request.form.get('part_number')
        part_number = db.session.query(Machinepart).filter(or_(Machinepart.part_number.like(
            '%'+input_part_number+'%'), Machinepart.part_name.like('%'+input_part_number+'%')))
        
        if part_number.count():

            return render_template('machinepart/mod_machinepart_index.html',  machinepart_numbers=part_number)
        else:
            flash('没有找到')
            
            machinepart_numbers = db.session.query(Machinepart).all()
        
            return render_template('machinepart/mod_machinepart_index.html', machinepart_numbers=machinepart_numbers)
# 修改零件详情
@machinepart.route("/mod_machinepart/<mod_machinepart_number>", methods=['GET', 'POST'])
def mod_machinepart(mod_machinepart_number):
    if request.method == "GET":
        # 查询
        
        part = db.session.query(Machinepart).filter_by(
            part_number=mod_machinepart_number).first()
        
        

        return render_template('machinepart/mod_machinepart_detail.html', mod_machinepart_number=mod_machinepart_number, mod_machinepart_name=part.part_name)
    elif request.method == "POST":
        input_part_name = request.form.get('part_name')
        input_part_number = request.form.get('part_number')
        db.session.query(Machinepart).filter(Machinepart.part_number == input_part_number).update(
            {Machinepart.part_name: input_part_name})
        db.session.commit()
        flash("修改成功")
        
        return render_template('machinepart/mod_machinepart_detail.html', mod_machinepart_number=mod_machinepart_number, mod_machinepart_name=input_part_name)