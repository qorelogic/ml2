#!/usr/bin/env python

from simulator import Simulator
from oandaq import OandaQ
import sys, pandas as p, numpy as n

def imports():
    import numpy as n
    import pandas as p
    import pymongo
    from matplotlib import pyplot as plt
    from pylab import rcParams
    #rcParams['figure.figsize'] = 20, 5
    import datetime as dd
    
    #import numpy as n
    #import pandas as p
    #import pymongo
    #from matplotlib import pyplot as plt
    #from pylab import rcParams
    ##rcParams['figure.figsize'] = 20, 5
    #from pylab import rcParams
    #rcParams['figure.figsize'] = 20, 5
    
    #import datetime as dd
    #import ujson as j
#imports()

##################
"""
def normalizeme(dfr, pinv=False):
    
    import numpy as n
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
    import numpy as n
    return 1.0 / (1 + pow(n.e,-dfr))

def _oandaToTimestamp(ptime):
    import datetime as dd
    dt = dd.datetime.strptime(ptime, '%Y-%m-%dT%H:%M:%S.%fZ')
    return (dt - dd.datetime(1970, 1, 1)).total_seconds() / dd.timedelta(seconds=1).total_seconds()

def oandaToTimestamp(ptime):
    
    try:
        tstmp = _oandaToTimestamp(ptime)
    except Exception as e:
        tstmp = []
        for i in ptime: tstmp.append(_oandaToTimestamp(i))                
    return tstmp

def timestampToDatetime(tst):
    import datetime as dd    
    def _timestampToDatetime(tst):
        return dd.datetime.fromtimestamp(tst)

    try:    ddt = _timestampToDatetime(tst)
    except Exception as e:
        print e
        ddt = []
        for i in tst: ddt.append(_timestampToDatetime(i))                
    return ddt
"""
##################

#@profile
def sparseTicks(num=2000):

    from matplotlib import pyplot as plt
    from pylab import rcParams
    from oandaq import OandaQ
    
    s = Simulator()
    df = s.getTicks(num=num)
    
    df = df.drop_duplicates('time')
    indexby = 'time'
    df['ts'] = OandaQ.oandaToTimestamp_S(df['time'])
    df = df.pivot(indexby, 'instrument', 'ask')
    #df['time'] = df.index
    df = df.bfill()
    df = df.ffill()
    df = df.convert_objects(convert_numeric=True)#.ix[:, 'AUD_CHF']
    
    #df = normalizeme(df)
    #df = sigmoidme(df)
    #print df
    #df.plot(legend=None); plt.show();
    #plt.plot(df); plt.show();

    return df

# convert sparse ticks dataframe to 3D matrix: 
#       the 3rd dimension composed of historical price of depth mdepth
#@profile
def sparseTicks2dim3(df, mdepth=200, verbose=False):
    
    import numpy as n
    import time
    from pandas import DataFrame as p_DataFrame
    
    dfn = df.get_values()
    #dir(dfn)

    dfnl = dfn.shape[0]-mdepth
    dfm = n.resize(n.zeros(dfnl * mdepth * dfn.shape[1]), (dfnl, mdepth, dfn.shape[1]))

    #print 'shape dfn: {0}'.format(dfn.shape)
    #print 'shape dfm: {0}'.format(dfm.shape)
    #print 'shape dfn: {0}'.format(dfn[0:200].shape)
    #print 'shape dfm: {0}'.format(dfm[0].shape)

    #print dfm[0,0]
    #print dfn#[0]
    #print dfm

    #print dfn[0:200]
    midepth = dfn.shape[0]-mdepth
    for i in xrange(midepth):
        dfm[i] = dfn[i:mdepth+i]
        
    if verbose == True:
        for i in xrange(midepth):
            #print dfn[i:mdepth+i]
            #print df.ix[i:mdepth+i]
            print p_DataFrame(dfn[i:mdepth+i], index=df.ix[i:mdepth+i].index, columns=df.columns)
            #print
        #print p_DataFrame(dfn)
        
    #print dfm
    #print 'shape dfn: {0}'.format(dfn.shape)
    #print 'shape dfm: {0}'.format(dfm.shape)

    #print dfm
    #print dfm#[0]
    #for i in range(10):
    #    print dfm[i]
#        print 
        #p_DataFrame(dfm[i]).plot(legend=False)
    
    return dfm

#@profile
def pipeline():
    #fp = open(sys.stdin)
    fp = sys.stdin
    df = p.DataFrame()
    tail = 5
    r = tail; c = 10;
    
    #ndf = n.zeros(r*c).reshape(r,c);
    ndf = n.random.randn(r*c).reshape(r,c);
    dfi = n.zeros(r)
    #dfc = n.zeros(c)
    dfc = {}
    
    while True:
        try:
            i = fp.readline()
            #print '---'
            #print i
            li = i.replace('"', '').replace('\n', '').split(',')
            #print li[0]
            ts = OandaQ.oandaToTimestamp_S(li[0])
            li.append(ts)
            #print li
            #print li[0]
            """
            #df.loc[str(li[4]), str(li[1])] = li[2]
            df.ix[str(li[4]), str(li[1])] = li[2]
            """
            dfi = n.append(dfi, [li[4]]); dfi = n.delete(dfi, [0])
            #dfc = n.append(dfc, [li[1]]); dfc = n.delete(dfc, [0])
            dfc[str(li[1])] = 0
            dfc_keys = dfc.keys()
            #ndf[str(li[4]), str(li[1])] = li[2]
            ndf = n.concatenate([n.concatenate(ndf[1:r,:]), ndf[r-1,:]]).reshape(r,c)
            #print '{0} {1} {2}'.format(ndf[4,dfc_keys.index(str(li[1]))], dfc_keys.index(str(li[1])), str(li[1]))
            ndf[4,dfc_keys.index(str(li[1]))] = li[2]
            #print '{0} {1} {2}'.format(ndf[4,dfc_keys.index(str(li[1]))], dfc_keys.index(str(li[1])), str(li[1]))
            """
            df = df.tail(tail)
            df = df.ffill()
            df = df.bfill()
            df = df.sort()
            """
            #print df.ix[:, [0,1,2,3,4,5]].get_values()
            #print df.ix[:, :]
            """
            print dfi
            print dfc_keys
            print ndf
            """
            #print '{0}:{1}'.format(li[1], li[2])
            print p.DataFrame(ndf, index=dfi, columns=dfc_keys[0:10])#.transpose()
            #print ''
        except Exception as e:
            ''
            #print e

##################
##########################

if __name__ == "__main__":

    # if std input is passed
    if not sys.stdin.isatty():
        pipeline()
    # if std input is not passed
    else:
        df = sparseTicks(num=1000)
        print df
        #for i in xrange(1):
        #    sparseTicks2dim3(df, mdepth=5)
        print sparseTicks2dim3(df, mdepth=5)
