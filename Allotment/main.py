from flask import Flask,render_template,request,flash,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
import csv
import db_connect as db1
import logic as l

flag_block=1

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
        usn = db.Column(db.String(30), primary_key=True)
        sname = db.Column(db.String(30), unique=False, nullable=False)
        status = db.Column(db.String(50), unique=True, nullable=False)
        sem = db.Column(db.String(50), unique=True, nullable=False)
        guide_id = db.Column(db.String(50), unique=True, nullable=False)
        section = db.Column(db.String(50), unique=True, nullable=False)
        preference = db.Column(db.String(50), unique=True, nullable=False)

class alloted_info(db.Model):
    usn=db.Column(db.String(20),primary_key=True)
    sname=db.Column(db.String(255))
    section=db.Column(db.String(255))
    tname=db.Column(db.String(255))

usn=''


@app.route('/',methods=['GET','POST'])
def home():
    global flag
    global usn
    if (request.method == 'POST'):
        usn = request.form.get('usn')
        password = request.form.get('pass')
        usn=usn.lower()
        flag = [0, 0]
        data = []
        with open('usn.csv') as f:
            r = csv.reader(f)
            next(r)
            for row in r:
                data.append(row)
        print(data)
        for i in data:
            if (usn.casefold() == i[0].casefold()):
                flag[0] = 1
                if (password == i[1]):
                    flag[1] = 1
                else:
                    break
        if (flag[0] == 0):
            print("USN number Error")
        elif (flag[1] == 0):
            print("Password Error")
        else:
            print("Successfully signed up")
            if(usn=="admin"):
                post = alloted_info.query.order_by(alloted_info.usn).all()
                print("HI")
                print(post)
                return render_template('main.html',post=post)
            print(flag_block,"Valueee")
            if(flag_block==1):
                l1=db1.tnames()
                #l1.insert(0,"Unselect--To Change the selected option--")
                l1.insert(0,"--Select--")
                print(l1)
                return render_template("pre.html",names=l1)
            else:
                return "Web Page Blocked"
    return render_template('index.html',params=params)

@app.route('/pre_ip',methods=['GET','POST'])
def pre():
    global usn
    f= request.form
    value_list=[]
    
    for key in f.keys():
        for value in f.getlist(key):
            value_list.append(value)
    print(usn.upper(),value_list)
    db1.update_preference(usn.upper(),value_list)
    return "done"

@app.route('/admin',methods=['GET','POST'])
def admin():
    global flag_block
    f= request.form
    key_list=[]
    value_list=[]

    for key in f.keys():
        for value in f.getlist(key):
            key_list.append(key)
            value_list.append(value)
    print(key_list,value_list)

    if(key_list[0]=='run'):    
        db1.run()
        return "Executed Succesfully"

    if(key_list[0]=='block'):
        flag_block=0
        print(flag_block,"Blockkk")
        return "Successfully Blocked"

    if(key_list[0]=="unblock"):
        print(flag_block,"Unblockkk")
        flag_block=1
        return "Unblocked"
 



if __name__=="__main__":
     app.run(host='0.0.0.0',port=80)
