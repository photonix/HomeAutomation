import sht21
import datetime
import pymysql.cursors
import socket

# Connect to the database
connection = pymysql.connect(host='RPI0',
                             user='user',
                             password='user',
                             db='home',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

try:
    with connection.cursor() as cursor:
        # Create a new record
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        room = socket.gethostname()[3]
        sql = "INSERT INTO temp_humid (timestamp, room, temp, humid) VALUES ('%s', %s, %s, %s)" % (
                                       timestamp, room, sht21.SHT21(1).read_temperature(), sht21.SHT21(1).read_humidity())
        cursor.execute(sql)

    # connection is not autocommit by default. So you must commit to save
    # your changes.
    connection.commit()

finally:
    connection.close()
    
