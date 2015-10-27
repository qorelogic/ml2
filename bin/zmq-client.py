
import zmq, time, sys

# option to change the port number from default 5555
try:
    port = sys.argv[1]
except:
    port = 5555    

ctx = zmq.Context()
#socket = ctx.socket(zmq.REQ)
socket = ctx.socket(zmq.SUB)
socket.connect('tcp://localhost:{0}'.format(port))


# Subscribe to tester
topicfilter = 'tester'
#socket.subscribe(topicfilter) # only for SUB
socket.setsockopt(zmq.SUBSCRIBE, topicfilter)

from pandas import DataFrame as p_DataFrame
from numpy import array as n_array
import numpy as n
#df = p_DataFrame()

from collections import deque

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



def currencyMatrix(pairs, df=None, mode=None, mong=None, depth=None):
    #from oandaq import OandaQ
    #oq = OandaQ()
    #pairs = ",".join(list(n.array(p_DataFrame(oq.oandaConnection().get_instruments(oq.aid)['instruments']).ix[:,'instrument'].get_values(), dtype=str)))
    
    if mode == 'avg':
        df = p_DataFrame(mong['avgs'])
        #print df
        for i in df.columns:
            #print df[i]
            #a = list(n.array(df[i], dtype=float))
            #a = filter(lambda x: x != 0, a)
            #print a
            #a = normalizeme(a)
            #a = sigmoidme(a)
            #a = n.divide(1, a) # only for USD as base currency
            #print a
            #b = a#[1,2,3]
            #df.ix[len(df)-len(b):len(df)-1, i] = b
            #df[i] = normalizeme(n.array(df[i], dtype=float))
            #df[i] = sigmoidme(n.array(df[i], dtype=float))
            ''
        """
        df = p_DataFrame()
        for i in avgs:
            #print i
            #print avgs[i]
            df[i] = [avgs[i]]
            print df[i]
            #df[i] = normalizeme(n.array(df[i], dtype=float))
            #df[i] = sigmoidme(n.array(df[i], dtype=float))
        """
        #print df  
        #print depth
        try:
            df=df.ix[depth-1, :]
        except:
            df=df.ix[depth-2, :]
    
    ps = []
    for i in pairs:#.split(','):
        pr = i.split('_')
        ps.append(pr[0])
        ps.append(pr[1])
    currs = list(p_DataFrame(ps).drop_duplicates().transpose().get_values()[0])
    lcurrs = len(currs)
    lc = n.zeros(lcurrs*lcurrs).reshape(lcurrs, lcurrs)
    di = df.to_dict()
    kdi = di.keys()
    vdi = di.values()
    dfm = p_DataFrame(lc, index=currs, columns=currs)
    for i in kdi:
        isp = i.split('_')
        #print vdi
        #print '{0} {1} {2}'.format(di[i], i, isp)
        dfm.ix[isp[1], isp[0]] = di[i]
    
    try: dfm.ix['total', 'AUD CAD NZD CHF EUR GBP USD'.split(' ')] = n.sum(dfm.ix[:, 'AUD CAD NZD CHF EUR GBP USD'.split(' ')])
    except: ''
    try:
        dfm = dfm.convert_objects(convert_numeric=True)
        dfu = dfm.ix[:, 'EUR USD'.split(' ')]
        #print dfu[(dfu.values) > 0]
        print dfu
        #print dfm.ix[:, 'AUD CAD NZD CHF EUR GBP USD'.split(' ')]
        #print dfm[(dfm.values < 5)] #.any(1)
        #print dfm[(dfm.values < 1.5).any(1)].ix[:, 'AUD CAD NZD CHF EUR GBP USD'.split(' ')]
        #print dfm.ix[:,(dfm.ix[:, 'AUD CAD NZD CHF EUR GBP USD'.split(' ')] < 10)]
    except:
        ''
    #print n.sum(dfm.ix[:, 'AUD CAD NZD CHF EUR GBP USD'.split(' ')])
    #print dfm.ix[:, ['USD']]
    dfu = dfm.ix[['USD'], :].transpose()
    dfu = dfu.convert_objects(convert_numeric=True)
    #print dfu
    #print (dfu['USD'] != int(0))

