
_mongod() {
	_mongodHdir="/etc"
	if [ -e "$_mongodHdir/mongod.conf" ]; then 
	sudo mongod --config=/$_mongodHdir/mongod.conf --rest
	#echo 1
	fi
	if [ -e "$_mongodHdir/mongodb.conf" ]; then 
	#echo 2
	sudo mongod --config=/$_mongodHdir/mongodb.conf --rest
	fi
}

_mongodlog() {
	_mongodHdir="/var/log/mongodb"

	
	if [ -e "$_mongodHdir/mongod.log" ]; then 
	tail -f  /$_mongodHdir/mongod.log
	#echo 1
	fi
	if [ -e "$_mongodHdir/mongodb.log" ]; then 
	tail -f  /$_mongodHdir/mongodb.log
	#echo 2
	fi
}

mongo.ql.ticks2csv() {
    ticks="`mongo --quiet --eval 'db.ticks.stats()["count"]' ql`"
    echo "ticks: $ticks"
    fname="mongo.ql.ticks.csv.gz"
    echo "writing to: $fname"
    # source: http://stackoverflow.com/questions/13577230/export-a-csv-from-mongodb
    mongoexport --csv -d ql -c ticks -f "instrument,bid,ask,time" | gzip > $fname
}

# examples:
# . ./functions.sh && cat mongo.ql.ticks.csv | pivot.mongo.ql.ticks.csv
# . ./functions.sh && zcat mongo.ql.ticks.csv.gz | pivot.mongo.ql.ticks.csv
pivot.mongo.ql.ticks.csv() {
python -c "
import pandas as p
import sys

df = p.read_csv(sys.stdin)
#df = p.read_csv('/mldev/bin/mongo.ql.ticks.csv')

df = df.drop_duplicates(subset='time')
#print df

dfp = df.pivot('time', 'instrument', 'bid')

dfp = dfp.ffill().bfill().sort()

dfp.to_csv('/mldev/bin/mongo.ql.ticks.pivot.csv')
print dfp
"
}

swapOn() {
	# free | grep -i swap | perl -pe 's/[\s]+/ /g' | cut -d' ' -f2
	let swapSpace=`free | grep -i mem | perl -pe 's/[\s]+/ /g' | cut -d' ' -f2`
	let swapSpace=`python -c "print $swapSpace * 2"`
	if [ ! -f "/tmp/swapfile1" ]; then
	# turn swap on
	# http://stackoverflow.com/questions/18334366/out-of-memory-issue-in-installing-packages-on-ubuntu-server
	echo 'turning swap on'
	#sudo dd if=/dev/zero of=/tmp/swapfile1 bs=1024 count=524288
	# https://github.com/tensorflow/models/issues/80
	sudo dd if=/dev/zero of=/tmp/swapfile1 bs=1024 count=$swapSpace
	sudo mkswap /tmp/swapfile1
	sudo chown root:root /tmp/swapfile1
	sudo chmod 0600 /tmp/swapfile1
	sudo swapon /tmp/swapfile1
	else
	echo 'swap already on'
	fi
}

swapOff() {
	if [ -f "/tmp/swapfile1" ]; then
	# swapp off
	echo 'turning swap off'
	sudo swapoff -v /tmp/swapfile1
	sudo rm -f /tmp/swapfile1
	else
	echo 'swap already off'
	fi
}

