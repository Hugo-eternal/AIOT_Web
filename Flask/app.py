# -*- coding: utf-8 -*-
from flask import Flask, render_template, jsonify
import pandas as pd
from six.moves import urllib
import json

app = Flask(__name__) #flash 框架

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/indexNoAI")
def indexNoAI():
    return render_template("indexNoAI.html")

@app.route("/indexAI")
def indexAI():
    return render_template("indexAI.html")
#增加資料庫調用並更新網頁的部分
@app.route("/getData")
def getData():
    
    myserver ="localhost"
    myuser="test123"
    mypassword="test123"
    mydb="aiotdb"
    
    debug =0
    from  pandas import DataFrame as df
    import pandas as pd                     # 引用套件並縮寫為 pd
    import numpy as np

    import pymysql.cursors
    #db = mysql.connector.connect(host="140.120.15.45",user="toto321", passwd="12345678", db="lightdb")
    #conn = mysql.connector.connect(host=myserver,user=myuser, passwd=mypassword, db=mydb)
    conn = pymysql.connect(host=myserver,user=myuser, passwd=mypassword, db=mydb)

    c = conn.cursor()
    if debug:
        input("pause.. conn.cursor() ok.......")

    #====== 執行 MySQL 查詢指令 ======#
    c.execute("SELECT * FROM sensors")

    #====== 取回所有查詢結果 ======#
    results = c.fetchall()
    print(type(results))
    print(results[:10])
    if debug:
        input("pause ....select ok..........")

    test_df = df(list(results),columns=['id','time','value','temp','humi','status'])

    print(test_df.head(10))
    result = test_df.to_dict(orient='records')
    seq = [[item['id'], item['time'], item['value'], item['temp'], item['humi'], item['status']] for item in result]
    return jsonify(seq)
    ######### cursor close, conn close
    c.close()
    conn.close()

@app.route("/setRandom")
def setRandom():
    myserver ="localhost"
    myuser="test123"
    mypassword="test123"
    mydb="aiotdb"
    
    debug =0
    from  pandas import DataFrame as df
    import pandas as pd                     # 引用套件並縮寫為 pd
    import numpy as np

    import pymysql.cursors
    #db = mysql.connector.connect(host="140.120.15.45",user="toto321", passwd="12345678", db="lightdb")
    #conn = mysql.connector.connect(host=myserver,user=myuser, passwd=mypassword, db=mydb)
    conn = pymysql.connect(host=myserver,user=myuser, passwd=mypassword, db=mydb)

    c = conn.cursor()
    if debug:
        input("pause.. conn.cursor() ok.......")
    
    #====== 執行 MySQL 查詢指令 ======#
    c.execute("update sensors set status=Rand() where TRUE")
    conn.commit()
    c.execute("SELECT * FROM sensors")

    #====== 取回所有查詢結果 ======#
    results = c.fetchall()
    print(type(results))
    print(results[:10])
    if debug:
        input("pause ....select ok..........")

    test_df = df(list(results),columns=['id','time','value','temp','humi','status'])

    print(test_df.head(10))
    result = test_df.to_dict(orient='records')
    seq = [[item['id'], item['time'], item['value'], item['temp'], item['humi'], item['status']] for item in result]
    #return jsonify(seq)
    return render_template("indexNoAI.html")
    ######### cursor close, conn close
    c.close()
    conn.close()

@app.route("/getPredict")
def getPredict():
    debug =0
    
    #needed packages
    from  pandas import DataFrame as df
    import pandas as pd                     # 引用套件並縮寫為 pd
    
    #Account & Passwords
    myserver ="localhost"
    myuser="test123"
    mypassword="test123"
    mydb="aiotdb"
     
    #Load Model
    import pickle
    import gzip
    
    with gzip.GzipFile('myModel.pgz', 'r') as f:
        model = pickle.load(f)
    #----------------------------------------------------#
    
    import pymysql.cursors
    conn = pymysql.connect(host=myserver,user=myuser, passwd=mypassword, db=mydb)
    
    c = conn.cursor()
    if debug:
        input("pause.. conn.cursor() ok.......")
    
    #====== 執行 MySQL 查詢指令 ======#
    c.execute("SELECT * FROM sensors")
    
    #====== 取回所有查詢結果 ======#
    results = c.fetchall()
    print(type(results))
    print(results[:10])
    if debug:
        input("pause ....select ok..........")
    
    test_df = df(list(results),columns=['id','time','value','temp','humi','status'])
    
    print(test_df.head(10))
    if debug:
        input("pause..  show original one above (NOT correct).......")
    
    testX=test_df['value'].values.reshape(-1,1)
    testY=model.predict(testX)
    print(model.score(testX,testY))
    
    test_df['status']=testY
    print(test_df.head(10))
    
    if debug:
        input("pause.. now show correct one above.......")
    
    #########################################
    c.execute('update sensors set status=0 where true')
    conn.commit()
    ## choose status ==1 have their id available
    id_list=list(test_df[test_df['status']==1].id)
    print(id_list)
                
    for _id in id_list:
        #print('update light set status=1 where id=='+str(_id))
        c.execute('update sensors set status=1 where id='+str(_id))
    
    conn.commit()
    result = test_df.to_dict(orient='records')
    seq = [[item['id'], item['time'], item['value'], item['temp'], item['humi'], item['status']] for item in result]
    return jsonify(seq)
    if debug:
        input("pause ....update ok..........")
        
    ######### cursor close, conn close
    c.close()
    conn.close()


if __name__ == "__main__" :
    app.run(debug=True,use_reloader=True,port=8080)




