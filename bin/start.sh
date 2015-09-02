#!/bin/bash

sudo pip install ujson
rm -f ~/.tmuxifier/layouts
./datafeeds/setup.sh 
sudo puppet apply provisioner/default.pp 

/home/qore/mldev/lib/DataPipeline/setup.sh 
ln -s /home/qore/mldev/lib/DataPipeline /home/qore/mldev/lib/crawlers/finance/dataPipeline.scrapy
mkdir -p /home/qore/mldev/lib/crawlers/finance/
