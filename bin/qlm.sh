#!/bin/bash

ps aux | grep -i qore-l - | cut -d' ' -f7 | xargs kill -9 
ps aux | grep -i qore-l - | cut -d' ' -f7 | xargs kill -9 
ps aux | grep -i qore-l - | cut -d' ' -f6 | xargs kill -9 
ps aux | grep -i qore-l - | cut -d' ' -f6 | xargs kill -9

investingTechnicals() {
	ppwd="`pwd`"
	cd /mldev/lib/crawlers/finance/dataPipeline.scrapy/
	scrapy crawl investingTechnical
	cd $ppwd
}

investingTechnicals
/mldev/bin/qlm.py ta
