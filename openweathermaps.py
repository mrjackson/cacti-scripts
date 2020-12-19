#!/usr/bin/env python3
#./openweathermaps.py <api_key> <api_loc>

import urllib.request, urllib.parse, urllib.error
import json
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime, timedelta
import sys

logfile="/var/www/htdocs/cacti/log/cacti-openweathermaps.log"

logger = logging.getLogger("Rotating Log")
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler(filename=logfile, maxBytes=1048576, backupCount=1)
logger.addHandler(handler)
logger.info("Script started: " + str(datetime.now()) + " -- Arguments -- " + str(sys.argv[1:]))

try:
    api_key = str(sys.argv[1])
    api_loc = str(sys.argv[2])
    api_url = "https://api.openweathermap.org/data/2.5/weather?APPID=" + api_key + "&id=" + api_loc
except Exception as e:
    logger.error("Script Failed: " + str(datetime.now()) + " -- Arguments Error -- " + str(e))
    sys.exit(1)


def KtoF(K):
    return round(((9.0/5.0) * (K - 273) + 32),1)

try:

    #OpenWeatherMaps API
    #f = urllib.request.urlopen('https://api.openweathermap.org/data/2.5/weather?APPID=d9471a68f16db2356487665c51cf0e8a&id=5219488')
    f = urllib.request.urlopen(api_url)
    json_string = f.read()
    parsed_json = json.loads(json_string.decode("utf8"))
    outsidetemp = parsed_json['main']['temp']
    outsidefeelslike = parsed_json['main']['feels_like']
    outsidepressure = parsed_json['main']['pressure']
    outsidehumidity = parsed_json['main']['humidity']
    outsidewindspeed = parsed_json['wind']['speed']
    f.close()
    #print(parsed_json)
except Exception as e:
    logger.error("Script Failed: " + str(datetime.now()) + " -- API or JSON Error -- " + str(e))
    sys.exit(1)

try:
    returndata = "out_temp:" + str(KtoF(outsidetemp))\
                + " out_feelslike:" + str(KtoF(outsidefeelslike))\
                + " out_pressure:" + str(round(outsidepressure * 0.02953,4))\
                + " out_humidity:" + str(outsidehumidity)\
                + " out_windspeed:" + str(round(outsidewindspeed * 2.23694,2))

    print(returndata)
except Exception as e:
    logger.error("Script Failed: " + str(datetime.now()) + " -- Data Output Error -- " + str(e))
    sys.exit(1)

logger.info("Script ended: " + str(datetime.now()) + " -- Output -- " + returndata)

