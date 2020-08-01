from flask import Flask, render_template, get_flashed_messages, flash, request, redirect, url_for
from config import engine
from model import *
from datetime import datetime
from sqlalchemy import and_, func, or_
from utils import get_date
from sqlalchemy.orm import sessionmaker
import time
import json
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import os
import logging

# 创建日志文件目录
basedir = os.path.abspath(os.path.dirname(__file__))
logs_floder = os.path.join(basedir, "logs")
if not os.path.exists(logs_floder):
    os.mkdir(logs_floder)
# 第一步，创建一个logger
logger = logging.getLogger()
logger.setLevel(logging.WARNING)  # Log等级总开关
# 第二步，创建一个handler，用于写入日志文件
rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
log_path = logs_floder + '/'
logfile = log_path + rq + '.log'
fh = logging.FileHandler(logfile, mode='w')
fh.setLevel(logging.DEBUG)  # 输出到file的log等级的开关
# 第三步，定义handler的输出格式
formatter = logging.Formatter(
    "%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
fh.setFormatter(formatter)
# 第四步，将logger添加到handler里面
logger.addHandler(fh)
# 日志
logger.debug('this is a logger debug message')
logger.info('this is a logger info message')
logger.warning('this is a logger warning message')
logger.error('this is a logger error message')
logger.critical('this is a logger critical message')

app = Flask(__name__)
app.secret_key = "tianjin"


DBSession = sessionmaker(bind=engine)

login_manager = LoginManager(app)

login_manager.login_view = '/'
login_manager.login_message_category = 'info'
login_manager.login_message = 'Access denied.'

today = datetime.now().timetuple()
today = str(today.tm_mon) + "月" + str(today.tm_mday)+"日"
# print(today)


@login_manager.user_loader
def get_user(user_id):
    dbsession = DBSession()
    return dbsession.query(User).filter_by(id=user_id).first()


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")


@app.route('/')
def index():
    dbsession = DBSession()
    ret = dbsession.query(Run).filter(Run.appointment_date == func.date_format(
        func.now(), '%Y-%m-%d')).order_by("unloading_time").all()
    dbsession.close()

    return render_template("index.html", ret=ret, today=today)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        username = request.form.get('username')
        password = request.form.get("password")
        dbsession = DBSession()
        user = dbsession.query(User).filter_by(username=username).first()
        # print(user)
        if not user:
            flash("用户尚未注册")
            return redirect("/login")

        if not user.verify_password(password):
            flash("密码错误")
            return redirect("/login")
        login_user(user)

        return redirect(url_for('wms_index'))


@app.route('/wms_index', methods=['GET', 'POST'])
@login_required
def wms_index():

    return render_template("view_base.html")

# 查询供应商信息
@app.route('/supplier_info', methods=['GET', 'POST'])
@login_required
def supplier_info():
    dbsession = DBSession()
    supplier_amount = dbsession.query(func.count(Supplier.id)).scalar()
    dbsession.close()
    return render_template("supplier_info.html", today=today, supplier_amount=supplier_amount)


@app.route('/supplier', methods=['GET', 'POST'])
@login_required
def supplier():
    return render_template("supplier.html")


@app.route('/add_supplier', methods=['GET', 'POST'])
@login_required
def add_supplier():
    if request.method == "GET":
        return render_template('add_supplier.html')
    elif request.method == "POST":
        input_supplier_name = request.form.get('supplier_name')
        input_supplier_number = request.form.get('supplier_number')
        # print(input_supplier_number,input_supplier_name)
        dbsession = DBSession()
        supplier_number = dbsession.query(Supplier).filter_by(
            supplier_number=input_supplier_number).first()
        supplier_name = dbsession.query(Supplier).filter_by(
            supplier_name=input_supplier_name).first()
        print(supplier_number, supplier_name)
        if supplier_number:
            flash('此供应商号已存在')
            return redirect('/add_supplier')
        if supplier_name:
            flash('此供应商名称已存在')
            return redirect('/add_supplier')
        new_supplier = Supplier(
            supplier_number=input_supplier_number, supplier_name=input_supplier_name)
        dbsession.add(new_supplier)
        dbsession.commit()
        dbsession.close()
        flash("添加成功")
        time.sleep(1)
        return render_template("add_supplier.html")


@app.route('/del_supplier_index', methods=['GET', 'POST'])
@login_required
def del_supplier_index():

    if request.method == "GET":
        dbsession = DBSession()
        supplier_numbers = dbsession.query(Supplier).all()
        dbsession.close()
        return render_template('del_supplier_index.html', supplier_numbers=supplier_numbers)
    elif request.method == "POST":

        input_supplier = request.form.get('supplier_number')
        dbsession = DBSession()
        input_supplier = dbsession.query(Supplier).filter(or_(Supplier.supplier_number.like(
            '%'+input_supplier+'%'), Supplier.supplier_name.like('%'+input_supplier+'%')))
        dbsession.close()
        # print(input_supplier.count())
        if input_supplier.count():

            return render_template('del_supplier_index.html', supplier_numbers=input_supplier)
        else:
            flash('没有找到')
            dbsession = DBSession()
            supplier_numbers = dbsession.query(Supplier).all()
            dbsession.close()
            return render_template('del_supplier_index.html', supplier_numbers=supplier_numbers)


@app.route("/del_supplier/<del_supplier_number>")
@login_required
def del_supplier(del_supplier_number):

    # 查询
    dbsession = DBSession()
    supplier = dbsession.query(Supplier).filter_by(
        supplier_number=del_supplier_number).first()
    # 有就删除
    if supplier:
        try:

            dbsession.delete(supplier)
            dbsession.commit()
            dbsession.close()
            flash("已删除")
        except Exception as e:
            print(e)
            flash("删除供应商出错")
            dbsession.rollback()
            dbsession.close()
            return redirect(url_for("del_supplier_index"))
    else:
        flash("供应商找不到")
    return redirect(url_for("del_supplier_index"))


@app.route('/mod_supplier_index', methods=['GET', 'POST'])
@login_required
def mod_supplier_index():
    if request.method == "GET":
        dbsession = DBSession()
        supplier_numbers = dbsession.query(Supplier).all()
        dbsession.close()
        return render_template('mod_supplier_index.html', supplier_numbers=supplier_numbers)
    elif request.method == "POST":

        input_supplier = request.form.get('supplier_number')
        dbsession = DBSession()
        input_supplier = dbsession.query(Supplier).filter(or_(Supplier.supplier_number.like(
            '%'+input_supplier+'%'), Supplier.supplier_name.like('%'+input_supplier+'%')))
        dbsession.close()
        # print(input_supplier.count())
        if input_supplier.count():

            return render_template('mod_supplier_index.html', supplier_numbers=input_supplier)
        else:
            flash('没有找到')
            dbsession = DBSession()
            supplier_numbers = dbsession.query(Supplier).all()
            dbsession.close()
            return render_template('mod_supplier_index.html', supplier_numbers=supplier_numbers)


@app.route("/mod_supplier/<mod_supplier_number>", methods=['GET', 'POST'])
@login_required
def mod_supplier(mod_supplier_number):
    if request.method == "GET":
        # 查询
        dbsession = DBSession()
        supplier = dbsession.query(Supplier).filter_by(
            supplier_number=mod_supplier_number).first()
        # print(supplier.supplier_name)
        dbsession.close()
        if supplier:

            return render_template('mod_supplier_detail.html', mod_supplier_number=mod_supplier_number, mod_supplier_name=supplier.supplier_name)
    elif request.method == "POST":
        input_supplier_name = request.form.get('supplier_name')
        input_supplier_number = request.form.get('supplier_number')
        # print(input_supplier_number, input_supplier_name)
        dbsession = DBSession()
        supplier_number = dbsession.query(Supplier).filter_by(
            supplier_number=input_supplier_number).first()

        supplier_name = dbsession.query(Supplier).filter_by(
            supplier_name=input_supplier_name).first()
        # print(supplier_number, supplier_name)
        if supplier_name:
            flash('此供应商名称已存在')
            return render_template('mod_supplier_detail.html', mod_supplier_number=mod_supplier_number, mod_supplier_name=input_supplier_name)
        dbsession.query(Supplier).filter(Supplier.supplier_number == input_supplier_number).update(
            {Supplier.supplier_name: input_supplier_name})
        dbsession.commit()
        dbsession.close()
        flash("修改成功")
        time.sleep(1)
        return render_template('mod_supplier_detail.html', mod_supplier_number=mod_supplier_number, mod_supplier_name=input_supplier_name)


@app.route('/machinepart_info', methods=['GET', 'POST'])
@login_required
def machinepart_info():
    dbsession = DBSession()
    machinepart_amount = dbsession.query(func.count(Machinepart.id)).scalar()
    dbsession.close()
    return render_template("machinepart_info.html", today=today, machinepart_amount=machinepart_amount)


@app.route('/machinepart', methods=['GET', 'POST'])
@login_required
def machinepart():
    return render_template("machinepart.html")

# 添加零部件
@app.route('/add_machinepart', methods=['GET', 'POST'])
@login_required
def add_machinepart():
    # 查询零部件所属的供应商
    dbsession = DBSession()
    suppliers = dbsession.query(Supplier).all()
    # print(supplier.supplier_name)
    dbsession.close()
    if request.method == "GET":
        
        return render_template('add_machinepart.html',suppliers=suppliers)
    elif request.method == "POST":
        input_supplier=request.form.get("supplier")
        input_part_name = request.form.get('part_name')
        input_part_number = request.form.get('part_number')
        input_amount = request.form.get("amount")
        input_quantifier = request.form.get("quantifier")
        # print(request.form)
        # print(input_part_number,input_part_name)
        dbsession = DBSession()
        supplier=dbsession.query(Supplier).filter_by(supplier_number=input_supplier).first()
        # print(supplier)
        part = dbsession.query(Machinepart).filter_by(
            part_number=input_part_number).first()
        # print(part)
        # part_name = dbsession.query(Machinepart).filter_by(
        #     part_name=input_part_name).first()
        # print(supplier, part)
        if part:
            flash('此零部件号已存在')
            return render_template('add_machinepart.html',suppliers=suppliers)
        new_part = Machinepart(
            part_number=input_part_number, part_name=input_part_name, amount=int(input_amount), quantifier=input_quantifier)
        dbsession.add(new_part)
        dbsession.commit()
        add_part = dbsession.query(Machinepart).filter_by(
            part_number=input_part_number).first()
        new_stom=Supplier_To_Machinepart(supplier_id=supplier.id,machinepart_id=add_part.id)
        dbsession.add(new_stom)
        dbsession.commit()
        dbsession.close()
        flash("添加成功")
        time.sleep(1)
        return render_template('add_machinepart.html',suppliers=suppliers)

@app.route('/del_machinepart_index', methods=['GET', 'POST'])
@login_required
def del_machinepart_index():

    if request.method == "GET":
        dbsession = DBSession()
        part_numbers = dbsession.query(Machinepart).all()
        dbsession.close()
        return render_template('del_machinepart_index.html', part_numbers=part_numbers)
    elif request.method == "POST":

        input_machinepart = request.form.get('machinepart')
        dbsession = DBSession()
        input_machinepart = dbsession.query(Machinepart).filter(or_(Machinepart.part_number.like(
            '%'+input_machinepart+'%'), Machinepart.part_name.like('%'+input_machinepart+'%')))
        dbsession.close()
        # print(input_supplier.count())
        if input_machinepart.count():

            return render_template('del_machinepart_index.html', part_numbers=input_machinepart)
        else:
            flash('没有找到')
            dbsession = DBSession()
            part_numbers = dbsession.query(Machinepart).all()
            dbsession.close()
            return render_template('del_machinepart_index.html', part_numbers=part_numbers)

@app.route("/del_machinepart/<del_part_number>")
@login_required
def del_machinepart(del_part_number):

    # 查询
    dbsession = DBSession()
    machinepart = dbsession.query(Machinepart).filter_by(
        part_number=del_part_number).first()
    # 有就删除
    if machinepart:
        try:

            dbsession.delete(machinepart)
            dbsession.commit()
            dbsession.close()
            flash("已删除")
        except Exception as e:
            print(e)
            flash("删除零部件出错")
            dbsession.rollback()
            dbsession.close()
            return redirect(url_for("del_machinepart_index"))
    else:
        flash("供应商找不到")
    return redirect(url_for("del_machinepart_index"))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        username = request.form.get('username')
        password = request.form.get("password")
        repeat_password = request.form.get("repeat_password")
        dbsession = DBSession()
        user = dbsession.query(User).filter_by(username=username).first()
        if not user:
            if password != repeat_password:
                flash("密码不一样")
                return redirect(url_for('login'))
            new_user = User(username=username)
            new_user.hash_password(password)
            dbsession.add(new_user)
            dbsession.commit()
            dbsession.close()
            flash("注册成功")
            return redirect(url_for('login'))
        else:
            flash("用户已经注册")
            return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)
