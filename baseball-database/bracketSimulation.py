import pandas as pd
from sqlalchemy import create_engine
import random
from itertools import batched
from pandasCompCalculation import simulateWinner


db_connection_str = 'mysql+pymysql://root:password@127.0.0.1/the_show'
db_connection = create_engine(db_connection_str)

df = pd.read_sql('SELECT DISTINCT away FROM games', con=db_connection)

print(df, end="\n\n")

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


def simulateBracketRound(teams: str):
    # Prepare for odd case
    free_win_team = None
    if len(teams) % 2 == 1:
        free_win_team = teams.pop(-1)


    bracket_winners = []
    # First Bracket Simulation
    for team1, team2 in batched(teams, 2):
        bracket_winners.append(simulateWinner(team1, team2, db_connection))
    
    # Append free winning team if it exists
    if free_win_team is not None:
        bracket_winners.append(free_win_team)
    
    return bracket_winners

print("Teams in first bracket")
print(len(mlb_teams))

first_bracket_winners = simulateBracketRound(mlb_teams)

print(len(first_bracket_winners))

second_bracket_winners = simulateBracketRound(first_bracket_winners)
print(len(second_bracket_winners))

third_bracket_winners = simulateBracketRound(second_bracket_winners)
print(len(third_bracket_winners))

semi_finals_winner = simulateBracketRound(third_bracket_winners)
print(len(semi_finals_winner))

finals_winner = simulateBracketRound(semi_finals_winner)
print(len(finals_winner))

print(f"Winner!: {finals_winner[0]}")