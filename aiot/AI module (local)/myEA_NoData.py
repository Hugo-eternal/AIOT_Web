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

with gzip.GzipFile('./myModel.pgz', 'r') as f:
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
c.execute('update sensors set status=0 where value>0')
conn.commit()
## choose status ==1 have their id available
id_list=list(test_df[test_df['status']==1].id)
print(id_list)
            
for _id in id_list:
    #print('update light set status=1 where id=='+str(_id))
    c.execute('update sensors set status=1 where id='+str(_id))

conn.commit()

if debug:
    input("pause ....update ok..........")
    
######### cursor close, conn close
c.close()
conn.close()

