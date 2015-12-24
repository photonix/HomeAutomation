
import sys
import datetime
import pymysql
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('mysql+pymysql://user:user@RPI0/home', echo=False)

room_code = [1, 2, 3, 0]
room_name = ['1', '2', '3', '4']

for (code, name, i) in zip(room_code, room_name, range(len(room_code))):
    SQL_query = "SELECT * FROM temp_humid WHERE room={0} and (timestamp>date_sub(now(), interval 3 day));".format(code)
    df = pd.read_sql_query(SQL_query, engine)
    df.index = df['timestamp']
    df_resampled = df.resample('H', how='mean')
    df_resampled['room'] = code
    df_resampled['timestamp'] = df_resampled.index
    df_resampled = df_resampled[df_resampled['timestamp'] != datetime.datetime(datetime.datetime.now().year,
                                                                           datetime.datetime.now().month,
                                                                           datetime.datetime.now().day,
                                                                           datetime.datetime.now().hour)]

    SQL_query_hourly = "SELECT * FROM temp_humid_hourly WHERE room={0};".format(code)
    df_hourly = pd.read_sql_query(SQL_query_hourly, engine)

    new_list = list(set(df_resampled['timestamp'].astype(str)) - set(df_hourly['timestamp'].astype(str)))
    if len(new_list)>0:
        new_index = [pd.Timestamp(x) for x in new_list]
        df_resampled.loc[new_index].to_sql(name = 'temp_humid_hourly', con = engine, index=False,
                                           flavor='mysql', schema = 'home', if_exists='append')