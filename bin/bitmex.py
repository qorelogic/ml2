# coding: utf-8

def portfolioTokenization():
    #import pandas as p
    from pandas import DataFrame, option_context
    import sys
    txs = [
        {'action':'invest', 'amount':1, 'investorId':1, 'date':1},
        {'action':'profit', 'amount':2.6, 'date':1},
        {'action':'invest', 'amount':3, 'investorId':2, 'date':2},
        {'action':'profit', 'amount':75, 'date':2},
        {'action':'invest', 'amount':3,  'investorId':1, 'date':2},
        {'action':'invest', 'amount':23, 'investorId':3, 'date':2},
        {'action':'invest', 'amount':5,  'investorId':2, 'date':2},
        {'action':'invest', 'amount':8,  'investorId':2, 'date':2},
        {'action':'profit', 'amount':1.12, 'date':3},
        {'action':'profit', 'amount':1.13423, 'date':4},
        {'action':'invest', 'amount':100,  'investorId':6, 'date':4},
        {'action':'profit', 'amount':1.32, 'date':5},
        {'action':'invest', 'amount':1100,  'investorId':7, 'date':5},
        {'action':'invest', 'amount':3, 'investorId':3, 'date':5},
        {'action':'profit', 'amount':3.123, 'date':6},
    ]
    txs = DataFrame(txs)


    dfi = txs[txs['action'] == 'invest']
    dfi['marketcap']       = dfi['amount'].cumsum()
    dfi['fundPcntInitial'] = dfi['amount'] / dfi['marketcap']
    dfi['fundPcnt']        = dfi['amount'] / dfi['amount'].sum()

    txs = txs.combine_first(dfi)

    profits = DataFrame(index=txs['date'].unique(), columns=txs['investorId'].unique())


    print txs
    dfig = dfi.groupby('investorId')
    print dfi
    #print dfig.describe()
    print dfig.sum()['amount']
    print txs[txs['action'] == 'profit']
    profits = profits.combine_first(txs[txs['action'] == 'profit'].pivot(index='date', columns='action', values='amount'))
    print '---'
    for i in list(dfig.sum().index):
        print int(i)
        dfii = dfi[dfi['investorId'] == i]
        dfii['amountCumsum'] = dfii['amount'].cumsum()
        with option_context('display.max_rows', 400, 'display.max_columns', 4000, 'display.width', 1000000):
            print dfii#.#loc[max(dfii.index), :]
        for j in dfii.index:
            #print '%s %s' % (j, i)
            print 
            #jj = dfii.index[j]
            #print jj
            try:
                profits.loc[int(j), i] = dfii.loc[int(j), 'amount']
            except: ''
        print list(dfii.index)
    print '---'

    import numpy as n
    pr = profits.sort_index().fillna(0)
    capital = DataFrame(n.zeros(pr.shape), index=pr.index, columns=pr.columns)
    capital = pr.get_values()
    for i in capital.index:
        ''
    print pr
    print capital

    #print txs.pivot(index='investorId', columns='action', values='amount')

#portfolioTokenization()
#sys.exit()

from qore import QoreDebug
qdb = QoreDebug()
qdb.colorStacktraces()

import sys
try: sys.path.index('/ml.dev/bin/datafeeds')
except: sys.path.append('/ml.dev/bin/datafeeds')
#--------------------------

import pandas as p
import numpy as n
from qoreliquid import pf

import requests as req
import ujson as js
import datetime
from oandaq import OandaQ

import numpy as n
import calendar, datetime, time

import hashlib as hl
import hmac
import urllib
import httplib
import ujson as uj


def makeTimeseriesTimestampRange(timestamp=None, period=14400, bars=50):
        #print '---'
        #print 'timestamp:%s' % timestamp
        #print 'period:%s' % period
        #print 'bars:%s' % bars
        if timestamp == None:
            #tss = int(time.time())
            tss = time.time()
            timestamp = int(tss)
        else:
            tss = timestamp
        tsd = datetime.datetime.fromtimestamp(tss)
        tss = calendar.timegm([tsd.year,tsd.month,tsd.day,0,0,0,0,0,0])
        divisible = 60 * 60 * 24.0 / period
        a = list(n.arange(tss-period*(bars-1),tss+1, period))
        b = list(n.arange(tss, tss+period * (divisible+1), period, dtype=n.int))[1:]
        adf = p.DataFrame(a)
        adf['date2'] = OandaQ.timestampToDatetime_S(adf[0], utc=True)
        adf['date3'] = map(lambda x: timestamp-x, adf[0])
        bdf = p.DataFrame(b)
        adf = adf.set_index(0)
        bdf['date2'] = OandaQ.timestampToDatetime_S(bdf[0], utc=True)
        bdf['date3'] = map(lambda x: timestamp-x, bdf[0])
        bdf = bdf.set_index(0)
        cdf = adf.combine_first(bdf)
        with p.option_context('display.max_rows', 400, 'display.max_columns', 4000, 'display.width', 1000000):
            #print adf
            #print bdf
            #print cdf
            d2 = cdf[cdf['date3'] >= 0]
            #print d2
        c = a + b
        #print c
        #print len(c)-10
        #d = c[len(c)-bars+0:len(c)]
        d = list(d2.index[len(d2.index)-bars+0:len(d2.index)])
        #print d
        return {'start':d[0], 'end':d[len(d)-1], 'range':d, 'timestamp':timestamp, 'bars':bars, 'period':period}

class Poloniex:

    def __init__(self):
        self.btc = 'DASH ETH FCT GNO LTC XMR REP XRP ZEC'.split(' ')
        self.periods = '1 5 15 30 60 240 14400'.split(' ')
        self.periods = [300, 900, 1800, 7200, 14400, 86400]
        #self.periods = [1, 5, 15, 30, 60, 3600, 14400, 86400]
        print self.periods

    def getPoloniexHistorical(self, symbol='BTC_XMR', period=14400, start=1405699200, end=9999999999, bars=15):
        import time,calendar
        ts = time.time()
        #print ts
        tsd = datetime.datetime.fromtimestamp(ts)
        #print tsd
        tss = calendar.timegm([tsd.year,tsd.month,tsd.day,0,0,0,0,0,0])
        start = tss
        
        #start = start - period
        oq = OandaQ()
        # doc: https://poloniex.com/support/api/
        tms = makeTimeseriesTimestampRange(timestamp=int(ts), period=period, bars=bars)
        start = tms['start']
        end = tms['end']
        url = 'https://poloniex.com/public?command=returnChartData&currencyPair=%s&start=%s&end=%s&period=%s' % (symbol, start, end, period)
        res = req.get(url)
        #res.text
        li = js.loads(res.text)
        try:
            df = p.DataFrame(li)
        except:
            df = p.DataFrame(li, index=[0])
        df['date2'] = oq.timestampToDatetime_S(df['date'], utc=True)
        with p.option_context('display.max_rows', 40, 'display.max_columns', 4000, 'display.width', 1000000):
            #print df.head(5)
            #print df.tail(5)
            #print df
            #print len(df.index)
            ''
        return df

    def viewHistoricalPricePoloniex(self):
        from matplotlib import pyplot as plt
        from pylab import rcParams
        import seaborn as sns
        sns.set()
        #%pylab inline
        rcParams['figure.figsize'] = 30, 5
        df = pl.getPoloniexHistorical(symbol='BTC_ETC', period=86400, bars=300)
        df.ix[:, 'open high low close'.split(' ')].plot()
        #df = pl.getPoloniexHistorical(symbol='BTC_ETC', period=240)
        #df.ix[:, 'open high low close'.split(' ')].plot()
        plt.show()
    
    def viewChartsPoloniex(self):
        from matplotlib import pyplot as plt
        from pylab import rcParams
        import seaborn as sns
        sns.set()
        #%pylab inline
        rcParams['figure.figsize'] = 30, 5
        btc_usd = 2400
        for i in self.btc:
            print i
            df = pl.getPoloniexHistorical(symbol='BTC_%s' % i, period=300, bars=300)
            mdfp = df.ix[:, 'open high low close'.split(' ')]
            mdfp = mdfp.ix[:, :] * btc_usd
            print mdfp.head(10)
            mdfp.plot()
            plt.show()
            print '====='

def currencyCube(r=None,tf=None, c=None,d=None, index=None, columns=None, rdf=None):
    #r = 550 #rows history
    #c = 40   #columns currencypairs
    #d = 9  # depth fields [open, high, low, close...]
    #e = 9

    #rdf = n.zeros([c,r,d])
    #rf = []
    # 
    #for i in range(d): rf.append(n.random.randn(r,c))
    # 
    #for i in range(d): rdf[:,:,i] = rf[i][:,:].T
    #print rdf
    #p.DataFrame(rdf[:,:,0].T).head(5)

    # 
    #for i in range(c): rf.append(n.random.randn(r,d))

    # 
    #for i in range(c): rdf[i,:,:] = rf[i][:,:]
    print rdf.shape
    if rdf != None:
        try:
            print rf.shape
            print rf
            print rdf
            for i in range(c): rdf[i,:,:] = rf[i][:,:]
        except:
            ''

    #print rdf
    with p.option_context('display.max_rows', 400, 'display.max_columns', 4000, 'display.width', 1000000):
        if rdf != None:
            for i in range(rdf.shape[0]):
                print p.DataFrame(rdf[i,:,:].T, index=columns, columns=index).transpose().head(5)
        #print p.DataFrame(rdf[39,:,:].T).transpose().head(5)
        ''
    return {'data':rdf, 'index':index, 'columns':columns}

