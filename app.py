from flask import Flask, render_template, get_flashed_messages, flash, request
from config import session, engine
from modle import Run
from datetime import datetime
from sqlalchemy import and_, func

app = Flask(__name__)
app.secret_key = "tianjin"


@app.route('/')
def index():
    ret = session.query(Run).filter(Run.app_time == func.date_format(func.now(), '%Y-%m-%d')).order_by("dis_time").all()
    # print(ret)
    return render_template("index.html", ret=ret)

if __name__ == "__main__":
    app.run(debug=True)
