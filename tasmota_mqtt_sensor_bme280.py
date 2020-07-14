#!/usr/bin/env python3
#./mqtt_sensor_bme280.py <mqtt broker address> <topic> <username> <password>

import paho.mqtt.subscribe as subscribe
import json
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime, timedelta
import sys

logfile="/var/www/htdocs/cacti/log/tasmota-mqtt-sensor-bme280.log"

logger = logging.getLogger("Rotating Log")
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler(filename=logfile, maxBytes=1048576, backupCount=1)
logger.addHandler(handler)
logger.info("Script started: " + str(datetime.now()) + " -- Arguments -- " + str(sys.argv[1:]))

try:
    mqtt_broker = str(sys.argv[1])
    mqtt_topic = str(sys.argv[2])
    mqtt_username = str(sys.argv[3])
    mqtt_password = str(sys.argv[4])
except Exception as e:
    logger.error("Script Failed: " + str(datetime.now()) + " -- Arguments Error -- " + str(e))
    sys.exit(1)

try:
    #msg = subscribe.simple("tele/AnemoiNode_D188C2/SENSOR", hostname="localhost", auth = {'username':"mrorion", 'password':"happyman1"})
    msg = subscribe.simple(mqtt_topic, hostname=mqtt_broker, auth = {'username':mqtt_username, 'password':mqtt_password})
    #print("%s %s" % (msg.topic, msg.payload))
except Exception as e:
    logger.error("Script Failed: " + str(datetime.now()) + " -- Subscribe Error -- " + str(e))
    sys.exit(1)

try:
    parsed_json = json.loads(msg.payload.decode("utf8"))
    bme_time = parsed_json['Time']
    bme_temperature = round(9.0/5.0 * parsed_json['BME280']['Temperature'] + 32,2)
    bme_humidity = parsed_json['BME280']['Humidity']
    bme_pressure = round(parsed_json['BME280']['Pressure'] * 0.02953,4)
    bme_dewpoint = 9.0/5.0 * parsed_json['BME280']['DewPoint'] + 32

    #bme_time = "2020-07-08T17:42:00"
    bme_age = datetime.utcnow() - datetime.strptime(bme_time, '%Y-%m-%dT%H:%M:%S')
    bme_age = (bme_age.days * 86400) + bme_age.seconds
    if bme_age > 31536000:
        #print("Time probably incorrect")
        bme_age = "U"

except Exception as e:
    logger.error("Script Failed: " + str(datetime.now()) + " -- Processing Error -- " + str(e))
    sys.exit(1)

#print(type(bme_time))
#print('Time difference:', str(datetime.now() - str(bme_time)))
#print(bme_time)
#print(bme_temperature)
#print(bme_humidity)
#print(bme_pressure)
#print(bme_dewpoint)

try:
    returndata = "bme_temperature:" + str(bme_temperature)\
		+ " bme_humidity:" + str(bme_humidity)\
		+ " bme_pressure:" + str(bme_pressure)\
		+ " bme_dewpoint:" + str(bme_dewpoint)\
        	+ " bme_age:" + str(bme_age)

    print(returndata)
except Exception as e:
    logger.error("Script Failed: " + str(datetime.now()) + " -- Data Output Error -- " + str(e))
    sys.exit(1)

logger.info("Script ended: " + str(datetime.now()) + " -- Output -- " + returndata)
