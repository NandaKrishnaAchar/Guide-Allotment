import mysql.connector
from mysql.connector import Error
import logic as l

def run():
    try: 
        

         allot=l.run()
         for key,value in allot.items():
            connection = mysql.connector.connect(host= "ec2-13-233-208-238.ap-south-1.compute.amazonaws.com",port=3306,database="SJCE",user= "ec2-user@13.233.208.238",password= "Hello123@")
         
            print(key,value)
            cursor = connection.cursor()
            sql_fetch_query ="""update student set guide_id=%s where usn=%s"""
            name=(value,key)
            result=cursor.execute(sql_fetch_query,name)
            connection.commit()
            cursor.close()
            connection.close()
         return result

    except mysql.connector.Error as error:
         print("Failed to read data from MySQL table {}".format(error))
         return -1
"""    
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
""" 

def read_preference():
    try: 
         connection = mysql.connector.connect(host= "ec2-13-233-208-238.ap-south-1.compute.amazonaws.com",port=3306,database="SJCE",user= "ec2-user@13.233.208.238",password= "Hello123@")
  
         cursor = connection.cursor()
         sql_fetch_query ="""SELECT * from preference"""
         cursor.execute(sql_fetch_query)
         record = cursor.fetchall()
         pre_dict = dict(record)
         print(pre_dict)
         return pre_dict

    except mysql.connector.Error as error:
         print("Failed to read data from MySQL table {}".format(error))
         return -1

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


def tnames():
    try: 
         connection = mysql.connector.connect(host= "ec2-13-233-208-238.ap-south-1.compute.amazonaws.com",port=3306,database="SJCE",user= "ec2-user@13.233.208.238",password= "Hello123@")
  
         cursor = connection.cursor()
         sql_fetch_query ="""SELECT tname from teacher"""
         cursor.execute(sql_fetch_query)
         record = cursor.fetchall()
         l1=[]
         for rec in record:
             l1.append(rec[0])
           
         return l1

    except mysql.connector.Error as error:
         print("Failed to read data from MySQL table {}".format(error))
         return -1

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

def tname2id(name):
    try: 
         connection = mysql.connector.connect(host= "ec2-13-233-208-238.ap-south-1.compute.amazonaws.com",port=3306,database="SJCE",user= "ec2-user@13.233.208.238",password= "Hello123@")
  
         cursor = connection.cursor()
         sql_fetch_query ="""select tid from teacher where tname=%s"""
         name=(name,)
         cursor.execute(sql_fetch_query,name)
         record = cursor.fetchall()
        
         return record[0][0]

    except mysql.connector.Error as error:
         print("Failed to read data from MySQL table {}".format(error))
         return -1

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")



def update_preference(usn,plist):
    try: 
         connection = mysql.connector.connect(host= "ec2-13-233-208-238.ap-south-1.compute.amazonaws.com",port=3306,database="SJCE",user= "ec2-user@13.233.208.238",password= "Hello123@")
         try:
             plist.remove("--Select--")
             plist.remove("Unselect--To Change the selected option--")
         except:
             print("All preference not accepted")
         p=''
         for n in plist:
            p=p+str(tname2id(n))+","
         print(p[:-1])

         cursor = connection.cursor()
         sql_fetch_query ="""update student set preference=%s where usn=%s"""
         name=(p[:-1],usn)
         result=cursor.execute(sql_fetch_query,name)
         connection.commit()
         return result

    except mysql.connector.Error as error:
         print("Failed to read data from MySQL table {}".format(error))
         return -1
    
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
    



#print(tnames())
#print(read_preference())
#print(tname2id('AMC'))
#print(update_preference("01JST17CS096",['AMC','AKM']))
