
# Usage: python summary_daily.py <days>

import sys
import datetime
import pymysql
import pandas as pd
from sqlalchemy import create_engine

if len(sys.argv) > 0:
    days = int(sys.argv[1])
else:
    days = 3 #default value 3 days
    
engine = create_engine('mysql+pymysql://user:user@RPI0/home', echo=False)


room_code = [1, 2, 3, 0]
room_name = ['1', '2', '3', '4']

for (code, name, i) in zip(room_code, room_name, range(len(room_code))):
    SQL_query = "SELECT * FROM temp_humid WHERE room={0} and (timestamp>=subdate(current_date, {1}) and timestamp<current_date);".format(code, days)
    df = pd.read_sql_query(SQL_query, engine)
    df.index = df['timestamp']
    df_resampled = df.resample('D', how='mean')
    df_resampled['room'] = code
    df_resampled['timestamp'] = df_resampled.index.date
    df_resampled = df_resampled[df_resampled['timestamp'] != datetime.date(datetime.datetime.now().year,
                                                                           datetime.datetime.now().month,
                                                                           datetime.datetime.now().day)]

    SQL_query_daily = "SELECT * FROM temp_humid_daily WHERE room={0} and (timestamp>=subdate(current_date, {1}) and timestamp<current_date);".format(code, days)
    df_daily = pd.read_sql_query(SQL_query_daily, engine)
    
    new_list = list(set(df_resampled['timestamp'].astype(str)) - set(df_daily['timestamp'].astype(str)))
    if len(new_list)>0:
        new_index = [pd.Timestamp(x) for x in new_list]
        df_resampled.loc[new_index].to_sql(name = 'temp_humid_daily', con = engine, index=False,
                                           flavor='mysql', schema = 'home', if_exists='append')
    

