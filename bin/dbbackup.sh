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
	#sudo rsync -avP /var/lib/mongodb/ /mnt/$ipaddr/data/var-lib-mongodb/
	#echo "rsync -avP /var/lib/mongodb/ /mnt/$ipaddr/mongodb/"
	sudo rsync -avn \
	  --exclude='admin.*' --exclude='local.*' --exclude='mongod.lock'  --exclude='mydb*'  --exclude='storage.*'  --exclude='journal*' \
	  data/var-lib-mongodb/ /var/lib/mongodb/
	sudo chown mongodb:nogroup /var/lib/mongodb/*.*

	scrdir="data/db3"
	dsttarball="db3.tar.bz2"
	wipe -fqQ1 data/db2.tar.bz2
	rm -rf $scrdir
#	mongodump -d ql -c equity --out $scrdir/
	mongodump -d ql --out $scrdir/
	tar jcfv /mnt/$ipaddr/data/$dsttarball $scrdir/
fi
