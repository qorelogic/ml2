
import numpy as n
import pandas as p
import pymongo
from matplotlib import pyplot as plt
from pylab import rcParams
#rcParams['figure.figsize'] = 20, 5
import datetime as dd

##################
def normalizeme(dfr, pinv=False):
    
    nmean = n.mean(dfr, axis=0)
    nstd = n.std(dfr, axis=0)
    #nmean = n.mean(dfr)
    #nstd = n.std(dfr)
    dfr = (dfr - nmean) / nstd
    #dfr = n.divide((dfr - nmean), nstd)
    if pinv == False:
        return dfr
    else:
        return [dfr, nmean, nstd]

def sigmoidme(dfr):
    return 1.0 / (1 + pow(n.e,-dfr))

def oandaToTimestamp(ptime):
    
    def _oandaToTimestamp(ptime):
        dt = dd.datetime.strptime(ptime, '%Y-%m-%dT%H:%M:%S.%fZ')
        return (dt - dd.datetime(1970, 1, 1)).total_seconds() / dd.timedelta(seconds=1).total_seconds()
        
    try:
        tstmp = _oandaToTimestamp(ptime)
    except Exception as e:
        tstmp = []
        for i in ptime: tstmp.append(_oandaToTimestamp(i))                
    return tstmp
##########################

#@profile
def sparseTicks():
    # Connection to Mongo DB
    try:
        conn = pymongo.MongoClient(port=27017)
        print "Connected successfully!!!"
    except pymongo.errors.ConnectionFailure, e:
        print "Could not connect to MongoDB: %s" % e 
        ''
    ##############
    
    #@profile
    def _pe(db, dfi, num=100):
        df = p.DataFrame()
        for i in db.ticks.find(dfi)[0:num]:
            try: df = df.combine_first(p.DataFrame(i, index=[i['_id']]))
            except KeyError as e: ''
        return df
    
    #@profile
    def _pe2(db, dfi, num=100):
        lis = []
        #for i in db.ticks.find(dfi)[0:num]:
        ticks = db.ticks.find(dfi)
        #print dir(ticks)
        if num == 0: num = ticks.count()
        for i in ticks[0:num]:
            k = i.keys()
            v = i.values()
            lis.append(v)
        return p.DataFrame(lis, columns=k)

    # sparse ticks
    db = conn.ql
    dfi = {}
    num=500
    #df = _pe(db, dfi, , num=num)
    df = _pe2(db, dfi, num=num)

    df = df.drop_duplicates('time')
    df['ts'] = oandaToTimestamp(df['time'])
    df = df.pivot('ts', 'instrument', 'ask')
    df = df.bfill()
    df = df.ffill()
    df = df.convert_objects(convert_numeric=True)#.ix[:, 'AUD_CHF']
    df = normalizeme(df)
    df = sigmoidme(df)
    print df
    df.plot(legend=None); plt.show();
    #plt.plot(df); plt.show();
    
sparseTicks()