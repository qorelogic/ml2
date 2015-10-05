#!/bin/bash

miaddr="104.131.163.27"

mkdir /mnt/$miaddr

#ssh -L 3049:localhost:2049 -oStrictHostKeyChecking=no root@$miaddr
sudo mount -t nfs -o port=2049 $miaddr:/mldev/bin/data /mnt/$miaddr
