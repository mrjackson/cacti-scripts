#!/usr/bin/env python3

import sys
import subprocess
import logging
from logging.handlers import RotatingFileHandler
import datetime

logger = logging.getLogger("Rotating Log")
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler(filename="/var/www/htdocs/cacti/log/esxi_cpu_load.log", maxBytes=1048576, backupCount=1)
logger.addHandler(handler)

logger.info("Script started: " + str(datetime.datetime.now()) + " -- " + sys.argv[1] + " -- " + sys.argv[2])

host = (sys.argv[1])
community = (sys.argv[2])
oidprefix = ".1.3.6.1.2.1.25.3.3"
cpucount = 0
cputotal = 0
results = ""

try:
	snmpcommand = ("/usr/bin/snmpwalk -O n -t 30 -r 0 -v 2c -c " + community + " " +  host + " " + oidprefix + " 2> /dev/null")
	snmpbulk = subprocess.getoutput(snmpcommand)
	#logger.info("snmpwalk output --" + sys.argv[1] + " -- " + snmpbulk)
	for line in snmpbulk.split('\n'):
		cpucount += 1
		cpunum = (int((line[24:26]).rstrip()))
		cpuload = (int((line[-2::]).lstrip()))
		cputotal = cputotal + cpuload
		results = results + "cpu" + str(cpunum) + ":" + str(cpuload) + " "

	results = results + "cpuavg:" + str(int(cputotal / cpunum))
	print(results)
	logger.info("Script finished: " + str(datetime.datetime.now()) + " -- " + sys.argv[1] + " -- " + results)

except Exception as e:
	logger.error("Script Failed: " + str(datetime.datetime.now()) + " -- " + sys.argv[1] + " -- " + str(e))
	sys.exit(1)
