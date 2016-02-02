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
def sparseTicks2dim3(df, mdepth=200, verbose=False):
    
    import numpy as n
    import time
    from pandas import DataFrame as p_DataFrame
    
    #n.set_printoptions(threshold=10)
    n.set_printoptions(suppress=False)
    n.set_printoptions(threshold=n.nan)
    
    dfn = df.get_values()#.T
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
            dfv = p_DataFrame(dfn[i:mdepth+i], index=df.ix[i:mdepth+i].index, columns=df.columns)
            dfv.ix['stdev', :] = n.std(dfn[i:mdepth+i], 0)
            print dfv
            #print
        #print p_DataFrame(dfn)
    
    # prep the dataframe indeces into a list
    dfi = []
    for i in xrange(midepth):
        #dfi.append(df.ix[i:mdepth+i].index)
        dfi.append(df.ix[i:mdepth+i].index)
        
    #print dfm
    #print 'shape dfn: {0}'.format(dfn.shape)
    #print 'shape dfm: {0}'.format(dfm.shape)

    #print dfm
    #print dfm#[0]
    #for i in range(10):
    #    print dfm[i]
#        print 
        #p_DataFrame(dfm[i]).plot(legend=False)
    
    return [dfm, dfi, df.columns]

#@profile
def pipeline():
    #fp = open(sys.stdin)
    fp = sys.stdin
    df = p.DataFrame()
    tail = 100
    r = tail; c = 4;
    
    ndf = n.zeros(r*c).reshape(r,c);
    #ndf = n.random.randn(r*c).reshape(r,c);
    dfi = n.zeros(r)
    #dfc = n.zeros(c)
    dfc = {}
    
    #p.set_option('max_colwidth',10)
    p.set_option('precision', 3)
    #p.set_eng_float_format(accuracy=3, use_eng_prefix=False)
    #p.set_eng_float_format(use_eng_prefix=False)
    
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
            ndf[r-1,dfc_keys.index(str(li[1]))] = li[2]
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
            df = p.DataFrame(ndf, index=dfi, columns=dfc_keys[0:c])#.transpose()
            
            df.ix['stdev', :] = n.std(ndf, 0)
            
            #df =  df.ix['stdev',:]
            print df
            #print df.get_values()
            
            #print ''
        except Exception as e:
            ''
            #print e

# source: http://stackoverflow.com/questions/24196932/how-can-i-get-the-ip-address-of-eth0-in-python
def getActiveIface():
    import os, re
    li = []
    f = os.popen('grep 0 /proc/net/dev')
    for i in f.read().strip().split('\n'):
        res = re.sub(re.compile(r'[\s]+'), ' ', i)
        res = res.strip().split(' ')
        iface = res[0].replace(':', '').strip()
        if int(res[1]) > 0 and iface != 'lo':
            li.append(res)
            return iface
    #print p.DataFrame(li)#.transpose()
iface1 = getActiveIface()
"""
def getipaddr():
    import socket, fcntl, struct
    def get_ip_address(ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15])
        )[20:24])
    return get_ip_address(iface1)  # '192.168.0.110'
"""
def getIpAddr():
    import socket
    def get_ip_address():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    return get_ip_address()
"""
def getipaddr():
    import os
    f = os.popen('ifconfig %s | grep "inet\ addr" | cut -d: -f2 | cut -d" " -f1' % iface1)
    return f.read()
"""
##################
##########################
if __name__ == "__main__":

    import argparse
    # source: https://docs.python.org/2/howto/argparse.html
    parser = argparse.ArgumentParser()
    
    # saving options
    parser.add_argument('-s', "--save", help="save to csv file", action="store_true")

    parser.add_argument('-l', "--label", help="label")
    
    # statistics options
    parser.add_argument('-d3', "--dim3", help="3 dimensional matrix", action="store_true")
    parser.add_argument("--stdev", help="standard deviation", action="store_true")
    parser.add_argument("--mdepth", help="The depth of the 3-dimensional matrix. How many ticks past should be considered to compute statistics.")

    # machine learning options
    parser.add_argument('-t', "--train", help="train via h2o[deeplearning]", action="store_true")
    
    # dataset size options
    parser.add_argument('-n', "--num", help="number of rows")
    
    # connection options
    parser.add_argument('-p', "--port", help="port number")
    args = parser.parse_args()
    
    from simulator import Simulator
    from oandaq import OandaQ
    import sys, pandas as p, numpy as n
    import matplotlib.pylab as plt
    from qoreliquid import normalizeme
    from qoreliquid import sigmoidme
    
    p.set_option('expand_frame_repr', False)
    # http://stackoverflow.com/questions/21137150/format-suppress-scientific-notation-from-python-pandas-aggregation-results
    # Format / Suppress Scientific Notation
    p.set_option('display.float_format', lambda x: '%2.10f' % x)

    try:    num = int(args.num)
    except: num = 100
    
    try:    label = args.label
    except: label = 'EUR_USD'
    if label == None: label = 'EUR_USD'
    
    # if std input is passed
    if not sys.stdin.isatty():
        pipeline()
    # if std input is not passed
    else:
        fname = '/tmp/ql.ticks.{0}.csv'.format(num)
        if args.save and not (args.dim3 or args.stdev):
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
            
            h2o.init(ip=getIpAddr(), port=54321)
            
            fr1 = h2o.import_frame(fname);
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

        df = sparseTicks(num=num)
        print 'label: %s' % label
        dfl = df.ix[:, label]

        if args.dim3 or args.stdev:
            if args.dim3:
                mode = 'dim3'
            if args.stdev:
                mode = 'stdev'
            try:    mdepth = int(args.mdepth)
            except: mdepth = 15
            #for i in xrange(1):
            #    sparseTicks2dim3(df, mdepth=mdepth)
            
            if args.stdev:
                d3 = sparseTicks2dim3(df, mdepth=mdepth, verbose=False)
                stdev = n.std(d3[0], 1)
                #print d3
                #print d3[1][0][len(d3[1][0])-1]
                indx = p.DataFrame(d3[1]).ix[:, len(d3[1][0])-1]
                df = p.DataFrame(stdev, index=indx.get_values(), columns=d3[2])
            else:
                d3 = sparseTicks2dim3(df, mdepth=mdepth, verbose=True)
                df = d3[0]
                
            df = normalizeme(df)
            df = sigmoidme(df)

            if args.save:
                fname = '/tmp/ql.ticks.%s.%s.csv' % (num, mode)
                df.to_csv(fname)
                print 'saved to {0}'.format(fname)
             
            print '----------df-------'
            with p.option_context('display.max_rows', 2000, 'display.max_columns', 500):
                print df
            #print df
            #df.plot()
            #plt.show()            
            sys.exit()

        print df
        sys.exit()
