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

response = requests.get("https://statsapi.mlb.com/api/v1/standings?leagueId=103,104&season=2025&standingsTypes=regularSeason")

# To get all 2025 season games
# params = {
#         "sportId": 1,     # 1 is the ID for MLB
#         "season": 2025    # The season year
#     }
# response = requests.get("https://statsapi.mlb.com/api/v1/schedule", params)

data = response.json()  # Convert JSON response to a Python dictionary

with open("data2.json", "w") as file:
    json.dump(data, file, indent=4)
    sys.exit(0)


teamsDict = {}

for division in data['records']:
  for team in division['teamRecords']:
    print("Team: ", team, end="\n\n")
    teamsDict[team['team']['name']] = team["leagueRecord"]

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