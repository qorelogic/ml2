#!/usr/bin/env python

import os, time

import sys

def defp(pt):
    try:    sys.path.index(pt)
    except: sys.path.append(pt)

defp('/ml.dev/bin')
defp('/ml.dev/lib/oanda/oandapy')

from oandaq import OandaQ
#import pandas as p
import pymongo


# uncomment thr @profile line for profiling via kernprof 
#   as per source: http://www.huyng.com/posts/python-performance-analysis/
#@profile
def parseEquityLogs():
    
    # Connection to Mongo DB
    try:
        conn = pymongo.MongoClient(port=27017)
        #print "Connected successfully!!!"
    except pymongo.errors.ConnectionFailure, e:
        print "Could not connect to MongoDB: %s" % e 
        ''
    
    hdir = '/ml.dev/bin/data/oanda'
    
    db = conn.ql
    #db.equity.drop()  # use with CAUTION
    
    oq = OandaQ()
    header = oq.logEquity(daemon=False, csvSave=False, mongodbSave=False, onlyHeader=True)
    
    print 'inserting...'
    tlines = os.popen('wc -l  {0}/logs/* | grep -i total'.format(hdir)).read().strip().split(' ')[0]
    print tlines
    
    print header
    files = os.popen('ls {0}/logs/'.format(hdir)).read().split('\n')
    lnum = 1
    
    st = time.time()

    for file in files:
        
        l = ''
        for l in os.popen('cat {0}/logs/{1} 2> /dev/null'.format(hdir, file)).readlines():
            
            currt = time.time()
            #est = (currt - st) / lnum * int(tlines)
            
            # percentage complete
            pcnt   = (float(lnum) / int(tlines) * 100)
            
            #  [in seconds from start of run]
            endest = (currt - st) / pcnt * 100
            
            # ETA [in seconds]
            eta    = st + endest - currt
    
            li = l.split('\n')[0].split(',')
            #dc = p.DataFrame(li, index=header).to_dict()[0]
            # source: http://stackoverflow.com/questions/4576115/python-list-to-dictionary
            dc = dict(zip(header, li)) # 6.76X speedup over the above p.Dataframe method
            if lnum % 1000 == 0:
                #print '{0} of {1} [{2} {3} {4}]'.format(lnum, tlines, pcnt, endest, eta)
                #print str(lnum)+' of '+str(tlines)+' ['+str(pcnt)+' '+str(endest)+' '+str(eta)+']'
                print '%s of %s [%s %s %s]' % (lnum, tlines, pcnt, endest, eta)
                #print dc
            
            #try:
            db.equity.insert(dc)
            #except Exception as e:
            #print e
            
            lnum += 1
            
            # uncomment for kernprof
            #if lnum  > 1000: break
        #if lnum  > 1000: break
            
parseEquityLogs()
