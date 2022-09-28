from flask import render_template

from dbconnect import app


@app.route('/test', methods=['GET'])
def pager():
    return render_template('index.html')