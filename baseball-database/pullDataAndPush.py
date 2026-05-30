# Goal of this file is to call the API for The Show and push all of that onto SQL

import mysql.connector
import requests
import json

mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  password="password"
)

print(mydb)

mydb.close()

response = requests.get("https://statsapi.mlb.com/api/v1/teams?&hydrate=nextSchedule(team,gameType=[S,R,F,D,L,W,C],inclusive=false,limit=1)")

data = response.json()  # Convert JSON response to a Python dictionary

# with open('data.json', 'w') as f:
#     json.dump(data, f, indent=4)

teamsData = []
teamsDict = {}

# print(data['teams'])
# print(len(data['teams']))

for team in data['teams']:
  if("name" in team['league']  and (team['league']['name'] == "National League" or team['league']['name'] == "American League")):
    # print(team['name'])
    # print(team, end="\n\n")
    print(team["nextGameSchedule"]["dates"][0]['games'][0]['teams']['away']['leagueRecord'], end="\n")
    print(team["nextGameSchedule"]["dates"][0]['games'][0]['teams']['away']['team']['name'], end="\n")
    print(team["nextGameSchedule"]["dates"][0]['games'][0]['teams']['home']['leagueRecord'], end="\n")
    print(team["nextGameSchedule"]["dates"][0]['games'][0]['teams']['home']['team']['name'], end="\n\n")

    teamsDict[team["nextGameSchedule"]["dates"][0]['games'][0]['teams']['away']['team']['name']] = team["nextGameSchedule"]["dates"][0]['games'][0]['teams']['away']['leagueRecord']
    teamsDict[team["nextGameSchedule"]["dates"][0]['games'][0]['teams']['home']['team']['name']] = team["nextGameSchedule"]["dates"][0]['games'][0]['teams']['home']['leagueRecord']

print(teamsDict)
