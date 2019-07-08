from tinydb import TinyDB, Query
import mysql.connector
import json

db_host = 'localhost'
db_user = 'user'
db_pass = 'password'
db_name = 'slurmrestapi'

mysqldb = mysql.connector.connect(host=db_host, user=db_user, passwd=db_pass, database=db_name)

db_path = 'db.json'
db = TinyDB(db_path)

all_data = db.all()

for entry in all_data:
    time = entry['time']
    mydata = json.dumps(entry)
    print(time)
    
    sqlc= 'INSERT INTO loadtable (time_id, data_dump) VALUES (%s, %s)'
    valc= (time, mydata)    
    my_cur = mysqldb.cursor()
    my_cur.execute(sqlc, valc)
    mysqldb.commit()