def getCurrencies():
    # all currencies

    #$x('//table[@id="marketBTC"]//td[2]/text()')
    btc = ["XRP", "STR", "ETH", "LTC", "ETC", "XMR", "DGB", "DASH", "FCT", "DOGE", "BTS", "XEM", "GNO", "SC", "GNT", "ZEC", "STEEM", "MAID", "PASC", "SYS", "LSK", "CLAM", "STRAT", "DCR", "XCP", "REP", "NXT", "POT", "FLDC", "VTC", "NAV", "PINK", "ARDR", "GAME", "BCN", "BURST", "VRC", "BELA", "AMP", "SJCX", "LBC", "XBC", "PPC", "XVC", "GRC", "NAUT", "BTM", "OMNI", "BCY", "EXP", "EMC2", "SBD", "NOTE", "HUC", "VIA", "BLK", "NMC", "XPM", "RIC", "NXC", "RADS", "NEOS", "FLO", "BTCD"]
    #$x('//table[@id="marketETH"]//td[2]/text()')
    eth = ["GNO", "ETC", "GNT", "ZEC", "REP", "STEEM", "LSK"]
    #$x('//table[@id="marketXMR"]//td[2]/text()')
    xmr = ["LTC", "ZEC", "DASH", "NXT", "MAID", "BCN", "BTCD", "BLK"]
    #$x('//table[@id="marketUSDT"]//td[2]/text()')
    usdt = ["BTC", "XRP", "STR", "LTC", "ETH", "ETC", "XMR", "DASH", "ZEC", "NXT", "REP"]

    #df = getPoloniexHistorical('BTC_XMR')

    lss = []
    #btc = 'ETH BURST XMR SC'.split(' ')
    for i in range(len(btc)):
        lss.append('BTC_%s' % btc[i])
    #lss = ['BTC_ETC', 'BTC_ETH']
    #print lss
    return lss

def currencyChartOverlay():
    from qoreliquid import normalizeme
    from qoreliquid import sigmoidme
    import matplotlib.pylab as plt
    mdf = p.DataFrame()
    for i in lss[0:5]:
        try:
            print i
            df = pl.getPoloniexHistorical(symbol=i, period=14400, bars=300)
            sdf = df.set_index('date').ix[:, 'close'.split(' ')]
            sdf[i] = sdf['close']
            sdf = sdf[[i]]
            sdf = sdf.ffill().bfill()
            mdf = mdf.combine_first(sdf)
        except KeyboardInterrupt as e:
            break
            print e
    mdf = normalizeme(mdf)
    #mdf.ffill().bfill()
    #print mdf
    #sdf.plot()
    import seaborn as sns
    sns.set()
    plt.plot(mdf)
    plt.legend(lss)
    plt.show()

def instrumentIndecesBitmex():
    # bitmex
    import drest
    #api = drest.API('http://socket.coincap.io/')
    api = drest.API('https://www.bitmex.com/api/v1')
    #response = api.make_request('GET', '/trade?count=100&reverse=false')
    #response = api.make_request('GET', '/instrument')
    response = api.make_request('GET', '/instrument/indices')
    #print response.data

    df = p.DataFrame(response.data)#.transpose()
    #pf(df)
    return df

#import drest
import ujson as uj
import requests as req, requests_cache
#@profile
def apiRequest(baseurl, query, method='GET', noCache=False):
    #api = drest.API(baseurl)
    #response = api.make_request(method, query)
    #res = response.data
    
    backend='sqlite'
    #backend='memory'

    if noCache == False:
        print '[caching] %s: %s %s' % (method, baseurl, query)
        expire_after = 3600 * 24 #* 365
        # source: https://stackoverflow.com/questions/27118086/maintain-updated-file-cache-of-web-pages-in-python
        requests_cache.install_cache('scraper_cache', backend=backend, expire_after=expire_after)
    else:
        print '[getting] %s: %s %s' % (method, baseurl, query)
        requests_cache.install_cache('scraper_cache', backend='sqlite', expire_after=300)
    #else:
    #    expire_after = 1

    #baseurl = 'http://api.coinmarketcap.com/'
    #method  = '/v1/ticker/'
    #api = drest.API(baseurl)
    #response = api.make_request(method, query)
    #res = response.data
    #try: 
    resp = req.get('%s%s' % (baseurl, query))
    res = uj.loads(resp.text)
    #except ConnectionError as e:
    #    ''
    return res

class CoinMarketCap:
    
    def  __init__(self):
        from qore import XPath
        self.xp = XPath()
        # cypto api 
        self.exchangePriority = {
            'Bittrex':3,
            'Cryptopia':1,
            'Novaexchange':2,
            'Poloniex':5,
            'YoBit':4,
            'Livecoin':6,
            'Liqui':7,
            'HitBTC':8,
            'EtherDelta':9,
        }
        self.parseCoinMarketCapSkipTo = 0
        self.portfolioModelSelect = None
        self.symbolMapper = None
        self.symbolMap = {
            'SONM':'SNM',
            'GOOD':'∞',
        }
        self.resTicker = apiRequest('https://api.coinmarketcap.com', '/v1/ticker')#, noCache=True)
        pass

    #@profile
    def tickers(self):
        #import drest
        #api = drest.API('http://api.coinmarketcap.com/')
        #response = api.make_request('GET', '/v1/ticker/')
        #res = response.data
        res = apiRequest('http://api.coinmarketcap.com/', '/v1/ticker/')
    
        c = '24h_volume_usd available_supply id last_updated market_cap_usd name percent_change_1h percent_change_24h percent_change_7d price_btc price_usd rank symbol total_supply'.split(' ')    
    
        dfc = p.DataFrame(res)
        dfc = dfc.set_index('symbol')
        #with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
        #    print dfc
        self.dfc = dfc
        return dfc
    
    #@profile
    def getExchanges(self, coin):
        url = 'http://coinmarketcap.com/currencies/%s/' % coin
        #print 'getExchanges: %s' % url
        xresd = self.xp.xpath2df(url, {
            'source'       : '//tbody/tr/td[2]/a/text()',
            'pair'         : '//tbody/tr/td[3]/a/text()',
            'volume_24h'   : '//tbody/tr/td[4]/span/text()',
            'price'        : '//tbody/tr/td[5]/span/text()',
            'volume_pcnt'  : '//tbody/tr/td[6]/text()',
            'updated'      : '//tbody/tr/td[7]/text()',
        })
        df = p.DataFrame(xresd)
        df = p.DataFrame(df['source'].drop_duplicates())
        df[coin] = 1
        df = df.set_index('source')
        #print df.transpose()
        df = df.transpose()
        return df

    #@profile
    def check(self, checkTradableCoins=False):
        try: self.dfc
        except Exception as e:
            #print e
            self.tickers()
        
        if checkTradableCoins:
            try: self.tradableCoins
            except Exception as e:
                #print e
                self.parseCoinMarketCap()
        
    #@profile
    def parseCoinMarketCap(self, verbose=False):
        # coinmarketcap create portfolio
        # goes thru all coins on coinmarketcap
        import pandas as p
        dfxs = p.DataFrame();
        self.check()
        fname = '/tmp/exchanges.csv'
        try:
            dfxs = p.read_csv(fname, index_col=0)
        except:
            for i, v in enumerate(self.dfc['id']):#[0:20]:
                print '%s: %s' % (i, v);
                if i >= self.parseCoinMarketCapSkipTo:
                    dfxs = dfxs.combine_first(self.getExchanges(v))
            dfxs.to_csv(fname)
        #print dfxs.fillna(0)
        with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
            mostFrequentExchanges = p.DataFrame(dfxs.fillna(0).sum()).sort_values(by=0, ascending=False)
            mostFrequentExchanges['indx'] = range(len(mostFrequentExchanges.index), 0, -1)
            pdfxs = dfxs.ix[:, list(mostFrequentExchanges.index[0:5])].fillna(0)
            pdfxs = dfxs[dfxs.fillna(0).transpose().sum() > 0]#.fillna(0)
            tradableCoins = pdfxs.ix[:, list(mostFrequentExchanges.index)][pdfxs > 0]
    
            a1 = mostFrequentExchanges.ix[tradableCoins.columns, 'indx'].get_values()
            b1 = tradableCoins.fillna(0).get_values()
            c1 = b1 * a1
            tradableCoins.ix[:,:] = c1
            tradableCoins['exchangeId'] = n.max(c1, 1)

            if verbose:
                #print df
                print
                print 'list most frequent exchanges:'
                print mostFrequentExchanges
                print 
                print 'list tradableCoins:'
                print tradableCoins
                #print tradableCoins.transpose()
                print 
                print 'list coins that trade on most exchanges:'
                print p.DataFrame(dfxs.fillna(0).transpose().sum()).sort_values(by=0, ascending=False)
                #print pdfxs#.transpose()
        #df.index
        #df = df.combine_first(getExchanges('1337'))
        self.tradableCoins = tradableCoins

    #@profile
    def getTradableCoins(self):

        self.check(checkTradableCoins=True)
        
        df = self.dfc
        c = '24h_volume_usd available_supply id market_cap_usd name percent_change_24h percent_change_7d price_btc price_usd rank symbol total_supply'.split(' ')
        #print c
        #print df.dtypes
    
        # convert to numeric
        for i in c:
            try:    df[i] = p.to_numeric(df[i])
            except: ''
    
        # filter idea sourced from:
        # https://www.youtube.com/watch?v=JF3eXDbzmg0 @ 15:01
        #df = df[df['price_usd'] <= 0.1]
        df = df[df['24h_volume_usd'] >= 100000]
        try:
            df = df.drop('FEDS')
        except:
            ''
    
        df = df.ix[:, c]
        df = df.sort_values(by='24h_volume_usd', ascending=False)
        df = df.sort_values(by='percent_change_24h', ascending=False)
    
        self.df = df
        return df

    #@profile
    def generatePortfolio(self, bal=165.11):
        try:
            self.df
        except:
            self.getTradableCoins()
        df = self.df

        pm = PortfolioModeler()
        if self.portfolioModelSelect:
            pm.model = self.portfolioModelSelect
        pm.modelCoinMarketCap(df, bal=bal)

        c = '24h_volume_usd id market_cap_usd name percent_change_24h percent_change_7d price_btc price_usd portPcnt portPcntPinv portPcntPinv2 portAmount_usd portAmount_units'.split(' ')
        c = '24h_volume_usd name percent_change_24h percent_change_7d price_usd portPcnt portPcntPinv portPcntPinv2 portAmount_usd portAmount_units'.split(' ')

        # tradableCoins2
        tradableCoins = self.tradableCoins
        #print list(tradableCoins.index)
        tradableCoins2 = df.set_index('id').ix[list(tradableCoins.index), c]
        tradableCoins2 = tradableCoins2.combine_first(tradableCoins)
        tradableCoins2 = tradableCoins2[tradableCoins2['portAmount_units'] > 0].sort_values(by='portAmount_units', ascending=False)
    
        with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
            print '            PortfolioModeler: %s' % pm.version
            print '            bal: %s' % bal
            print '   price_usdSUM: %s' % df['price_usd'].sum()
            print '    portPcntSUM: %s [assert =1]' % df['portPcnt'].sum()
            print 'portPcntPinvSUM: %s' % df['portPcntPinv'].sum()
            print 'portAmount_usdSUM: %s' % tradableCoins2['portAmount_usd'].sum()
            print 'portAmount_unitsSUM: %s' % df['portAmount_units'].sum()
            try:
                print 'portAmount_usd_YoBit_SUM: %s' % tradableCoins2[tradableCoins2['YoBit'] == 1]['portAmount_usd'].sum()
            except:
                ''
    
            #tradableCoins2['Poloniex'] = tradableCoins2['Poloniex'] - tradableCoins2['YoBit']
            #print tradableCoins2[tradableCoins2['YoBit'] == 1]
            #print tradableCoins
            #print tradableCoins2
    
            #print df
            #print df.ix[:, c]
    
        #df = p.DataFrame(response.data)#.transpose()
        #pf(df)
        #df    print list(tradableCoins.index)
        self.tradableCoins  = tradableCoins
        self.tradableCoins2 = tradableCoins2

        df = df.sort_values(by='portPcntPinv2', ascending=False)
        df['symbol'] = df.index
        df = df.set_index('id')
        df = tradableCoins.combine_first(df)
        """
        for i in df.index[0:10]:
            dfe = self.getExchanges(i)
            print dfe
            df = df.combine_first(dfe)
        """
        fc = ' '.join(self.exchangePriority.keys())
        c = ('symbol exchangeId 24h_volume_usd name available_supply total_supply at mv market_cap_usd percent_change_24h percent_change_7d price_usd price_btc portPcnt portPcntPinv portPcntPinv2 portAmount_usd portAmount_units %s'%fc).split(' ')
        #c = 'name price_usd portPcntPinv2 portAmount_usd portAmount_units Poloniex YoBit'.split(' ')
        with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
            sb = '24h_volume_usd portAmount_usd mv market_cap_usd'.split(' ')[1]
            dfv = df.fillna(0).ix[:, c].sort_values(by=sb, ascending=False)
            dfv = dfv[dfv['24h_volume_usd'] > 0]
            print dfv
            pm.dfv = dfv
            pm.to_cointracking()
            try:
                import dfgui # https://github.com/bluenote10/PandasDataFrameGUI
                dfgui.show(dfv)
            except: ''
        #print xresd
        #print p.DataFrame(xresd)
        self.df = df
        return df

    #@profile
    def getTicker(self, symbol):
        df = p.DataFrame(self.resTicker)
        self.symbolMapper = df.loc[:, 'symbol id'.split()].set_index('symbol')
        #with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
        #    print self.symbolMapper.sort_index()
        #return
        
        try:
            ticker = self.symbolMapper.loc[symbol, 'id']
            res = apiRequest('https://api.coinmarketcap.com', '/v1/ticker/%s/' % ticker, noCache=True)
            res = p.DataFrame(res)
            #print res.transpose()
            return res
        except:
            ''


