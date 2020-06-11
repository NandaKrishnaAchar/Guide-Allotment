from flask import Flask,render_template,request,flash,redirect,url_for,session
from flask_sqlalchemy import SQLAlchemy
import datetime
import json
import random
import random_link as rl
import csv
import mail as m

with open('config.json','r') as c:
    params=json.load(c)["params"]

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
if(params['local_server']):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']
db = SQLAlchemy(app)

class group_others(db.Model):
    usn= db.Column(db.String(255), primary_key=True)
    name = db.Column(db.String(255), unique=False,nullable=False)
    email = db.Column(db.String(255), unique=False, nullable=False)
    phn = db.Column(db.String(15), unique=False, nullable=False)
    sec = db.Column(db.String(2), unique=False, nullable=False)
    GA = db.Column(db.String(2), unique=False, nullable=False)
    status = db.Column(db.Integer, unique=True,nullable=False)

class group_a(db.Model):
    USN= db.Column(db.String(255), primary_key=True)
    Name = db.Column(db.String(255), unique=False,nullable=False)
    sent_string = db.Column(db.String(255), unique=False,nullable=False)
    GB= db.Column(db.String(15), unique=False,nullable=False)
    GC= db.Column(db.String(15), unique=False,nullable=False)
    GD= db.Column(db.String(15), unique=False,nullable=False)




class transaction(db.Model):
    tid=db.Column(db.String(15),primary_key=True)
    susn=db.Column(db.String(15),primary_key=False)
    rusn=db.Column(db.String(15), unique=False,nullable=False)
    GA=db.Column(db.String(2), unique=False,nullable=False)
    transaction_date=db.Column(db.TIMESTAMP(),unique=False,nullable=False)

@app.route('/',methods=['GET','POST'])
def home():
    if (request.method == 'POST'):
        usn = request.form.get('usn')
        password = request.form.get('pass')
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
            flash('USN number Error')
        elif (flag[1] == 0):
            flash("Password Error")
        else:
            session['user']=usn
            if(usn=="admin"):
                post = alloted_info.query.order_by(alloted_info.usn).all()
                print("HI")
                print(post)
                return render_template('main.html',post=post)
            return redirect(url_for('page1'))
    return render_template('index.html')


@app.route('/page2',methods=['GET','POST'])
def page2():

    if(session.get('user') is None):
        print("Condition Satisfied")
        return redirect(url_for('home'))
    else:
        sen = session['user']
        post = group_others.query.order_by(group_others.usn).all()
        post2= group_a.query.filter_by(USN=sen)
        print("post",post)
        print("post2",post2)
        var=""
        for i in post2:
            var=i.sent_string

        arr=var.split(",")
        arr[len(arr)-1]=arr[len(arr)-1][0:12]
        if (request.method == 'POST'):
            f = request.form
            for i in f.keys():
                print("Helloooo  ",end=" ")
                print(i,end=" ")
                for j in f.getlist(i):
                    print(j)
                    rn_seed=int(sen[-3:]+j[-3:])
                    print("Random  ",rn_seed)
                    arr.append(j)
                    lnk=rl.randomlink(rn_seed)
                    entry = transaction(tid=lnk, susn=sen, rusn=j,transaction_date=datetime.datetime.now(),GA=i)
                    db.session.add(entry)
                    db.session.commit()

            stri = ""
            for k in arr:
                if(k==""):
                    continue
                else:
                    stri=stri+k+","
    
            query = group_a.query.filter_by(USN=sen).first()
            ename=query.Name
            query.sent_string = stri
            db.session.commit()
            flash('Mail Sent Sucessfully')
            ed=group_others.query.filter_by(usn=j).all()
            print("Email  ",ed)
            for e in ed:
                email=e.email
                rname=e.name
            
            link="http://ec2-13-233-208-238.ap-south-1.compute.amazonaws.com/confirmation/"+ename.split(" ")[0]+"/"+j+"/"+lnk
            print(link)
            
            m.mail(ename,sen,rname,email,link)



            return redirect(url_for('page2'))

        return render_template('group_allotment.html',post=post,post2=arr)




