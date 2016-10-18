#!/bin/bash

#. ./vdir000_2.7.6/bin/activate
. ~/virtualenv-tmp/vdir000_2.7.6/bin/activate

export PYTHONPATH="$PYTHONPATH:/ml.dev/lib/oanda/oandapy";
#echo $PYTHONPATH;
/mldev/bin/logEquity2.py 2>&1 >> /tmp/logEquity2.py.log

deactivate
