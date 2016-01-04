
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
    fname="ticks.csv.gz"
    echo "writing to: $fname"
    mongoexport --csv -d ql -c ticks -f "instrument,bid,ask,time" | gzip > $fname
}
