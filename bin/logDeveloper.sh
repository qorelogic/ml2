#!/bin/bash

# source: http://serverfault.com/questions/280558/need-with-crontab-and-gui-python-popup
export XAUTHORITY=/home/$USER/.Xauthority;
export DISPLAY=:0;
export USER=qore2;

/mldev/bin/logDeveloper.py

# alternatives:
# http://blog.bryanbibat.net/2011/10/03/take-periodic-screenshots-in-ubuntu-with-scrot-and-cron/