class PortfolioModeler:
    
    def __init__(self):
        self.version = 'v0.0.1'
        self.models = {
            1: 'Q001aa',
            2: 'Q001a',
            3: 'Q001',
        }
        self.model   = None
    
    def listModels(self):
        for i in self.models.keys():
            print '\t%s: %s' % (i, self.models[i])

    def setModel(self, select=None):
        if self.model == None:
            print 'models:'
            for i in self.models.keys():
                print '\t%s: %s' % (i, self.models[i])
            try:
                self.model = int(raw_input('model: '))
                self.model = self.models[self.model]
            except KeyboardInterrupt as e:
                sys.exit('')
    
    def to_cointracking(self):
        #df = self.dfv.ix[:,'Type Buy Cur. Sell Cur. Fee Exchange Group Comment Date name symbol price_usd portPcntPinv2 portAmount_usd portAmount_units'.split(' ')]
        df = self.dfv.ix[:,'Type Buy Cur. Sell Cur. Fee Exchange Group Comment Date symbol portAmount_units'.split(' ')]
        df['Type']      = '-IN-'
        df['Buy']       = df['portAmount_units']
        df['Cur.']      = df['symbol']
        df['Sell']      = df['symbol']
        #df['Cur.']      = df['']
        #df['Fee']       = df['']
        #df['Cur.']      = df['']
        #df['Exchange']  = df['']
        #df['Group']     = df['']
        #df['Comment']   = df['']
        #df['Date']      = df['']
        print df
        df.to_csv('/tmp/portfolio.cointracking.csv', sep=' ', index=False)
        

    def modelCoinMarketCap(self, df, bal=100):
        ### ----------------------------------------------------------------------------
        # portfolio model
        ### ----------------------------------------------------------------------------
        self.setModel()
        c = '24h_volume_usd id market_cap_usd name percent_change_24h percent_change_7d price_btc price_usd portPcnt portPcntPinv portPcntPinv2 portAmount_usd portAmount_units'.split(' ')
        c = '24h_volume_usd name percent_change_24h percent_change_7d price_usd portPcnt portPcntPinv portPcntPinv2 portAmount_usd portAmount_units'.split(' ')
        if self.model == 'Q001aa':
            df['portPcnt']         =      df['price_usd'] / df['price_usd'].sum() * 1
        if self.model == 'Q001a':
            df['portPcnt']         =      (df['24h_volume_usd'] / df['price_usd']) / ((df['24h_volume_usd'] / df['price_usd'])).sum() * 1
        if self.model == 'Q001':
            df['price_per_24h_volume_usd'] = df['price_usd'] / df['24h_volume_usd']
            df['portPcnt']                 = df['price_per_24h_volume_usd'] / df['price_per_24h_volume_usd'].sum() * 1
        #df['portPcntPinv']     =   1 - df['portPcnt']
        df['portPcntPinv']     =   1 / df['portPcnt'] # df['portPcnt']
        df['portPcntPinv2']    =   df['portPcntPinv'] / df['portPcntPinv'].sum() * 100
        df['portAmount']       =  df['portPcntPinv2'] * bal / 100
        df['portAmount_usd']   =  df['portPcntPinv2'] * bal / 100
        df['portAmount_units'] = df['portAmount_usd'] / df['price_usd']
        df['at'] = df['available_supply'] / df['total_supply']
        df['mv'] = df['24h_volume_usd'] / df['market_cap_usd']
        ### ----------------------------------------------------------------------------

        df = df.sort_values(by='portPcntPinv2', ascending=False)
        #return

