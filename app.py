from flask import Flask, render_template, get_flashed_messages, flash, request
from config import session, engine
from modle import Run
from datetime import datetime
from sqlalchemy import and_, func
from utils import get_date

app = Flask(__name__)
app.secret_key = "tianjin"
if len(get_date.get_date())!=0:
    riqi=get_date.get_date()

@app.route('/')
def index():
    ret = session.query(Run).filter(Run.appointment_date == func.date_format(func.now(), '%Y-%m-%d')).order_by("unloading_time").all()
    # print(ret)
    return render_template("index.html", ret=ret,riqi=riqi)

if __name__ == "__main__":
    app.run(debug=True)
