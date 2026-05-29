# Goal of this file is to call the API for The Show and push all of that onto SQL

import mysql.connector
import requests
import json

mlb = mlbstatsapi.Mlb()

mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  password="password"
)

print(mydb)

mydb.close()

response = requests.get("https://statsapi.mlb.com/api/v1/teams?&hydrate=nextSchedule(team,gameType=[S,R,F,D,L,W,C],inclusive=false,limit=1)")

data = response.json()  # Convert JSON response to a Python dictionary

with open('data.json', 'w') as f:
    json.dump(data, f, indent=4)