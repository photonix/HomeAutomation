import sys
import datetime
import pymysql
from plotly import tools
import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd
import lttb

hours = int(sys.argv[1])

username = 'photonix'
api_key = 'q99v5kud1t'
py.sign_in(username, api_key)


# Connect to the database
connection = pymysql.connect(host='RPI0', user='user', password='user', db='home',
                             charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

room_code = [1, 2, 3, 0]
room_name = ['1', '2', '3', '4']
temp = [None] * len(room_code)
humid = [None] * len(room_code)
seq = range(len(room_code))
down_sampling_ratio = 20

fig = tools.make_subplots(rows=2, cols=1, shared_xaxes=True)

for (code, name, i) in zip(room_code, room_name, range(len(room_code))):
    SQL_query = "SELECT * FROM temp_humid WHERE room={0} and (timestamp > DATE_SUB(NOW(), INTERVAL {1} HOUR));".format(code, hours)
    df = pd.read_sql_query(SQL_query, connection)
    df.index = df['timestamp']
    if len(df.index)//down_sampling_ratio >= 2:
        df_lttb_temp = lttb.largest_triangle_three_buckets(df['temp'], len(df.index)//down_sampling_ratio)
        df_lttb_humid = lttb.largest_triangle_three_buckets(df['humid'], len(df.index)//down_sampling_ratio)
    else:
        df_lttb_temp = df['temp']
        df_lttb_humid = df['humid']
    temp[i] = go.Scatter(x=df_lttb_temp.index, y=df_lttb_temp, name='T_Room #'+name)
    fig.append_trace(temp[i], 1, 1)
    humid[i] = go.Scatter(x=df_lttb_humid.index, y=df_lttb_humid, name='H_Room #'+name, yaxis='y2' )
    fig.append_trace(humid[i], 2, 1)

fig['layout'].update(title='Home Temperature/Humidity')

fig['layout']['yaxis1'].update(title='Temperature', range=[21, 25])
fig['layout']['yaxis2'].update(title='Humidity')

plot_url = py.plot(fig, filename='Home Monitoring', auto_open=False)

