#!/bin/bash

srcdb="ql22"
dstdb="ql22b"
dsthost="localhost"
dstuser="qore2"

#mongodump --db=$srcdb --tar --out=-
#mongodump --db=$srcdb --tar --out=- | bzip2 --fast | ssh ${dstuser}@${dsthost} 'bunzip2 | mongorestore --db=$dstdb --drop --tar --dir=-'

# source: http://stackoverflow.com/questions/16619598/sync-mongodb-via-ssh
ssh -L27018:localhost:27017 $dsthost '
    echo "Connected on Remote End, sleeping for 10"; 
    sleep 10; 
    exit' &
echo "Waiting 5 sec on local";
sleep 5;
echo "Connecting to Mongo and piping in script";
cat pull-db.js | mongo

