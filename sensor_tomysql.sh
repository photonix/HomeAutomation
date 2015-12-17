cd /home/pi/sensor

while true
do 
    python sensor_tomysql.py
    sleep 10
done

