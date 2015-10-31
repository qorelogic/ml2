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
	sudo rsync -avP /mnt/$ipaddr/mongodb/ /var/lib/mongodb/
	#sudo rsync -avP /var/lib/mongodb/ /mnt/$ipaddr/data/var-lib-mongodb/
	#echo "rsync -avP /var/lib/mongodb/ /mnt/$ipaddr/mongodb/"
	#rsync -avP /mnt/$ipaddr/data/db-archive/ data/db-archive/
	#sudo rsync -avn \
	#  --exclude='admin.*' --exclude='local.*' --exclude='mongod.lock'  --exclude='mydb*'  --exclude='storage.*'  --exclude='journal*' \
	#  data/var-lib-mongodb/ /var/lib/mongodb/
	#sudo chown mongodb:nogroup /var/lib/mongodb/*.*
	sudo service mongod start

	tmdate="`date +'%Y%m%d_%H%M%S'`"
	dname="db${dbx}_$tmdate"
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
	md5sum data/db-archive/$dsttarball  /mnt/$ipaddr/data/db-archive/$dsttarball
fi

history12() {

.gpull
git fetch origin 
git fetch origin forecaster.refactored-0.3-backupSlug1gb:forecaster.refactored-0.3-backupSlug1gb 
git checkout -m forecaster.refactored-0.3-backupSlug1gb
nano provisioner/default.pp 

### 

###
cd /mldev/bin/
.gb
.gpull
nano dbbackup.sh 
git fetch origin 
echo 'git fetch origin ' >> dbbackup.sh 
df -h
nano dbbackup.sh 
git fetch origin forecaster.refactored-0.3-backupSlug1gb:forecaster.refactored-0.3-backupSlug1gb 
echo 'git fetch origin forecaster.refactored-0.3-backupSlug1gb:forecaster.refactored-0.3-backupSlug1gb ' >> dbbackup.sh 
git checkout forecaster.refactored-0.3-backupSlug1gb
.gdl
git checkout -m forecaster.refactored-0.3-backupSlug1gb
.gb
echo 'git checkout -m forecaster.refactored-0.3-backupSlug1gb' >> dbbackup.sh 
sudo nano provisioner/default.pp 
echo 'nano provisioner/default.pp ' >> dbbackup.sh 
sudo puppet apply provisioner/default.pp 
df
nano ~/.bash_history 

###

ls /var/lib/mongodb/
mx
mx l
mx w mongo
cd "/ml.dev/bin"
clear
sudo mongod --config=/etc/mongod.conf
sudo mongod --config=/etc/mongod.conf 
sudo service mongod stop
sudo mongod --config=/etc/mongod.conf 
sudo service mongod start
sudo service mongod stop
./dbbackup.sh 104.131.47.179 db-011
sudo service mongod start
./dbbackup.sh 104.131.47.179 db-011
sudo service mongod start
sudo service mongod stop
sudo service mongod start
sudo service mongod stop
rm -f /var/lib/mongodb/mongod.lock 
sudo rm -f /var/lib/mongodb/mongod.lock 
sudo service mongod stop
sudo service mongod start
sudo mongod --config=/etc/mongod.conf 
cd "/ml.dev/bin"
clear
tail -f /var/log/mongodb/mongod.log
watch -n1 df -h
cd /mldev/bin/
nano ~/.bash_history 
df
./nfs.sh 
df
nano dbbackup.sh 
./dbbackup.sh 
./dbbackup.sh 104.131.47.179 
./dbbackup.sh 104.131.47.179 db-011
df
df -h
nano dbbackup.sh 
./dbbackup.sh 104.131.47.179 db-011
df -h
wipe
sudo apt-get install wipe
wipe -rfqQ1 data/db*
df
nano dbbackup.sh 
./dbbackup.sh 104.131.47.179 db-011
nano dbbackup.sh 
./dbbackup.sh 104.131.47.179 db-011
nano dbbackup.sh 
md5sum data/db-archive/dbdb-011_2015103*
df
.gai
.gb

}