class TokenMarket:
    
    def  __init__(self):
        import pandas as p
        import numpy as n
        from qore import XPath
        import pandas as p
        self.xp = XPath()
        self.allAssetsICOsBlockchain = p.DataFrame()
        pass

    def allAssetsBlockchainTokenMarket(self):
    
        #def tokenmarket():
        #"""
        import re
        xresd = self.xp.xpath2df('https://tokenmarket.net/blockchain/all-assets', {
            'name'       : '//*[@id="table-all-assets-wrapper"]/table/tbody/tr/td[4]/div[1]/a/text()',
            'href'       : '//*[@id="table-all-assets-wrapper"]/table/tbody/tr/td[4]/div[1]/a/@href',
            #'status'     : '//*[@id="table-all-assets-wrapper"]/table/tbody/tr/td[3]/span/text()',
            'symbol'     : '//*[@id="table-all-assets-wrapper"]/table/tbody/tr/td[5]/text()',
            'description': '//*[@id="table-all-assets-wrapper"]/table/tbody/tr/td[6]/text()',
            #'hot': '//*[@id="table-all-assets-wrapper"]/table/tbody/tr/td[4]/div[2]/text()',        
        })
        #print xresd
        #"""
        df = p.DataFrame(xresd)
        li = 'name href symbol description'.split()
        for i in li:
            df[i] = map(lambda x: x.strip(), df[i])
        #df['href'] = map(lambda x: x.replace('https://tokenmarket.net/blockchain/ethereum/assets/', ''), df['href'])
        df['type'] = map(lambda x: re.sub(re.compile(r'https.*?\/blockchain\/(.*?)\/.*'), '\\1', x), df['href'])
        #df['tmid'] = map(lambda x: re.sub(re.compile(r'https.*\/assets\/(.*?)\/'), '\\1', x), df['href'])
        #df = p.DataFrame(df['name'].drop_duplicates())
        #df[coin] = 1
        #df = df.set_index('name')
        #print df.transpose()
        df = df#.transpose()
        #return df
        with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
            #print df
            #print df#.sort_values(by='type')
            pass
        self.allAssetsICOsBlockchain = df
        return self.allAssetsICOsBlockchain
    
    def tokenICOsTokenMarket(self):
        
        import re
        self.dfp = self.allAssetsICOsBlockchain
        nn = 66
        lili = self.dfp.index#[nn:nn+5]
        for i in lili:#[0:5]:
    
            url = '%s' % self.dfp.ix[self.dfp.index[i], 'href'] 
            print '%s %s' % (i, url)
            #"""
            xresd = self.xp.xpath2df(url, {
                'name'             : '//*[@id="page-wrapper"]/main/div[2]/div[3]/div[1]/h1/text()[2]',
                'symbol'           : '//*[@id="page-wrapper"]/main/div[2]/div[4]/div[1]/table[1]//tr[1]/td/text()',
                'trading'          : '//*[@id="page-wrapper"]/main/div[2]/div[4]/div[1]/table[1]//tr[2]/td/span/text()[2]',
                'links-website'    : '//*[@id="page-wrapper"]/main/div[2]/div[4]/div[2]/div[1]/table//tr[1]/td/a/@href',
                'links-blog'       : '//*[@id="page-wrapper"]/main/div[2]/div[4]/div[2]/div[1]/table//tr[2]/td/a/@href',
                'links-whitepaper' : '//*[@id="page-wrapper"]/main/div[2]/div[4]/div[2]/div[1]/table//tr[3]/td/a/@href',
                'links-facebook'   : '//*[@id="page-wrapper"]/main/div[2]/div[4]/div[2]/div[1]/table//tr[4]/td/a/@href',
                'links-twitter'    : '//*[@id="page-wrapper"]/main/div[2]/div[4]/div[2]/div[1]/table//tr[5]/td/a/@href',
                'links-linkedin'   : '//*[@id="page-wrapper"]/main/div[2]/div[4]/div[2]/div[1]/table//tr[6]/td/a/@href',
                'links-slack'      : '//*[@id="page-wrapper"]/main/div[2]/div[4]/div[2]/div[1]/table//tr[7]/td/a/@href',
                'links-telegram'   : '//*[@id="page-wrapper"]/main/div[2]/div[4]/div[2]/div[1]/table//tr[8]/td/a/@href',
                'links-github'     : '//*[@id="page-wrapper"]/main/div[2]/div[4]/div[2]/div[1]/table//tr[9]/td/a/@href',
                'domain-score'     : '//*[@id="page-wrapper"]/main/div[2]/div[4]/div[2]/table[1]//tr[1]/td/text()[1]',
                #'backlinks'        : '//*[@id="page-wrapper"]/main/div[2]/div[4]/div[2]/table[2]//tr[2]/td/text()[1]',
                'backlinks'        : '//*[@id="page-wrapper"]/main/div[2]/div[4]/div[2]/table[1]//tr[2]/td/text()[1]',
                'github-starredby' : '//*[@id="page-wrapper"]/main/div[2]/div[4]/div[1]/div[3]/table//tr[1]/td/text()',
                'github-watchings' : '//*[@id="page-wrapper"]/main/div[2]/div[4]/div[1]/div[3]/table//tr[2]/td/text()',
                'github-contributors' : '//*[@id="page-wrapper"]/main/div[2]/div[4]/div[1]/div[3]/table//tr[2]/td/text()',
                'github-forks'        : '//*[@id="page-wrapper"]/main/div[2]/div[4]/div[1]/div[3]/table//tr[3]/td/text()',
                'github-commits'      : '//*[@id="page-wrapper"]/main/div[2]/div[4]/div[1]/div[3]/table//tr[4]/td/text()',
                'github-openIssues'   : '//*[@id="page-wrapper"]/main/div[2]/div[4]/div[1]/div[3]/table//tr[5]/td/text()',
                'crowdsale-opening-date' : '//*[@id="page-wrapper"]/main/div[2]/div[4]/div[1]/table[1]//tr[2]/td/p[1]/text()',
                'crowdsale-closing-date' : '//*[@id="page-wrapper"]/main/div[2]/div[4]/div[1]/table[1]//tr[3]/td/p[1]/text()',

            })#, expire=1)
            #"""
            xresdlen = {}
            for j in xresd:
                xresdlen[j] = len(xresd[j])
            xresdlen = p.DataFrame(xresdlen, index=['len']).transpose()
            xresdlen['max'] = n.max(xresdlen['len'])
            xresdlen['diff'] = xresdlen['max'] - xresdlen['len']
            #print xresdlen
            #print xresd
            for j in xrange(len(xresdlen['diff'])):
                try:
                    #print '%s %s' % (j, xresdlen['diff'][j])
                    if xresdlen['diff'][j] > 0:
                        #print j
                        #xresdlen = xresdlen.drop(xresdlen.index[j])
                        xresd.pop(xresdlen.index[j])
                        #print p.DataFrame(xresd)
                except:
                    ''
            #print xresdlen
            #print xresd
            dftm = p.DataFrame(xresd, index=[i])
            li = 'name backlinks domain-score github-starredby github-commits github-contributors github-forks github-openIssues github-watchings crowdsale-opening-date crowdsale-closing-date'.split()
            #backlinks domain-score
            #links-blog links-facebook links-github links-twitter links-website links-whitepaper name symbol trading    
            for j in li:
                try:    dftm[j] = map(lambda x: x.strip(), dftm[j])
                except: ''
            # dates
            for j in dftm.index:
                try: dftm.loc[j, 'crowdsale-opening-date-ts'] = datetime.datetime.strptime(dftm.loc[j, 'crowdsale-opening-date'], '%d. %b %Y')
                except Exception as e: ''#print e
                try: dftm.loc[j, 'crowdsale-closing-date-ts'] = datetime.datetime.strptime(dftm.loc[j, 'crowdsale-closing-date'], '%d. %b %Y')
                except Exception as e: ''#print e
                try: dftm.loc[j, 'crowdsale-days'] = (dftm.loc[j, 'crowdsale-closing-date-ts'] - dftm.loc[j, 'crowdsale-opening-date-ts']).days
                except Exception as e: ''#print e
                try: dftm.loc[j, 'crowdsale-days-to-close'] = (datetime.datetime.now() - dftm.loc[j, 'crowdsale-closing-date-ts']).days
                except Exception as e: ''#print e

            self.dfp = self.dfp.combine_first(dftm)
            with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
                #print dftm#.transpose()
                #print dftm.transpose()
                ''
            #break


    def underTheRadarTokens(self):
        # TokenMarket [UnderTheRadar Tokens]
        #self.allAssetsBlockchainTokenMarket()
        #dfp = self.allAssetsICOsBlockchain
        #with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
        #    print self.dfp
        dfp = self.dfp
        #self.dfp.to_csv('tokenmarket.csv', encoding='utf8')
        fi = 'name symbol trading type backlinks domain-score links-blog links-facebook links-github links-twitter links-website links-whitepaper github-starredby github-commits github-contributors github-forks github-openIssues github-watchings crowdsale-opening-date-ts crowdsale-closing-date-ts crowdsale-days crowdsale-days-to-close'
        li = 'backlinks domain-score github-starredby github-commits github-contributors github-forks github-openIssues github-watchings crowdsale-opening-date crowdsale-closing-date'.split(' ')
        dfp = dfp.fillna(0)
        for i in li:
            try: dfp[i] = p.to_numeric(dfp[i])
            except Exception as e: 
                #print '%s %s' % (i,e)
                ''
        #print dfp.dtypes
        with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
            dfm = dfp.ix[:, fi.split()].sort_values(by='github-starredby')
            #print dfm
            ''
            df1 = self.allAssetsICOsBlockchain.set_index('name')
            df1['symbol'] = self.allAssetsICOsBlockchain.index
            dfm = dfm.set_index('name').combine_first(df1)
            #print ' '.join(list(dfm.columns))
            ff = '24h_volume_usd available_supply backlinks domain-score github-commits github-contributors github-forks github-openIssues github-starredby github-watchings id last_updated links-blog links-facebook links-github links-twitter links-website links-whitepaper market_cap_usd name percent_change_1h percent_change_24h percent_change_7d price_btc price_usd rank total_supply trading type'
            ff = 'symbol 24h_volume_usd available_supply backlinks domain-score github-commits github-contributors github-forks github-openIssues github-starredby github-watchings id last_updated market_cap_usd name percent_change_1h percent_change_24h percent_change_7d price_btc price_usd rank total_supply trading type'
            ff = 'X3 X X2 symbol backlinks domain-score github-commits github-contributors github-forks github-openIssues github-starredby github-watchings id  links-github type crowdsale-opening-date crowdsale-closing-date'
            def numerix(arr):
                arr = map(lambda x: 0 if x == 'None' else x, arr)
                arr = p.to_numeric(arr)
                return arr    
            dfm['github-commits'] = numerix(dfm['github-commits'])
            dfm['github-contributors'] = numerix(dfm['github-contributors'])
            dfm['github-forks'] = numerix(dfm['github-forks'])
            dfm['github-openIssues'] = numerix(dfm['github-openIssues'])
            #"""
            def div0( a, b ):
                "#"" ignore / 0, div0( [-1, 0, 1], 0 ) -> [0, 0, 0] "#""
                with n.errstate(divide='ignore', invalid='ignore'):
                    #c = n.true_divide( a, b )
                    #c[ ~ n.isfinite( c )] = 0  # -inf inf NaN
                    #c = n.true_divide(a,b)
                    #c = n.divide(a, b, out=n.zeros_like(a), where=b!=0)
                    #c[c == n.inf] = 0
                    #c = n.nan_to_num(c)
                    return c
            #dfm['X'] = div0(dfm['github-commits'].get_values(), dfm['github-contributors'].get_values())
            #"""
            dfm['X']  = dfm['github-commits'].get_values()    / dfm['github-contributors'].get_values()
            #dfm['X2'] = dfm['domain-score'].get_values()) * dfm['github-openIssues'].get_values() / dfm['github-forks'].get_values()
            dfm['X2'] = n.log(dfm['backlinks'].get_values() * dfm['domain-score'].get_values()) * dfm['github-openIssues'].get_values() / dfm['github-forks'].get_values()
            #dfm['X3'] = dfm['X2'].get_values()                / dfm['X'].get_values()
            dfm['X3'] = dfm['X2'].get_values()                / dfm['X'].get_values()
            
            from qoreliquid import normalizeme
            dfm['X4'] = (n.log(dfm['backlinks'].get_values()))
            #* dfm['domain-score'].get_values()))

            dfm = dfm[dfm['type'] == 'ethereum']
            dfm = dfm[dfm['crowdsale-days-to-close'] > 0]
            
            #sortby='github-commits'
            sortby='X3'
            #print dfm.dtypes
            dfr = dfm
            print dfr.sort_values(by='X3', ascending=False)
            for i in dfr[dfr['github-commits'] == 10].index: dfr = dfr.drop(i)
            dfr = dfr.ix[:,ff.split(' ')].fillna(0).sort_values(by=sortby, ascending=False)
            ff = 'symbol X3 weight crowdsale-days-to-close' # to publish
            dfr = dfm.ix[:,ff.split(' ')].fillna(0).sort_values(by=sortby, ascending=False)
            for i in dfr[dfr['X3'] == n.inf].index: dfr = dfr.drop(i)

            dfr = dfr.head(10)

            dfr['potentialPortfolioWeight'] = dfr['X3'] / dfr['X3'].sum()
            print dfr
    
            import datetime, time
    
            # UnderTheRadar Suggestions
            print '== UnderTheRadar::tokens [%s]' % datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d')
            print '====================================='
            print
            print '== OpenSource Token Suggestions:'
            print '== FutureTokens  [Untradable::pre&postICO]'
            print
            print dfr.ix[:,['potentialPortfolioWeight']]#.head(20)
            print
            print 'note: Some tokens are pre-ICO, therefore not yet on the market.'
            print '      They are, however, worth looking into.'
    
            #dfr2 = dfr.ix[:,['potentialPortfolioWeight']].head(20)
            #dfr2['name'] = dfr2.index
            #print dfr2.ix[:,'name potentialPortfolioWeight'.split()].get_values()
            #print ",".join(dfr2.get_values())
    
            print
            print
            print
            print '== Closed Source Token Suggestions:'
            print '== FutureTokens  [Untradable::pre&postICO]'
            print
            print '   [Stay tuned]'
            print
    
            print '== PresentTokens [Untradable::pre&postICO]'
            print
            print '   [Stay tuned]'
            print
            #print df
            #print dfp
            #print df#.ix[:, 'id'].sort_index()
            #print dfp.ix[:, 'name symbol'.split(' ')].sort_values(by='symbol')
        #print dfp.ix[:, fi.split()].sort_values(by='github-starredby')']
            #24h_volume_usd available_supply backlinks domain-score github-commits github-contributors github-forks github-openIssues github-starredby github-watchings id last_updated links-blog links-facebook links-github links-twitter links-website links-whitepaper market_cap_usd name percent_change_1h percent_change_24h percent_change_7d price_btc price_usd rank total_supply trading type
        #print dfp.ix[:, fi.split()].sort_values(by='github-starredby')

    def tokenmarket(self):
        dfp = self.allAssetsICOsBlockchain
        #"""
        import re
        xresd = self.xp.xpath2df('https://tokenmarket.net/blockchain/all-assets', {
            'name'       : '//*[@id="table-all-assets-wrapper"]/table//tr/td[4]/div[1]/a/text()',
            'href'       : '//*[@id="table-all-assets-wrapper"]/table//tr/td[4]/div[1]/a/@href',
            #'status'     : '//*[@id="table-all-assets-wrapper"]/table//tr/td[3]/span/text()',
            #'status'     : '//*[@id="table-all-assets-wrapper"]/table//tr/td[3]/span',
            #'status'     : '//*[@id="table-all-assets-wrapper"]/table//tr/td[3]//text()',
            'symbol'     : '//*[@id="table-all-assets-wrapper"]/table//tr/td[5]/text()',
            'description': '//*[@id="table-all-assets-wrapper"]/table//tr/td[6]/text()',
            #'hot': '//*[@id="table-all-assets-wrapper"]/table/tbody/tr/td[4]/div[2]/text()',        
        })
        for i in xresd.keys(): print '%s' % len(xresd[i])
        #print xresd
        #"""
        
        df = p.DataFrame(xresd)
        li = 'name href symbol description'.split()
        for i in li:
            df[i] = map(lambda x: x.strip(), df[i])
        #df['href'] = map(lambda x: x.replace('https://tokenmarket.net/blockchain/ethereum/assets/', ''), df['href'])
        df['href'] = map(lambda x: re.sub(re.compile(r'https.*\/assets\/'), '', x), df['href'])
        #df = p.DataFrame(df['name'].drop_duplicates())
        #df[coin] = 1
        #df = df.set_index('name')
        #print df.transpose()
        df = df#.transpose()
        #with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
        #    print df
        return df

