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
	sudo rsync -avP /var/lib/mongodb/ /mnt/$ipaddr/data/var-lib-mongodb/
	echo "rsync -avP /var/lib/mongodb/ /mnt/$ipaddr/mongodb/"
fi