#@profile
def client(mode='avg'):
    de = deque()
    #bids = deque()
    pairs = {}
    bids = {}
    asks = {}
    avgs = {}
    spreads = {}
    from pandas import read_csv as p_read_csv
    instruments = p_read_csv('data/oanda/cache/instruments.csv').set_index('instrument')

    depth = 20
    c = 0
    while True:
        #socket.send('test client') # only for REQ
        data = socket.recv(0)
        data = data.split(' ')[1]
        data = data.split(',')
        #print data
        ts = str(data[4][0:10])+str(data[3][19:26])
        #de.append(ts)
        
        pair = data[0]
        # append data into pairs
        def _uwe(name, pairs, pair, data):
            try:
                pairs[pair]['bids'].append(data[1])
            except:
                try:
                    pairs[pair]['bids'] = deque()
                    pairs[pair]['bids'].append(data[1])
                except:
                    pairs[pair] = {}
                    pairs[pair]['bids'] = deque()
                    pairs[pair]['bids'].append(data[1])
            return pairs
            
        pairs = _uwe('bids', pairs, pair, data)
        pairs = _uwe('asks', pairs, pair, data)
        pairs = _uwe('avgs', pairs, pair, data)
        pairs = _uwe('spreads', pairs, pair, data)
        
        mong = {'bids':bids, 'asks':asks, 'avgs':avgs, 'spreads':spreads}
        ########
        # bids
        try:
            bids[pair].append(data[1])
        except:
            bids[pair] = deque([0]*depth)
            bids[pair].append(data[1])                
        
        if len(pairs[pair]['bids']) >= depth: pairs[pair]['bids'].popleft()
        #df = normalizeme(n.array(pairs[pair]['bids'], dtype=float))
        #df = sigmoidme(n.array(bids, dtype=float))

        if len(bids[pair]) >= depth: bids[pair].popleft()
        #df = normalizeme(n.array(bids[pair], dtype=float))
        #df = sigmoidme(n.array(bids, dtype=float))
        
        #print pair
        #print list(df)
        #print pairs.keys()
        df = p_DataFrame(bids)
        for i in df.columns:
            df[i] = normalizeme(n.array(df[i], dtype=float))
            df[i] = sigmoidme(n.array(df[i], dtype=float))
        #df = normalizeme(n.array(df, dtype=float))
        #df[]
        #print df.ix[depth-1, :]#.bfill().ffill()#.transpose()
        #print 'plot'
        
        #print list(df.ix[depth-1, :].index)
        #currencyMatrix(list(df.ix[depth-1, :].index), df=df.ix[depth-1, :])
        ########
        # asks
        try:
            asks[pair].append(data[1])
        except:
            asks[pair] = deque([0]*depth)
            asks[pair].append(data[1])
        
        if len(asks[pair]) >= depth: asks[pair].popleft()
        df = p_DataFrame(asks)
        #for i in df.columns:
        #    df[i] = normalizeme(n.array(df[i], dtype=float))
        #    df[i] = sigmoidme(n.array(df[i], dtype=float))
        #currencyMatrix(list(df.ix[depth-1, :].index), df=df.ix[depth-1, :])
        ########
        # avgs
        try:
            avg = abs(float(data[1]) - float(data[2])) / instruments.ix[pair, 'pip']
        except:
            continue
        try:
            avgs[pair].append(avg)
        except:
            avgs[pair] = deque()
            avgs[pair] = deque([0]*depth)
            avgs[pair].append(avg)
        
        if len(avgs[pair]) >= depth: avgs[pair].popleft()

        if mode == 'avg':
            #try:
            #currencyMatrix(list(df.ix[depth-1, :].index), mode=mode, mong=mong, depth=depth)
            #except:
            print avgs
        ########
        # spreads
        spread = abs(float(data[1]) - float(data[2])) / instruments.ix[pair, 'pip']
        try:
            spreads[pair].append(spread)
        except:
            spreads[pair] = deque([0]*depth)
            spreads[pair].append(spread)
        
        if len(spreads[pair]) >= depth: spreads[pair].popleft()
        df = p_DataFrame(spreads)
        #for i in df.columns:
        #    df[i] = normalizeme(n.array(df[i], dtype=float))
        #    df[i] = sigmoidme(n.array(df[i], dtype=float))
        if mode == 'spread':
            currencyMatrix(list(df.ix[depth-1, :].index), df=df.ix[depth-1, :])
        ########
        
        #print de
        #print list(de)
        de.append(data)
        if len(de) >= depth: de.popleft()

        """
        #df = n_array(list(de))
        #print pivot(df, )
        df = p_DataFrame(list(de))
        
        #df = df.pivot(4, 3, 2)#.bfill().ffill()
        #df = df.convert_objects(convert_numeric=True)
        #df = df.drop_duplicates()
        try:
            #df = df.pivot(3, 0, 1)#.bfill().ffill()
            #df = df.describe().transpose().sort('count', ascending=False)
            print df.ix[:, [3]]
        except:
            ''
        #print prevData
        #print data
        print
        #dfd = p_DataFrame([prevData, data])
        #print dfd#.pivot(4, 3, 2)
        #print dfd.ix[[0,2,3,4], :].transpose()
        #print df.combine_first()
        
        
        c += 1
        """
        #time.sleep(0.1)
mode = sys.argv[2]
client(mode)

#from pandas import read_csv as p_read_csv
#instruments = p_read_csv('data/oanda/cache/instruments.csv').set_index('instrument')
#instruments

#from pandas import read_csv as p_read_csv
#df = p_read_csv('data/oanda/cache/instruments.csv')
#pairs = list(df.ix[:, 'instrument'])
#currencyMatrix(pairs)
