#!/bin/bash

hdir="/mldev"
hlogs="$hdir/bin/data/infofeeds/logs"
dName="dataminerInvestingWorldGovernmentBonds"

#killall -9 python 

pcwd=`pwd`

mkdir -p $hlogs

cd $hdir/lib/DataPipeline/

echo '=========='  >> $hlogs/$dName.log
date               >> $hlogs/$dName.log
echo '=========='  >> $hlogs/$dName.err.log
date               >> $hlogs/$dName.err.log

/usr/bin/scrapy crawl investingWorldGovernmentBonds --nolog \
                  1>> $hlogs/$dName.log \
                  2>> $hlogs/$dName.err.log

cd $pcwd

echo '=========='  >> $hlogs/$dName.log
echo '=========='  >> $hlogs/$dName.err.log

exit 0
