import pandas as pd
from sqlalchemy import create_engine

# This returns the string of team name of who won the matchup
def simulateWinner(team1: str, team2: str, db_connection: any):
    df = pd.read_sql('SELECT * FROM games', con=db_connection)

    # Split up like this to not do querying and to avoid boolean series warning
    team1_wins = df[df['away'].str.contains(f'{team1}|{team2}')]
    team1_wins = team1_wins[team1_wins['home'].str.contains(f'{team1}|{team2}')]
    team1_wins = team1_wins[team1_wins['winner'] == f"{team1}"]

    team2_wins = df[df['away'].str.contains(f'{team1}|{team2}')]
    team2_wins = team2_wins[team2_wins['home'].str.contains(f'{team1}|{team2}')]
    team2_wins = team2_wins[team2_wins['winner'] == f"{team2}"]

    if (len(team1_wins.index) > len(team2_wins.index)):
        return team1
    
    return team2


if __name__ == '__main__':
    db_connection_str = 'mysql+pymysql://root:password@127.0.0.1/the_show'
    db_connection = create_engine(db_connection_str)

    print(simulateWinner("Los Angeles Dodgers", "San Diego Padres", db_connection))