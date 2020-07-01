from flask import Flask, render_template, get_flashed_messages, flash, request
from config import engine
from model import Run
from datetime import datetime
from sqlalchemy import and_, func
from utils import get_date
from sqlalchemy.orm import sessionmaker
import time
import json

app = Flask(__name__)
app.secret_key = "tianjin"


Session = sessionmaker(bind=engine)


@app.route('/')
def index():
    with open("utils/date.json", 'r') as load_f:
        load_dict = json.load(load_f)
    print(load_dict["1"])
    today = datetime.now().timetuple()
    today=str(today.tm_mon) +"月"+ str(today.tm_mday)+"日"
    print(today)
    if today != load_dict["1"]:
        riqi = get_date.get_date()
    else:
        riqi = load_dict
    session = Session()
    ret = session.query(Run).filter(Run.appointment_date == func.date_format(
        func.now(), '%Y-%m-%d')).order_by("unloading_time").all()
    session.close()

    return render_template("index.html", ret=ret, riqi=riqi)


if __name__ == "__main__":
    app.run(debug=True)
