#!/bin/bash

mongoexport -h 127.0.0.1 -p 27017 -d ql -c ticks --csv -f 'time,instrument,bid,ask'
