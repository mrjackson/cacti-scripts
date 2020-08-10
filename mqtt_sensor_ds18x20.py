#!/usr/bin/env python3
#./mqtt_sensor_ds18x20.py <mqtt broker address> <topic> <username> <password>

import paho.mqtt.subscribe as subscribe
import json
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime, timedelta
import sys

logfile="/var/www/htdocs/cacti/log/cacti-mqtt-sensor-ds18x20.log"

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
    ds_time = parsed_json['Time']

    #ds_time = "2020-07-08T17:42:00"
    ds_age = datetime.utcnow() - datetime.strptime(ds_time, '%Y-%m-%dT%H:%M:%S')
    ds_age = (ds_age.days * 86400) + ds_age.seconds
    if ds_age > 31536000:
        #print("Time probably incorrect")
        bme_age = "U"

    #ds18x20
    #ds_one = round(9.0/5.0 * parsed_json['DS18B20-1']['Temperature'] + 32,2)
    #ds_two = round(9.0/5.0 * parsed_json['DS18B20-2']['Temperature'] + 32,2)
    #ds_three = round(9.0/5.0 * parsed_json['DS18B20-3']['Temperature'] + 32,2)
    try:
        ds_one = round(9.0/5.0 * parsed_json['DS18B20-1']['Temperature'] + 32,2)
    except:
        try:
            ds_one = round(9.0/5.0 * parsed_json['DS18B20']['Temperature'] + 32,2)
        except:
            ds_one = "U"
    try:
        ds_two = round(9.0/5.0 * parsed_json['DS18B20-2']['Temperature'] + 32,2)
    except:
        ds_two = "U"
    try:
        ds_three = round(9.0/5.0 * parsed_json['DS18B20-3']['Temperature'] + 32,2)
    except:
        ds_three = "U"
    try:
        ds_four = round(9.0/5.0 * parsed_json['DS18B20-4']['Temperature'] + 32,2)
    except:
        ds_four = "U"
    try:
        ds_five = round(9.0/5.0 * parsed_json['DS18B20-5']['Temperature'] + 32,2)
    except:
        ds_five = "U"

    ds_five = "U"


except Exception as e:
    logger.error("Script Failed: " + str(datetime.now()) + " -- Processing Error -- " + str(e))
    sys.exit(1)

try:
    returndata = "ds_one:" + str(ds_one)\
		+ " ds_two:" + str(ds_two)\
                + " ds_three:" + str(ds_three)\
                + " ds_four:" + str(ds_four)\
                + " ds_five:" + str(ds_five)\
        	+ " ds_age:" + str(ds_age)

    print(returndata)
except Exception as e:
    logger.error("Script Failed: " + str(datetime.now()) + " -- Data Output Error -- " + str(e))
    sys.exit(1)

logger.info("Script ended: " + str(datetime.now()) + " -- Output -- " + returndata)
