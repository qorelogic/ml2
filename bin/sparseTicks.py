#!/usr/bin/env python

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
def sparseTicks2dim3(df, mdepth=200, verbose=False, returnList=False):
    
    import numpy as n
    import time
    from pandas import DataFrame as p_DataFrame
    
    dfn = df.get_values()
    #dir(dfn)
    #print df

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
    
    if returnList == True:
        return [dfm, df.index, df.columns]
    else:
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
def generateData(fname):

    import pandas as p
    from qoreliquid import StatWing, normalizeme, sigmoidme

    mdepth=1

    df = sparseTicks(num=10000)
    #for i in xrange(1):
    #    sparseTicks2dim3(df, mdepth=5)
    #print sparseTicks2dim3(df, mdepth=5)    

    
    """
    dim3 = sparseTicks2dim3(df, mdepth=1)    
    print len(dim3)
    for i in dim3:
        print p.DataFrame(i).transpose()
    """
    [dim3, indx, cols] = sparseTicks2dim3(df, mdepth=mdepth, returnList=True)
    print dim3.shape
    #print dim3
    #dim3 = dim3.reshape(dim3.shape[0], dim3.shape[2], dim3.shape[1])
    dim3 = dim3.reshape(dim3.shape[1], dim3.shape[0], dim3.shape[2])
    print dim3.shape
    #print dim3
    dfm = p.DataFrame(dim3[0], index=indx[mdepth:len(indx)], columns=cols)#.transpose()
    dfm = normalizeme(dfm)    
    dfm = sigmoidme(dfm)    
    sw = StatWing()
    #pairLabel = 'EUR_USD'
    pairLabel = 'USD_JPY'
    windowFrame = 10
    #dfm['label2'] = sw.nextBar(dfm, pairLabel, barsForward=3)
    #dfm['label'] = sw.higherNextDay(dfm, pairLabel)*1 + sw.lowerNextDay(dfm, pairLabel)*2
    dfm['label'] = sw.higherNextBars(dfm, pairLabel, barsForward=windowFrame)*1 + sw.lowerNextBars(dfm, pairLabel, barsForward=windowFrame)*-1    
    
    print dfm
    dfm.to_csv(fname)

class ML:
    
    def generateModel(self, fname):
    
        import h2o    
        
        label = 'label'
        h2o.init()
        
        fr1 = h2o.import_frame(fname)
        #fr1 = h2o.H2OFrame(f1)
        
        #self.splitFrame = fr1.split_frame([0.75])
        self.splitFrame = fr1.split_frame([0.60, 0.20])
        
        self.model = h2o.deeplearning(           x=self.splitFrame[0].drop(label),            y=self.splitFrame[0][label], 
                                      validation_x=self.splitFrame[1].drop(label), validation_y=self.splitFrame[1][label], 
                                            epochs=100,
                                            hidden=[100]*pow(2,4),
                                            activation='TanhWithDropout',
                                 )
        """
        self.model = h2o.gbm(           x=self.splitFrame[0].drop(label),            y=self.splitFrame[0][label], 
                             validation_x=self.splitFrame[1].drop(label), validation_y=self.splitFrame[1][label], 
                                   ntrees=1000, max_depth=100
                            )
        self.model = h2o.glm(           x=self.splitFrame[0].drop(label),            y=self.splitFrame[0][label], 
                             validation_x=self.splitFrame[1].drop(label), validation_y=self.splitFrame[1][label] 
                            )
        """
        print self.model
        #print self.model.model_performance(self.splitFrame[1])

        #print 
        #print 'Model Performance:'
        #print self.model.model_performance()
        
        print 
        print '========================================'
        print 'Model Performance on: TRAINING data::'
        print self.model.model_performance(self.splitFrame[0])
        print 
        print '========================================'
        print 'Model Performance on: VALIDATION data::'
        print self.model.model_performance(self.splitFrame[1])
        print 
        print '========================================'
        print 'Model Performance on: TEST data::'
        print self.model.model_performance(self.splitFrame[2])

    def predictFromModel(self):
        
        predict = self.model.predict(self.splitFrame[2])#.get_frame('C1')
        #print predict
        #print dir(predict)
        #print predict.show()
        
        print 
        #print 'Prediction Data Frame:'
        #print predict.as_data_frame()
        #print predict.split_frame()
    
        print 
        print 'Prediction Summary:'
        print predict.summary()
        #print predict.table()
        
        #import matplotlib.pylab as plt
        #plt.plot(predict.as_data_frame())
        #plt.show()
    
