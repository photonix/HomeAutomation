import sys
import datetime
import pymysql
import plotly.plotly as py
import plotly.graph_objas as go
import pandas as pd

hours = int(sys.argv[1])

username = 'photonix'
api_key = 'q99v5kud1t'
py.sign_in(username, api_key)


# Connect to the database
connection = pymysql.connect(host='RPI0',
                             user='user',
                             password='user',
                             db='home',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

room_code = [1, 2, 3, 0]
room_name = ['1', '2', '3', '4']
trace = [None] * len(room_code)

for (code, name, i) in zip(room_code, room_name, range(len(room_code))):
    SQL_query = "SELECT * FROM home WHERE room={0} and (timestamp > DATE_SUB(NOW(), INTERVAL {1} HOUR));".format(code, hours)
    df = pd.read_sql_query(SQL_query, connection)
    df.index = df['timestamp']
    trace[i] = go.Scatter( x=df['timestamp'], y=df['temp'] )

data = [trace]

# IPython notebook
# py.iplot(data, filename='pandas-time-series')

url = py.plot(data, filename='Home Monitoring')