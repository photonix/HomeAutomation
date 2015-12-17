import sht21

with sht21.SHT21(1) as sht21:
    print "Temperature: %5.2f" % sht21.read_temperature()    
    print "Humidity: %5.2f" % sht21.read_humidity()
