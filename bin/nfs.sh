#!/bin/bash

#miaddr="104.131.163.27"
miaddr="45.55.92.77"

sudo mkdir /mnt/$miaddr 2> /dev/null

#ssh -L 3049:localhost:2049 -oStrictHostKeyChecking=no root@$miaddr
sudo mount -t nfs -o port=2049 $miaddr:/mldev/bin/data /mnt/$miaddr
