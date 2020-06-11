from flask_sqlalchemy import SQLAlchemy
import json

from flask import Flask, redirect, url_for, request, render_template, Response, jsonify
def run():
    
    
    app = Flask(__name__)

    with open('config.json','r') as c:
        params=json.load(c)["params"]

    if(params['local_server']):
        app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']
    db = SQLAlchemy(app)

    class student(db.Model):
        usn= db.Column(db.String(30), primary_key=True)
        preference = db.Column(db.String(255), unique=True,nullable=False)
        status=db.Column(db.Integer)

    class teacher(db.Model):
        tid=db.Column(db.Integer, primary_key=True)
        cnt=db.Column(db.Integer)


    post1=teacher.query.all()
    post = student.query.all()



    for i in post:
        print(i.usn," ",i.preference," ",i.status)

    mentor_status=[]
    for i in post1:
        mentor_status.append(i.cnt)

    print("Mentor Status Initial : ",mentor_status)


    preference={}

    for i in post:
        preference[i.usn]=i.preference

    status={}
    alloted={}
    for key,value in preference.items():
        preference_list=value.split(",")
        for i in preference_list:
            if(mentor_status[int(i)]>0):
                alloted[key]=i
                status[key]=1
                mentor_status[int(i)]-=1
                
                break
        else:
            status[key]=0
            alloted[key]="NULL"
    for key,value in alloted.items():
        print(f"{key} : {value}")
    print("Mentor Status after allocation :  ",mentor_status) 
    return alloted
print(run())
