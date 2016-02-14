#!/usr/bin/env python

#./sparseTicks.py -n10000 --stdev -t -l EUR_USD -la la
#./sparseTicks.py -n500 --stdev -p -l EUR_USD -la la5b 
 
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
def sparseTicks(num=2000, verbose=True):

    from matplotlib import pyplot as plt
    from pylab import rcParams
    from oandaq import OandaQ
    
    s = Simulator()
    
    df = s.getTicks(num=num, verbose=verbose)
    
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

# preps df for h2o dict
def removeIndexFromDict(di):
    for i in di.keys(): di[i] = di[i].values()
    #print di
    return di

def getLastQlPklFilename(num=0, type='model'):
    #import os
    #print os.system("ls -t /tmp/ql*.pkl")
    import subprocess
    hdir = '/tmp/'
    cmd  = 'ls -t %s' % hdir
    #subprocess.check_output(['ls', '-t', '/tmp/ql*.pkl']).strip()
    res = subprocess.check_output(cmd.split(' ')).strip()
    import re
    li = []
    for i in res.split('\n'):
        if type == 'model':
            rx = r'.*ql.*pkl$'
        if type == 'dataset':
            rx = r'.*ql.*csv$'
        if re.match(re.compile(rx), i):
            fname = '%s%s' % (hdir, i)
            li.append(fname)
    print li[num]
    return li[num]
    #return '%s%s' % (hdir, li[num])

def parseFname(fnameModel):
    import re
    k = []
    v = []
    for i in fnameModel.split('.'):
        res = re.match(re.compile(r'(.*=.*)'), i)#.groups(0)
        try:
            #print dir(res)
            rs = res.group(0).split('=')
            k.append(rs[0])
            v.append(rs[1])
            #print i
        except:
            ''
    #print k
    #print v
    return dict(zip(k, v))

def debug(msg):
    if args.verbose: 
        return msg

import subprocess
def get_git_revision_hash():
    return subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip()
    
def get_git_revision_short_hash():
    return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).strip()

def hostname():
    fname = '/etc/hostname'
    fp    = open(fname)
    res   = fp.read().strip()
    fp.close()
    return res

#class ST:
def setupargs():
    import argparse
    # source: https://docs.python.org/2/howto/argparse.html
    parser = argparse.ArgumentParser()
    
    parser.add_argument('-f', "--file", help="dataset filename")

    # saving options
    parser.add_argument('-s', "--save", help="save to csv file", action="store_true")
    parser.add_argument('-v', "--verbose", help="verbose", action="store_true")
    parser.add_argument('-vv', "--verbose2", help="debugs", action="store_true")
    parser.add_argument('-df', "--printdfs", help="debugs", action="store_true")

    parser.add_argument('-l', "--label", help="label")
    parser.add_argument('-la', "--la", help="la")
    
    # statistics options
    parser.add_argument('-d3', "--dim3", help="3 dimensional matrix", action="store_true")
    parser.add_argument("--stdev", help="standard deviation", action="store_true")
    parser.add_argument("--mdepth", help="The depth of the 3-dimensional matrix. How many ticks past should be considered to compute statistics.")

    # machine learning options
    parser.add_argument('-t', "--train", help="train via h2o[deeplearning]", action="store_true")
    parser.add_argument('-p', "--predict", help="predict via h2o[deeplearning]", action="store_true")
    parser.add_argument('-vp', "--viewplots", help="show the plot after training/prediction", action="store_true")
    
    # dataset size options
    parser.add_argument('-n', "--num", help="number of rows")
    
    # connection options
    parser.add_argument("--port", help="port number")
    parser.add_argument("-ip", "--h2o_ip", help="h2o ip address")

    args = parser.parse_args()
    
    return args


def importDataset():
    print 'Dataset import..'
    
    fr1 = h2o.import_frame(fname);
    #fr1 = h2o.H2OFrame(f1)
    if args.printdfs: print fr1
    
    #p1 = h2o.parse_setup(fr1)
    #print p1            
    #print p1['destination_frame']
    
    sp1 = fr1.split_frame([0.75])
    
    #print sp1#[0]
    #sp1[0].drop(label)
    if args.printdfs: print sp1[0][label].as_data_frame()
    #sp1[1].drop(label)
    if args.printdfs: print sp1[1][label].as_data_frame()
        
    return sp1

