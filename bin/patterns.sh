#!/bin/bash

ppwd="`pwd`"

#python patterns.py -g 90 -v -acc 558788 -dp 5 -s
cd /mldev/bin
python patterns.py -a >> /tmp/patterns.log
cd $ppwd
