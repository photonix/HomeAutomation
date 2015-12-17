#!/bin/bash
# Usage : sensor_tomysql.sh interval
# interval is sampling period in seconds

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd $DIR

while true
do 
    python sensor_tomysql.py
    sleep $1
done

