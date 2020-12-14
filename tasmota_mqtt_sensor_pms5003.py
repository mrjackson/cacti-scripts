#!/usr/bin/env python3
#./tasmota_mqtt_sensor_pms5003.py <mqtt broker address> <topic> <username> <password>

import paho.mqtt.subscribe as subscribe
import json
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime, timedelta
import sys

logfile="/var/www/htdocs/cacti/log/tasmota-mqtt-sensor-pms5003.log"

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
    pms_time = parsed_json['Time']
    #bme_temperature = round(9.0/5.0 * parsed_json['BME280']['Temperature'] + 32,2)
    #bme_humidity = round(parsed_json['BME280']['Humidity'],2)
    #bme_pressure = round(parsed_json['BME280']['Pressure'] * 0.02953,4)
    #bme_dewpoint = round(9.0/5.0 * parsed_json['BME280']['DewPoint'] + 32,2)

    pms_cf1 = parsed_json['PMS5003']['CF1']
    pms_cf2_5 = parsed_json['PMS5003']['CF2.5']
    pms_cf10 = parsed_json['PMS5003']['CF10']

    pms_pm1 = parsed_json['PMS5003']['PM1']
    pms_pm2_5 = parsed_json['PMS5003']['PM2.5']
    pms_pm10 = parsed_json['PMS5003']['PM10']

    pms_pb0_3 = parsed_json['PMS5003']['PB0.3']
    pms_pb0_5 = parsed_json['PMS5003']['PB0.5']
    pms_pb1 = parsed_json['PMS5003']['PB1']
    pms_pb2_5 = parsed_json['PMS5003']['PB2.5']
    pms_pb5 = parsed_json['PMS5003']['PB5']
    pms_pb10 = parsed_json['PMS5003']['PB10']




    #pms_time = "2020-07-08T17:42:00"
    pms_age = datetime.utcnow() - datetime.strptime(pms_time, '%Y-%m-%dT%H:%M:%S')
    pms_age = (pms_age.days * 86400) + pms_age.seconds
    if pms_age > 31536000:
        #print("Time probably incorrect")
        pms_age = "U"

except Exception as e:
    logger.error("Script Failed: " + str(datetime.now()) + " -- Processing Error -- " + str(e))
    sys.exit(1)


try:
    returndata = "pms_cf1:" + str(pms_cf1)\
		+ " pms_cf2_5:" + str(pms_cf2_5)\
		+ " pms_cf10:" + str(pms_cf10)\
                + " pms_pm1:" + str(pms_pm1)\
                + " pms_pm2_5:" + str(pms_pm2_5)\
                + " pms_pm10:" + str(pms_pm10)\
                + " pms_pb0_3:" + str(pms_pb0_3)\
                + " pms_pb0_5:" + str(pms_pb0_5)\
                + " pms_pb1:" + str(pms_pb1)\
                + " pms_pb2_5:" + str(pms_pb2_5)\
                + " pms_pb5:" + str(pms_pb5)\
                + " pms_pb10:" + str(pms_pb10)\
        	+ " pms_age:" + str(pms_age)

    print(returndata)
except Exception as e:
    logger.error("Script Failed: " + str(datetime.now()) + " -- Data Output Error -- " + str(e))
    sys.exit(1)

logger.info("Script ended: " + str(datetime.now()) + " -- Output -- " + returndata)
