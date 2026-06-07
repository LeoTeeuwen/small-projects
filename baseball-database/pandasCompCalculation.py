import pandas as pd
from sqlalchemy import create_engine


db_connection_str = 'mysql+pymysql://root:password@127.0.0.1/the_show'
db_connection = create_engine(db_connection_str)

dataframe = pd.read_sql('SELECT * FROM games', con=db_connection)

print(dataframe)