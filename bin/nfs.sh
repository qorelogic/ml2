#!/bin/bash

nfsmount() {
	miaddr="$1"
	sudo mkdir /mnt/$miaddr 2> /dev/null
	
	#ssh -L 3049:localhost:2049 -oStrictHostKeyChecking=no root@$miaddr
	sudo mount -t nfs -o port=2049 $miaddr:/mldev/bin/data /mnt/$miaddr
}

nfsmount 45.55.92.77
nfsmount 104.131.163.27
nfsmount 159.203.64.99
