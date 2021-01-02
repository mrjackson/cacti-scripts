#!/usr/bin/env python3
#./CertExpire.py misterjackson.info 443 04AA86C05CB9C8F5D43DC1B88DC25DB5109B no yes yes no
#./CertExpire.py <hostname> <port> <serial> <verifyserial> <verifycn>

#thold: Incorrect serial = daysafter:-99, incorrect commonname = daysbefore:99

import socket
import ssl
import OpenSSL.crypto as crypto
import datetime
import sys
import logging
from logging.handlers import RotatingFileHandler


logger = logging.getLogger("Rotating Log")
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler(filename="/var/www/htdocs/cacti/log/CertExpire.log", maxBytes=1048576, backupCount=1)
logger.addHandler(handler)

logger.info("Script started: " + str(datetime.datetime.now()))
logger.info("Script Arguments: " + str(sys.argv))
today = datetime.datetime.today()

try:
	hostname = (sys.argv[1])
	port = int(sys.argv[2])
	serial = (sys.argv[3])
	verifyserial = (sys.argv[4])
	verifycn = (sys.argv[5])
except Exception as e:
	logger.error("Script Failed: " + str(datetime.datetime.now()) + " -- Arguments Error -- " + str(e))
	sys.exit(1)

results = ""

dst = (hostname,port)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(dst)

# upgrade the socket to SSL without checking the certificate
# !!!! don't transfer any sensitive data over this socket !!!!
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
s = ctx.wrap_socket(s, server_hostname=dst[0])

try:
	cert_bin = s.getpeercert(True)
	x509 = crypto.load_certificate(crypto.FILETYPE_ASN1,cert_bin)
	#print("CN=" + x509.get_subject().CN)
	#print("Issuer=" + x509.get_issuer().CN)
	#print("notAfter=" + str(x509.get_notAfter().decode('ascii')))
	#print("notBefore=" + str(x509.get_notBefore().decode('ascii')))
	#print("SerialNumber=" + str(x509.get_serial_number()))
	#print("hasExpired=" + str(x509.has_expired()))
	#print("sigAlgorithm=" + str(x509.get_signature_algorithm().decode('ascii')))

	notBefore = datetime.datetime.strptime(x509.get_notBefore().decode('ascii'), '%Y%m%d%H%M%SZ')
	notAfter = datetime.datetime.strptime(x509.get_notAfter().decode('ascii'), '%Y%m%d%H%M%SZ')
	serialNumber = str(x509.get_serial_number())
	commonName = x509.get_subject().CN

	daysafter = (notAfter - today).days
	daysbefore = (notBefore - today).days
	expiredate = notAfter

	#print(commonName[0])
	if commonName[0] == '*':
		commonNameCorrected = commonName[2:]
		#print(commonNameCorrected)
	else:
		commonNameCorrected = commonName

	if commonNameCorrected != hostname and verifycn == "yes":
		daysbefore = 99

	if serialNumber != serial and verifyserial == "yes":
		daysafter = -99

	results = "daysafter:" + str(daysafter) + " daysbefore:" + str(daysbefore)
	#Uncomment line below to force fake data
	#results = "daysafter:60 daysbefore:-348 expirereg:55"
	print(results)
	logger.info("Script finished: " + str(datetime.datetime.now()) + " -- " + sys.argv[1] + " -- " + results + " cur serial:" + serialNumber + ", good serial:" + serial + ", commonName: " + commonName)

except Exception as e:
        logger.error("Script Failed: " + str(datetime.datetime.now()) + " -- " + sys.argv[1] + " -- " + str(e))
        sys.exit(1)
