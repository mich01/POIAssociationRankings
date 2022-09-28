from flask import Flask, jsonify, make_response,request, json
from dbconnect import app
from models.Admin import db, Admin
from flask_cors import CORS, cross_origin

cors = CORS(app)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/')
def index():
    SearchAdmin = json.dumps([u.as_dict() for u in Admin.query.all()])
    return SearchAdmin

@app.route('/Admin')
def testOriginal():
    SearchAdmin = Admin.query.all()
    for i in SearchAdmin:
        print(i.ID," ",i.UserName)
    return make_response("SS")

