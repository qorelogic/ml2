#!/bin/bash

hdir="data/db-archive"

if [ "$1" == "" ]; then
	echo "usage: db<int>"
else
tar jxfv $hdir/$1.tar.bz2  -C $hdir
mongorestore $hdir/data/$1/

wipe -rfqQ1 $hdir/data/$1/ql/equity.*
wipe -rfqQ1 $hdir/data/$1/ql/system.*
rm -rfv $hdir/data/$1/
fi
