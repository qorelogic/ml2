#!/bin/bash

dbwot="ticks"
#colwot="equity"

#mongodump --host=127.0.0.1 --port=27017 -d ql -c "${colwot}" --out - | gzip > /mldev/bin/data/db/${colwot}-db.date +%F.gz
#mongodump --host=127.0.0.1 --port=27017 -d ql -c "${colwot}" --out - | bzip -z > /mldev/bin/data/db/${colwot}-db.date +%F.bz2

if [ "$1" == "" ] || [ "$2" == "" ]; then
	echo "usage: <ipaddr> <dbname dbX where X=integer>"
else
	ipaddr="$1"
	dbx="$2"
	#mongodump --host=127.0.0.1 --port=27017 -d ql -c "${colwot}" --out /mnt/$ipaddr/db/

	sudo service mongod stop
	#rsync -avP /var/lib/mongodb/ root@$ipaddr:/var/lib/mongodb/
	echo "rsync -avP /mnt/$ipaddr/mongodb/ /var/lib/mongodb/"
	#sudo rm -rfv /var/lib/mongodb/*
	sudo rsync -avP --exclude=*.lock /mnt/$ipaddr/mongodb/ /var/lib/mongodb/
	#sudo rsync -avP /var/lib/mongodb/ /mnt/$ipaddr/data/var-lib-mongodb/
	#echo "rsync -avP /var/lib/mongodb/ /mnt/$ipaddr/mongodb/"
	#rsync -avP /mnt/$ipaddr/data/db-archive/ data/db-archive/
	#sudo rsync -avn \
	#  --exclude='admin.*' --exclude='local.*' --exclude='mongod.lock'  --exclude='mydb*'  --exclude='storage.*'  --exclude='journal*' \
	#  data/var-lib-mongodb/ /var/lib/mongodb/
	#sudo chown mongodb:nogroup /var/lib/mongodb/*.*
	#sudo service mongod start

	tmdate="`date +'%Y%m%d_%H%M%S'`"
	dname="db-${dbx}_$tmdate"
	scrdir="data/$dname"
	dbarchive="data/db-archive"
	dsttarball="$dbarchive/$dname.tar.bz2"
	mkdir -p "$dbarchive"

	#wipe -fqQ1 $dsttarball
	#rm -rf $scrdir
	
	echo "mongodump -h 127.0.0.1 --port 27017 -d numbeo --out $scrdir/"
	mongodump -h 127.0.0.1 --port 27017 -d numbeo --out $scrdir/
	echo "mongodump -h 127.0.0.1 --port 27017 -d ql --out $scrdir/"
	mongodump -h 127.0.0.1 --port 27017 -d ql --out $scrdir/
	
	#echo "mongodump -h $ipaddr -d numbeo --out $scrdir/"
	#mongodump -h $ipaddr -d numbeo --out $scrdir/
	#mongodump -h $ipaddr -d ql --out $scrdir/
	#mongodump -d numbeo --out $scrdir/
	#mongodump -d ql --out $scrdir/
	
	#tar jcfv /mnt/$ipaddr/$dsttarball $scrdir/
	tar jcfv $dsttarball $scrdir/
	
	#rm -rf $scrdir
	rsync -avP data/db-archive/ /mnt/$ipaddr/data/db-archive/
fi

#sudo rsync -zavP qore@104.207.135.67:/usr/lib/mongodb.ql002-1.tar.xz /usr/lib/mongodb.ql002-1.tar.xz  
#sha1sum /usr/lib/mongodb.ql001-3.tar.xz > /usr/lib/mongodb.ql001-3.tar.xz.sha1sum

