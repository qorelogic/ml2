#!/usr/bin/env python 

import os, time
import datetime as dd

import sys

def defp(pt):
    try:    sys.path.index(pt)
    except: sys.path.append(pt)

defp('/ml.dev/bin')
defp('/ml.dev/lib/oanda/oandapy')

hdir = '/ml.dev/screenshots/developerLogs/screen/qore2/'

from pandas import DataFrame as pDataFrame

try:
    li = []
    for fname in os.popen('ls {0}'.format(hdir)).read().split('\n'):
        #print fname
        #os.popen('eog '+fname)
        ts = fname.split('-')[3].split('.')[0]
        mtime = dd.datetime.fromtimestamp(int(ts))
        #print mtime
        #print time.strptime('%Y', mtime)
        intt = mtime.strftime('%Y')
        #if int(intt) == 2015:
        li.append({     'fname'  : fname,\
                        'ts'     : ts, \
                        'mtime'  : mtime, \
                        'year'   : mtime.strftime('%Y'), \
                        'month'  : mtime.strftime('%m'), \
                        'day'    : mtime.strftime('%d'), \
                        'hour'   : mtime.strftime('%H'), \
                        'minute' : mtime.strftime('%M'), \
                        'second' : mtime.strftime('%S') \
                    })
        #print time.time()
        #break
except Exception as e:
	print e
	''
print pDataFrame(li).set_index('ts')
