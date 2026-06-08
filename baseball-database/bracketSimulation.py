import pandas as pd
from sqlalchemy import create_engine
import random
from itertools import pairwise
from pandasCompCalculation import simulateWinner


db_connection_str = 'mysql+pymysql://root:password@127.0.0.1/the_show'
db_connection = create_engine(db_connection_str)

df = pd.read_sql('SELECT DISTINCT away FROM games', con=db_connection)

print(df)

mlb_teams = [
    "Arizona Diamondbacks",
    "Atlanta Braves",
    "Baltimore Orioles",
    "Boston Red Sox",
    "Chicago White Sox",
    "Chicago Cubs",
    "Cincinnati Reds",
    "Cleveland Guardians",
    "Colorado Rockies",
    "Detroit Tigers",
    "Houston Astros",
    "Kansas City Royals",
    "Los Angeles Angels",
    "Los Angeles Dodgers",
    "Miami Marlins",
    "Milwaukee Brewers",
    "Minnesota Twins",
    "New York Yankees",
    "New York Mets",
    "Athletics",
    "Philadelphia Phillies",
    "Pittsburgh Pirates",
    "San Diego Padres",
    "San Francisco Giants",
    "Seattle Mariners",
    "St. Louis Cardinals",
    "Tampa Bay Rays",
    "Texas Rangers",
    "Toronto Blue Jays",
    "Washington Nationals"
]

random.shuffle(mlb_teams)

print(mlb_teams)

for team1, team2 in pairwise(mlb_teams):
    print(f"{team1} vs {team2}")