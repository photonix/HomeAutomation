import sys
import datetime
import pymysql
from plotly import tools
import plotly.plotly as py
import plotly.graph_objs as go
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
temp = [None] * len(room_code)
humid = [None] * len(room_code)
seq = range(len(room_code))

fig = tools.make_subplots(rows=2, cols=1, shared_xaxes=True)

for (code, name, i) in zip(room_code, room_name, range(len(room_code))):
    SQL_query = "SELECT * FROM temp_humid WHERE room={0} and (timestamp > DATE_SUB(NOW(), INTERVAL {1} HOUR));".format(code, hours)
    df = pd.read_sql_query(SQL_query, connection)
    df.index = df['timestamp']
    temp[i] = go.Scatter(x=df['timestamp'], y=df['temp'], name='T_Room #'+name)
    fig.append_trace(temp[i], 1, 1)
    humid[i] = go.Scatter(x=df['timestamp'], y=df['humid'], name='H_Room #'+name, yaxis='y2' )
    fig.append_trace(humid[i], 2, 1)

fig['layout'].update(title='Home Temperature/Humidity')

fig['layout']['yaxis1'].update(title='Temperature')
fig['layout']['yaxis2'].update(title='Humidity')

plot_url = py.plot(fig, filename='Home Monitoring', auto_open=False)

