import csv
flag=[0,0]
data = []
usn="01jst17cs005"
password=str(1234)
with open('usn.csv') as f:
    r = csv.reader(f)
    next(r)
    for row in r:
        data.append(row)
for i in data:
    if(usn==i[0]):
        flag[0]=1
        if(password==i[1]):
            flag[1]=1
        else:
            break
if(flag[0]==0):
    print("USN number Error")
elif(flag[1]==0):
    print("Password Error")
else:
    print("Successfully signed up")

