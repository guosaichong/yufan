#!/usr/bin/env
import math
from flask import Blueprint, render_template, request, jsonify, url_for, redirect
from flask.helpers import flash
from .models import db, Supplier
from sqlalchemy import and_, func, or_

supplier = Blueprint('supplier', __name__)


@supplier.route('/supplier_info', methods=["GET","POST"])
def supplier_info():
    if request.method == "GET":
        return render_template("supplier/supplier_info.html")
    else:
        supplier_amount = Supplier.query.count()
        # print(supplier_amount)
        # 每页显示15条，共有多少页
        page_total = math.ceil(supplier_amount/15)
        # 前15条数据
        ret = Supplier.query.limit(15).all()
        # print(ret)
        supplier_list=[]
        for r in ret:
            obj={"supplier_number":r.supplier_number,"supplier_name":r.supplier_name}
            # print(obj)
            part_list=[]
            for s in r.machineparts:
                
                part_list.append(s.part_name)
            
            obj["parts"]=list(set(part_list))  
            
            # print(obj)
            supplier_list.append(obj)
        # print(supplier_list)
        
        RET = {
            "supplier_amount": supplier_amount,
            "page_total":page_total,
            "supplier_list":supplier_list
        }
        return jsonify(RET)

# 管理供应商


@supplier.route('/supplier_management', methods=['GET', 'POST'])
def supplier_management():
    return render_template("supplier/supplier_management.html")
# 添加供应商


@supplier.route('/add_supplier', methods=['GET', 'POST'])
def add_supplier():
    if request.method == "GET":
        return render_template('supplier/add_supplier.html')
    elif request.method == "POST":
        input_supplier_name = request.form.get('supplier_name')
        input_supplier_number = request.form.get('supplier_number')
        # print(input_supplier_number,input_supplier_name)

        supplier_number = Supplier.query.filter_by(
            supplier_number=input_supplier_number).first()
        supplier_name = Supplier.query.filter_by(
            supplier_name=input_supplier_name).first()
        print(supplier_number, supplier_name)
        if supplier_number:
            flash('此供应商号已存在')
            return render_template("supplier/add_supplier.html")
        new_supplier = Supplier(
            supplier_number=input_supplier_number, supplier_name=input_supplier_name)
        db.session.add(new_supplier)
        db.session.commit()
        flash('添加成功！')
        return render_template("supplier/add_supplier.html")
# 删除供应商


@supplier.route('/del_supplier_index', methods=['GET', 'POST'])
def del_supplier_index():

    if request.method == "GET":

        supplier_numbers = Supplier.query.all()
        return render_template('supplier/del_supplier_index.html', supplier_numbers=supplier_numbers)
    elif request.method == "POST":

        input_supplier = request.form.get('supplier_number')

        input_supplier = db.session.query(Supplier).filter(or_(Supplier.supplier_number.like(
            '%'+input_supplier+'%'), Supplier.supplier_name.like('%'+input_supplier+'%')))

        # print(input_supplier.count())
        if input_supplier.count():

            return render_template('supplier/del_supplier_index.html', supplier_numbers=input_supplier)
        else:
            flash('没有找到')
            supplier_numbers = db.session.query(Supplier).all()
            return render_template('supplier/del_supplier_index.html', supplier_numbers=supplier_numbers)

# 删除供应商


@supplier.route("/del/<del_supplier_number>")
def del_info(del_supplier_number):

    # 查询

    supplier = db.session.query(Supplier).filter_by(
        supplier_number=del_supplier_number).first()
    # 有就删除
    
    try:
        db.session.delete(supplier)
        db.session.commit()

        flash("已删除")
    except Exception as e:
        print(e)
        flash("删除供应商出错")
        db.session.rollback()
        return redirect(url_for("supplier.del_supplier_index"))
    return redirect(url_for("supplier.del_supplier_index"))
# 修改供应商
@supplier.route('/mod_supplier_index', methods=['GET', 'POST'])
def mod_supplier_index():
    if request.method == "GET":
        supplier_numbers = db.session.query(Supplier).all()
        return render_template('supplier/mod_supplier_index.html', supplier_numbers=supplier_numbers)
    elif request.method == "POST":

        input_supplier = request.form.get('supplier_number')
        input_supplier = db.session.query(Supplier).filter(or_(Supplier.supplier_number.like(
            '%'+input_supplier+'%'), Supplier.supplier_name.like('%'+input_supplier+'%')))
        # print(input_supplier.count())
        if input_supplier.count():

            return render_template('supplier/mod_supplier_index.html', supplier_numbers=input_supplier)
        else:
            flash('没有找到')
            
            supplier_numbers = db.session.query(Supplier).all()
        
            return render_template('supplier/mod_supplier_index.html', supplier_numbers=supplier_numbers)

# 修改供应商
@supplier.route("/mod_supplier/<mod_supplier_number>", methods=['GET', 'POST'])
def mod_supplier(mod_supplier_number):
    if request.method == "GET":
        # 查询
        
        supplier = db.session.query(Supplier).filter_by(
            supplier_number=mod_supplier_number).first()
        

        return render_template('supplier/mod_supplier_detail.html', mod_supplier_number=mod_supplier_number, mod_supplier_name=supplier.supplier_name)
    elif request.method == "POST":
        input_supplier_name = request.form.get('supplier_name')
        input_supplier_number = request.form.get('supplier_number')
        # print(input_supplier_number, input_supplier_name)
        # supplier_number = db.session.query(Supplier).filter_by(
        #     supplier_number=input_supplier_number).first()

        supplier_name = db.session.query(Supplier).filter_by(
            supplier_name=input_supplier_name).first()
        # print(supplier_number, supplier_name)
        if supplier_name:
            flash('此供应商名称已存在')
            return render_template('supplier/mod_supplier_detail.html', mod_supplier_number=mod_supplier_number, mod_supplier_name=input_supplier_name)
        db.session.query(Supplier).filter(Supplier.supplier_number == input_supplier_number).update(
            {Supplier.supplier_name: input_supplier_name})
        db.session.commit()
        flash("修改成功")
    
        return render_template('supplier/mod_supplier_detail.html', mod_supplier_number=mod_supplier_number, mod_supplier_name=input_supplier_name)
