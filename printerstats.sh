#!/bin/bash

host=$1

LOG="/var/www/htdocs/cacti/log/printerstats.log"
echo "$(date) -- Printerstats Started - $host" >> $LOG

totalpage="U"
scannerpage="U"
faxrxpage="U"
faxtxpage="U"
blackper="U"
cyanper="U"
magentaper="U"
yellowper="U"

#Current Page Count
pagecounttotal () {
	totalpage=$(snmpwalk -v1 -c public $host .1.3.6.1.2.1.43.10.2.1.4.1.1)
	totalpage=$(echo $totalpage | cut -d ' ' -f 4-)
}

#Scanner Page Count
scannersendtotal () {
        scannerpage=$(snmpwalk -v1 -c public $host .1.3.6.1.4.1.367.3.2.1.2.19.5.1.9.29)
        scannerpage=$(echo $scannerpage | cut -d ' ' -f 4-)
}

#Scanner Page Count
faxtotal () {
        faxtxpage=$(snmpwalk -v1 -c public $host .1.3.6.1.4.1.367.3.2.1.2.19.5.1.9.27)
        faxtxpage=$(echo $faxtxpage | cut -d ' ' -f 4-)
	faxrxpage=$(snmpwalk -v1 -c public $host .1.3.6.1.4.1.367.3.2.1.2.19.5.1.9.22)
        faxrxpage=$(echo $faxrxpage | cut -d ' ' -f 4-)
}

#Black Toner Percentage Remaining
blacktoner () {
	blackmax=$(snmpwalk -v1 -c public $host .1.3.6.1.2.1.43.11.1.1.8.1.$1)
	blackmax=$(echo $blackmax | cut -d ' ' -f 4-)
	blackcur=$(snmpwalk -v1 -c public $host .1.3.6.1.2.1.43.11.1.1.9.1.$1)
	blackcur=$(echo $blackcur | cut -d ' ' -f 4-)
	blackper=$(echo "scale=4; $blackcur/$blackmax*100" | bc)
#	echo $blackmax $blackcur $blackper
}

#Cyan Toner Percentage Remaining
cyantoner () {
	cyanmax=$(snmpwalk -v1 -c public $host .1.3.6.1.2.1.43.11.1.1.8.1.$1)
	cyanmax=$(echo $cyanmax | cut -d ' ' -f 4-)
	cyancur=$(snmpwalk -v1 -c public $host .1.3.6.1.2.1.43.11.1.1.9.1.$1)
	cyancur=$(echo $cyancur | cut -d ' ' -f 4-)
	cyanper=$(echo "scale=4; $cyancur/$cyanmax*100" | bc)
#	echo $cyanmax $cyancur $cyanper
}

#Magenta Toner Percentage Remaining
magentatoner () {
	magentamax=$(snmpwalk -v1 -c public $host .1.3.6.1.2.1.43.11.1.1.8.1.$1)
	magentamax=$(echo $magentamax | cut -d ' ' -f 4-)
	magentacur=$(snmpwalk -v1 -c public $host .1.3.6.1.2.1.43.11.1.1.9.1.$1)
	magentacur=$(echo $magentacur | cut -d ' ' -f 4-)
	magentaper=$(echo "scale=4; $magentacur/$magentamax*100" | bc)
#	echo $magentamax $magentacur $magentaper
}

#Yellow Toner Percentage Remaining
yellowtoner () {
	yellowmax=$(snmpwalk -v1 -c public $host .1.3.6.1.2.1.43.11.1.1.8.1.$1)
	yellowmax=$(echo $yellowmax | cut -d ' ' -f 4-)
	yellowcur=$(snmpwalk -v1 -c public $host .1.3.6.1.2.1.43.11.1.1.9.1.$1)
	yellowcur=$(echo $yellowcur | cut -d ' ' -f 4-)
	yellowper=$(echo "scale=4; $yellowcur/$yellowmax*100" | bc)
#	echo $yellowmax $yellowcur $yellowper
}


oidprefix=".1.3.6.1.2.1.43.11.1.1."

for arg in 1 2 3 4
do
	oidsec="6.1."
	oid="$oidprefix$oidsec$arg"
#	echo $oid

	tonercolor=$(snmpwalk -O T -v1 -c public $host $oid)
	echo $tonercolor
        oidcolor=$(echo $tonercolor | cut -d ' ' -f 4 | cut -c 2-)
#	echo $oidcolor
        if [[ "$tonercolor" == *"Black"* ]] || [[ "$tonercolor" == *"black"* ]]; then
                blacktoner $arg
        elif [[ "$tonercolor" == *"Cyan"* ]] || [[ "$tonercolor" == *"cyan"* ]]; then
                cyantoner $arg
        elif [[ "$tonercolor" == *"Magenta"* ]] || [[ "$tonercolor" == *"magenta"* ]]; then
                magentatoner $arg
        elif [[ "$tonercolor" == *"Yellow"* ]] || [[ "$tonercolor" == *"yellow"* ]]; then
                yellowtoner $arg
        else
                blacktoner 1
        fi
done


pagecounttotal
scannersendtotal
faxtotal
#blacktoner 1

#totalpage=99
#blackper=24
#cyanper=25
#magentaper=26
#yellowper=27


#RES="totalpage:$totalpage blackper:$blackper cyanper:$cyanper magentaper:$magentaper yellowper:$yellowper scannerpage:$scannerpage faxrxpage:$faxrxpage faxtxpage:$faxtxpage"
RES="totalpage:$totalpage blackper:$blackper cyanper:$cyanper magentaper:$magentaper yellowper:$yellowper"
echo "$RES - $host" >> $LOG
echo $RES
 