class Exchange:

    def __init__(self, key, secret, exchange):
        self.debug = False
        self.key    = key.strip()
        self.secret = secret.strip()
        self.exchange = exchange.strip()

    def debugon(self):
        self.debug = True

    def signHMAC512(self, params=None, msg=None):
        #p1 = {'a':'1', 'b':'2'}
        #p1 = params
        #p1.update({'nonce':str(1)})
        #li = []
        #for i in zip(p1.keys(), p1.values()):
        #    li.append('='.join(i))
        #p1p = '&'.join(li)
        #ahash = hm.sha512(p1p)
        #return ahash.hexdigest()
        if self.exchange == 'liqui':
            H = hmac.new(self.secret, digestmod=hl.sha512)
            #params = urllib.urlencode(params)
            H.update(params)
            return H.hexdigest()
        if self.exchange == 'bittrex':
            H = hmac.new(self.secret.encode(), msg.encode(), hl.sha512)
            #print 'msg: %s' % msg
            return H.hexdigest()

    #def getResponse():
    
    def requestAuthenticated(self, method=None, url=None, params={}, requestType='POST'):
        if method:
            params.update({'method':method})
        if self.exchange == 'liqui':
            nonce = str(1)
        if self.exchange == 'bittrex':
            nonce = str(int(time.time() * 1000))
        params.update({'nonce':nonce})
        params = urllib.urlencode(params)

        if self.exchange == 'liqui':
            headers = {'Content-type': 'application/x-www-form-urlencoded',
                      'Key':  self.key,
                      'Sign': self.signHMAC512(params=params)}
        if self.exchange == 'bittrex':
            headers = {'apisign': self.signHMAC512(msg='https://bittrex.com' + url)}

        conn = httplib.HTTPSConnection(self.apiServer)
        if url:
            conn.request(requestType, url, params, headers)
        else:
            conn.request(requestType, self.apiMethod, params, headers)
        response = conn.getresponse()

        if self.debug:
            print response.msg
            print response.status
            print response.reason
            #print res

            #print dir(response)

            print 'params:'
            print params
            print
            print 'headers:'
            print headers

        try:
            data = uj.load(response)
        except Exception as e:
            #print e
            data = uj.loads(response.read())
        try:
            if self.debug:
                print data
            return data
        except Exception as e:
            print
            print e

class Liqui(Exchange):
    
    def __init__(self, key, secret):
        Exchange.__init__(self, key, secret, exchange='liqui')
        self.apiServer = 'api.liqui.io'
        self.apiMethod = '/tapi'

    def getInfo(self):
        data = self.requestAuthenticated('getInfo')
        df = p.DataFrame(data['return'])#.transpose()
        #pf(df)
        return df

    def tradeHistory(self):
        data = self.requestAuthenticated('TradeHistory')
        df = p.DataFrame(data['return'])#.transpose()
        #pf(df)
        return df.transpose()

    def trade(self, pair=None, mtype=None, rate=None, amount=None):
        params =   {'pair':pair,
                    'type':mtype,
                    'rate':rate,
                    'amount':amount}
        data = self.requestAuthenticated('Trade', params)
        df = p.DataFrame(data['return'])#.transpose()
        #pf(df)
        return df.transpose()

class OpenLedger:
    ''

class Bittrex(Exchange):

    def __init__(self, key, secret):
        Exchange.__init__(self, key, secret, exchange='bittrex')
        self.apiServer = 'bittrex.com' # https://bittrex.com/api/v1.1/account/getbalances?apikey=apikey
        self.apiMethod = '/api/v1.1'

    def getInfo(self):
        data = self.requestAuthenticated(url='%s/account/getbalances?apikey=%s&nonce=1' % (self.apiMethod, self.key), requestType='GET')
        try:
            df = p.DataFrame(data['result'])#.transpose()
            return df
        except Exception as e:
            print e

    def getCurrencies(self):
        data = self.requestAuthenticated(url='%s/public/getcurrencies?apikey=%s&nonce=1' % (self.apiMethod, self.key), requestType='GET')
        try:
            df = p.DataFrame(data['result'])#.transpose()
            return df
        except:
            ''

    def getDepositAddress(self, currency): # currency=BTC
        data = self.requestAuthenticated(url='%s/account/getdepositaddress?apikey=%s&currency=%s&nonce=1' % (self.apiMethod, self.key, currency), requestType='GET')
        try:
            df = p.DataFrame(data['result'])#.transpose()
            return df
        except:
            ''

    def getMarketSummaries(self):
        data = self.requestAuthenticated(url='%s/public/getmarketsummaries?apikey=%s&nonce=1' % (self.apiMethod, self.key), requestType='GET')
        try:
            df = p.DataFrame(data['result'])#.transpose()
            return df
        except:
            ''

    def getMarkets(self):
        data = self.requestAuthenticated(url='%s/public/getmarkets?apikey=%s&nonce=1' % (self.apiMethod, self.key), requestType='GET')
        try:
            df = p.DataFrame(data['result'])#.transpose()
            return df
        except:
            ''