@app.route('/page1',methods=['GET','POST'])
def page1():
    if(session.get('user')):

        sen = session['user']
        print(sen)
        post1=group_a.query.filter_by(USN=sen).first()
        post2=transaction.query.filter_by(susn=sen)
        arrb={}
        arrc={}
        arrd={}
        res={}
        for i in post2:
            if(i.GA=='B'):
                arrb[i.rusn]=[]
                arrb[i.rusn].append(i.transaction_date)
                arrb[i.rusn].append(i.tid)
            elif(i.GA=='C'):
                arrc[i.rusn]=[]
                arrc[i.rusn].append(i.transaction_date)
                arrc[i.rusn].append(i.tid)

            else:
                arrd[i.rusn]=[]
                arrd[i.rusn].append(i.transaction_date)
                arrd[i.rusn].append(i.tid)
        for key in arrb:
            query=group_others.query.filter_by(usn=key).first()
            arrb[key].append(query.name)
        for key in arrc:
            query=group_others.query.filter_by(usn=key).first()
            arrc[key].append(query.name)
        for key in arrd:
            query=group_others.query.filter_by(usn=key).first()
            arrd[key].append(query.name)

        try:
            gb=group_others.query.filter_by(usn=post1.GB).first()
            res['B']=[post1.GB,gb.name]
        except:
            res['B']=['None','None']


        try:
            gc=group_others.query.filter_by(usn=post1.GC).first()
            res['C']=[post1.GC,gc.name]
        except:
            res['C']=['None','None']
    
        try:
            gd=group_others.query.filter_by(usn=post1.GD).first()
            res['D']=[post1.GB,gd.name]
        except:
            res['D']=['None','None']




        return render_template('group_allotment_front.html',arrb=arrb,arrc=arrc,arrd=arrd,res=res,post1=post1)

    else:
        return redirect(url_for('home'))

@app.route('/logout',methods=['GET','POST'])
def logout():
    session.pop('user',None)
    return render_template('index.html')


@app.route('/unsent',methods=['GET','POST'])
def unsent():
    if (request.method == 'POST'):
        delid=""
        f = request.form
        for i in f.keys():
             for j in f.getlist(i):
                delid=j
        print("delid is : ",delid)
        query1=transaction.query.filter_by(tid=delid).first()
        rusn=query1.rusn
        susn=query1.susn
        query2=group_a.query.filter_by(USN=susn).first()
        sent=query2.sent_string
        arr=sent.split(",")
        arr.remove(rusn)
        string=""
        for i in arr:
            if(i==""):
                continue
            else:
                string=string+i+","

        query2.sent_string=string
        db.session.commit()
        db.session.delete(query1)
        db.session.commit()

        return redirect(url_for('page1'))
    else:
        return redirect(url_for('home'))



@app.route('/confirmation/<name>/<rusn>/<key>')
def hello_name(name,rusn,key):
    print(name,rusn,key)

    query1=transaction.query.filter_by(tid=key).first()
    ga=query1.GA
    susn=query1.susn
    print(susn,ga)
    
    query = group_others.query.filter_by(usn=rusn).one()        
    query.status = 1
    db.session.commit()

    query = group_a.query.filter_by(USN=susn).one()

    if(ga=='B'):
        query.GB=rusn
    elif(ga=='C'):
        query.GC=rusn
    else:
        query.GD=rusn
    db.session.commit()

     
    x=transaction.query.filter_by(tid=key).one()
    db.session.delete(x)
    db.session.commit()

    

    return render_template('tq.html',name=name)

@app.route("/home")
def home2():
    return render_template("front_page1.html")


if __name__=="__main__":
     app.run(host='0.0.0.0',port=80)

