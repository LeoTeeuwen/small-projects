import pandas as pd
from sqlalchemy import create_engine


db_connection_str = 'mysql+pymysql://root:password@127.0.0.1/the_show'
db_connection = create_engine(db_connection_str)

df = pd.read_sql('SELECT * FROM games', con=db_connection)

print(df)


# Figure out who is winning the Padres vs Dodgers matchup test
result = df[df['away'].str.contains('Los Angeles Dodgers|San Diego Padres')][df['home'].str.contains('Los Angeles Dodgers|San Diego Padres')]

print(result)

dodgers_wins = df[df['away'].str.contains('Los Angeles Dodgers|San Diego Padres')][df['home'].str.contains('Los Angeles Dodgers|San Diego Padres')][df['winner'] == "Los Angeles Dodgers"]
padres_wins = df[df['away'].str.contains('Los Angeles Dodgers|San Diego Padres')][df['home'].str.contains('Los Angeles Dodgers|San Diego Padres')][df['winner'] == "San Diego Padres"]

print(len(result.index))
print(dodgers_wins)
print(padres_wins)

if (len(dodgers_wins.index) > len(padres_wins.index)):
    print("Dodgers Beat Padres!")
else:
    print("Padres Beat Dodgers!")