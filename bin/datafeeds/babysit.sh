#!/bin/bash

qstart() {
	if [ "$1" == "" ]; then
		echo 'usage: '
	fi
	qport="$1"
	/usr/bin/lsof -i | grep -i $qport | grep -i listen | perl -pe "s/.*?python.+?([\d]+).+/\\1/g" | xargs kill -9
}

qstart 5555
python oanda.py zmq
