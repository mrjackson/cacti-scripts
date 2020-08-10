#!/usr/bin/env python3
#./speedtest --server-id=15197 --unit=Mbps --format=json-pretty
#./speedtest.py 15197 1500 100 100 15
#Server List https://c.speedtest.net/speedtest-servers-static.php
#Download cli client https://www.speedtest.net/apps/cli


import sys
import subprocess
from datetime import datetime
from datetime import timedelta
import json
from os import path
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger("Rotating Log")
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler(filename="/var/www/htdocs/cacti/log/speedtest.log", maxBytes=1048576, backupCount=1)
logger.addHandler(handler)
logger.info("Script started: " + str(datetime.now()) + " -- Arguments -- " + str(sys.argv[1:]))
prevrunfile = "/var/www/htdocs/cacti/log/speedtestres.txt"
datacurrent = 0

try:
    serverid = str(sys.argv[1])
    interval = int(sys.argv[2])
    speedup = int(sys.argv[3])
    speeddn = int(sys.argv[4])
    slowper = int(sys.argv[5])

    if serverid != "00000":
        serverid = " --server-id=" + str(serverid)
    else:
        serverid = ""
except Exception as e:
    logger.error("Script Failed: " + str(datetime.now()) + " -- Arguments Error -- " + str(e))
    sys.exit(1)

#PTD Palmnerton --server-id=15197, use 00000 for auto selection
cmd = "/var/www/htdocs/cacti/scripts/speedtest --accept-license" + serverid + " --format=json"
#Run speedtest and return json data
def speedtest(cmd):
    process = subprocess.Popen(
        cmd,
        shell=True,
        stdout=subprocess.PIPE)
    process.wait()
    data, err = process.communicate()
    if process.returncode is 0:
        return data.decode('utf-8')
    else:
        print("Error:", err)
    return ""

def BpstoMbps(byte):
    return round((byte / 125000),2)

def percentage(percent, whole):
    return (percent * whole) / 100.0

#Load last run data
try:
    if (path.exists(prevrunfile)):
        logger.info("File Esists")
        with open(prevrunfile) as f:
            json_string_prev = json.load(f)
        prevjitter = json_string_prev['ping']['jitter']
        prevping = json_string_prev['ping']['latency']
        prevdownload = BpstoMbps(json_string_prev['download']['bandwidth'])
        prevupload = BpstoMbps(json_string_prev['upload']['bandwidth'])
        prevtimestamp = datetime.strptime(json_string_prev['timestamp'], '%Y-%m-%dT%H:%M:%SZ')
    else:
        prevupload = 1
        prevdownload = 1
        prevtimestamp = datetime.strptime('2019-5-1 12:34:56', '%Y-%m-%d %H:%M:%S')
        logger.info("File does not exist: " + str(prevupload) + " " + str(prevdownload) + " " + str(prevtimestamp))
except Exception as e:
    logger.error("Script Failed: " + str(datetime.now()) + " -- Read Prev Run -- " + str(e))

#Run speedtest and log-output data
try:
    if (datetime.utcnow() > (prevtimestamp + timedelta(seconds=interval))) or (percentage(slowper, speeddn) > prevdownload) or (percentage(slowper, speedup) > prevupload):
        logger.info("-- " + str(datetime.now()) + " -- Using new data" )
        json_string=json.loads(speedtest(cmd))
        with open(prevrunfile, 'w') as json_file:
            json.dump(json_string, json_file)
        datacurrent = 1
    else:
        logger.info("-- : " + str(datetime.now()) + " -- Using old data --")
        json_string = json_string_prev

    jitter = json_string['ping']['jitter']
    ping = json_string['ping']['latency']
    download = BpstoMbps(json_string['download']['bandwidth'])
    upload = BpstoMbps(json_string['upload']['bandwidth'])

    results = "jitter:" + str(jitter) + " ping:" + str(ping) + " download:" + str(download) + " upload:" + str(upload) + " current:" + str(datacurrent)
    print(results)
    logger.info("Script finished: " + str(datetime.now()) + " -- " + serverid + " -- " + results)

except Exception as e:
    logger.error("Script Failed: " + str(datetime.now()) + " -- Run Test -- " + str(e))
    sys.exit(1)
