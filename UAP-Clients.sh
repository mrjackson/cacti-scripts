#!/bin/bash

host=$1

LOG="/var/www/htdocs/cacti/log/UAP-Clients.log"
echo "$(date) -- UAP-Clients Started - $host" >> $LOG

OIDAPChan=.1.3.6.1.4.1.41112.1.6.1.2.1.4.
OIDAPName=.1.3.6.1.4.1.41112.1.6.1.2.1.6.
OIDclient=.1.3.6.1.4.1.41112.1.6.1.2.1.8.

community="public"
client2g="U"
client5g="U"
clientguest2g="U"
clientguest5g="U"
clienttotal="U"
clientguesttotal="U"


#Match OID to APName/Radio
for arg in 1 2 3 4 5 6 7 8 9
do
	oidName="$OIDAPName$arg"
	oidChan="$OIDAPChan$arg"
#	echo $oid

	APNameQuery=$(snmpwalk -O n -t 30 -r 0 -v 1 -c $community $host $oidName)
#	echo $APNameQuery
        APChanQuery=$(snmpwalk -O n -t 30 -r 0 -v 1 -c $community $host $oidChan)
#        echo $APChanQuery
        APName=$(echo $APNameQuery | cut -d '"' -f 2)
#	echo $APName
        APChan=$(echo $APChanQuery | cut -d ':' -f 2)
#	APChan="${APChan//[$'\t\r\n ']}"
#	echo $APChan
        if [ "$((APChan))" -lt 15 ]; then
                if [ "$APName" == "LIGINS" ]; then
					OIDclient2g="$arg"
				elif [ "$APName" == "LIGINS-GUEST" ]; then
					OIDclientguest2g="$arg"
				fi
        elif [ "$((APChan))" -gt 15 ]; then
                if [ "$APName" == "LIGINS" ]; then
					OIDclient5g="$arg"
				elif [ "$APName" == "LIGINS-GUEST" ]; then
					OIDclientguest5g="$arg"
				fi

        fi
done


#add up clients per APName & Radio
client2g=$((snmpwalk -v1 -c $community $host $OIDclient$OIDclient2g) | cut -d ' ' -f 4)
client5g=$((snmpwalk -v1 -c $community $host $OIDclient$OIDclient5g) | cut -d ' ' -f 4)
clientguest2g=$((snmpwalk -v1 -c $community $host $OIDclient$OIDclientguest2g) | cut -d ' ' -f 4)
clientguest5g=$((snmpwalk -v1 -c $community $host $OIDclient$OIDclientguest5g) | cut -d ' ' -f 4)
clienttotal=$((client2g + client5g))
clientguesttotal=$((clientguest2g + clientguest5g))

#pagecounttotal
#blacktoner 1




RES="clienttotal:$clienttotal client2g:$client2g client5g:$client5g clientguesttotal:$clientguesttotal clientguest2g:$clientguest2g clientguest5g:$clientguest5g"
echo "$RES - $host" >> $LOG
echo $RES
 
