#!/usr/bin/env python3

#pip3 install python-whois

from urllib.request import Request, urlopen, ssl, socket
from urllib.error import URLError, HTTPError
import sys
import datetime
import time
import json
import whois
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger("Rotating Log")
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler(filename="/var/www/htdocs/cacti/log/DomainExpire.log", maxBytes=1048576, backupCount=1)
logger.addHandler(handler)

logger.info("Script started: " + str(datetime.datetime.now()))

today = datetime.datetime.today()
port = '443'
serial = "U"

try:
	hostname = (sys.argv[1])
except Exception as e:
	logger.error("Script Failed: " + str(datetime.datetime.now()) + " -- Argument Error -- " + str(e))
	sys.exit(1)

##try:
##	serial = (sys.argv[2])
##except Exception as e:
##	serial = "U"

results = ""
##context = ssl.create_default_context()

try:
	try:
		w = whois.whois(hostname)
	except:
		e = sys.exc_info()[0]
		logger.error("Script Error: " + str(datetime.datetime.now()) + " -- " + sys.argv[1] + " -- " + str(e))

#	try:
#		print(w)
#	except:
#		e = sys.exc_info()[0]
#		logger.error("Script Error: " + str(datetime.datetime.now()) + " -- " + sys.argv[1] + " -- " + str(e))

	#print(w)
	#print(type(w.expiration_date))
	if type(w.expiration_date) is not list:
		expiredate = w.expiration_date
	else:
		expiredate = w.expiration_date[0]

	expirereg = (expiredate - today).days
	results = "expirereg:" + str(expirereg)
	#Uncomment line below to force fake data
	#results = "daysafter:60 daysbefore:-348 expirereg:55"
	print(results)
	logger.info("Script finished: " + str(datetime.datetime.now()) + " -- " + sys.argv[1] + " -- " + results)

except Exception as e:
        logger.error("Script Failed: " + str(datetime.datetime.now()) + " -- " + sys.argv[1] + " -- " + str(e))
        sys.exit(1)




