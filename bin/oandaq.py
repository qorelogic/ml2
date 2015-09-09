
#import curses  # Get the module

#from numpy import *
from numpy import array as n_array
from numpy import dot as n_dot
from numpy import divide as n_divide
from numpy import float16 as n_float16
from numpy import rint as n_rint
from numpy import c_ as n_c_
from numpy import min as n_min
from numpy import max as n_max
from numpy import tanh as n_tanh
from numpy import concatenate as n_concatenate

import plotly.plotly as py
from plotly.graph_objs import *

import os, sys, oandapy
import datetime as dd
from matplotlib.pyplot import plot, legend, title, show, imshow, tight_layout
from pylab import rcParams
from IPython.display import display, clear_output
import ujson as j

from qore import *
from qore_qstk import *
from matplotlib.pylab import *

import numpy as n
import pandas as p
import Quandl as q
import datetime as dd
import urllib2 as u
import html2text
import exceptions as ex
import re, sys
import StringIO as sio
import threading,time
import itertools as it

import oandapy

class OandaQ:
    
    oanda2 = None
    oandapys = {}
    
    def __init__(self, verbose=False):
        self.qd = QoreDebug()
        self.qd._getMethod()
        
        self.verbose = verbose

	#self.stdscr = curses.initscr()  # initialise it
        
        # get current quotes
        co = p.read_csv('/mldev/bin/datafeeds/config.csv', header=None)
        selAccount         = 1
        self.oandaUsername = co.ix[selAccount,0]
        self.env2          = co.ix[selAccount,1]
        self.access_token2 = co.ix[selAccount,2]
        #self.oanda2 = 
        
        oc = self.oandaConnection(self.oandaUsername, self.env2, self.access_token2)
        self.oanda2 = oc #oandapy.API(environment=self.env2, access_token=self.access_token2)
    
        self.aid = self.oandaConnection().get_accounts()['accounts'][0]['accountId']
        #self.oandaConnection().create_order(aid, type='market', instrument='EUR_USD', side='sell', units=10)
        """
        if verbose == True:
            res = self.oandaConnection().get_trades(self.aid)
            for i in res:
                print p.DataFrame(res[i])
        
            print p.DataFrame(self.oandaConnection().get_account(self.aid), index=[0])
        """
    
        self.dfa = {}
        
        self.granularityMap = {
            'S5' : 5, # seconds
            'S10' : 10, # seconds
            'S15' : 15, # seconds
            'S30' : 30, # seconds
            'M1' : 1 * 60, # minute
    
            'M2' : 2 * 60, # minutes
            'M3' : 3 * 60, # minutes
            'M4' : 4 * 60, # minutes
            'M5' : 5 * 60, # minutes
            'M10' : 10 * 60, # minutes
            'M15' : 15 * 60, # minutes
            'M30' : 30 * 60, # minutes
            'H1' : 1 * 3600, # hour
            'H2' : 2 * 3600, # hours
            'H3' : 3 * 3600, # hours
            'H4' : 4 * 3600, # hours
            'H6' : 6 * 3600, # hours
            'H8' : 8 * 3600, # hours
            'H12' : 12 * 3600, # hours
            'D' : 1 * 86400, # Day
            #Start of week alignment (default Friday)        
            'W' : 1 * 604800, # Week
            #Start of month alignment (First day of the month)        
            'M' : 1 * 2419200 # Month
        }

        self.instruments = self.oandaConnection().get_instruments(self.aid)['instruments']
        self.ticks = {}
        self.accountInfo = {}
        self.ctime = 0
        self.ptime = 0
        
    def log(self, msg, printDot=False):
        if self.verbose == True: 
            print msg
        if printDot == True:
            print '.',
    
    def debug(self, msg):
        if self.verbose == True: 
            print msg
    
    def oandaConnection(self, name=None, env=None, access_token=None):
        if name != None and env != None and access_token != None:
            self.oandapys[name] = oandapy.API(environment=env, access_token=access_token)
            return self.oandapys[name]
        else:
            return self.oandapys[self.oandaUsername]

    def datetimeToTimestamp(self, ddt):
        self.qd._getMethod()

        def _datetimeToTimestamp(ddt):
            return (ddt - dd.datetime(1970, 1, 1)).total_seconds() / dd.timedelta(seconds=1).total_seconds()
        
        try:    tstmp = _datetimeToTimestamp(ddt)
        except Exception as e:
            print e
            tstmp = []
            for i in ddt: tstmp.append(_datetimeToTimestamp(i))
        return tstmp
        
    def timestampToDatetime(self, tst):
        self.qd._getMethod()

        def _timestampToDatetime(tst):
            return dd.datetime.fromtimestamp(tst)

        try:    ddt = _timestampToDatetime(tst)
        except Exception as e:
            print e
            ddt = []
            for i in tst: ddt.append(_timestampToDatetime(i))                
        return ddt
        
    """
    timestampToDatetimeFormat [1435942800.0, 1436130000.0, 1436144400.0, 1436158800.0, 1436173200.0, 1436187600.0, 1436202000.0, 1436216400.0, 1436230800.0, 1436245200.0]
    Out]:
    ['2015-07-03 14:00:00',
     '2015-07-05 18:00:00',
     '2015-07-05 22:00:00',
     '2015-07-06 02:00:00',
     '2015-07-06 06:00:00',
     '2015-07-06 10:00:00',
     '2015-07-06 14:00:00',
     '2015-07-06 18:00:00',
     '2015-07-06 22:00:00',
     '2015-07-07 02:00:00']
     """
    def timestampToDatetimeFormat(self, tst, fmt='%Y-%m-%d %H:%M:%S %Z'):
        self.qd._getMethod()

        def _timestampToDatetimeFormat(tst):
            w2 = dd.datetime.fromtimestamp(tst)
            return w2.strftime(fmt)
            #return dd.datetime.fromtimestamp(tst)

        try:    
            ddt = _timestampToDatetimeFormat(tst)
        except Exception as e:
            print e
            ddt = []
            for i in tst: ddt.append(_timestampToDatetimeFormat(i))                
        return ddt

    # source: http://stackoverflow.com/questions/14695309/conversion-from-numpy-datetime64-to-pandas-tslib-timestamp-bug
    def timestampToNumpyTimestamp(self, ts):
        self.qd._getMethod()

        def _timestampToNumpyTimestamp(ts):
            return ts * 1e9
           
        try:
            tss = _timestampToNumpyTimestamp(ts)
        except Exception as e:
            self.log(e)
            tss = []
            for i in ts: tss.append(_timestampToNumpyTimestamp(i))                
        return tss
            
    def numpyTimestampToTslibTimestamp(self, ts):
        self.qd._getMethod()

        def _numpyTimestampToTslibTimestamp(ts):
            return p.tslib.Timestamp(ts, tz=None)

        try:
            tss = _numpyTimestampToTslibTimestamp(ts)
        except Exception as e:
            self.log(e)
            tss = []
            for i in ts: tss.append(_numpyTimestampToTslibTimestamp(i))                
        return tss

    def oandaToTslibTimeStamp(self, dfin):
        self.qd._getMethod()
        
        dfin = self.oandaToTimestamp(dfin)
        dfin = self.timestampToNumpyTimestamp(dfin)
        dfin = self.numpyTimestampToTslibTimestamp(dfin)
        return dfin

    def oandaToTimestamp(self, ptime):
        self.qd._getMethod()
        
        def _oandaToTimestamp(ptime):
            dt = dd.datetime.strptime(ptime, '%Y-%m-%dT%H:%M:%S.%fZ')
            return (dt - dd.datetime(1970, 1, 1)).total_seconds() / dd.timedelta(seconds=1).total_seconds()
            
        try:
            tstmp = _oandaToTimestamp(ptime)
        except Exception as e:
            self.log(e)
            tstmp = []
            for i in ptime: tstmp.append(_oandaToTimestamp(i))                
        return tstmp

    def oandaToDatetime(self, ptime):
        self.qd._getMethod()
        return dd.datetime.strptime(ptime, '%Y-%m-%dT%H:%M:%S.%fZ')

    def trade(self, risk, stop, instrument, side, tp=None, nostoploss=False):
        self.qd._getMethod()
        
        """
        if instrument == 'eu':
            instrument = 'EUR_USD'
        if instrument == 'au':
            instrument = 'AUD_USD'
        if instrument == 'nu':
            instrument = 'NZD_USD'
        if instrument == 'ej':
            instrument = 'EUR_JPY'
        if instrument == 'uj':
            instrument = 'USD_JPY'
        """
        
        if side == 'b':
            side ='buy'
            self.buy(risk, stop, instrument=instrument, tp=tp, nostoploss=nostoploss)
        if side == 's':
            side ='sell'
            self.sell(risk, stop, instrument=instrument, tp=tp, nostoploss=nostoploss)
        
    def buy(self, risk, stop, instrument='EUR_USD', tp=None, nostoploss=False):
        self.qd._getMethod()
        
        self.order(risk, stop, 'buy', instrument=instrument, tp=tp, nostoploss=nostoploss)
        
    def sell(self, risk, stop, instrument='EUR_USD', tp=None, nostoploss=False):
        self.qd._getMethod()
        
        self.order(risk, stop, 'sell', instrument=instrument, tp=tp, nostoploss=nostoploss)

    def order(self, risk, stop, side, instrument='EUR_USD', tp=None, price=None, expiry=None, nostoploss=False):
        self.qd._getMethod()
        
        stop = abs(float(stop)) # pips
        risk = float(risk) # percentage risk
        
        #print self.oandaConnection().get_accounts()['accounts'][0]['accountId']
        acc = self.oandaConnection().get_account(self.aid)
        #mprice = self.oandaConnection().get_prices(instruments='EUR_USD')['prices'][0]['ask']
        #leverage = 50
        
        amount = self.calculateAmount(acc['marginAvail'], risk, stop)
        
        #print acc['marginAvail'] * float(leverage) / mprice
        #print acc
        #print mprice
        print 'amount:{0}'.format(amount)
        
        prc = self.oandaConnection().get_prices(instruments=instrument)['prices'][0]
        
        limitprice = self.oandaConnection().get_prices(instruments='EUR_USD')['prices'][0]
                
        # modify the stop to mimic no stoploss
        if nostoploss == True:
            stop = 1000

        # set the stoploss & takeprofit
        if side == 'buy':
            stopLoss   = prc['bid'] - float(stop) / 10000
            takeProfit = prc['bid'] + float(stop) / 10000
            print takeProfit
            limitprice = limitprice['bid']
        if side == 'sell':
            stopLoss = prc['ask'] + float(stop) / 10000
            takeProfit = prc['ask'] - float(stop) / 10000
            print takeProfit
            limitprice = limitprice['ask']
        
        if tp != None:
            takeProfit = tp
        else:
            takeProfit = None
        
        try:
            print 'attempting market order'
            order = self.oandaConnection().create_order(self.aid, type='market', instrument=instrument, side=side, units=amount, stopLoss=stopLoss, takeProfit=takeProfit)
            print 'market order success'
        except oandapy.OandaError, e:
            print 'attempting limit order'
            tti = dd.datetime.now()
            tti = tti+ dd.timedelta(days=30)
            tti = self.datetimeToTimestamp(tti)
            expiry = self.timestampToDatetimeFormat(tti, fmt='%Y-%m-%dT%H:%M:%S-3:00')
            #print e
            order = self.oandaConnection().create_order(self.aid, type='limit', expiry=expiry, price=limitprice, instrument=instrument, side=side, units=amount, stopLoss=stopLoss, takeProfit=takeProfit)
            print order
            print 'limit order success'

    def calculateAmount(self, bal, pcnt, stop):
        self.qd._getMethod()

        bal  = float(bal)
        lev  = 30.0
        stop = float(stop)
        openp = 1 #1.13024
        pcnt = float(pcnt)
        
        amount = bal * lev
        pl     = amount * ((openp + float(stop) / 10000.0) - openp )
        #pcnt   = 100.0*pl / bal
        
        amount = (pcnt * bal) / (100* ((openp + float(stop) / 10000.0) - openp ) )
        #amount = (pcnt * bal) / (100* ((openp - float(stop) / 10000.0) - openp ) )
        amount = abs(int(amount))
        print 'amount {0}'.format(amount)
        print 'pl {0}'.format(pl)
        print 'pcnt {0}'.format(pcnt)
        print 'bal {0}'.format(bal)
        
        return amount
        
    def calculateStopLossFromPrice(self, pair, mprice):
        self.qd._getMethod()

        current = self.oandaConnection().get_prices(instruments=[pair])['prices'][0]['bid']
        mstop = (mprice-current) * 10000
        #print 'mstop {0}'.format(mstop)
        return mstop
        
    def generateRelatedColsFromOandaTickers(self, data, pair):
        self.qd._getMethod()
        
        if type(data) == type(None):
            print data
            raise ValueError('given input is none')
        
        # generate relatedCols from oandas tickers
        fname = '/mldev/bin/data/oanda/cache/instruments.csv'
        try:
            inst = readcache(fname)
        except Exception as e:
            print e
            inst = p.DataFrame(self.oandaConnection().get_instruments(self.aid)['instruments'])
            writecache(inst, fname)
        lse = []
        lsf = []
        for i in inst.ix[:, 'instrument']:

            ipair = i.replace('_', '')
            
            if pair[0:3] == ipair[0:3] or pair[0:3] == ipair[3:6]:
                lse.append('BNP.'+ipair+' - '+ipair[0:3]+'/'+ipair[3:6]+'_x')

            if pair[3:6] == ipair[0:3] or pair[3:6] == ipair[3:6]:
                lse.append('BNP.'+ipair+' - '+ipair[0:3]+'/'+ipair[3:6]+'_x')
                
            if pair[0:3] == ipair[0:3] and pair[3:6] == ipair[3:6]:
                lse.pop()
        for i in lse:
            try:    
                lsf.append(list(data.columns).index(i))
            except Exception as e:
                print e
                
        #for i in inst:
        #    print i['instrument']
        
        #print lsf
        try:
            lsf  = list(p.DataFrame(lsf).sort(0).transpose().get_values()[0])
        except KeyError, e:
            print e
        #print lsf
        return lsf
        
    def getPairsRelatedToOandaTickers(self, pair):
        self.qd._getMethod()
        
        # generate relatedCols from oandas tickers
        
        fname = '/mldev/bin/data/oanda/cache/instruments.csv'
        try:
            inst = readcache(fname)
        except Exception as e:
            print e     
            inst = p.DataFrame(self.oandaConnection().get_instruments(self.aid)['instruments'])
            writecache(inst, fname)

        lse = []
        lsf = []
        lsp = []
        for i in inst.ix[:, 'instrument']:

            ipair = i.replace('_', '')
            
            if pair[0:3] == ipair[0:3] or pair[0:3] == ipair[3:6]:
                lse.append('BNP.'+ipair+' - '+ipair[0:3]+'/'+ipair[3:6]+'_x')
                lsp.append([i, ipair])

            if pair[3:6] == ipair[0:3] or pair[3:6] == ipair[3:6]:
                lse.append('BNP.'+ipair+' - '+ipair[0:3]+'/'+ipair[3:6]+'_x')
                lsp.append([i, ipair])
                
        #print lse
        #print lsp
        
        r = {}
        r['lse'] = lse
        r['lsf'] = lsf
        r['lsp'] = lsp
        
        return r
    
    def getPricesLatest(self, data, sw, trueprices=False):
        self.qd._getMethod()
        
        ins = []
        pairs = []
        for i in list(data.ix[:, sw.relatedCols].columns):
            pair = re.sub(re.compile(r'.*?-\ (.*)_x'), '\\1', i).replace('/', '_')
            #print pair
            pr = p.DataFrame(self.oandaConnection().get_prices(instruments=[pair])['prices'])
            #print 
            ins.append(n.mean(pr.ix[0, ['bid', 'ask']].get_values()))
            pairs.append(pair)
        prices = p.DataFrame(ins, index=pairs)
        if trueprices:
            return prices
        #print #prices
        list(prices.ix[1:,0])#.insert(0,1)
        nprices = p.DataFrame([list(sw.theta), list(prices.ix[1:,0]) ]).transpose()
        #nprices = nprices.fillna(0)
        
        #prices.ix[1:,0], sw.dmean, sw.dstd] = normalizeme(prices.ix[1:,0], pinv=True)
        #rices.ix[1:,0] = sigmoidme(prices.ix[1:,0])
        nprices = p.DataFrame([list(sw.theta), list(prices.ix[1:,0]) ], columns=list(prices.index)).transpose()
        pr2 = list(nprices.ix[:,1])[0:10]
        pr2.insert(0,1)
        #print pr2
        #print 
        #print prices
        nprices[1] = pr2
        print nprices
        return nprices

    def oandaTransactionHistory(self, plot=True, fname=None, startTs=1200000000):
        self.qd._getMethod()

        # oanda transaction history (long-term)
        from pylab import rcParams
        rcParams['figure.figsize'] = 20, 5
        # oanda equity viz
        if fname == None:            
            fname = '/home/qore/sec-svn.git/assets/oanda/{0}/primary/statement.csv'.format(self.oandaUsername)
        df0 = p.read_csv(fname)
        #df0 = df0.ix[3000:, 'Balance']
        df0 = df0.sort(columns=['Transaction ID'])
        df0 = df0.ix[:, :]
        df0 = df0.set_index('Transaction ID')
        
        #dfn = df0.ix[:, 'Balance']
        #dfn = normalizeme(dfn)
        #dfn = sigmoidme(dfn)
        #dfn.plot(); show();
        #print df.ix[:,['Type','Currency Pair','Units','Balance','Interest','Pl']]
        
        # oanda transaction history (short-term)
        df1 = p.DataFrame(self.oandaConnection().get_transaction_history(self.aid)['transactions']).bfill()
        df1 = df1.sort('id', ascending=True)
        df1 = df1.set_index('id')
        
        #print df0.tail()
        #print dfn.tail()
        #print df0 #.transpose()
        #print df1
        
        df1['Balance'] = df1['accountBalance']
        #print df0.tail()
        #print df1.tail()
        #df = df0.combine_first(df1)
        df = df1.combine_first(df0)
        #print df.tail()
        #df.ix[:,['Balance','accountBalance']]
        
        #print 'long term'
        #df0.ix[:,'Balance'].plot(); show();
        #print 'short term'
        #df1['accountBalance'].plot(); show();
        #print 'merge'
        if plot == True:            
            df.ix[startTs:,'Balance'].plot(); show();
        return df
        
    def getHistoricalPrice(self, pair, granularity='S5', count=2, plot=True):
        self.qd._getMethod()
        
        df = self.oandaConnection().get_history(instrument=pair, count=count, granularity=granularity)
        #hed = ['closeAsk', 'closeBid', 'highAsk', 'highBid', 'lowAsk', 'lowBid', 'openAsk', 'openBid', 'volume']
        #hed = ['closeAsk', 'closeBid', 'highAsk', 'highBid', 'lowAsk', 'lowBid', 'openAsk', 'openBid']
        hed = ['closeAsk', 'closeBid', 'volume']
        df = p.DataFrame(df['candles'], dtype=n.float16)
        df = df.set_index('time')
        #print df
        df = df.ix[:,hed]
        #df = normalizeme(df)
        #df = sigmoidme(df)
        if plot == True:
            df.ix[:,:].plot(legend=False, title=pair); show();
        #print df
        
        return df
    
    def appendHistoricalPrice(self, df, pair, granularity='S5', plot=True, count=None):
        self.qd._getMethod()

        safeShift = 0
        
        ti = df.tail(1).index[0]
        ddt = self.datetimeToTimestamp(dd.datetime.now()) 
        #print ddt
        ddtdiff = ddt - self.oandaToTimestamp(ti) + (60*60*3)
        self.log('{0} seconds behind'.format(ddtdiff))
        self.log('{0} minutes behind'.format(ddtdiff / 60))
        if count == None:
            reqcount = int(ceil(ddtdiff / self.granularityMap[granularity])) + safeShift
        else:
            reqcount = count
        self.log(self.granularityMap[granularity])
        self.log('requesting {0} ticks'.format(reqcount))
        if safeShift > 0:
            plotHiPr = True
        else:
            plotHiPr = False

        if reqcount > 1:
            dfn = self.getHistoricalPrice(pair, count=reqcount, granularity=granularity, plot=plotHiPr)#.tail()
            #print df.tail()
            #print dfn.tail()
            dfc = df.combine_first(dfn)
            df = dfc
        
            if plot == True:
                #df.plot(); show();
                dfc.plot(title=pair); show();
            return dfc
        return df
        
    def updatePairGranularity(self, pair, granularity, noUpdate=False, plot=True):
        self.qd._getMethod()

        ob = ''
        #ob += '{0} {1}'.format(pair, granularity)
        fname = '/mldev/bin/data/oanda/ticks/{0}/{0}-{1}.csv'.format(pair, granularity)
        try:    
            self.dfa[pair][granularity]
        except Exception as e:
            print e
            # if dataframe not in memory
            self.log('{0} {1} dataframe not in memory'.format(pair, granularity))
            try:
                # read from csv
                self.dfa[pair][granularity] = p.read_csv(fname, index_col=0)
                ob += ' reading from {0} {1} {2}'.format(fname, pair, granularity)
                ob += ' len {0}.'.format(len(self.dfa[pair][granularity]))
            except KeyError, e:
                self.debug(e)
                self.dfa[pair] = {}
            except IOError, e:
                # if no csv file, initialize memory for the dataframe
                #print e
                self.dfa[pair] = {}
            except Exception as e:
                print e
                print 'exception {0}'.format(pair)
                
        # append to current dataframe in memory
        if noUpdate == False:
            self.log('{0} {1} attempting update {2}'.format(pair, granularity, noUpdate))
            self.log('{0} {1} updating'.format(pair, granularity))
            try:
                self.log('len {0} before append.'.format(len(self.dfa[pair][granularity])))
                self.dfa[pair][granularity] = self.appendHistoricalPrice(self.dfa[pair][granularity], pair, granularity=granularity, plot=plot)
                self.log('len {0} after append.'.format(len(self.dfa[pair][granularity])))
                self.log('appended to {0}'.format(pair))
                # if no dataframe in memory, download from data source
            except Exception as e:
                self.debug(e)
                try:
                    self.dfa[pair][granularity] = self.getHistoricalPrice(pair, count=5000, granularity=granularity, plot=plot)
                    self.log('got clean series {0}'.format(pair))
                except oandapy.OandaError, e:
                    self.debug(e)
        
        if noUpdate == False:
            try:
                # save to csv file
                li = fname.split('/'); li.pop(); hdir = '/'.join(li);
                mkdir_p(hdir)
                self.dfa[pair][granularity].to_csv(fname)
                #if plot == True:
                #    self.dfa[pair][granularity].plot(); show();
                self.log('saved {0} to {1}'.format(pair, fname))
            except KeyError, e:
                print e
        self.log(ob)
        #print self.dfa[pair][granularity]
        return self.dfa[pair][granularity]
        
    def updateBarsFromOanda(self, pair='EURUSD', granularities = 'H4', plot=True, noUpdate=False):
        self.qd._getMethod()

        pair = pair.replace('_', '') # remove the underscore
        relatedPairs = self.getPairsRelatedToOandaTickers(pair)        
        
        pairs = list(p.DataFrame(relatedPairs['lsp']).ix[:,0])
        #self.log(pairs)
        self.granularities = granularities.split(' ')
        for pair in pairs:
            self.log('')
            try:                self.dfa[pair]
            except KeyError, e: 
                self.dfa[pair] = {}; 
                self.debug(e)
            for granularity in self.granularities:
                self.updatePairGranularity(pair, granularity, noUpdate=noUpdate, plot=plot)
                
        #print self.dfa
        return self.dfa

    def prepareDfData(self, dfa):
        self.qd._getMethod()

        dfac = p.DataFrame()
        gran = self.granularities[0]
        
        try:
            for i in dfa:
                #dfa[i][gran][i+'closeAsk'] = dfa[i][gran]['closeAsk']
                #dfa[i][gran][i+'closeBid'] = dfa[i][gran]['closeBid']
                par = 'BNP.{0} - {1}_x'.format(i.replace('_', ''), i.replace('_', '/'))
                dfa[i][gran][par] = (dfa[i][gran]['closeAsk'] + dfa[i][gran]['closeBid']) / 2       
                #print dfa[i][gran].ix[:,[2,3]].tail(1)#.transpose()
                #dfac = dfac.combine_first(dfa[i][gran].ix[:,[2,3,4]]) #.tail(1)#.transpose()
                dfac = dfac.combine_first(dfa[i][gran].ix[:,[par]]) #.tail(1)#.transpose()
        except Exception as e:
            print e
            print gran+' granularity not available, please update for '+gran
        #dfac = normalizeme(dfac)
        #dfac = sigmoidme(dfac)
        #dfac = (1 - n.power(n.e, -dfac)) / (1 + n.power(n.e, -dfac)) # hyperbolic tangent, tanh
        #dfac = n.log(1 + n.power(n.e, dfac)) # relu
        #dfac = n.tanh(dfac) # tanh
        #dfac.plot(legend=False); show();
        #dfac
        
        #from qoreliquid import *
        #qq = QoreQuant()
        
        return dfac

    def getAccountInfo(self):
        self.qd._getMethod()
        
        try: self.lastAccountCheck
        except: self.lastAccountCheck = 0
        #print self.lastAccountCheck
        if time.time() - 600 >= self.lastAccountCheck:
            self.lastAccountCheck = time.time()
            #self.accountInfo = self.oandaConnection().get_account(self.aid)
            self.accountInfo = self.oandaConnection().get_account(self.aid)
            print 'account checked'
        return self.accountInfo

    def getPipValue(self, instrument):
        self.qd._getMethod()
        
        return n_float16(p.DataFrame(self.instruments).set_index('instrument').ix[instrument, 'pip'])

    def calcDoublingFactorPeriod(self, x):
        self.qd._getMethod()
        
        return 100*((n.power(10, log10(2)/x))-1)
    
    def wew(self, ds):
        #print '---2---'
        #print ds
        ds = n.unique(ds)
        #print ds
        ds = list(ds)
        #print ds
        #ds.remove(ds.index('na')+1)
        try: ds.remove('na')
        except: ''
        #print ds
        return ds

    def getBabySitPairs (self):
        self.qd._getMethod()
        
        df = self.oandaConnection().get_trades(self.aid)['trades']
        pairdf = p.DataFrame(df)
        print pairdf
        try:
            pdf = pairdf.ix[:,'instrument'].get_values()
            pdf = n.array(pdf)            
            #print pdf
            #print '---'
            df = self.syntheticCurrencyTable(pdf, homeCurrency='USD')
            df = p.DataFrame(df).set_index('instrument').ix[:,['pairedCurrency','pow']]
            pcdf = df.ix[:,'pairedCurrency'].get_values()
            #print pcdf
            pcdf = self.wew(pcdf)
            #pdf = n.c_[pdf,pcdf]#[0]
            pdf = list(pdf)+list(pcdf)
            #print pdf
            #fdf = fdf.combine_first(df)
            pairs = ','.join(list(pdf))
            #print pairs
            return pairs
        except Exception as e: print e
        return ''
    
    def logEquity(self):
        self.qd._getMethod()

        mkdir_p('/mldev/bin/data/oanda/logs')
        self.ptime = self.ctime
        self.ctime = time.strftime('%S')
        #if self.ptime < self.ctime:
        #    print '--'            
        if self.ptime > self.ctime:
            print '---------'
            res = self.oandaConnection().get_accounts()['accounts']
            #print res
            for i in list(p.DataFrame(res).ix[:, 'accountId']):
                #print i
                ctime = time.time()
                df = p.DataFrame(self.oandaConnection().get_account(i), index=[ctime])#.transpose()
                df['ts'] = ctime
                #print df.columns
                csv = ','.join(list(n.array(df, dtype=string0)[0]))
                print csv
                fp = open('/mldev/bin/data/oanda/logs/{0}.equity.log.csv'.format(self.oandaUsername), 'a')
                fp.write(csv+'\n')
                fp.close()
        #print self.ctime
        #print '{0} {1}'.format(self.ctime, self.ptime)

    def babysitTrades(self, df, tick):
        #self.qd._getMethod()
    
  	#self.stdscr.clear()  # Clear the screen
    	#os.system('clear')
	#print(100*'\n')
        #print tick
        
        self.ticks[tick['instrument']] = tick 
        #print p.DataFrame(self.ticks).transpose()
        #print df
   
        mdf = p.DataFrame()
        
        for i in df:
            
            dfi = p.DataFrame(i, index=[0])
            dfi['tid'] = dfi['id']
            dfi = dfi.set_index('id')
            pair = dfi.ix[:,'instrument'].get_values()[0]
            side = dfi.ix[:,'side'].get_values()[0]
            # if selling, you need to buy back@ bid price
            # and vice versa, if buying, you need to sell back@ ask price
            mside = 'bid' if side == 'sell' else 'ask'
            
            dfi['units'] = dfi.ix[:,'units'].get_values()[0]
            
            try:
                dfi['currentprice'] = self.ticks[pair][mside]
                dfi['bid']          = self.ticks[pair]['bid']
                dfi['ask']          = self.ticks[pair]['ask']
                dfi['pipval']       = self.getPipValue(pair)
                dfi['spread']       = abs(self.ticks[pair]['bid'] - self.ticks[pair]['ask'])
                dfi['spreadpips']   = float(abs(self.ticks[pair]['bid'] - self.ticks[pair]['ask'])) / float(list(dfi['pipval'])[0])
                mdf = mdf.combine_first(dfi)
            except:
                ''
            #print dfi.transpose()
    
        if len(mdf) > 0:
            
            #print 'shape:'.format(mdf.shape)
            #print 'lenmdf:'.format(len(mdf))
            mdf['pole'] = list(n_array(n_array(mdf.ix[:,'side']) == 'buy', dtype=int))
        
            # inspired source: http://brenocon.com/blog/2013/10/tanh-is-a-rescaled-logistic-sigmoid-function/
            # gx = ((2.*(e.^z./(1+e.^z))) .* (2.*z)) - 1
            #z = n.matrix('1;0.1').A
            z = mdf['pole']
            
            mdf['poleTanh']          = n_rint(n_tanh((2*(n_power(n_e, z) / (1 + n_power(n_e, z))) * (2*z))-1))    
            mdf['pips']              = n_divide(1.0, n_array(mdf.ix[:,'pipval'], dtype=n_float16)) * (mdf.ix[:,'currentprice'] - mdf.ix[:,'price']) * mdf.ix[:,'poleTanh']
            mdf['trailpips']         = 2
            mdf['trail']             = mdf['pips'] - mdf['trailpips']
            mdf['pl']                = (mdf.ix[:,'currentprice'] - mdf.ix[:,'price']) * mdf.ix[:,'poleTanh']  * mdf.ix[:,'units']
            mdf['plpcnt']            = n_dot(n_divide(mdf['pl'], self.getAccountInfo()['balance']), 100)
            mdf['plpcntExSpread'] = n_dot(n_divide(mdf['pl'] - mdf['spread'], self.getAccountInfo()['balance']), 100)
    
            #print mdf.ix[:,'poleTanh']
            #print mdf.ix[:,'currentprice']
            #print mdf.ix[:,'price']
            #print (mdf.ix[:,'currentprice'] - mdf.ix[:,'price'])
            #print (mdf.ix[:,'currentprice'] - mdf.ix[:,'price']) * mdf.ix[:,'poleTanh']
            #print (mdf.ix[:,'currentprice'] - mdf.ix[:,'price']) * mdf.ix[:,'poleTanh']  * mdf.ix[:,'units'] 
            #print self.getAccountInfo()['balance']
            #print mdf['pips']
        
            #print mdf.ix[:, 'instrument price side currentprice pips trail trailpips'.split(' ')]
            #print '---------------------------------------------------------------------'
            # display the dataframe        
            #columns = 'instrument price units side currentprice bid ask spread spreadpips plpcntExSpread pl plpcnt pips trail trailpips'.split(' ')
            columns  = 'instrument price units side currentprice bid ask spreadpips plpcntExSpread pl plpcnt pips'.split(' ')
            columns  = 'tid instrument side units price currentprice pl plpcnt plpcntExSpread pips spread spreadpips pipval'.split(' ')
            fcolumns = 'price units side currprice bid ask spread pl%-spread pl$ pl% pips trail trailpips'.split(' ')
            amdf = mdf.ix[:, columns]
            #amdf['id'] = amdf.index
            amdf       = amdf.set_index('instrument')
            #mamdf = n_array(amdf.ix[:, columns].fillna(0).get_values())#, dtype=n_float16)
            #mamdf = n_around(mamdf, decimals=4)
            #p.options.display.float_format = '{:,.1f}'.format
            fdf = p.DataFrame(amdf, index=amdf.index, columns=amdf.columns) #.transpose()
            #print fdf#.to_dict()
            #print fdf.ix[:,:]#.to_dict()
            #os.system('clear')

            self.logEquity()

            tspm = float(time.time())*100
            #print tspm
            #if int(tspm) % 5 == 0:
            
            df = self.syntheticCurrencyTable(fdf.index, homeCurrency='USD')
            df = p.DataFrame(df).set_index('instrument').ix[:,['pairedCurrency','pow']]
            #print '---1---'
            ds = df['pairedCurrency'].get_values()
            ds = self.wew(ds)
            #print ds
            #print '---4---'
            gdf = p.DataFrame(self.ticks).transpose().ix[df['pairedCurrency'].get_values(), :]
            gdf['fdfi'] = fdf.index
            gdf = gdf.set_index('fdfi')
            gdf['pask'] = gdf['ask']
            gdf['pbid'] = gdf['bid']
            gdf = gdf.ix[:,['pask','pbid']]
            gdf = gdf.fillna(1)
            #[df['pairedCurrency'].get_values()[0]]
            #print '------'
            #print df
            fdf = fdf.combine_first(df)
            fdf = fdf.combine_first(gdf)
            #fdf['ple'] = pow(fdf['pl'] / fdf['pask'], fdf['pow'])
            #print fdf['pipval']
            fdf['ple'] = (fdf['price'] - fdf['currentprice']) * fdf['units'] * pow(fdf['pask'], fdf['pow'])
            fdf['plpecnt'] = n_dot(n_divide(fdf['ple'], self.getAccountInfo()['balance']), 100)
            fdf['period72'] = 500
            fdf['doublineFactorPeriod'] = self.calcDoublingFactorPeriod(fdf['period72'])
            
            print
            print fdf.transpose()

            #time.sleep(0.10)

            #print len(mdf)
            #print mdf
            for i in xrange(len(mdf)):
                tid = mdf.index[i]
                instrument = mdf['instrument'].ix[tid,:]
                plpcntExSpread = fdf['plpecnt'].ix[fdf.index[i],:]
                doublineFactorPeriod = fdf['doublineFactorPeriod'].ix[fdf.index[i],:]
                #print doublineFactorPeriod
                if plpcntExSpread >= doublineFactorPeriod: # and False:
                    print 'closing trade: {0}-{1}'.format(tid, instrument)
                    self.oandaConnection().close_trade(self.aid, tid)
                    
                    #time.sleep(1)
                    self.gotoMarket()
                #print plpcntExSpread

