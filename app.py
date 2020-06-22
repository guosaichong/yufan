from flask import Flask,render_template,get_flashed_messages,flash,request
from config import session,engine
from modle import Run
import datetime
from sqlalchemy import and_

app=Flask(__name__)
app.secret_key = "tianjin"


@app.route('/')
def index():
    ret = session.query(Run).order_by("dis_time").all()
    # print(ret)
    return render_template("index.html",ret=ret)

if __name__ == "__main__":
    app.run(debug=True)