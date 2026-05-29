# Goal of this file is to call the API for The Show and push all of that onto SQL

import mysql.connector

mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  password="password"
)

print(mydb)

mydb.close()
