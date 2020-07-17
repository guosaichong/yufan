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
app = Flask(__name__)
app.secret_key = "tianjin"


DBSession = sessionmaker(bind=engine)

login_manager = LoginManager(app)

login_manager.login_view = '/'
login_manager.login_message_category = 'info'
login_manager.login_message = 'Access denied.'


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
    # with open("utils/date.json", 'r') as load_f:
    #     load_dict = json.load(load_f)
    # print(load_dict["1"])
    today = datetime.now().timetuple()
    today=str(today.tm_mon) +"月"+ str(today.tm_mday)+"日"
    print(today)
    # if today != load_dict["1"]:
    #     riqi = get_date.get_date()
    # else:
    #     riqi = load_dict
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

        return render_template("wms_index.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        username = request.form.get('username')
        password = request.form.get("password")
        repet_password=request.form.get("repet_password")
        dbsession=DBSession()
        user =dbsession.query(User).filter_by(username=username).first()
        if not user:
            if password != repet_password:
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
