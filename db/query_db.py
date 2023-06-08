import mysql.connector
import pandas as pd

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password"
)

cur = mydb.cursor()
cur.execute("USE DB")

sql_stmt = f"SELECT * FROM Journals"
cur.execute(sql_stmt)
response = cur.fetchall()
for row in response[0:5]:
    print(row)
cur.close()
mydb.close()
       