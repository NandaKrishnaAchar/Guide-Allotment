import db_connect as db
from flask import Flask, redirect, url_for, request, render_template, Response, jsonify

app = Flask(__name__)

@app.route('/pre_ip',methods=['GET','POST'])
def pre():

    print(str(select))
    f= request.form
    value_list=[]

    for key in f.keys():
        for value in f.getlist(key):
            value_list.append(value)
    print(value_list)
    return "done"

@app.route('/pre',methods=['GET','POST'])
def mn():
    l1=db.tnames()
    l1.insert(0,"Unselect--To Change the selected option--")
    l1.insert(0,"--Select--")
    print(l1)
    return render_template("pre.html",names=l1)
    
if __name__=="__main__":
     app.run(host='0.0.0.0',port=80)

