from flask import Flask,render_template,request,flash,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from datetime import datetime
import json

with open('config.json','r') as c:
    params=json.load(c)["params"]

app = Flask(__name__)

if(params['local_server']):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']
db = SQLAlchemy(app)

if(params['local_server']):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']
db = SQLAlchemy(app)

class student(db.Model):
    usn= db.Column(db.String(30), primary_key=True)
    sname = db.Column(db.String(30), unique=False,nullable=False)
    status = db.Column(db.String(50), unique=True,nullable=False)
    sem = db.Column(db.String(50), unique=True,nullable=False)
    guide_id = db.Column(db.String(50), unique=True,nullable=False)
    section = db.Column(db.String(50), unique=True,nullable=False)
    preference = db.Column(db.String(50), unique=True,nullable=False)


@app.route('/')
def home():
    post = student.query.order_by(student.usn).all()
    return render_template('main.html',params=params,post=post)

