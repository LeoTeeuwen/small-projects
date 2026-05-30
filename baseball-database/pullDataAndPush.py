# Goal of this file is to call the API for The Show and push all of that onto SQL

import mysql.connector
import requests

mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  password="password",
  database="the_show"
)

response = requests.get("https://statsapi.mlb.com/api/v1/teams?&hydrate=nextSchedule(team,gameType=[S,R,F,D,L,W,C],inclusive=false,limit=1)")

data = response.json()  # Convert JSON response to a Python dictionary

teamsData = []
teamsDict = {}


for team in data['teams']:
  if("name" in team['league']  and (team['league']['name'] == "National League" or team['league']['name'] == "American League")):

    teamsDict[team["nextGameSchedule"]["dates"][0]['games'][0]['teams']['away']['team']['name']] = team["nextGameSchedule"]["dates"][0]['games'][0]['teams']['away']['leagueRecord']
    teamsDict[team["nextGameSchedule"]["dates"][0]['games'][0]['teams']['home']['team']['name']] = team["nextGameSchedule"]["dates"][0]['games'][0]['teams']['home']['leagueRecord']

# print(teamsDict)

myCursor = mydb.cursor()

myCursor.execute("SHOW TABLES")


# There is likely a more elegant way of doing this, but I do not want to wrap everything in a for loop so this is to escape that
tableExists = False
for x in myCursor:
  if x[0] == 'teams':
    tableExists = True

if not tableExists:
  myCursor.execute("CREATE TABLE teams (name VARCHAR(255) PRIMARY KEY, wins INT, losses INT, pct FLOAT)")

myCursor.execute("TRUNCATE TABLE teams")

for team in teamsDict:
  myCursor.execute(f"INSERT INTO teams (name, wins, losses, pct) VALUES (%s, %s, %s, %s)", (team, teamsDict[team]['wins'], teamsDict[team]['losses'], teamsDict[team]['pct']))

# Remember, you need to commit!!
mydb.commit()

mydb.close()