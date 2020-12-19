#!/usr/bin/env python3
#./CertExpire.py misterjackson.info 443 04AA86C05CB9C8F5D43DC1B88DC25DB5109B no yes yes no
#./CertExpire.py <hostname> <port> <serial> <unsigned> <serialverify> <hostnameverify> <debug>

from urllib.request import Request, urlopen, ssl, socket
from urllib.error import URLError, HTTPError
import urllib3
import sys
import datetime
import time
import json
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger("Rotating Log")
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler(filename="/var/www/htdocs/cacti/log/CertExpire.log", maxBytes=1048576, backupCount=1)
logger.addHandler(handler)

logger.info("Script started: " + str(datetime.datetime.now()))
logger.info("Script Arguments: " + str(sys.argv))
today = datetime.datetime.today()
port = '443'
serial = "U"

try:
	hostname = (sys.argv[1])
	port = (sys.argv[2])
	serial = (sys.argv[3])
except Exception as e:
	logger.error("Script Failed: " + str(datetime.datetime.now()) + " -- Arguments Error -- " + str(e))
	sys.exit(1)

results = ""

try:
	unsigned = (sys.argv[4])
	serialverify = (sys.argv[5])
	hostnameverify = (sys.argv[6])
	debug = (sys.argv[7])
except Exception as e:
	unsigned = "no"
	serialverify = "yes"
	domainverify = "yes"
	debug = "no"

context = ssl.create_default_context()

if unsigned == "yes":
#	context = ssl._create_unverified_context()
	#ssl._create_default_https_context = ssl._create_unverified_context
#	context = ssl.create_default_context()
	urllib3.disable_warnings()
	context.check_hostname = False
#	context.verify_mode = ssl.CERT_NONE
#	print("Unverified context")
#else:
#	context = ssl.create_default_context()
#context = ssl.create_default_context()
#context = ssl._create_unverified_context()

try:
	with socket.create_connection((hostname, port)) as sock:
		#print(sock)
		with context.wrap_socket(sock, server_hostname=hostname) as ssock:
			#print(ssock)
			json_string = ssock.getpeercert()

			if (debug == "debug"):
				print(json_string)
				print(context)

			notBefore = json_string['notBefore']
			notAfter = json_string['notAfter']
			serialNumber = json_string['serialNumber']

			for i in range(len(json_string['subject'])):
				s = (str(json_string['subject'][i]))
				if (s.find('commonName') != -1):
					commonName = json_string['subject'][i][0][1]

	daysafter = datetime.datetime.strptime(notAfter, "%b %d %H:%M:%S %Y %Z") - today
	daysbefore = datetime.datetime.strptime(notBefore, "%b %d %H:%M:%S %Y %Z") - today
	daysafter = (daysafter.days)
	daysbefore = (daysbefore.days)
	expiredate = datetime.datetime.date(datetime.datetime.strptime(notAfter, "%b %d %H:%M:%S %Y %Z"))

	if serialNumber != serial and serialverify == "yes":
		daysafter = -99

	if serial == "U":
		daysafter = "U"
		daysbefore = "U"

	if commonName[0] == '*':
		commonNameCorrected = commonName[2:]
		#print(commonNameCorrected)
	else:
		commonNameCorrected = commonName

	if commonNameCorrected != hostname and hostnameverify == "yes":
		daysafter = -89

	results = "daysafter:" + str(daysafter) + " daysbefore:" + str(daysbefore)
	##results = "daysafter:" + str(daysafter) + " daysbefore:" + str(daysbefore) + " expirereg:" + str(expirereg)
	#Uncomment line below to force fake data
	#results = "daysafter:60 daysbefore:-348 expirereg:55"
	print(results)
	logger.info("Script finished: " + str(datetime.datetime.now()) + " -- " + sys.argv[1] + " -- " + results + " cur serial:" + serialNumber + " good serial:" + serial + " commonName: " + commonName)

except Exception as e:
        logger.error("Script Failed: " + str(datetime.datetime.now()) + " -- " + sys.argv[1] + " -- " + str(e))
        sys.exit(1)




