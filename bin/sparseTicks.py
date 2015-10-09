
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
##################

def getTicks(num=2000):
    import pymongo
    #import pandas as p
    from pandas import DataFrame as p_DataFrame

    # Connection to Mongo DB
    try:
        conn = pymongo.MongoClient(port=27017)
        #print "Connected successfully!!!"
    except pymongo.errors.ConnectionFailure, e:
        print "Could not connect to MongoDB: %s" % e 
        ''
    ##############
    
    #@profile
    def _pe(db, dfi, num=100):
        df = p_DataFrame()
        for i in db.ticks.find(dfi)[0:num]:
            try: df = df.combine_first(p_DataFrame(i, index=[i['_id']]))
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
        return p_DataFrame(lis, columns=k)

    # sparse ticks
    db = conn.ql
    dfi = {}    
    
    #df = _pe(db, dfi, , num=num)
    df = _pe2(db, dfi, num=num)
    #print df
    return df
    
#@profile
def sparseTicks(num=2000):

    from matplotlib import pyplot as plt
    from pylab import rcParams
    
    df = getTicks(num=num)
    
    df = df.drop_duplicates('time')
    indexby = 'time'
    df['ts'] = oandaToTimestamp(df['time'])
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
def simulator(df=None, simulator=True, num=200):
    from pandas import DataFrame as p_DataFrame
    import time
    import numpy as n
    if type(df) == type(None):
        df = getTicks(num=num)
    dfn = df.get_values()
    if simulator == True:
        dff = p_DataFrame(dfn, index=df.index, columns=df.columns)
        #if dff.index.dtype == 'int64':
        #    dff = dff.set_index('time')
        #print dff.index.dtype
        #print type(dff.index.dtype)
        try:
            dff['ts'] = oandaToTimestamp(dff.index)
        except:
            dff['ts'] = oandaToTimestamp(dff['time'])
        dff['dts'] = timestampToDatetime(dff['ts'])        
        ts = dff.ix[10,'ts']
        cts = time.time()
        #print ts
        #print cts
        ndiff = cts - ts
        #print ndiff
        dff['tsnowts'] = dff['ts'] + ndiff        
        dff['tsnow'] = timestampToDatetime(dff['ts'] + ndiff)        
        for i in dff.get_values():
            while i[len(i)-2] >= time.time():
                time.sleep(0.001)
            v = n.array(list(i), dtype=str)
            csv = ','.join(v)
            k = list(dff.columns)
            res = dict(zip(k, v))
            #print res
            dfp = p_DataFrame(res, index=[0])
            if dff.index.dtype == 'int64':
                dfp = dfp.ix[:,['instrument', 'ask','bid', 'dts', 'time']]
            print dfp.transpose()[0].to_dict()

##################
##########################

df = sparseTicks(num=10000)
#for i in xrange(1):
#    sparseTicks2dim3(df, mdepth=5)
#sparseTicks2dim3(df, mdepth=5)
simulator(df=df, num=40)

#simulator(num=40)
