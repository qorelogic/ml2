#!/usr/bin/env python

import zmq, time, sys
from pandas import DataFrame as p_DataFrame
from pandas import option_context as p_option_context
from numpy import array as n_array
import numpy as n
from collections import deque

from qore import QoreDebug
qd = QoreDebug()

import argparse
# source: https://docs.python.org/2/howto/argparse.html
parser = argparse.ArgumentParser()
parser.add_argument("-v", '--verbose', help="verbose", action="store_true")
parser.add_argument("-hp", '--hostport', help="<host>:<port>")
parser.add_argument("-m", '--mode', help="avg | spread | pos")

args = parser.parse_args()

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


class ZMQClient:

    def __init__(self):

        from qore import QoreDebug
        self.qd = QoreDebug()
        self.qd._getMethod()

        # option to change the port number from default 5555
        try:
            hostport = args.hostport
        except:
            hostport = 5555    
        
        res      = hostport.split(':')
        host     = res[len(res)-2]
        if host == '': host = 'localhost'
        port     = res[len(res)-1]
        hostport = '{0}:{1}'.format(host, port)
        connect  = 'tcp://{0}'.format(hostport)

        ctx = zmq.Context()
        #self.socket = ctx.socket(zmq.REQ)
        self.socket = ctx.socket(zmq.SUB)
        self.socket.connect(connect)
        
        # Subscribe to tester
        topicfilter = 'tester'
        #socket.subscribe(topicfilter) # only for SUB
        self.socket.setsockopt(zmq.SUBSCRIBE, topicfilter)
        
        #df = p_DataFrame()
        
    #@profile
    def currencyMatrix(self, pairs, df=None, mode=None, mong=None, depth=None):
        #from oandaq import OandaQ
        #oq = OandaQ()
        #pairs = ",".join(list(n.array(p_DataFrame(oq.oandaConnection().get_instruments(oq.aid)['instruments']).ix[:,'instrument'].get_values(), dtype=str)))
        
        if mode == 'avg':
            #print mong['avgs'].keys()
            #for i in mong['avgs'].keys():
            #    print len(mong['avgs'][i])
            #    print mong['avgs'][i]
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

        if mode == 'pos':
            df = p_DataFrame(mong['pos'])
            try:
                df=df.ix[depth-1, :]
            except:
                df=df.ix[depth-2, :]
        
        # transforn from currency pairs (EUR_USD, GBP_USD) to currencies (EUR, GBP, USD)
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
        
        cpairs = 'AUD CAD CHF EUR USD GBP JPY NZD MXN'.split(' ')
        
        try: dfm.ix['total', cpairs] = n.sum(dfm.ix[:, cpairs])
        except: ''
        try:
            dfm = dfm.convert_objects(convert_numeric=True)
            dfu = dfm.ix[:, cpairs]
            #print dfu[(dfu.values) > 0]
            with p_option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
                print dfu.sort()
            #print dfm.ix[:, cpairs]
            #print dfm[(dfm.values < 5)] #.any(1)
            #print dfm[(dfm.values < 1.5).any(1)].ix[:, cpairs]
            #print dfm.ix[:,(dfm.ix[:, cpairs] < 10)]
        except Exception as e:
            print e
        #print n.sum(dfm.ix[:, cpairs])
        #print dfm.ix[:, ['USD']]
        dfu = dfm.ix[['USD'], :].transpose()
        dfu = dfu.convert_objects(convert_numeric=True)
        #print dfu
        #print (dfu['USD'] != int(0))
    
    #@profile
    def client(self, args):
        mode = args.mode
        de = deque()
        #bids = deque()
        pairs = {}
        bids = {}
        asks = {}
        avgs = {}
        spreads = {}
        poss = {}
        from pandas import read_csv as p_read_csv
	
        from oandaq import OandaQ
        oq = OandaQ(selectOandaAccount=0)
        oq.generateInstruments()
        instruments = p_read_csv('data/oanda/cache/instruments.csv').set_index('instrument')
        
        maccid = 947325
        from pandas import DataFrame as p_DataFrame
        def getDfp(oq, maccid):
            positions = oq.oanda2.get_positions(maccid)['positions']
            dfp = p_DataFrame(positions).set_index('instrument')#.ix[:, 'instrument price side time units'.split(' ')]
            dfp['i1'] = map(lambda x: x[0:3], dfp.index)
            dfp['i2'] = map(lambda x: x[4:7], dfp.index)
            dfp['sideBool'] = map(lambda x: 1 if x == 'buy' else -1, dfp['side'])
            return dfp
        dfp = getDfp(oq, maccid)
        #print
        trades = oq.oanda2.get_trades(maccid)['trades']
        dft = p_DataFrame(trades).set_index('id').ix[:, 'instrument price side time units'.split(' ')]
        
        #accounts = oq.oanda2.get_accounts()
        account = p_DataFrame(oq.oanda2.get_account(maccid), index=[0])
    
        depth = 20
        c = 0
        while True:
            # update positions
            #tts = time.time()
            #print tts
            #if int(tts) % 10 == 0:
            #    print tts
            #    print 'getting positions:'
            #    #dfp = getDfp(oq, maccid)
            #    #print dfp
                
            #print dft.sort('instrument')
            #self.socket.send('test client') # only for REQ
            data = self.socket.recv(0)
            data = data.split(' ')
            data = ' '.join(data[1:]) # fixes the previous space split
            data = data.split(',')
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
            pairs = _uwe('pos', pairs, pair, data)
            
            mong = {'bids':bids, 'asks':asks, 'avgs':avgs, 'spreads':spreads, 'pos':poss}
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
            #self.currencyMatrix(list(df.ix[depth-1, :].index), df=df.ix[depth-1, :])
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
            #self.currencyMatrix(list(df.ix[depth-1, :].index), df=df.ix[depth-1, :])
            ########
            # avgs
            try: # catch exceptions from commodity instruments
                avg = abs( (float(data[1]) + float(data[2]))/2 )
            except:
                continue
            try:
                avgs[pair].append(avg)
            except:
                #avgs[pair] = deque()
                avgs[pair] = deque([0]*depth)
                avgs[pair].append(avg)
            
            if len(avgs[pair]) >= depth:
                #print 'len avg pair:{0} depth:{1}'.format(len(avgs[pair]), depth)
                avgs[pair].popleft()
                #print len(avgs[pair])

            df = p_DataFrame(avgs)
            if mode == 'avg':
                self.currencyMatrix(list(df.ix[depth-1, :].index), mode=mode, mong=mong, depth=depth)

            ########
            # spreads
            try: # catch exceptions from commodity instruments
                spread = abs(float(data[1]) - float(data[2])) / instruments.ix[pair, 'pip']
            except:
                continue
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
                self.currencyMatrix(list(df.ix[depth-1, :].index), df=df.ix[depth-1, :], mode=mode, mong=mong, depth=depth)
            ########
            
            ########
            # pos
            try: # catch exceptions from commodity instruments
                #cprice = float((float(data[1]) + float(data[2])) / 2) # avg price
                #cprice = float(data[1]) if dfp.ix[data[0], 'sideBool'] == 1 else float(data[2]) # ask price if long position, bid price if short
                cprice = float(data[2]) if dfp.ix[data[0], 'sideBool'] == 1 else float(data[1]) # bid price if long position, ask price if short
                avgPrice = float(dfp.ix[data[0], 'avgPrice'])
                units = dfp.ix[data[0], 'sideBool'] * (cprice - avgPrice)  * float(dfp.ix[data[0], 'units']) * instruments.ix[data[0], 'pip'] * (10000 if instruments.ix[data[0], 'pip'] == 0.0001 else 1)
                pos = units
            except Exception as e:
                #print e
                units = 0
                pos = units
                continue
            try:
                poss[pair].append(pos)
            except:
                poss[pair] = deque([0]*depth)
                poss[pair].append(pos)
            
            if len(poss[pair]) >= depth: poss[pair].popleft()
            df = p_DataFrame(poss)
            #df = p_DataFrame(dfp)
            if mode == 'pos':
                balance = account.ix[0,'balance']
                with p_option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
                    dftt = df.tail(1).transpose()
                    dftt['pl'] = dftt[19]
                    try:
                        dftt['plpcnt'] = 100 * n.divide(dftt['pl'].get_values(), float(balance))
                        dftt['plpcnt'] = 100 * n.divide(dftt['pl'], float(balance))
                        dftt['plpcnt'] = 100 * dftt['pl'].get_values() / float(balance)
                        dftt['plpcnt'] = 100 * dftt['pl'] / float(balance)
                        dftt['plpcnt'] = 100 * n.divide(dftt['pl'].get_values(), float(balance))
                        dftt['pl'].get_values() / n.array(balance)
                        dftt['isClosable'] = dftt['plpcnt'] > ((2.0/n.pi)/10)
                    except Exception as e:
                        print e
                    dftt = dfp.combine_first(dftt)
                    #dftt = dftt[dftt['pl'] > 0]
                    dfw = dftt.sort('pl', ascending=False)
                    if args.verbose:
                        print dfw
                    for i in dfw.index:
                        pl         = dfw.ix[i, 'pl']
                        isClosable = dfw.ix[i, 'isClosable']
                        if isClosable == 1:
                            dfp = getDfp(oq, maccid)
                            print 'closing %s' % i
                            print "oq.oanda2.close_position(%s, '%s')" % (maccid, i)
                            oq.oanda2.close_position(maccid, i)
                        
                #self.currencyMatrix(list(df.ix[depth-1, :].index), mode=mode, mong=mong, depth=depth)

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


try:
    zc = ZMQClient()
    zc.client(args)
except KeyboardInterrupt as e:
    print ''
except Exception as e:
    qd.logTraceBack(e)
    print 'usage: <host:port> <avg|spread|pos>'
    qd.on()
    qd.printTraceBack()
    sys.exit(0)

#from pandas import read_csv as p_read_csv
#instruments = p_read_csv('data/oanda/cache/instruments.csv').set_index('instrument')
#instruments

#from pandas import read_csv as p_read_csv
#df = p_read_csv('data/oanda/cache/instruments.csv')
#pairs = list(df.ix[:, 'instrument'])
#currencyMatrix(pairs)
