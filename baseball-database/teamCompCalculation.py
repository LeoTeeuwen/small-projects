# Goal of this file is to call the API for The Show and push all of that onto SQL

import mysql.connector
import requests
import json
import sys

mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  password="password",
  database="the_show"
)

# To get all 2025 season games
params = {
        "sportId": 1,     # 1 is the ID for MLB
        "season": 2025    # The season year
    }
response = requests.get("https://statsapi.mlb.com/api/v1/schedule", params)

data = response.json()  # Convert JSON response to a Python dictionary

with open("data2.json", "w") as file:
    json.dump(data, file, indent=4)


# Each team and then their win/loss ratio against another team
# team: team: {wins: number, losses: number}
#       team
matchUpsDict = {}
noWinnerCount = 0
gamesTotal = 0

for date in data['dates']:
    for game in date['games']:
        gamesTotal += 1
        if game['teams']['away']['team']['name'] not in matchUpsDict:
            matchUpsDict[game['teams']['away']['team']['name']] = {}
        if game['teams']['home']['team']['name'] not in  matchUpsDict:
            matchUpsDict[game['teams']['home']['team']['name']] = {}

        if 'isWinner' not in game['teams']['away']:
            print("no winner somehow??")
            noWinnerCount += 1
            continue

        if game['teams']['away']['isWinner'] == True:
            if game['teams']['home']['team']['name'] not in matchUpsDict[game['teams']['away']['team']['name']]:
                matchUpsDict[game['teams']['away']['team']['name']][game['teams']['home']['team']['name']] = {"wins": 1, "losses": 0}
            else:
                matchUpsDict[game['teams']['away']['team']['name']][game['teams']['home']['team']['name']]['wins'] += 1

            if game['teams']['away']['team']['name'] not in matchUpsDict[game['teams']['home']['team']['name']]:
                matchUpsDict[game['teams']['home']['team']['name']][game['teams']['away']['team']['name']] = {"wins": 0, "losses": 1}
            else:
                matchUpsDict[game['teams']['home']['team']['name']][game['teams']['away']['team']['name']]['losses'] += 1
        else:
            if game['teams']['home']['team']['name'] not in matchUpsDict[game['teams']['away']['team']['name']]:
                matchUpsDict[game['teams']['away']['team']['name']][game['teams']['home']['team']['name']] = {"wins": 0, "losses": 1}
            else:
                matchUpsDict[game['teams']['away']['team']['name']][game['teams']['home']['team']['name']]['losses'] += 1

            if game['teams']['away']['team']['name'] not in matchUpsDict[game['teams']['home']['team']['name']]:
                matchUpsDict[game['teams']['home']['team']['name']][game['teams']['away']['team']['name']] = {"wins": 1, "losses": 0}
            else:
                matchUpsDict[game['teams']['home']['team']['name']][game['teams']['away']['team']['name']]['wins'] += 1

print(matchUpsDict)
print(noWinnerCount)
print(gamesTotal)

with open("final.json", "w") as file:
    json.dump(matchUpsDict, file, indent=4)

sys.exit(0)

# for division in data['records']:
#   for team in division['teamRecords']:
#     print("Team: ", team, end="\n\n")
#     teamsDict[team['team']['name']] = team["leagueRecord"]

# myCursor = mydb.cursor()

# myCursor.execute("SHOW TABLES")


# # There is likely a more elegant way of doing this, but I do not want to wrap everything in a for loop so this is to escape that
# tableExists = False
# for x in myCursor:
#   if x[0] == 'teams':
#     tableExists = True

# if not tableExists:
#   myCursor.execute("CREATE TABLE teams (name VARCHAR(255) PRIMARY KEY, wins INT, losses INT, pct FLOAT)")

# myCursor.execute("TRUNCATE TABLE teams")

# for team in teamsDict:
#   myCursor.execute(f"INSERT INTO teams (name, wins, losses, pct) VALUES (%s, %s, %s, %s)", (team, teamsDict[team]['wins'], teamsDict[team]['losses'], teamsDict[team]['pct']))

# # Remember, you need to commit!!
# mydb.commit()

mydb.close()