#@profile
def getAdressInfoEthplorer(ethaddr, verbose=False, instruments=5, noCache=True, initialInvestment=0):
    
    if type(ethaddr) == type(''):
        ethaddr = ethaddr.split(' ')
    
    cmc = CoinMarketCap()
    eth = cmc.getTicker('ETH').set_index('symbol').transpose()
    ethusd = float(eth.loc['price_usd', 'ETH'])
    mdf0 = p.DataFrame([])
    dfp = modelPortfolio(num=instruments)
    mdf0 = mdf0.combine_first(dfp)
    addressInfos = p.DataFrame()
    dfinfo = p.DataFrame([])
    mdfs = {}
    
    # get all tokens to fill in missing data
    res = apiRequest('https://api.ethplorer.io', '/getTopTokens?limit=100&apiKey=freekey', noCache=noCache)
    ttdf = p.DataFrame(res['tokens'])
    ttdf = ttdf.set_index('symbol')
    #with p.option_context('display.max_rows', 400, 'display.max_columns', 4000, 'display.width', 1000000):
    #    print ttdf
    """
    liss = list(ttdf['address'])#.split(' ')
    for tokenAddress in liss:
        try:
            res = apiRequest('https://api.ethplorer.io', '/getTokenInfo/%s?apiKey=freekey' % tokenAddress, noCache=noCache)
            print res
        except: ''
    """

    for ea in ethaddr:
        ethaddrSmall = ea[0:7]
        #res = apiRequest('https://api.coinmarketcap.com', '/v1/ticker/')
        res = apiRequest('https://api.ethplorer.io', '/getAddressInfo/%s?apiKey=freekey' % ea, noCache=noCache)
        #res = apiRequest('https://api.ethplorer.io', '/getTokenInfo/0xff71cb760666ab06aa73f34995b42dd4b85ea07b?apiKey=freekey')
        res1 = p.DataFrame(res['ETH'], index=[ethaddrSmall])
        addressInfos = addressInfos.combine_first(res1)
        #res2 = p.DataFrame(res['tokens'], index=['tokens'])#.transpose()
        with p.option_context('display.max_rows', 400, 'display.max_columns', 4000, 'display.width', 1000000):
            # if tokens continue to next iteration [ie. ethaddr]
            try: res['tokens']
            except: continue
            if verbose:
                print p.DataFrame(res['tokens'][0])
            """
            print '=1=1=1=1=1'
            print res['tokens']
            for qwe in res['tokens']:
                print '---'
                df8 = p.DataFrame(qwe)
                df8.loc['balance123', 'tokenInfo'] = float(df8.loc['address', 'balance']) / pow(10, int(df8.loc['decimals', 'tokenInfo']))
                print df8
            print '=1=1=1=1=1'
            #print cmc.symbolMapper
            return
            """
        mdf    = p.DataFrame([])
        try:
            res['tokens']
        except:
            break
        for i in res['tokens']:
            avg = 0
            #print 'tokens: %s' % i
            df = p.DataFrame(i)#.transpose()
            decimals = float(df.loc['decimals', 'tokenInfo'])
            balance  = float(df.loc['address', 'balance']) / n.power(10, decimals)
            df['balance']  = map(lambda x: float(x) / n.power(10, decimals), df['balance'])
            df['totalIn']  = map(lambda x: float(x) / n.power(10, decimals), df['totalIn'])
            df['totalOut'] = map(lambda x: float(x) / n.power(10, decimals), df['totalOut'])
            df['ethaddr']  = ea
            symbol = df.loc['symbol', 'tokenInfo']
            try:
                df1    = cmc.getTicker(symbol).set_index('symbol').transpose()
                df1['tokenInfo'] = df1[df1.columns[0]]
                df = df.combine_first(df.loc[:, ['tokenInfo']].combine_first(df1.loc[:, ['tokenInfo']]))
            except Exception as e:
                print e
                ''
            try:    df.loc['24h_volume_marketcap_ratio', 'tokenInfo'] = float(df.loc['24h_volume_usd', 'tokenInfo']) / float(df.loc['market_cap_usd', 'tokenInfo']) * 100
            except: ''
            df.loc['balance', 'tokenInfo']     = balance
            with p.option_context('display.max_rows', 400, 'display.max_columns', 4000, 'display.width', 1000000):
                try:
                    dfp1 = dfp.transpose().loc[:, [symbol]]
                    dff1 =  df.loc[:, ['tokenInfo']].transpose().set_index('symbol').transpose()
                    dff1 = dff1.combine_first(dfp1)
                    dff1['tokenInfo'] = dff1[symbol]
                    #df22 = p.concat([dff1, df], axis=1)
                    #combineDF3(df.to_dict(), dff1.to_dict())
                    df = df.combine_first(dff1)
                    """
                    print '======4324234===='
                    print df.dtypes
                    print dff1.dtypes
                    print df22.dtypes
                    print df
                    print dff1
                    print df22
                    print df
                    print '======4324234====/'
                    return
                    """
                    df = df.drop(symbol, axis=1)
                    if verbose == True:
                        print '----'
                        print 'dfp1'
                        print dfp1
                        print
                        print 'dff1'
                        print dff1
                        print
                        print df
                except: ''
                #print '--123--'
                #print df
                #print '--123--'
            try:
                # some tokens barf as they do not quote a bid or offer
                #with p.option_context('display.max_rows', 400, 'display.max_columns', 4000, 'display.width', 1000000):
                #    print df
                #    print df.loc['avg', 'tokenInfo']
                #try: df.loc['avg', 'tokenInfo']
                #except: continue
                avg = df.loc['avg', 'tokenInfo']
            except Exception as e:
                #print e
                try: 
                    df.loc['price', 'tokenInfo']
                    dfPrice = p.DataFrame(df.loc['price', 'tokenInfo'], index=[0]).transpose()
                    dfPrice.loc['rateETH', 0] = dfPrice.loc['rate', 0] / ethusd
                    avg = dfPrice.loc['rateETH', 0]
                    print dfPrice
                    df.loc['price_usd', 'tokenInfo'] = dfPrice.loc['rate', 0]
                except Exception as e2:
                    print e2
                    #continue
                try: df.loc['price_usd', 'tokenInfo']
                except:
                    ''
                    #continue
                df.loc['price_usd', 'tokenInfo'] = avg #* ethusd
                #df.loc['price', 'tokenInfo'] = avg
                dfp = modelPortfolio(num=instruments)
                #df = df.combine_first(dfp)
                #df = genPortfolio(df)
                with p.option_context('display.max_rows', 400, 'display.max_columns', 4000, 'display.width', 1000000):
                    if verbose:
                        print '---/////6546456///---'
                        print df
                        print '---/////6546456///---/'
                df.loc['balance_usd', 'tokenInfo'] = float(df.loc['price_usd', 'tokenInfo']) * balance
            df.loc['balance_usd', 'tokenInfo'] = float(df.loc['balance', 'tokenInfo']) * float(avg) * ethusd
            df.loc[:, 'balance totalIn totalOut'.split(' ')]  = balance
            df.loc['ethaddr', 'tokenInfo']  = ethaddrSmall
            with p.option_context('display.max_rows', 400, 'display.max_columns', 4000, 'display.width', 1000000):
                #print '---'
                #print df1.columns
                #print df1
                #print type(df1)
                #print '---'
                #print df.dtypes
                #print df1
                #print df.loc[:, ['tokenInfo']]
                #print df1
                dfinfo = dfinfo.combine_first(df.loc['address decimals symbol'.split(' '), 'tokenInfo'.split(' ')].transpose().set_index('symbol'))
                if verbose:
                    print df.loc[:, 'tokenInfo'.split(' ')]#.transpose()
                else:
                    df.loc['id2', 'tokenInfo'] = '%s-%s' % (df.loc['symbol', 'tokenInfo'], df.loc['ethaddr', 'tokenInfo'])
                    dfpremdf = df.loc['symbol id2 id3 ethaddr 24h_volume_usd holdersCount issuancesCount price_btc price_usd rank balance balance_usd'.split(' '), 'tokenInfo'.split(' ')].transpose().set_index('symbol')
                    mdf = mdf.combine_first(dfpremdf)
                    #mdf = dfpremdf.combine_first(mdf)

                #print
            #res2 = p.DataFrame(res['tokens'])#.transpose()
        #if not verbose:

        # fill in missing data
        mdf0 = mdf0.combine_first(ttdf)

        mdf0 = mdf0.combine_first(mdf)
        mdfs.update({ea:mdf.loc[:, 'balance balance_usd ethaddr'.split(' ')].to_dict()})
        with p.option_context('display.max_rows', 400, 'display.max_columns', 4000, 'display.width', 1000000):
            ''
            symbolMapR = dict(zip(cmc.symbolMap.values(), cmc.symbolMap.keys()))
            dddf = p.DataFrame(symbolMapR, index=[0]).transpose()            
            for ix in mdf.index:
                #try: mdf.loc[ix, 'id3'] = symbolMapR[ix]
                #except: ''
                try: mdf.loc[ix, 'id3'] = dddf.loc[ix, 0]
                except: ''
            print mdf.sort_values(by='balance_usd', ascending=False)
            #return
            #print mdf
            #print df
            #return
        #['tokenInfo']
        #print res2
    with p.option_context('display.max_rows', 400, 'display.max_columns', 4000, 'display.width', 1000000):
        mmdfs = p.DataFrame()
        for kmdfs in mdfs.keys():
            mmdfs = mmdfs.add(p.DataFrame(mdfs[kmdfs]).loc[:, 'balance balance_usd'.split(' ')], fill_value=0)
        mdf0 = mmdfs.combine_first(mdf0)
        #mdf0 = mdf0.combine_first(mmdfs)
        if verbose:
            print 'mdfs======'
            print mdfs.keys()
            print p.DataFrame(mdfs)
            print mmdfs
            print 'mdfs======/'
    
    if not verbose:
        with p.option_context('display.max_rows', 400, 'display.max_columns', 4000, 'display.width', 1000000):
            print
            print '============================================================'
            print ethaddr
            print '---'
            print addressInfos
            print '---'
            balanceUSDTotal = mdf0['balance_usd'].sum() #+ 89.736
            ethUSDTotal     = addressInfos['balance'].sum() * ethusd
            pc  = ((balanceUSDTotal + ethUSDTotal) / initialInvestment * 100)-100
            pc2 = (balanceUSDTotal + ethUSDTotal) - initialInvestment
            #for i3 in addressInfos.index:
            #    print mdf0[mdf0['ethaddr'] == i3]
            mdf0['ethUSDTotal'] = ethUSDTotal
            mdf0 = genPortfolio(mdf0)
            mdf0 = mdf0.fillna(0)
            # rebalance portfolio
            mdf0['unitsDiff'] = mdf0['portUnits']    - mdf0['balance']
            mdf0['unitsDiffPerBalance'] = n.abs(mdf0['unitsDiff'] / mdf0['balance']) # 1 - (mdf0['portUnits'] / mdf0['balance'])
            mdf0['balancePerUnitsDiff'] = mdf0['balance'] / mdf0['unitsDiff']
            mdf0['balanceUsdDiff'] = mdf0['portUsd'] - mdf0['balance_usd']
            mdf0['balanceETHDiff'] = mdf0['balanceUsdDiff'] / ethusd
            mdf0['balanceByUnitsDiff']      = mdf0['balance_usd'] / mdf0['unitsDiff']
            # used for closing positions, find the largest balanceUsdDiff and the lowest balancePerUnitsDiff
            #mdf0['balanceByUnitsDiff2']     = mdf0['balanceUsdDiff'] / (mdf0['balancePerUnitsDiff'] * n.abs(mdf0['unitsDiff']))
            #mdf0['balanceByBalanceUsdDiff'] = mdf0['balance_usd'] / mdf0['balanceUsdDiff']
            mdf0['t1'] = mdf0['unitsDiffPerBalance'] * mdf0['balanceUsdDiff']
            mdf0['mname'] = mdf0.index
            print dfinfo
            f = '24h_volume_usd allocation avg balance balance_usd bid ethaddr holdersCount id2 id3 issuancesCount offer price_btc price_usd rank symbol t1 t2 volume portWeight portPcnt totalBalanceUsd portUsd portUnits unitsDiff balanceUsdDiff balanceETHDiff'.split()
            f = 'totalBalanceUsd 24h_volume_usd allocation avg balance balance_usd portUsd balancePortDiffUSD balancePerPort bid offer spread spreadPcnt spreadPcntA ethaddr holdersCount price_btc price_usd rank mname volume volumePerHolder holdersPerVolume portWeight portPcnt portUsd portUnits mname avg balance unitsDiff unitsDiffPerBalance balancePerUnitsDiff balanceByUnitsDiff balanceByUnitsDiff2 balanceByBalanceUsdDiff balanceUsdDiff balanceETHDiff t1'.split()
            def sortDataFrame(df, field, f, ascending):
                
                sortFlag = '^' if ascending == True else 'v'
                df = df.loc[:,f]
                if field == None or field == 'index':
                    df = df.sort_index()
                else:
                    df = df.sort_values(by=field, ascending=False)
                df = df.rename(columns={field:('%s %s' % (field, sortFlag))})
                return df
            print sortDataFrame(mdf0, None, f, False)
            print sortDataFrame(mdf0, 'allocation', f, False)
            print 'delever'
            print sortDataFrame(mdf0, 'balance_usd', f, False)
            print 'lever'
            print sortDataFrame(mdf0, 'balanceETHDiff', f, False)
            print 'lever'
            print sortDataFrame(mdf0, 'unitsDiff', f, False)
            print sortDataFrame(mdf0, 'spreadPcnt', f, False)
            print sortDataFrame(mdf0, 'volumePerHolder', f, False)
            print 'delever2'
            print sortDataFrame(mdf0, 'balanceByUnitsDiff', f, False)
            # test
            #print sortDataFrame(mdf0, 'balanceByUnitsDiff2', f, True)
            #print sortDataFrame(mdf0, 'balanceByBalanceUsdDiff', f, True)
            #pdf = mdf0[mdf0['unitsDiffPerBalance'] != n.inf]
            #f1 = ' '.join(f).replace('unitsDiff ', 'unitsDiff spreadPcnt ').split(' ')
            #print sortDataFrame(pdf, 'unitsDiffPerBalance', f1, True)
            print sortDataFrame(mdf0, 't1', f, True)
            print '---'
            print 'balanceUSDTotal[incl. ethUSDTotal]: %s' % (balanceUSDTotal + ethUSDTotal)
            print '                    initial investment: %s' % (initialInvestment)
            print '                    initial investment: %s [%s]' % (pc, pc2) #+'%'
            print '                      portPcnt sum: %s' % mdf0['portPcnt'].sum()
            print '                balanceUsdDiff sum: %s' % mdf0['balanceUsdDiff'].sum()
            print '               balanceETHDiff  sum: %s' % mdf0['balanceETHDiff'].sum()
            print '               balanceETHDiff+ sum: %s' % mdf0[mdf0['balanceETHDiff'] > 0]['balanceETHDiff'].sum()
            print '               balanceETHDiff- sum: %s' % mdf0[mdf0['balanceETHDiff'] < 0]['balanceETHDiff'].sum()
            print '           balancePortDiffUSD  sum: %s [takingTheWheatFromTheChaff]' % mdf0[mdf0['balancePortDiffUSD'] > 0]['balancePortDiffUSD'].sum()

            print '                     portUnits sum: %s' % mdf0['portUnits'].sum()
            print '                       balance sum: %s' % mdf0['balance'].sum()
            print '                            ethusd: %s' % ethusd
            print '---'

