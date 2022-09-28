from flask import Flask, render_template, flash, redirect, url_for, session, request, logging, jsonify
from wtforms import Form , StringField ,TextAreaField ,PasswordField, validators





# connection code
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#the sqlalchemy is set to track y default this command disallows that feature
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
#connection databse
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:@localhost:3306/rankpoi'
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


#instatiate the db model
db=SQLAlchemy(app)