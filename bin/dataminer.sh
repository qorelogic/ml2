#!/bin/bash

hdir="/mldev"
hlogs="$hdir/bin/data/infofeeds/logs"

#killall -9 python 

pcwd=`pwd`

mkdir -p $hlogs

cd $hdir/lib/DataPipeline/

echo '=========='  >> $hlogs/dataminer.log
date               >> $hlogs/dataminer.log
echo '=========='  >> $hlogs/dataminer.err.log
date               >> $hlogs/dataminer.err.log

/usr/bin/scrapy crawl investingTechnical --nolog \
                  1>> $hlogs/dataminer.log \
                  2>> $hlogs/dataminer.err.log

cd $pcwd

# run it!
$hdir/bin/qlm.py ta 1>> $hlogs/dataminer.log 2>> $hlogs/dataminer.err.log

echo '=========='  >> $hlogs/dataminer.log
echo '=========='  >> $hlogs/dataminer.err.log

exit 0
