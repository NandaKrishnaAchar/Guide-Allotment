from flask import Flask,render_template,request,flash,redirect,url_for
from datetime import datetime
import json

with open('config.json','r') as c:
    params=json.load(c)["params"]

app = Flask(__name__)
@app.route('/',methods=['GET','POST'])
def home():
    if (request.method == 'POST'):
        f=request.form
        key_list=[]
        val=[]
        for key in f.keys():
            for value in f.getlist(key):
                key_list.append(key)
                val.append(value)
        print(key_list)
        print(val)
    return render_template('garbage.html',params=params)

if __name__=="__main__":
     app.run(port=5000, debug=True)