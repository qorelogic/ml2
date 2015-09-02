#!/bin/bash

killall -9 python 

pcwd=`pwd`

cd /mldev/lib/DataPipeline/
/usr/bin/scrapy crawl investingTechnical --nolog
cd $pcwd
/mldev/bin/qlm.py ta
