#!/usr/bin/env
from app import creat_app
from flask import render_template
app = creat_app("product")
@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404
if __name__ == "__main__":
    app.run(port=8000)
