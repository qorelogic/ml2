
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
