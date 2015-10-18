#!/bin/bash

hdir="data/db-archive"

srcdb="mydb2"
dstdb="mydb234"
#dsthost="localhost"
dsthost="159.203.65.61"
#dstuser="qore2"
dstuser="root"
portmongo=27017
portlocal=3317

#mongodump --db=$srcdb --tar --out=- | bzip2 --fast | ssh ${dstuser}@${dsthost} 'bunzip2 | mongorestore --db=$dstdb --drop --tar --dir=-'

extractdb() {
	dbfname="$1"; 
	mkdir $hdir/$dbfname; 
	tar jxfv $hdir/$dbfname.tar.bz2 #-C $hdir/$dbfname
}

extract-all() {
	extractdb "db2"
	extractdb "db3"
	extractdb "db4"
	extractdb "db5"
	extractdb "db6"
}

restore-all() {
	for i in `ls $hdir/data`; do 
		echo $i; 
		echo '---'
		mongorestore -d $i $hdir/data/$i/ql/
		echo '==='
	done
}

pull-db() {
	# source: http://stackoverflow.com/questions/16619598/sync-mongodb-via-ssh
	ssh -L$portlocal:localhost:$portmongo ${dstuser}@${dsthost} '
	    echo "Connected on Remote End, sleeping for 10"; 
	    sleep 10; 
	    exit' &
	echo "Waiting 5 sec on local";
	sleep 5;
	echo "Connecting to Mongo and piping in script";
	echo "
	use $dstdb;
	db.dropDatabase();
	use $srcdb;
	db.copyDatabase(\"$srcdb\",\"$dstdb\",\"localhost:$portlocal\");
	" | mongo --verbose
}

pull-db2() {
	# source: http://stackoverflow.com/questions/16619598/sync-mongodb-via-ssh
	ssh -L$portlocal:localhost:$portmongo ${dstuser}@${dsthost} '
	    echo "Connected on Remote End, sleeping for 10"; 
	    sleep 30; 
	    exit' &
	echo "Waiting 5 sec on local";
	sleep 5;
	echo "Connecting to Mongo and piping in script";
	#./nfs.sh
	./dbbackup.sh ${dsthost}
}

#extract-all
#pull-db
#restore-all
