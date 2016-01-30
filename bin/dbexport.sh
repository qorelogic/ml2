#!/bin/bash

qhost="127.0.0.1"
qport=3310
qdb="ql"
qcollection="ticks"
qfields="time,instrument,bid,ask"

mongoversion="`mongoexport --version | cut -d' ' -f3`"

if [ "$mongoversion" == "2.4.9" ]; then
	mongoexport --host $qhost --port $qport -d $qdb -c $qcollection --csv -f  $qfields
else
	mongoexport --host $qhost --port $qport -d $qdb -c $qcollection --type=csv -f  $qfields
fi
