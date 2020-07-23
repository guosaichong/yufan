from flask import Flask, render_template, get_flashed_messages, flash, request,redirect,url_for
from config import engine
from model import *
from datetime import datetime
from sqlalchemy import and_, func
from utils import get_date
from sqlalchemy.orm import sessionmaker
import time
import json
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import os
import logging

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
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
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
today=str(today.tm_mon) +"月"+ str(today.tm_mday)+"日"
# print(today)

@login_manager.user_loader
def get_user(user_id):
    dbsession=DBSession()
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

    return render_template("index.html", ret=ret,today=today)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        username = request.form.get('username')
        password = request.form.get("password")
        dbsession=DBSession()
        user =dbsession.query(User).filter_by(username=username).first()
        if not user:
            flash("用户尚未注册")
            return redirect("/login")
                
        if not user.verify_password(password):
            flash("密码错误")
            return redirect("/login")
        login_user(user)

        return redirect(url_for('wms_index'))

@app.route('/wms_index',methods=['GET', 'POST'])
@login_required
def wms_index():
    
    return render_template("view_base.html")

@app.route('/supplier',methods=['GET', 'POST'])
@login_required
def supplier():
    return render_template("supplier.html")

@app.route('/add_supplier',methods=['GET', 'POST'])
@login_required
def add_supplier():
    if request.method == "GET":
        return render_template('add_supplier.html')
    elif request.method == "POST":
        input_supplier_name=request.form.get('supplier_name')
        input_supplier_number=request.form.get('supplier_number')
        # print(input_supplier_number,input_supplier_name)
        dbsession=DBSession()
        supplier_number =dbsession.query(Supplier).filter_by(supplier_number=input_supplier_number).first()
        supplier_name =dbsession.query(Supplier).filter_by(supplier_name=input_supplier_name).first()
        if supplier_number:
            flash('此供应商号已存在')
            return redirect('/add_supplier')
        if supplier_name:
            flash('此供应商名称已存在')
            return redirect('/add_supplier')
        new_supplier=Supplier(supplier_number=input_supplier_number,supplier_name=input_supplier_name)
        dbsession.add(new_supplier)
        dbsession.commit()
        dbsession.close()
        flash("添加成功")
        time.sleep(1)
        return render_template("add_supplier.html")

@app.route('/del_supplier',methods=['GET', 'POST'])
@login_required
def del_supplier():
    dbsession=DBSession()
    supplier_numbers =dbsession.query(Supplier).all().limit(10)
    dbsession.close()
    return render_template('del_supplier.html',supplier_numbers=supplier_numbers)

@app.route('/supplier_info',methods=['GET', 'POST'])
@login_required
def supplier_info():
    dbsession=DBSession()
    supplier_amount =dbsession.query(func.count(Supplier.id)).scalar()
    dbsession.close()
    return render_template("supplier_info.html",today=today,supplier_amount=supplier_amount)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        username = request.form.get('username')
        password = request.form.get("password")
        repeat_password=request.form.get("repeat_password")
        dbsession=DBSession()
        user =dbsession.query(User).filter_by(username=username).first()
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
