import plotly.plotly as py
from plotly import tools
from plotly.graph_objs import Scatter, Layout, Figure
import datetime
import time
import sht21
import pymysql
import pandas as pd


logfile = 'sensor_log.csv'
username = 'photonix'
api_key = 'q99v5kud1t'
stream_token = ['q4hqy34mxa', 'rzesexo19p', 'k0rutkz2uc', 'r8zqb5vnk7',
                'llv5uzy2g0', 'g9qwg4v88b', '31st3ta95q', 'cfuz1acgur']

py.sign_in(username, api_key)

# Connect to the database
connection = pymysql.connect(host='RPI0', user='user', password='user', db='home',
                             charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

n = 4
room_code = [1, 2, 3, 0]
room_name = ['1', '2', '3', '4']
temp = [None] * len(room_code)
humid = [None] * len(room_code)

fig = tools.make_subplots(rows=2, cols=1, shared_xaxes=True)

for i in xrange(n):
    temp[i] = Scatter(x=[], y=[], name='T_Room #' + room_name[i],
                stream = dict(token=stream_token[i], maxpoints=240) )
    fig.append_trace(temp[i], 1, 1)
    humid[i] = Scatter(x=[], y=[], name='H_Room #' + room_name[i], yaxis='y2',
                stream=dict(token=stream_token[n+i], maxpoints=240) )
    fig.append_trace(humid[i], 2, 1)

fig['layout'].update(title='Home Temperature/Humidity - Live Stream')
fig['layout']['yaxis1'].update(title='Temperature', range = [21, 26])
fig['layout']['yaxis2'].update(title='Humidity')

plot_url = py.plot(fig, filename='Home Monitoring Live Stream', auto_open=False)

temp_stream = [None] * n
humid_stream = [None] * n

for i in xrange(n):
    temp_stream[i] = py.Stream(stream_token[i])
    temp_stream[i].open()
    humid_stream[i] = py.Stream(stream_token[n+i])
    humid_stream[i].open()


interval_minute = 3
#the main sensor reading loop
while True:
    try:
        t = datetime.datetime.now() #.strftime("%H:%M %Y.%m.%d")

        for i in xrange(n):
            SQL_query = "SELECT * FROM temp_humid WHERE room={0} and (timestamp > DATE_SUB(NOW(), INTERVAL {1} MINUTE));".format(room_code[i], interval_minute)
            df = pd.read_sql_query(SQL_query, connection)
            df.index = df['timestamp']
    
            temp_stream[i].write({'x': t, 'y': df['temp'].mean()})
            humid_stream[i].write({'x': t, 'y': df['humid'].mean()})
        
    except:
        print 'Error...\n'
    finally:
        # delay between stream posts
        time.sleep(60*interval_minute)