#@profile
def genPortfolio(df, balance_usd='balance_usd', volume='volume'):
    cmc = CoinMarketCap()
    eth = cmc.getTicker('ETH').set_index('symbol').transpose()
    ethusd = float(eth.loc['price_usd', 'ETH'])
    gasUSD = 2

    try:    df['balance']
    except: df['balance']     = 0
    try:    df['ethUSDTotal']
    except: df['ethUSDTotal'] = 0

    try:    df['volumePerHolder'] = df[volume] / df['holdersCount']
    except: ''
    try:    df['holdersPerVolume'] = df['holdersCount'] / df[volume]
    except: ''
    df['portWeight'] = n.log(df['allocation']) / n.log(10)
    #df['portWeight'] = (df['allocation']) #/ n.log(10)
    df = df[df['portWeight'] < n.inf] # todo: get prices below 0.00001
    df['portPcnt']   = df['portWeight'] / df['portWeight'].sum() * 100
    side = 'avg'
    df[balance_usd]    = df['balance'] * ethusd * df[side]
    
    #df['totalBalanceUsd'] = df[balance].sum()
    df['totalBalanceUsd'] = (df['balance'] * ethusd * df[side]).sum()
    df['totalBalanceUsd'] = df['totalBalanceUsd'] + df['ethUSDTotal']
    
    df['portUsd']         = (df['totalBalanceUsd'] - gasUSD) * df['portPcnt'] / 100
    df['portUsd']       = df['portUsd'] * df['allocationBool']
    df['balancePortDiffUSD'] = df[balance_usd] - df['portUsd']
    df['portUnits']       = df['portUsd'] / ethusd / df[side]
    df['balancePerPort']  = df[balance_usd] / df['portUsd']
    df = df[df['portUnits'] != n.inf]
    return df

def parseEtherDeltaDump():
    import re
    fp = open('/mldev/bin/data/cache/coins/etherdelta.volume.tsv', 'r')
    res = fp.read()
    fp.close()
    #print res
    res = re.sub(re.compile(r'.*?Offer(.*?)(Token|Order|ORDER).*', re.S), '\\1', res)
    res = res.strip()
    return res

def toMjson(df, fname):
    import ujson as uj
    df = df.fillna(0)
    try:
        df = df.set_index('symbol')
    except:
        ''
    tojson = df.transpose().to_dict()
    tojson = {'timestamp':time.time(), 'data':tojson}
    tojson = uj.dumps(tojson)
    fp = open(fname, 'a')
    fp.write('%s\n' % tojson)
    fp.close()

try: import matplotlib.pylab as plt
except: ''
from qoreliquid import normalizeme, sigmoidme
#import qgrid
#from IPython.display import display
#@profile
def modelPortfolio(num=5, df=None):
    
    if type(df) == type(None):
        """
    cv = "#""PPT/ETH 	917552 	0.01600 	0.01600
MCAP/ETH 	52178 	0.01205 	0.02100
VERI/ETH 	4817 	0.60000 	0.61000
WINGS/ETH 	5661 	0.00031 	0.00160
XRL/ETH 	575830 	0.00051 	0.00060
DICE/ETH 	13083 	0.01810 	0.02090
...
BNB/ETH 	0 	0.00001 	0.00300
ETH/USD.DC 	0 		
ETH/BTC.DC 	0 	"""
        cv = parseEtherDeltaDump()
        #fp = open('/tmp/etherdelta.volume.tsv', 'r')
        #cv = fp.read(); fp.close()
        df = cv.split('\n')
        import re
        df = map(lambda x: re.sub(re.compile(r'[\s]+'), '\t', x), df)
        df = map(lambda x: x.split('\t'), df)
        ffields = 'symbol volume bid offer'.split(' ')
        df = p.DataFrame(df, columns=ffields)
        for i in ffields[1:]: df[i] = p.to_numeric(df[i])
        
    toMjson(df, '/mldev/bin/data/cache/coins/etherdelta.mjson')

    #df = df.fillna(0)
    #    for i in df.index:
    #        print 's/bid/offer: %s %s %s' % (df.loc[i, 'symbol'], df.loc[i, 'bid'], df.loc[i, 'offer'])
    df['avg'] = (df['bid'] + df['offer']) / 2
    df['spread'] = df['offer'] - df['bid']
    df['spreadPcnt'] = df['spread'] / df['avg'] * 100
    #df['spreadPcntA'] = n.log(df['spreadPcnt'])/-df['spreadPcnt'] #1/n.log(df['spreadPcnt']/100)
    df['spreadPcntA'] = 1/(df['spreadPcnt']+1)
    #df['spreadPcntA'] = normalizeme(df['spreadPcntA']) 
    df['t1'] = (df['volume'] / df['avg'])
    df['t1a'] = df['volume'] / (df['avg'] * n.log(df['spreadPcnt']/100) )
    df['t2'] = (df['volume'] * df['avg'])
    df['allocation']     = df['t1']
    #df['allocationBool'] = df[df['spreadPcntA'] < -0.03].loc[:,'spreadPcntA']
    df['allocationBool'] = 1 #df['spreadPcntA']
    
    df = df.set_index('symbol').fillna(0)
    
    #df = df[df['bid']   > 0.0001]
    #df = df[df['offer'] > 0.0001]
    df = df[df['allocation'] > 1]

    #with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
    #    print df.dtypes
    #    print df
    try: dfst1 = df.sort_values(by='t1', ascending=False).head(num)
    except: ''
    try: dfst2 = df.sort_values(by='t2', ascending=False).head(num)
    except: ''
    print df.index
    #sys.exit()

    #print '==='
    #with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
    #    print df
    #print '==='
    try:    df = df.sort_values(by='allocation', ascending=False).head(num)
    except: ''
    dfst = df

    dfst['symbol'] = dfst.index
    dfst['symbolCode'] = map(lambda x: x.split('/')[0], dfst.index)
    dfst = dfst.set_index('symbolCode')

    with p.option_context('display.max_rows', 400, 'display.max_columns', 4000, 'display.width', 1000000):
        #print dfst1
        #print dfst2
        #print 'modelPortfolio======'
        #print dfst
        #print 'modelPortfolio======/'
        ''
    #df['allocation'] = normalizeme(df['allocation'])
    #df['allocation'] = sigmoidme(df['allocation'])
    plt.plot(dfst['allocation'].get_values())
    plt.xlabel(dfst.index)
    #plt.yscale('log')
    #plt.show()
    #qgrid.show_grid(df)
    #grid = qgrid.QGridWidget(df=df)
    #display(grid)

    #print df.dtypes

    return dfst
    


