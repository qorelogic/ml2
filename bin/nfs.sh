#!/bin/bash

nfsmount() {
	miaddr="$1"
	
	#ssh -L 3049:localhost:2049 -oStrictHostKeyChecking=no root@$miaddr
	#sudo umount /mnt/$miaddr

	sudo mkdir -p /mnt/$miaddr/mongodb 2> /dev/null
	sudo umount /mnt/$miaddr/mongodb
	sudo mount -t nfs -o port=2049 $miaddr:/var/lib/mongodb /mnt/$miaddr/mongodb

	sudo mkdir -p /mnt/$miaddr/data 2> /dev/null
	sudo umount /mnt/$miaddr/data
	sudo mount -t nfs -o port=2049 $miaddr:/mldev/bin/data /mnt/$miaddr/data

	sudo mkdir -p /mnt/$miaddr/datapipeline 2> /dev/null
	sudo umount /mnt/$miaddr/datapipeline
	sudo mount -t nfs -o port=2049 $miaddr:/mldev/lib/DataPipeline /mnt/$miaddr/datapipeline
}

nfsmount 45.55.92.77
nfsmount 104.131.163.27
#nfsmount 159.203.64.99
