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

# with open("data2.json", "w") as file:
#     json.dump(data, file, indent=4)


myCursor = mydb.cursor()

myCursor.execute("SHOW TABLES")

# There is likely a more elegant way of doing this, but I do not want to wrap everything in a for loop so this is to escape that
tableExists = False

for x in myCursor:
  if x[0] == 'games':
    tableExists = True

if not tableExists:
  myCursor.execute("CREATE TABLE games (id VARCHAR(255) PRIMARY KEY, away VARCHAR(255), home VARCHAR(255), awayScore INT, homeScore INT, winner VARCHAR(255), season VARCHAR(255), gameType VARCHAR(255))")

for date in data['dates']:
    for game in date['games']:
        print(game['gameGuid'], game['teams']['away']['team']['name'], game['teams']['home']['team']['name'], game['teams']['away']['score'], game['teams']['home']['score'], game['teams']['away']['team']['name'], game['season'], game['seriesDescription'], end="\n\n")

        if game['teams']['away']['isWinner'] == True:
            myCursor.execute(f"INSERT INTO games (id, away, home, awayScore, homeScore, winner, season, gameType) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", 
                            (game['gameGuid'], game['teams']['away']['team']['name'], game['teams']['home']['team']['name'], game['teams']['away']['score'], game['teams']['home']['score'], game['teams']['away']['team']['name'], game['season'], game['seriesDescription']))
        elif game['teams']['home']['isWinner'] == True:
            myCursor.execute(f"INSERT INTO games (id, away, home, awayScore, homeScore, winner, season, gameType) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", 
                            (game['gameGuid'], game['teams']['away']['team']['name'], game['teams']['home']['team']['name'], game['teams']['away']['score'], game['teams']['home']['score'], game['teams']['home']['team']['name'], game['season'], game['seriesDescription']))
        else:
            myCursor.execute(f"INSERT INTO games (id, away, home, awayScore, homeScore, winner, season, gameType) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", 
                            (game['gameGuid'], game['teams']['away']['team']['name'], game['teams']['home']['team']['name'], game['teams']['away']['score'], game['teams']['home']['score'], "tie", game['season'], game['seriesDescription']))
        
# Remember, you need to commit!!
mydb.commit()

mydb.close()