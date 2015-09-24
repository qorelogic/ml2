#!/usr/bin/env python

import os, time

import sys

def defp(pt):
    try:    sys.path.index(pt)
    except: sys.path.append(pt)

defp('/ml.dev/bin')
defp('/ml.dev/lib/oanda/oandapy')

from oandaq import OandaQ
import pandas as p
import pymongo

# Connection to Mongo DB
try:
    conn = pymongo.MongoClient(port=27017)
    #print "Connected successfully!!!"
except pymongo.errors.ConnectionFailure, e:
    print "Could not connect to MongoDB: %s" % e 
    ''

db = conn.ql
#db.equity.drop()  # use with CAUTION

oq = OandaQ()
header = oq.logEquity(daemon=False, csvSave=False, mongodbSave=False, onlyHeader=True)

print 'inserting...'
tlines = os.popen('wc -l  logs/* | grep -i total').read().strip().split(' ')[0]
print tlines

print header
files = os.popen('ls logs/').read().split('\n')
lnum = 1

st = time.time()

for file in files:
    
    l = ''
    for l in os.popen('cat logs/'+file).readlines():
        
        currt = time.time()
        #est = (currt - st) / lnum * int(tlines)
        pcnt       = (float(lnum) / int(tlines) * 100)
        endest     = (currt - st) / pcnt * 100
        secsremain = st + endest - currt

        li = l.split('\n')[0].split(',')
        print '{0} of {1} [{2} {3} {4}]'.format(lnum, tlines, pcnt, endest, secsremain)
        dc = p.DataFrame(li, index=header).to_dict()[0]
        #print dc        
        db.equity.insert(dc)
        lnum += 1
        #time.sleep(0.01)
        #break
    #break