if __name__ == "__main__":

    import argparse
    # source: https://docs.python.org/2/howto/argparse.html
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", '--verbose', help="turn on verbosity")
    parser.add_argument("-lm", '--listPortfolioModels', help="", action="store_true")
    parser.add_argument("-pm", '--setPortfolioModel', help="")
    parser.add_argument("-pa", '--parse', help="go live and turn off dryrun", action="store_true")
    parser.add_argument("-p", '--portfolio', help="go live and turn off dryrun", action="store_true")
    parser.add_argument("-sk", '--parseCoinMarketCapSkipTo', help="parseCoinMrketCap skipTo")
    parser.add_argument("-b", '--balance', help="parseCoinMrketCap skipTo")
    parser.add_argument("-tm", '--tokenmarket', help="parseCoinMrketCap skipTo", action="store_true")
    parser.add_argument("-r01", '--research01', help="parseCoinMrketCap skipTo", action="store_true")
    parser.add_argument("-r01b", '--research01bittrex', help="parseCoinMrketCap skipTo", action="store_true")
    parser.add_argument("-r02", '--research02', help="parseCoinMrketCap skipTo", action="store_true")
    parser.add_argument("-r03", '--research03', help="parseCoinMrketCap skipTo", action="store_true")
    parser.add_argument("-r04", '--research04', help="parseCoinMrketCap skipTo", action="store_true")
    parser.add_argument("-r05", '--research05', help="parseCoinMrketCap skipTo", action="store_true")
    parser.add_argument("-c", '--cache', help="cache on", action="store_true")
    
    args = parser.parse_args()
    
    """
    # bitmex
    import drest
    #api = drest.API('http://socket.coincap.io/')
    api = drest.API('https://www.bitmex.com/api/v1')
    #response = api.make_request('GET', '/trade?count=100&reverse=false')
    #response = api.make_request('GET', '/instrument')
    response = api.make_request('GET', '/instrument/indices')
    #print response.data
    
    df = p.DataFrame(response.data)#.transpose()
    pf(df)
    """

    #nu = 150
    """
    print makeTimeseriesTimestampRange(bars=nu)
    print makeTimeseriesTimestampRange(bars=nu, period=86400)
    print makeTimeseriesTimestampRange(bars=nu, period=14400)
    print makeTimeseriesTimestampRange(bars=nu, period=1800)
    print makeTimeseriesTimestampRange(bars=nu, period=900)
    print makeTimeseriesTimestampRange(bars=nu, period=300)
    print makeTimeseriesTimestampRange(timestamp=1495209600, period=14400, bars=nu)
    print makeTimeseriesTimestampRange(timestamp=1495209642, period=14400, bars=nu)
    print makeTimeseriesTimestampRange(timestamp=1495209642, period=1800, bars=nu)
    print makeTimeseriesTimestampRange(timestamp=1495209642, period=900, bars=nu)
    print makeTimeseriesTimestampRange(timestamp=1495209642, period=300, bars=nu)
    #print makeTimeseriesTimestampRange(timestamp=1495209642, period=300, bars=nu)['range']
    """
    
    #%reload_ext autoreload
    #%autoreload 2
    from bitmex import *
    cmc = CoinMarketCap()
    #cmc.getTradableCoins()
    if args.listPortfolioModels:
        pm = PortfolioModeler()
        pm.listModels()
        sys.exit()
    if args.setPortfolioModel:
        cmc.portfolioModelSelect = int(args.setPortfolioModel)
    if args.parse:
        cmc.parseCoinMarketCap(verbose=True)
    if args.parseCoinMarketCapSkipTo:
        cmc.parseCoinMarketCapSkipTo = int(args.parseCoinMarketCapSkipTo)
    if args.balance:
        balance = float(args.balance)
    else:
        balance = 230
    if args.portfolio:
        portfolio = cmc.generatePortfolio(bal=balance)
    if args.tokenmarket:
        #%reload_ext autoreload
        #%autoreload 2
        from bitmex import TokenMarket
        # TokenMarket
        tm = TokenMarket()
        df = tm.allAssetsBlockchainTokenMarket()
        #with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
        #    print tm.allAssetsICOsBlockchain
        # TokenMarket
        tm.tokenICOsTokenMarket()
        tm.underTheRadarTokens()
    
    if args.cache:
        noCache = False
    else:
        noCache = True
        
    if args.research01:
        eth1_1 = '0x38a4Ff00C207cBD78aB34b6dDd1b8754E4498508'
        eth1_2 = '0xc73D7e4a40D4513eC7D114f521eA59DF607a7613'
        eth2_1 = '0xc978D12413CbC4ec37763944c57EF0100a4c15cf' #eth2 0
        eth2_2 = '0x2c8f659d57971449eb627FB78530Fc61867c4E50' #eth2 1
        
        #ethaddress1 = '0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae'
        getAdressInfoEthplorer([eth1_1, eth1_2], args.verbose, instruments=20, noCache=noCache)
        getAdressInfoEthplorer([eth2_1, eth2_2], args.verbose, instruments=50, noCache=noCache)
        #print getTicker('bitcoin')    

    if args.research03:
        df1 = getTicker('PPT').set_index('symbol').transpose()
        print df1
    
    if args.research02:
        with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
            dfp = modelPortfolio(num=20)
            gpdf = genPortfolio(dfp)
            print dfp
            print gpdf
    
    def on_message(ws, message):
        print message
    
    def on_error(ws, error):
        print error
    
    def on_close(ws):
        print "### closed ###"
    
    def on_open(ws):
        """
        def run(*args):
            for i in range(30000):
                time.sleep(1)
                ws.send("Hello %d" % i)
            time.sleep(1)
            ws.close()
            print "thread terminating..."
        thread.start_new_thread(run, ())
        """
        ''
    
    if args.research01bittrex:
        from qore import QoreDebug
        qdb = QoreDebug()
        qdb.colorStacktraces()
        #res = apiRequest('https://bittrex.com/api/v1.1/public', '/getcurrencies')
        #df = p.DataFrame(res['result']).set_index('Currency')
        
        #res = apiRequest('https://bittrex.com/api/v1.1/public', '/getmarkets')
        #df = p.DataFrame(res['result']).set_index('MarketName')
        
        res2 = apiRequest('https://bittrex.com/api/v1.1/public', '/getmarketsummaries')
        df = p.DataFrame(res2['result'])
        df['Quote'] = map(lambda x: x.split('-')[1], df['MarketName'])
        df['Base'] = map(lambda x: x.split('-')[0], df['MarketName'])
        df = df.set_index('Quote')

        o  = Bittrex('34fa3c1160d246e0a3f968040f4eb999', 'bd443220f548460cb09e6af82f3705b5')
        df2 = o.getInfo()
        df2 = df2.set_index('Currency')
        
        
        #df['VolumeBase'] = df['Volume'] * df['Last']
        #df.sort_values('VolumeBase', ascending=False)
        df = df.combine_first(df2)
        df = df.fillna(0)

        dfp = modelPortfolio(df=df)
        #df = genPortfolio(df, volume='Volume')

        with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
            print df[df['Balance'] > 0]#.head(10)
            print df#.head(10)
            #print df2
            
            print 
        """
        res3 = apiRequest('https://bittrex.com/api/v1.1/public', '/getorderbook?market=BTC-LTC&type=both', noCache=True)
        #df = p.DataFrame(res3['result'])#.set_index('MarketName')
        #df['VolumeBase'] = df['Volume'] * df['Last']
        #df#.sort_values('VolumeBase', ascending=False)
        mdf = p.DataFrame()
        for i in res['result']:
            with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
                df = p.DataFrame(i, index=[0]).set_index('MarketName')#.transpose()
                mdf = mdf.combine_first(df)
                #print df
        mdf
        #res3['result']
        print p.DataFrame(res3['result']['sell']).sort_index(ascending=False).tail(5)
        print p.DataFrame(res3['result']['buy']).head(5)
        """
        #print df
        #df = df.transpose()
        #for i in df.index:
        #    df.loc[i, 'basePair'] = i.split('_')[1]
        #df[df['basePair'] == 'eth']

    if args.research04:

        #!/usr/bin/python
        import websocket
        import thread
        import time
        
        websocket.enableTrace(True)
        #url = "ws://echo.websocket.org/"
        url = "wss://socket.bittrex.com/signalr"
        header = ['apikey: qwe', 'apisecret: 1qwe']
        ws = websocket.WebSocketApp(url, header=header, on_message = on_message, on_error = on_error, on_close = on_close)
        ws.on_open = on_open
    
        ws.run_forever()        


    # portfolio tokenization
    if args.research05:
        portfolioTokenization()