#            print '---------------------------------------------------------------------'

            #for res in n_array(mdf, dtype=n_string0):
            #    print ' '.join(list(res))
            #print '-----'
            
            """
            for i in xrange(len(mdf)):
                print mdf['trail'][i]
                if mdf['trail'][i] > 0:
                    #self.oandaConnection().modify_trade(self.aid, tid, trailingStop=10)
                    print 'setting trailstop'
            """
            """
            if pl > 0:
                print pl
                print 'setting trailstop'
                tid = trade['id']
                #self.oandaConnection().modify_trade(self.aid, tid, trailingStop=10)
            else:
                print 'trailstop too small, patience!'
            """
            
           #print mdf.ix[:,'side'].get_values()
            return mdf#.transpose()
        #else:
        #    return n.empty()
  
    def runCmd(self, cmd, dryrun=False):
        self.qd._getMethod()
        
        print cmd
        if dryrun == False:
            ###########################################################
            try:   exec(cmd)
            ###########################################################
            except Exception as e: print e
    
    def gotoMarket(self, manifest=None, dryrun=False):
        self.qd._getMethod()
        
        if manifest == None:
		#manifest = 'EURGBPv1560 HKDJPY^60 GBPNZDv15 GBPCHFv15 GBPUSDv603015 GBPJPYv15 GBPAUDv3060 USDCHFv240'.split(' ') #HKDJPYv30
        	fp = open('/ml.dev/bin/data/infofeeds/investing.csv', 'r')
        	mlog = fp.read().strip().split('\n')
        	#print mlog
        	manifest = mlog[len(mlog)-1].strip().split(',')
        	print manifest
        	fp.close()

        self = OandaQ()
        trades = self.oandaConnection().get_trades(self.aid)['trades']
        trades = p.DataFrame(trades)#.transpose()
        try:
            trades = trades.set_index('id')
            trades['stop'] = list(abs(trades['price'] - trades['stopLoss'])*10000)
        except:
            ''
        print trades.ix[:,'instrument price side stopLoss stop units'.split(' ')]
        #print trades.ix[:,:]
        
        for i in manifest:
            print 
    
            pair = i[0:6]
            side = i[6:7]
            timeframe = i[7:]  
            pair = '{0}_{1}'.format(pair[0:3], pair[3:6])
            sideS = 'b' if side == '^' else 's'
            sideO = 'buy' if side == '^' else 'sell'
            
            cmd = "print self.trade(3, 30, '{0}', '{1}', nostoploss=True)".format(pair, sideS)
            try:
                if pair not in list(trades.ix[:,'instrument']):
                    print 'no position open in trade table: opening trade..'
                    self.runCmd(cmd, dryrun=dryrun)
            except:
                    # if len(trades) is 0 do this:
                    self.runCmd(cmd, dryrun=dryrun)
                
            print '------'
            print '------'
            print i
            print '------'
            
            try:
                mtrades = trades.ix[(trades['instrument'] == pair),['instrument','side','units']]
                sideN = mtrades.get_values()[0][1]
                units = mtrades.get_values()[0][2]
                print units
                print 'for {0} from {1} to {2}'.format(pair, sideN, sideO)
                #print (trades['instrument'] == pair)
                if sideO != sideN:
                    print 'new opposite signal, reversing open position to: '+sideN
                    self.runCmd("print self.oandaConnection().close_position('{0}', '{1}')".format(self.aid, pair))

                    sideNS = 'b' if side == '^' else 's'
                    self.runCmd("print self.trade(3, 30, '{0}', '{1}', nostoploss=True)".format(pair, sideNS))
            except:
                print 'exp 12'
                
            print
    
    def syntheticCurrencyTable(self, currs, homeCurrency='USD'):
        self.qd._getMethod()
        
        # source: http://www.python-course.eu/lambda.php
        ret = {'quote':map(lambda x: x[0:3], currs), 'base':map(lambda x: x[4:7], currs)}
        ret['pairedCurrency'] = []
        
        df = p.read_csv('/mldev/bin/data/oanda/cache/instruments.csv')
        #dfp = p.DataFrame(self.oanda2.get_prices(instruments=','.join(list(currs)))['prices'])
        #print dfp
        for i in ret['base']:
            try:
                #print i
                dft = map(lambda x: (x[0:3] == homeCurrency and x[4:7] == i) or (x[0:3] == i and x[4:7] == homeCurrency), list(df['instrument']))
                #print dft
                #print df.ix[dft, 'instrument'].get_values()[0]
                ret['pairedCurrency'].append(df.ix[dft, 'instrument'].get_values()[0])
            except Exception as e:
                ret['pairedCurrency'].append('na')
                #print e
        poles      = [1, -1]
        po         = map(lambda x: x[0:3] == homeCurrency, ret['pairedCurrency'])
        po         = n.array(po, dtype=int0)    
        ret['instrument'] = list(currs)
        ret['pow'] = map(lambda x: poles[x], po)
        #ret['ask'] = list(dfp['ask'])
        #ret['bid'] = list(dfp['bid'])
        ini = ','.join(list(ret['pairedCurrency'])).replace(',na', '')
        #print ini#['prices'] 
        #print p.DataFrame(self.oanda2.get_prices(instruments=ini)['prices'])
        #print p.DataFrame(ret).ix[:, 'instrument quote base pairedCurrency ask bid pow'.split(' ')]    
        #ret = ret.set_index('instrument')
        return ret

if __name__ == "__main__":
    print 'stub'
