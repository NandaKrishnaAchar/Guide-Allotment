from flask import Flask,render_template,request,flash,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

with open('config.json','r') as c:
    params=json.load(c)["params"]

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

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


post = student.query.all()
print(post)

for i in post:
    print(i.usn,end=" ")
    print(i.sname,end=" ")
    print(i.status,end=" ")
    print(i.sem,end=" ")
    print(i.guide_id,end=" ")
    print(i.section,end=" ")
    print(i.preference)
