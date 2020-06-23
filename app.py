from flask import Flask, render_template, get_flashed_messages, flash, request
from config import engine
from modle import Run
from datetime import datetime
from sqlalchemy import and_, func
from utils import get_date
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
app.secret_key = "tianjin"


riqi=get_date.get_date()
Session = sessionmaker(bind=engine)
@app.route('/')
def index():
    session=Session()
    ret = session.query(Run).filter(Run.appointment_date == func.date_format(func.now(), '%Y-%m-%d')).order_by("unloading_time").all()
    # print(ret)
    return render_template("index.html", ret=ret,riqi=riqi)

if __name__ == "__main__":
    app.run(debug=True,host="192.168.11.200")
