#!/bin/bash

# source: http://serverfault.com/questions/280558/need-with-crontab-and-gui-python-popup
export XAUTHORITY=/home/$USER/.Xauthority;
export DISPLAY=:0;
export USER=qore;

source /mldev/bin/virtualenv/vdir000_2.7.6/bin/activate

if [ "$1" == "" ]; then
	echo 'usage: <project name>'
else
	/mldev/bin/logDeveloper.py -p $1
fi

# alternatives:
# http://blog.bryanbibat.net/2011/10/03/take-periodic-screenshots-in-ubuntu-with-scrot-and-cron/