##################
##########################
if __name__ == "__main__":

    args = setupargs()
        
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
    #p.set_option('display.precision', 2)    
    p.set_option('display.width', p.util.terminal.get_terminal_size()[0])
    p.set_option('max_colwidth', 800)

    if args.verbose:  verbose = (args.verbose)
    try:    verbose
    except: verbose = False

    if args.dim3:   mode = 'dim3'
    if args.stdev:  mode = 'stdev'
    try:    mode
    except: mode = 'stdev'
    
    try:    h2o_ip = (args.h2o_ip)
    except: h2o_ip = None
    if h2o_ip == None:
        try:
            h2o_ip = getIpAddr()
        except Exception as e:
            h2o_ip = '127.0.0.1'

    try:    num = int(args.num)
    except: num = 100
    
    try:    label = args.label
    except: label = None
    if label == None: label = 'EUR_USD'
    
    try:    la = args.la
    except: la = None
    if la == None: la = 'la'
    
    try:    fname = args.file
    except Exception as e:
        fname = None
    if fname == None:
        current_hash = get_git_revision_hash()
        #fname = '/tmp/ql.ticks.%s.%s.%s.%s.csv' % (num, mode, label, current_hash)
        fname = '/tmp/ql.ticks.num=%s.mode=%s.githash=%s.la=%s.hostname=%s.csv' % (num, mode, current_hash, label, hostname())
    
    # if std input is passed
    if not sys.stdin.isatty():
        pipeline()
    # if std input is not passed
    else:
        if args.save and not (args.dim3 or args.stdev):
            df = sparseTicks(num=num, verbose=verbose)
            df = normalizeme(df)
            df = sigmoidme(df)
            if args.printdfs: print df
            print 'saving to {0} ..'.format(fname)
            df.to_csv(fname)
            print 'saved.'
            #os.system("rsync -avrz /opt/data/filename root@ip:/opt/data/file")
            sys.exit()

        import h2o
        import pickle
        
        # there are two types of labels: 
        #  - reading label: this copies the labeled row (eg. EUR_USD) to the 'la' column before 
        #                   applying the prefilters (normalization filter / sigmoid filter, and so on..)
        #  - training/predicting label: this label sets the y vector label to the defined label prefiltered state.
        if not args.save:
            label = la
        
        if args.train or args.predict:
            h2o.init(ip=h2o_ip, port=54321)
            
        if args.train:# or args.predict:
                
            sp1 = importDataset()

        if args.train:

            print 'Training..'

            """
            model = h2o.gbm(x=sp1[0].drop(label), y=sp1[0][label], validation_x=sp1[1].drop(label), validation_y=sp1[1][label], ntrees=10000, max_depth=100)
            print model            
            predict = model.predict(sp1[1])#.get_frame('C1')
            print model.model_performance(sp1[1])
            """
            
            model2 = h2o.deeplearning(x           =sp1[0].drop(label), 
                                      y           =sp1[0][label], 
                                      validation_x=sp1[1].drop(label), 
                                      validation_y=sp1[1][label],
                                      hidden       = [100,100,100],
                                      epochs       = 10,
                                      #variable_importances = True,
                                      #balance_classes      = True,
                                      #loss                 = "Automatic",
                                      )
            """
            model2 = h2o.deeplearning(x           =fr1.drop(label), 
                                      y           =fr1[label], 
                                      validation_x=fr1.drop(label), 
                                      validation_y=fr1[label])
            """
            
            # save model object to pickle file
            startTime = model2._model_json['output']['start_time']
            endTime   = model2._model_json['output']['end_time']
            # features in X
            #print model._model_json['output']['names']
            fnameModel = '%s.label=%s.starttime=%s.endtime=%s.model.h2o.pkl' % (fname, label, startTime, endTime)
            s = pickle.dumps(model2)            
            fp = open(fnameModel, 'w')
            fp.write(s)
            fp.close()            
            model2 = pickle.loads(s)
            print 'saved model to %s' % (fnameModel)

            # insert model to db.models
            try:
                import pymongo as mong
                mongo = mong.MongoClient()
                parsedFname = parseFname(fnameModel)
                parsedFname['pickle'] = s
                mongo.ql.models.insert(parsedFname)
                mongo.close()
                print 'inserted model to db.models'
            except:
                ''
            
            #print model2
            predict = model2.predict(sp1[1])#.get_frame('C1')
            print model2.model_performance(sp1[1])
            #predict = model2.predict(fr1)#.get_frame('C1')
            #print model2.model_performance(fr1)
            
            # show prediction and plot data
            #print predict
            df = predict.as_data_frame()
            #df = df.combine_first(sp1[0].as_data_frame())
            df = df.combine_first(sp1[1].as_data_frame())
            #df = df.combine_first(fr1.as_data_frame())
            #if args.printdfs: print df.ix[:, [label, 'predict']]

            # print correlation coeficient
            a = df[label].get_values()
            b = df['predict'].get_values()
            print 'correlation coefficient: %s' % n.corrcoef(a, b)[0][1]
            #if args.printdfs: dfp

            if args.viewplots:
                df.ix[:, [label, 'predict']].plot()
                plt.show()
            
            sys.exit()

        if args.predict:
            #fname = "/tmp/ql.ticks.10000.stdev.987674089fe7815fb7872325d179127957df4209.csv"
            #fname = "/tmp/ql.ticks.1000.stdev.f9fd45fc4da82b8bf1064a5f9a15dff1fe038c1f.la=EUR_USD.muurl.csv"
            fname = getLastQlPklFilename(num=0, type='dataset')
            
            #fnameModel = '/tmp/ql.ticks.10000.stdev.987674089fe7815fb7872325d179127957df4209.csv.model.h2o.pkl'
            #fnameModel = '/tmp/ql.ticks.1000.stdev.f9fd45fc4da82b8bf1064a5f9a15dff1fe038c1f.la=EUR_USD.muurl.csv.model.h2o.pkl'
            #fnameModel = '/tmp/ql.ticks.10000.stdev.f9fd45fc4da82b8bf1064a5f9a15dff1fe038c1f.la=EUR_USD.muurl.csv.label=la.model.h2o.pkl'
            fnameModel = getLastQlPklFilename(num=0, type='model')
            
            fp = open(fnameModel)
            #print fp.read()
            model = pickle.loads(fp.read())
            fp.close()
            #print model
            
            #####
            #####
            
            #data_test = h2o.import_frame(fname)
            #data_test = h2o.H2OFrame([fname])
            #data_path = [h2o.locate(fname)]
            #data_test = h2o.H2OFrame([data_test])
            
            #####
            #####
            
            cnt = 5000
            df = p.read_csv(fname)
            df = df.ix[df.tail(cnt).index,:]
            df = df.set_index('Unnamed: 0')
            print df.columns
            #print 'dataframe df:'
            #print df
            examples = df.to_dict()
            #print 'examples:'
            #print examples
            #print fixdict(examples)
            #print 'dataframe examples:'
            #print p.DataFrame(examples)
            #fr1 = h2o.H2OFrame(python_obj = examples)
            #fr1 = h2o.H2OFrame(examples)
            fr1 = h2o.H2OFrame(removeIndexFromDict(examples))
            
            #####
            #####
            
            #label = 'la1b'
            #label = 'EUR_USD'
            modelParams = parseFname(fnameModel)
            label = modelParams['label']
            model_pred = model.predict(fr1.drop(label))
            print model_pred
            #print dir(model_pred)
            dfp = model_pred.as_data_frame()
            #print 'fr1 as dataframe:'
            fr1df = fr1.as_data_frame().ix[:, [label]]
            #print fr1df
            dfp = dfp.combine_first(fr1df)
            
            # print correlation coeficient
            a = dfp[label].get_values()
            b = dfp['predict'].get_values()
            print 'correlation coefficient: %s' % n.corrcoef(a, b)[0][1]
            #print dfp

            dfp.plot()
            plt.show()
            
            sys.exit()
        
        """
        if args.predict2:
            # read model object from pickle file
            #fnameModel = '%s.label=%s.model.h2o.pkl' % (fname, label)
            fnameModel = getLastQlPklFilename()
            fp = open(fnameModel, 'r')
            s = fp.read()
            fp.close()            
            model2 = pickle.loads(s)
            print 'model read from %s' % (fnameModel)
            
            #print model2
            
            sp1 = p.read_csv(fname)
            " ""
            sp1 = list(sp1.get_values())
            fr1 = h2o.H2OFrame(sp1[0])
            " ""
            
            predict = model2.predict(sp1[1])#.get_frame('C1')
            print model2.model_performance(sp1[1])
            print model2.confusion_matrix()
            
            # show prediction and plot data
            #print predict
            df = predict.as_data_frame()
            #df = df.combine_first(sp1[0].as_data_frame())
            df = df.combine_first(sp1[1].as_data_frame())
            if args.printdfs: print df.ix[:, [label, 'predict']]
            if args.viewplots:
                df.ix[:, [label, 'predict']].plot()
                plt.show()
            
            sys.exit()
        """

        df = sparseTicks(num=num, verbose=verbose)
        print 'label: %s' % label
        try:
            dfl = df.ix[:, label]
        except KeyError as e:
            print
            print '%s not found in the upstream:' % e
            print ' - this may be caused by receiving too few ticks:-'
            print '   - %s had not changed within the given window' % e
            print ' - increasing the -n/--num option to %s may solve this.' % (num*10)
            print
            sys.exit()

        if args.dim3 or args.stdev:
            try:    mdepth = int(args.mdepth)
            except: mdepth = 15
            #for i in xrange(1):
            #    sparseTicks2dim3(df, mdepth=mdepth)
            
            if args.stdev:
                d3 = sparseTicks2dim3(df, mdepth=mdepth, verbose=False)
                stdev = n.std(d3[0], 1)
                #if args.printdfs: print d3
                #if args.printdfs: print d3[1][0][len(d3[1][0])-1]
                indx = p.DataFrame(d3[1]).ix[:, len(d3[1][0])-1]
                df = p.DataFrame(stdev, index=indx.get_values(), columns=d3[2])
            else:
                d3 = sparseTicks2dim3(df, mdepth=mdepth, verbose=True)
                df = d3[0]
                
            df = normalizeme(df)
            df = sigmoidme(df)
            
            currencyColumns = df.columns
            
            # labels
            #from qoreliquid import StatWing
            #sw = StatWing()
            #sw.
            df['ts0'] = OandaQ.oandaToTimestamp_S(df.index)
            df['ts1'] = n.int32(OandaQ.oandaToTimestamp_S(df.index))
            #df['ts2'] = n.array(n.int32(OandaQ.oandaToTimestamp_S(df.index)) % 2 == 0, dtype=int)
            
            dfl0 = p.DataFrame()
            dfl0['ts1'] = df['ts1']
            dfl0['ts0'] = df['ts0']
            # la
            dfl0['la'] = dfl
            
            #dfl0['tss'] = dfl0.index
            #dfl0 = dfl0.set_index('ts1')
            #for i in [1,2,3,5,8,13,21,34,55,89,144]:
            for i in [1,2,3,5,10,15,30,60,240,1440]:
                dfl0['ts+%s' % i] = dfl0['ts1'] + i
                #dfl0['la+%s' % i] = dfl0.ix[dfl0['ts+%s' % i][0],:]
                #dfl0.ix['la+%s' % i] =
                id1 = dfl0.ix[:, 'ts+%s' % i][0]
                try:
                    dfl0.ix[id1,:]
                except Exception as e:
                    ''

                #print len(dfl0['la+%s' % i])
                #print len(dfl0['ts+%s' % i])
            
            #print dfl0.groupby(['ts1'])
            #if args.printdfs: print dfl0
            #dfl0.to_csv()
            #dfl0.to_csv('/tmp/dfl0.csv')
            
            # http://stackoverflow.com/questions/15707746/python-how-can-i-get-rows-which-have-the-max-value-of-the-group-to-which-they
            # timestamps for each period
            for i in [1,2,3,5,10,15,30,60,240,1440]:
                dfl0['ts%s' % i] =  dfl0.ix[dfl0.ix[:, 'ts1'] % i == 0, 'ts1']
            dfl0 = dfl0.ffill()
            
            df_by_second = dfl0.groupby('ts1').apply(lambda t: t[t.ts0==t.ts0.max()])
            df_by_second['la1'] = df_by_second['la']
            df_by_second['tsi'] = df_by_second.index
            df_by_second = df_by_second.set_index('ts1')
            
            df_by_2second = dfl0.groupby('ts2').apply(lambda t: t[t.ts0==t.ts0.max()])
            df_by_2second['la2'] = df_by_2second['la']
            df_by_2second['tsi'] = df_by_2second.index
            df_by_2second = df_by_2second.set_index('ts1')

            df_by_5second = dfl0.groupby('ts5').apply(lambda t: t[t.ts0==t.ts0.max()])
            df_by_5second['la5'] = df_by_5second['la']
            df_by_5second['tsi'] = df_by_5second.index
            df_by_5second = df_by_5second.set_index('ts1')
            
            #if args.printdfs: print df_by_second.ix[df_by_second.ix[:,'ts+1'], 'la']
            #if args.printdfs: print df_by_second.ix[[1442932286, 1442932287, 1442933724], 'la']
            df_by_second['ts1'] = df_by_second.index
            #df_by_second = df_by_second.set_index('ts1')
            
            #if args.printdfs: print df_by_second#.set_index('ts0')
            
            if args.printdfs: 
                print '----------dfl0-------'
                print dfl0.ix[dfl0.ix[:, 'ts+%s' % 1].index[0:10],:]
                print dfl0.ix[dfl0.ix[:, 'ts+%s' % 1].index,:]

            dfl0 = dfl0.set_index('ts1')
            if args.printdfs: 
                print '----------dfl0-------'
                print dfl0.index
                print dfl0
            df['label1'] = dfl
            df['tsi'] = df.index
            df = df.set_index('ts0')
            df.to_csv('/tmp/df.csv')
            df_by_second.to_csv('/tmp/df_by_second.csv')
            
            if args.printdfs: 
                print '----------df_by_second-------'
                print df_by_second.index
                print df_by_second
            
            if args.printdfs: 
                print '----------df-------'
                print df.index
                print df
            
            if args.printdfs: 
                print '----------label+1-------'
            df['label+1'] = df_by_second.ix[list(df_by_second.ix[:,'ts+1']), 'la']#.get_values()
            
            # http://pandas.pydata.org/pandas-docs/stable/merging.html
            df = p.concat([df, df_by_second, df_by_2second, df_by_5second], join='outer').sort()
            df = df.ffill().bfill().fillna(0)
            #df['la>label1'] = n.array(df['la'] > df['label1'], dtype=int)
            df['la1b']      = n.array(df['la1'] > df['label1'], dtype=int)
            df['la2b']      = n.array(df['la2'] > df['label1'], dtype=int)
            df['la5b']      = n.array(df['la5'] > df['label1'], dtype=int)            
            
            labels = ['la', 'la1', 'la1b', 'la2', 'la2b', 'la5', 'la5b', 'label1']
            #n.array(p.concat([p.DataFrame(currencyColumns), p.DataFrame(labels)], axis=0).transpose(), dtype=int).tolist()[0]
            Xy = n.concatenate([currencyColumns, labels]).tolist()

            if args.save:
                print 'saving to {0} ..'.format(fname)
                df.ix[:, Xy].to_csv(fname)
                print 'saved.'
                try:
                    if h2o_ip != getIpAddr():
                        import os
                        print 'Deploying dataset to h2o cluster @ %s' % h2o_ip
                        print os.system("rsync -avz %s root@%s:%s" % (fname, h2o_ip, fname))
                except:
                    ''
             
            if args.printdfs: 
                print '----------df-------'
            with p.option_context('display.max_rows', 2000, 'display.max_columns', 2000):
                #if args.printdfs: print df.ix[:, labels]
                #if args.printdfs: print df.ix[:, Xy].tail(10)
                if args.printdfs: debug(df)
                
            #if args.printdfs: print df
            #if args.viewplots:
            #    df.plot()
            #    plt.show()            
            
            if not args.predict:
                sys.exit()

        if args.predict:
                
            #fname = "/tmp/ql.ticks.10000.stdev.987674089fe7815fb7872325d179127957df4209.csv"
            #fname = "/tmp/ql.ticks.1000.stdev.f9fd45fc4da82b8bf1064a5f9a15dff1fe038c1f.la=EUR_USD.muurl.csv"
            fname = getLastQlPklFilename(num=0, type='dataset')
            
            #fnameModel = '/tmp/ql.ticks.10000.stdev.987674089fe7815fb7872325d179127957df4209.csv.model.h2o.pkl'
            #fnameModel = '/tmp/ql.ticks.1000.stdev.f9fd45fc4da82b8bf1064a5f9a15dff1fe038c1f.la=EUR_USD.muurl.csv.model.h2o.pkl'
            #fnameModel = '/tmp/ql.ticks.10000.stdev.f9fd45fc4da82b8bf1064a5f9a15dff1fe038c1f.la=EUR_USD.muurl.csv.label=la.model.h2o.pkl'
            fnameModel = getLastQlPklFilename(num=0, type='model')
            
            fp = open(fnameModel)
            #print fp.read()
            model = pickle.loads(fp.read())
            fp.close()
            #print model
            
            #####
            #####
            
            #data_test = h2o.import_frame(fname)
            #data_test = h2o.H2OFrame([fname])
            #data_path = [h2o.locate(fname)]
            #data_test = h2o.H2OFrame([data_test])
            
            #####
            #####
            
            msg = '(p)redict, (pp)lot, (q)uit: '
            ans = raw_input(msg)
            while ans != 'q':
                
                if ans == 'p':
                    
                    """
                    df = p.read_csv(fname)
                    df = df.ix[df.tail(num).index,:]
                    df = df.set_index('Unnamed: 0')
                    """
                    df = sparseTicks(num=num, verbose=verbose)
                    if args.printdfs: print df
                    try:    dfl = df.ix[:, label]
                    except: ''
                    df = normalizeme(df)
                    df = sigmoidme(df)                    
                    try:    df['la'] = dfl
                    except: ''
                    
                    print df.columns
                    print 'dataframe df:'
                    if args.printdfs: print df
                    examples = df.to_dict()
                    #print 'examples:'
                    #print examples
                    #print fixdict(examples)
                    #print 'dataframe examples:'
                    #print p.DataFrame(examples)
                    #fr1 = h2o.H2OFrame(python_obj = examples)
                    #fr1 = h2o.H2OFrame(examples)
                    fr1 = h2o.H2OFrame(removeIndexFromDict(examples))
                    
                    #####
                    #####
                    
                    #label = 'la1b'
                    #label = 'EUR_USD'
                    modelParams = parseFname(fnameModel)
                    label = modelParams['label']
                    model_pred = model.predict(fr1.drop(label))
                    print model_pred
                    #print dir(model_pred)
                    dfp = model_pred.as_data_frame()
                    #if args.printdfs: print 'fr1 as dataframe:'
                    fr1df = fr1.as_data_frame().ix[:, [label]]
                    #if args.printdfs: print fr1df
                    dfp = dfp.combine_first(fr1df)
                    
                    # print correlation coeficient
                    a = dfp[label].get_values()
                    b = dfp['predict'].get_values()
                    corrs = n.corrcoef(a, b)
                    if args.printdfs: print dfp
                    print corrs
                    print 'correlation coefficient: %s' % corrs[0][1]
        
                if ans == 'pp':
                    if args.viewplots:
                        dfp.plot()
                        plt.show()

                ans = raw_input(msg)            
            
            sys.exit()

        if args.printdfs: print df
        sys.exit()
