#!/bin/bash

dbwot="ticks"
#colwot="equity"

#mongodump --host=127.0.0.1 --port=27017 -d ql -c "${colwot}" --out - | gzip > /mldev/bin/data/db/${colwot}-db.date +%F.gz
#mongodump --host=127.0.0.1 --port=27017 -d ql -c "${colwot}" --out - | bzip -z > /mldev/bin/data/db/${colwot}-db.date +%F.bz2

if [ "$1" == "" ]; then
	echo "usage: <ipaddr>"
else
	ipaddr="$1"
	#mongodump --host=127.0.0.1 --port=27017 -d ql -c "${colwot}" --out /mnt/$ipaddr/db/

	#rsync -avP /var/lib/mongodb/ root@$ipaddr:/var/lib/mongodb/
	echo "rsync -avP /mnt/$ipaddr/mongodb/ /var/lib/mongodb/"
	sudo rsync -avP /mnt/$ipaddr/mongodb/ /var/lib/mongodb/
	#sudo rsync -avP /var/lib/mongodb/ /mnt/$ipaddr/data/var-lib-mongodb/
	#echo "rsync -avP /var/lib/mongodb/ /mnt/$ipaddr/mongodb/"
	#rsync -avP /mnt/$ipaddr/data/db-archive/ data/db-archive/
	#sudo rsync -avn \
	#  --exclude='admin.*' --exclude='local.*' --exclude='mongod.lock'  --exclude='mydb*'  --exclude='storage.*'  --exclude='journal*' \
	#  data/var-lib-mongodb/ /var/lib/mongodb/
	#sudo chown mongodb:nogroup /var/lib/mongodb/*.*

	dname="db8"
	scrdir="data/$dname"
	dbarchive="data/db-archive"
	dsttarball="$dbarchive/$dname.tar.bz2"
	mkdir -p "$dbarchive"

	#wipe -fqQ1 $dsttarball
	#rm -rf $scrdir
	
	mongodump -h 127.0.0.1 --port 27017 -d numbeo --out $scrdir/
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
