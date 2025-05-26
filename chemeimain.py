import sqlite3
import sqlite3 as sql
from datetime import datetime
import datetime

import numpy as np
#import pandas as pd
from flask import request,render_template,Flask, jsonify


#接收帳號密碼
app = Flask(__name__)

#擷取今天時間
date_today=str(datetime.date.today())
date_time=datetime.datetime.now()
date_time_out=date_time.strftime("%H:%M")  

@app.route('/',methods = ['GET','POST'])
def chimeimain():           
       
    return render_template("chimeimain.html",date_today=date_today,date_time=date_time_out)

@app.route('/carline',methods = ['GET','POST'])
def carline():           
       
    return render_template("carline.html",date_today=date_today,date_time=date_time_out)



@app.route('/eventinfo', methods=['POST', 'GET'])
def home():
    con = sql.connect("chimei.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from eventinfo")
    rows = cur.fetchall()
    aa=5
    return render_template("chimeihome.html", rows=rows,aa=aa  )


# 進行RFID API串接並存入eventinfo資料表中
@app.route('/chimeiaddrec', methods=['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        try:
            inserValue = request.get_json()
            # 每次感測資料進入資訊
            tagid = inserValue['tagid']            
                     
            readerid = inserValue['readerid']            
            eventtime_in = inserValue['eventtime_in']            
            eventtime_out= inserValue['eventtime_out']          
            date_time1=datetime.datetime.now()
            store_now=date_time1.strftime("%Y-%m-%d %H:%M")
            input = np.array([tagid, readerid, eventtime_in, eventtime_out,store_now])


            with sql.connect("chimei.db") as con:                 
                con.row_factory = sql.Row
                cur = con.cursor()
                cur.execute(
                    "INSERT INTO eventinfo (tagid,readerid,eventtime_in,eventtime_out,datalogintime)  VALUES(?,?,?,?,?)",
                    (tagid,  readerid, eventtime_in, eventtime_out, store_now))
                con.commit()
                msg_S = "Record successfully added"

        except:
            con.rollback()
            msg_S = "error in insert operation"


        finally:
            
            return jsonify(msg=msg_S)
           



if __name__=='__main__':
    app.run ( host='0.0.0.0' ,port=13066,debug=True)