##########################
if __name__ == "__main__":

    import argparse
    # source: https://docs.python.org/2/howto/argparse.html
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', "--save", help="save to csv file", action="store_true")
    parser.add_argument('-t', "--train", help="train via h2o[deeplearning]", action="store_true")
    parser.add_argument('-t2', "--train2", help="train via ML class h2o[deeplearning]", action="store_true")
    parser.add_argument('-n', "--num", help="number of rows")
    args = parser.parse_args()
    
    from simulator import Simulator
    from oandaq import OandaQ
    import sys, pandas as p, numpy as n
    import matplotlib.pylab as plt
    from qoreliquid import normalizeme
    from qoreliquid import sigmoidme
    
    try:    num = int(args.num)
    except: num = 100
    
    if args.train:
        fname = '/tmp/ql.ticks.{0}.csv'.format(num)
    if args.train2:
        fname = '/tmp/sparseTicks-test-001.csv'
    
    # if std input is passed
    if not sys.stdin.isatty():
        pipeline()
    # if std input is not passed
    else:
        if args.save:
            df = sparseTicks(num=num)
            df = normalizeme(df)
            df = sigmoidme(df)
            print df
            df.to_csv(fname)
            print 'saved to {0}'.format(fname)
            #os.system("rsync -avrz /opt/data/filename root@ip:/opt/data/file")
            sys.exit()

        if args.train:
            print 'training'
            import h2o
            
            h2o.init()            
            
            fr1 = h2o.import_frame(fname); label = 'EUR_USD'
            #fr1 = h2o.H2OFrame(f1)
            print fr1
            
            #p1 = h2o.parse_setup(fr1)
            #print p1            
            #print p1['destination_frame']
            
            sp1 = fr1.split_frame([0.75])
            
            print sp1#[0]
            #sp1[0].drop(label)
            print sp1[0][label]
            #sp1[1].drop(label)
            print sp1[1][label]
            
            model = h2o.gbm(x=sp1[0].drop(label), y=sp1[0][label], validation_x=sp1[1].drop(label), validation_y=sp1[1][label], ntrees=10000, max_depth=100)
            print model            
            predict = model.predict(sp1[1])#.get_frame('C1')
            print model.model_performance(sp1[1])
            
            """
            model2 = h2o.deeplearning(x=sp1[0].drop(label), y=sp1[0][label], validation_x=sp1[1].drop(label), validation_y=sp1[1][label])
            #print model2
            predict = model2.predict(sp1[1])#.get_frame('C1')
            print model2.model_performance(sp1[1])
            """
            
            # show prediction and plot data
            print predict
            df = predict.as_data_frame()
            df = df.combine_first(sp1[1].as_data_frame())
            print df.ix[:, ['EUR_USD', 'predict']]
            df.ix[:, ['EUR_USD', 'predict']].plot()
            plt.show()
            
            sys.exit()

        if args.train2:
            #generateData(fname)
            
            ml = ML()
            ml.generateModel(fname)
            ml.predictFromModel()
            sys.exit()
            
        df = sparseTicks(num=num)
        print df
        #for i in xrange(1):
        #    sparseTicks2dim3(df, mdepth=5)
        #print sparseTicks2dim3(df, mdepth=5)
        sys.exit()
