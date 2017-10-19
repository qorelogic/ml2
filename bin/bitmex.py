# coding: utf-8

"""
octave:52> a=0.00052; b=0.00048; (a+b)/2
ans =    5.00000000000000e-04
octave:53> a=0.00052; b=0.00048; x=(a+b)/2
x =    5.00000000000000e-04
octave:54> c=0.643;
octave:55> c/x
ans =  1286
octave:56> c=0.643; c/x
ans =  1286
octave:57> a=0.0005187; b=0.00046007; x=(a+b)/2
x =    4.89385000000000e-04
octave:58> c=0.643; c/x
ans =  1313.89396896104
octave:59> 0.11*300
ans =  33
octave:60> a=0.00052; b=0.00048; (a-b)
ans =    3.99999999999999e-05
octave:61> w = 280.333; x = 1233.309; x-(w+x)*2/100
ans =  1203.03616000000
octave:62> .138*300
ans =  41.4000000000000
octave:63> w = 4.607; x = 2.093; x-(w+x)*2/100
ans =  1.95900000000000

investment pyramid
model:

peak 150 Billion [retracement 1.0]:
      cash = 100 %
M001[-r01] =       age %
M002[ -tm] = (100-age) %

retracement = .786
      cash = 100 %
M001[-r01] =       age %
M002[ -tm] = (100-age) %

df      = [100:-1:0]';
df(:,2) = ((100-df(:,1)) * (1/(1-.236)))
df(:,3) = df(:,1)*70/100
df(:,4) = df(:,2)*70/100;
df(:,5) = df(:,1)/100*4452.49
"""

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
def apiRequest(baseurl, query, method='GET', noCache=False, verbose=False):
    #api = drest.API(baseurl)
    #response = api.make_request(method, query)
    #res = response.data
    
    backend='sqlite'
    #backend='memory'

    if noCache == False:
        if verbose:
            print '[caching] %s: %s %s url: %s' % (method, baseurl, query, baseurl+query)
        expire_after = 3600 * 24 #* 365
        # source: https://stackoverflow.com/questions/27118086/maintain-updated-file-cache-of-web-pages-in-python
        requests_cache.install_cache('scraper_cache', backend=backend, expire_after=expire_after)
    else:
        if verbose:
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
        self.qd = QoreDebug()
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
    def getCoinsExchanges(self, coin):
        coin = self.resolveCoin(coin)
        url = 'http://coinmarketcap.com/currencies/%s/' % coin
        #print 'getCoinsExchanges: %s' % url
        xresd = self.xp.xpath2df(url, {
            'source'       : '//tbody/tr/td[2]/a/text()',
            'pair'         : '//tbody/tr/td[3]/a/text()',
            'volume_24h'   : '//tbody/tr/td[4]/span/text()',
            'price'        : '//tbody/tr/td[5]/span/text()',
            'volume_pcnt'  : '//tbody/tr/td[6]/text()',
            'updated'      : '//tbody/tr/td[7]/text()',
        })
        df = p.DataFrame(xresd)
        df['volume24h'] = map(lambda x: x.replace(',', '').replace('$', '').replace('*', '').strip(), df['volume_24h'])
        df['volume24h'] = p.to_numeric(df['volume24h'])
        df = df.sort_values(by='volume24h')
        #print df['volume24h']
        #df['volume24h'].plot()
        #plt.show()
        df = p.DataFrame(df['source'].drop_duplicates())
        df[coin] = 1
        df = df.set_index('source')
        #print df.transpose()
        #print list(df.index)
        self.resolvedCoin['exchanges'] = ','.join(list(df.index))
        df = df.transpose()
        return df

    #@profile
    def check(self, checkTradableCoins=False):
        try: self.dfc
        except Exception as e:
            #self.qd.exception(e)
            self.tickers()
        
        if checkTradableCoins:
            try: self.tradableCoins
            except Exception as e:
                #self.qd.exception(e)
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
                    dfxs = dfxs.combine_first(self.getCoinsExchanges(v))
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
        #df = df.combine_first(getCoinsExchanges('1337'))
        self.tradableCoins = tradableCoins

    #@profile
    def getTradableCoins(self, filterVolume=True):

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
        if filterVolume:
            df = df[df['24h_volume_usd'] >= 100000] # volume strategy
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
            dfe = self.getCoinsExchanges(i)
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
    def getTicker(self, symbol, verbose=False):
        df = p.DataFrame(self.resTicker)
        self.symbolMapper = df.loc[:, 'symbol id'.split()].set_index('symbol')
        #with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
        #    print self.symbolMapper.sort_index()
        #return
        
        try:
            ticker = self.symbolMapper.loc[symbol, 'id']
            res = apiRequest('https://api.coinmarketcap.com', '/v1/ticker/%s/' % ticker, noCache=True, verbose=verbose)
        except Exception as e:
            #print e
            res = apiRequest('https://api.coinmarketcap.com', '/v1/ticker/%s/' % ticker, noCache=False, verbose=verbose)
        res = p.DataFrame(res)
        #print res.transpose()
        return res

    def getCoinsOnExchange(self, exchange='EtherDelta', cache=True):
        self.tokensOnOtherExchanges(exchange, cache=cache)
        dff = self.tickers().loc[:,['id']]
        dff['symbol'] = dff.index
        dff = dff.set_index('id')
        try:
            df = p.read_csv('/mldev/bin/data/cache/coins/coinsExchanges.%s.csv'%exchange, index_col=0)
            dff = dff.combine_first(df)
            dff = dff[dff[exchange] > 0]
        except: ''
        dff['id'] = dff.index
        dff = dff.set_index('symbol')
        return dff.loc[:, 'sum id'.split(' ')].sort_values(by='sum', ascending=True)

    def cacheTo(self, dff, fname):
        dff = dff.fillna(0)
        dff.loc['sum', :] = n.sum(dff.get_values(), 0)
        dff.loc[:, 'sum'] = n.sum(dff.get_values(), 1)
        dff = p.DataFrame(n.array(dff.get_values(), dtype=n.int), index=dff.index, columns=dff.columns)
        dff.to_csv(fname)
        return dff

    def filterByExchange(self, exchange, dff):
        cc = 'sum %s' % exchange
        dfe = dff.transpose().loc[:, cc.split(' ')]
        dfe = dfe[dfe[exchange] > 0].sort_values(by='sum', ascending=True)#.transpose()
        dfe.to_csv('/mldev/bin/data/cache/coins/coinsExchanges.%s.csv'%exchange)
        return dfe
    
    def tokensOnOtherExchanges(self, exchange, cache=False):
        import pandas as p
        # tokens on exchanges
        #from bitmex import *
        fname = '/mldev/bin/data/cache/coins/coinsExchanges.csv'
        li = []
        #di = {}
        
        if cache:
            #import qgrid
            dff = p.read_csv(fname, index_col=0)
            #qgrid.show_grid(df)
        else:
            dff = p.DataFrame()
            tc = self.getTradableCoins(filterVolume=False)
            ltc = list(tc['id'])
            print ltc
            for i in ltc:#[0:5]:
                print i
                lii = self.getCoinsExchanges(i).transpose().to_dict()
                #print lii
                dff = dff.combine_first(p.DataFrame(lii))
                #li.append(lii)
                #di.update(self.getCoinsExchanges(i).transpose().sum().to_dict())
            #print di
            #df = p.DataFrame(di, index=[0]).transpose()        
            dff = self.cacheTo(dff, fname)
        #df = p.DataFrame(li).transpose()
        dff = self.filterByExchange(exchange, dff)
        with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):                
            #print cc
            #print 'coins: %s'     % (len(list(dff.columns))-1)
            #print 'exchanges: %s' % (len(list(dff.index))-1)
            #print dff.transpose()
            #print df.transpose()
            ''

    #@profile
    def resolveCoin(self, nameOrSymbol):
        self.check()
        df = self.dfc
        df['symbol'] = df.index
        df['iname'] = map(lambda x: x.lower(), df['name'])
        #print df
        #print df.loc[:, 'id symbol'.split()]
        dfres = p.DataFrame()
        dfres = dfres.combine_first(df[df['id']     == nameOrSymbol.lower()])
        dfres = dfres.combine_first(df[df['symbol'] == nameOrSymbol.upper()])
        
        try:    currency = dfres[dfres['symbol'] == nameOrSymbol.upper()].loc[:,'id'][0]
        except: 
            try:
                currency = dfres[dfres['id']     == nameOrSymbol.lower()].loc[:,'id'][0]
            except KeyError as e:
                print 'coin %s not found' % (nameOrSymbol)
                sys.exit()
        #print dfres
        self.resolvedCoin = dfres
        return currency

class PortfolioModeler:
    
    def __init__(self):
        self.qd = QoreDebug()

        self.version = 'v0.0.1'
        self.models = {
            1: 'Q001aa',
            2: 'Q001a',
            3: 'Q001',
        }
        li = 't1 t1a t1b t1c t1d t1e t1f t2'.split(' ')
        self.models.update(dict(zip(range(4,len(li)+4), li)))
        self.model   = None
        self.cmc = CoinMarketCap()
    
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

    #@profile
    def genPortfolio(self, df, balance_usd='balance_usd', volume='volume'):
    
        cmc = CoinMarketCap()
        eth = cmc.getTicker('ETH').set_index('symbol').transpose()
        ethusd = float(eth.loc['price_usd', 'ETH'])
        gasUSD = 2
        side = 'avg'
    
        try:    df['balance']
        except: df['balance']     = 0
        try:    df['ethUSDTotal']
        except: df['ethUSDTotal'] = 0
    
        try:    df['volumeETH'] = df[volume] * df[side]
        except: ''
        try:    df['volumeETHPerHolder'] = df['volumeETH'] / df['holdersCount']
        except: ''
    
        try:    df['volumePerHolder'] = df['volumeETH'] / df['holdersCount']
        except: ''
        try:    df['holdersPerVolume'] = df['holdersCount'] / df['volumeETH']
        except: ''

        # set avg to max price between exchanges
        try:
            df['price_eth'] = df['price_usd'] / ethusd
            df['arb1'] = 100 * (df[side] / df['price_eth'] - 1)
            df[side] = n.max(df.loc[:, [side, 'price_eth']].fillna(0).get_values(), 1)
        except: ''

        df[balance_usd]    = df['balance'] * ethusd * df[side]
        df['balance_eth']  = df['balance'] * df[side]

        #df['totalBalanceUsd'] = df[balance].sum()
        df['totalBalanceUsd'] = (df['balance'] * ethusd * df[side]).sum()
        df['totalBalanceUsd'] = df['totalBalanceUsd'] + df['ethUSDTotal']
        df['totalBalanceEth'] = df['totalBalanceUsd'] / ethusd
        totalBalanceUsd = n.mean(df['totalBalanceUsd'])
        
        print list(df['allocation'])
        #from qoreliquid import normalizeme
        #from qoreliquid import sigmoidme
        #df['allocation'] = df['allocation'].fillna(0)
        #df['allocation'] = normalizeme(df['allocation'])
        #df['allocation'] = sigmoidme(df['allocation'])
        dfa = ((df.drop(df[df['allocation'] < 0].index)))
        #print dfa #df[df['allocation'] == 0].index
        df['portWeight'] = n.log(df['allocation']) / n.log(10)
        #df['portWeight'] = (df['allocation']) #/ n.log(10)
        #sys.exit()

        dfp = df
        dfp = dfp[dfp['balance'] > 0]
        
        df = df[df['portWeight'] < n.inf] # todo: get prices below 0.00001
        #df['totalBalanceUsd'] = totalBalanceUsd
        
        df['portWeight'] = map(lambda x: 0 if n.abs(x) == n.inf else x, df['portWeight'])
        df['currentPortPcnt'] = df['balance_eth'] / df['totalBalanceEth'] * 100
        df['portPcnt']   = df['portWeight'] / df['portWeight'].sum() * 100

        df['portUsd']         = (df['totalBalanceUsd'] - gasUSD) * df['portPcnt'] / 100
        df['portUsd']       = df['portUsd'] * df['allocationBool']
        df['balancePortDiffUSD'] = df[balance_usd] - df['portUsd']
        df['portUnits']       = df['portUsd'] / ethusd / df[side]
        df['balancePerPort']  = df[balance_usd] / df['portUsd']
        df = df[df['portUnits'] != n.inf]
        
        #df = df[n.abs(df['balance']) != 0]

        with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
            #print df.dtypes
            #print df
            #print
            #print dfp
            ''

        return df

    #@profile
    def modelPortfolio(self, num=5, df=None, allocationModel=None, ethusd=None, mode='etherdelta'):
        
        self.allocationModel = allocationModel
        if allocationModel == None:
            allocationModel='t1b'
        print 'allocationModel[%s]' % allocationModel
        #import qgrid
        #from IPython.display import display
        try: import matplotlib.pylab as plt
        except: ''
        #from qoreliquid import normalizeme, sigmoidme
        #import qgrid
        #from IPython.display import display
        #@profile
        if type(df) == type(None) and mode == 'etherdelta':
            ed = EtherDelta()
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
            cv = ed.parseEtherDeltaDump()
            #fp = open('/tmp/etherdelta.volume.tsv', 'r')
            #cv = fp.read(); fp.close()
            df = cv.split('\n')
            import re
            df = map(lambda x: re.sub(re.compile(r'[\s]+'), '\t', x), df)
            df = map(lambda x: x.split('\t'), df)
            ffields = 'symbol volume bid offer'.split(' ')
            try:
                df = p.DataFrame(df, columns=ffields)
                for i in ffields[1:]: df[i] = p.to_numeric(df[i])
            except:
                df = p.DataFrame({'volume': 0, 'symbol': 'STUB/ETH', 'bid': 0, 'offer': 0}, index=[0])
            ed.toMjson(df, '/mldev/bin/data/cache/coins/etherdelta.mjson')
        
        if type(df) == type(None) and mode == 'poloniex':
            # ---
            pl  = Poloniex()
            df2 = pl.getCurrencies()
            #df2['symbol'] = df2.index
            #df2['bid'] = df2['last']
            df2['range'] = range(len(df2.index))
            df2 = df2.set_index('range')
            df2['offer'] = df2['last']
            #with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
            #    print df2
            df2 = df2.loc[:, 'symbol quoteVolume last offer'.split(' ')]
            df2 = df2.rename_axis({'quoteVolume':'volume', 'last':'bid'}, axis='columns')
            df2['volume'] = p.to_numeric(df2['volume'])
            df2['bid']    = p.to_numeric(df2['bid'])
            df2['offer']  = p.to_numeric(df2['offer'])
            df = df2
            #with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
            #    print df2
            # ---
    
        #df = df.fillna(0)
        #    for i in df.index:
        #        print 's/bid/offer: %s %s %s' % (df.loc[i, 'symbol'], df.loc[i, 'bid'], df.loc[i, 'offer'])

        try:    df['bid']
        except: df['bid'] = df['Bid']
        try:    df['offer']
        except: df['offer'] = df['Ask']
        try:    df['volume']
        except: df['volume'] = df['BaseVolume']
        try:    df['symbol']
        except: df['symbol'] = df['MarketName']

        df = df.set_index('symbol').fillna(0)
        df['symbol'] = df.index
        df['symbolCode'] = map(lambda x: x.split('/')[0], df.index)
        df = df.set_index('symbolCode')
    
        # coins on exchanges ex. etherdelta
        df = df.combine_first(self.cmc.getCoinsOnExchange(exchange='EtherDelta', cache=True))
        df['sum'] = df['sum'].fillna(1)
        
        # minimum viable product
        mvp = p.DataFrame()
        mvp['mvp'] = p.Series({'CDT':1, 'VERI':1, 'PAY':1, 'PLR':0.3, 'PPT':0.2, 'MCO':0.7,'ZRX':1})
        df = df.combine_first(mvp)

        df['avg'] = (df['bid'] + df['offer']) / 2
        df['spread'] = df['offer'] - df['bid']
        df['spreadPcnt'] = df['spread'] / df['avg'] * 100
        #df['spreadPcntA'] = n.log(df['spreadPcnt'])/-df['spreadPcnt'] #1/n.log(df['spreadPcnt']/100)
        df['spreadPcntA'] = 1/(df['spreadPcnt']+1)
        #df['spreadPcntA'] = normalizeme(df['spreadPcntA'])
        df['t1'] = (df['volume'] / df['avg'])
        df['t1a'] = df['volume'] / (df['avg'] * n.log(df['spreadPcnt']/100) )
        df['t1b'] = (df['volume'] * df['avg'])
    
        try:    df['volumeETH'] = df['volume'] * df['avg']
        except Exception as e: self.qd.exception(e)
            
        try:
            if ethusd:
                df['volumeUSD'] = df['volumeETH'] * ethusd
        except Exception as e: self.qd.exception(e)
        try:    
            df['volumePerHolder'] = df['volumeETH'] / df['holdersCount']
            df['volumeETHPerHolder'] = df['volumeETH'] / df['holdersCount']
            df['t1c'] = (df['volumePerHolder'])
            df['t1d'] = (df['volumeETHPerHolder'] / (df['avg'] * df['sum']))
        except Exception as e: self.qd.exception(e)
    
        df['t1e'] = (df['volumeETH'] / (df['avg'] * n.power(df['sum'], 4*3)))
        df['t1f'] = ((df['volumeETH'] * df['mvp']) / (df['avg'] * n.power(df['sum'], 3*1)))
        df['t2'] = (df['volume'] * df['avg'])

        try:    df[allocationModel]
        except Exception as e: 
            print 'No allocationModel[%s] found.' % e
            print 'Available models:'
            print self.listModels()
            sys.exit()
        self.allocationModels = 't1 t1a t1b t1c t1d t1e t1f t2'
    
        df['allocation']     = df[allocationModel]
        df['allocation']     = df['allocation'].fillna(0)
        #df['allocationBool'] = df[df['spreadPcntA'] < -0.03].loc[:,'spreadPcntA']
        df['allocationBool'] = 1 #df['spreadPcntA']
        
        #df = df[df['bid']   > 0.0001]
        #df = df[df['offer'] > 0.0001]
        #df = df[df['allocation'] > 1]
        
        #with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
        #    print df.dtypes
        #    print df
        try: dfst1 = df.sort_values(by='t1', ascending=False)#.head(num)
        except: ''
        try: dfst2 = df.sort_values(by='t2', ascending=False)#.head(num)
        except: ''
        #print df.index
        #sys.exit()
    
        #print '==='
        #with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
        #    print df
        #print '==='
        try:    df = df.sort_values(by='allocation', ascending=False)#.head(num)
        except: ''
        
        dfst = df
        
        with p.option_context('display.max_rows', 400, 'display.max_columns', 4000, 'display.width', 1000000):
            #print dfst1
            #print dfst2
            #print 'modelPortfolio======'
            #print dfst
            #print 'modelPortfolio======/'
            ''
        #df['allocation'] = normalizeme(df['allocation'])
        #df['allocation'] = sigmoidme(df['allocation'])
        #plt.plot(dfst['allocation'].get_values())
        #plt.xlabel(dfst.index)
        #plt.yscale('log')
        #plt.show()
        #qgrid.show_grid(df)
        #grid = qgrid.QGridWidget(df=df)
        #display(grid)
    
        #print df.dtypes
    
        return dfst

    def sortDataFrame(self, df, field, f, ascending, title=None):
        
        sortFlag = '^' if ascending == True else 'v'
        if field == None or field == 'index':
            df = df.sort_index()
        else:
            df = df.sort_values(by=field, ascending=False)
        df['balanceETHDiffCumsum'] = df['balanceETHDiff'].cumsum()
        df = df.loc[:,f]
        sf = ('%s %s' % (field, sortFlag))
        df = df.rename(columns={field:sf})
        print
        if title: print ('%s::%s %s [model:%s]' % (title, field, sortFlag, self.allocationModel))
        else:     print '%s [model:%s]' % (sf, self.allocationModel)
        print df

    def printPortfolio(self, mdf0, f=None):
        if f == None:
            f = 'totalBalanceUsd 24h_volume_usd allocation avg balance balance_usd portUsd balancePortDiffUSD balancePerPort bid offer spread spreadPcnt spreadPcntA ethaddr holdersCount price_btc price_usd rank mname volume volumePerHolder holdersPerVolume portWeight portPcnt portUsd portUnits mname avg balance unitsDiff unitsDiffPerBalance balancePerUnitsDiff balanceByUnitsDiff balanceByUnitsDiff2 balanceByBalanceUsdDiff balanceUsdDiff balanceETHDiff t1'.split()
        
        mdf0 = mdf0[n.abs(mdf0['balance']) != 0]
        
        print
        self.sortDataFrame(mdf0, 'allocation', f, False, title='') # same forting as portUsd
        self.sortDataFrame(mdf0, 'currentPortPcnt', f, False, title='delever') # same sorting as balance_usd
        self.sortDataFrame(mdf0, 'balancePortDiffUSD', f, False, title='delever2')
        self.sortDataFrame(mdf0, 'balanceETHDiff', f, False, title='lever')
        self.sortDataFrame(mdf0, 'unitsDiff', f, False, title='lever2')
        self.sortDataFrame(mdf0, 'sum', f, True, title='lever3')
        self.sortDataFrame(mdf0, 'spreadPcnt', f, False, title='')
        self.sortDataFrame(mdf0, 'volume', f, False, title='')
        self.sortDataFrame(mdf0, 'volumeETH', f, False, title='')
        self.sortDataFrame(mdf0, 'volumePerHolder', f, False, title='')
        self.sortDataFrame(mdf0, None, f, False, title='A-Z')
        self.sortDataFrame(mdf0, 'balanceByUnitsDiff', f, False, title='delever3')
        # test
        #self.sortDataFrame(mdf0, 'balanceByUnitsDiff2', f, True)
        #self.sortDataFrame(mdf0, 'balanceByBalanceUsdDiff', f, True)
        #pdf = mdf0[mdf0['unitsDiffPerBalance'] != n.inf]
        #f1 = ' '.join(f).replace('unitsDiff ', 'unitsDiff spreadPcnt ').split(' ')
        #self.sortDataFrame(pdf, 'unitsDiffPerBalance', f1, True)
        self.sortDataFrame(mdf0, 't1', f, True)
        print
        print

        #import dfgui
        #dfgui.show(mdf0)

        ev = Eveningstar()
        """        
        #df.loc[2, :] = p.Series(se.to_dict())
        ev.addToPortFolio('tenx', 23.052199999999999, 0)
        #df.loc[3, :] = p.Series({'Quantity': 23.052199999999999, 'Cost Basis Each (USD)': 0, 'Asset Id': 'tenx'})
        """
        for i in mdf0.index:
            try:
                balance = mdf0.loc[i, 'balance']
                idn = mdf0.loc[i, 'id']
                di = {'Quantity': balance, 'Asset Id':idn, 'Cost Basis Each (USD)':0}
                if balance > 0 and idn != 0:
                    #print di
                    ev.addToPortFolio(di['Asset Id'], di['Quantity'], di['Cost Basis Each (USD)'])
            except: ''
        ev.exportPortfolio()
        df = p.DataFrame(list(mdf0.index))
        df.to_csv('/tmp/symbols.txt')
        print ev.df

class TokenMarket:
    
    def  __init__(self):
        self.qd = QoreDebug()
        import pandas as p
        import numpy as n
        from qore import XPath
        import pandas as p
        self.xp = XPath()
        self.allAssetsICOsBlockchain = p.DataFrame()
        self.cmc = CoinMarketCap()
        pass

    def allAssetsBlockchainTokenMarket(self):
    
        #def tokenmarket():
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
        print 
        for i in xresd.keys(): print '%s' % len(xresd[i])
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
        from qoreliquid import combineDF3
        self.dfp = self.allAssetsICOsBlockchain
        #print '====='
        #with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
        #    print self.dfp
        #print '====='
        for ii in 'description links-blog links-facebook links-github links-linkedin links-slack links-telegram links-twitter links-website links-whitepaper'.split():
            try: self.dfp = self.dfp.drop(ii, 1)
            except Exception as e: ''#print e
        nn = 66
        lili = self.dfp.index#[nn:nn+5]
        for i in lili:#[0:3]:
    
            url = '%s' % self.dfp.ix[self.dfp.index[i], 'href'] 
            print '%s %s' % (i, url)
            #"""
            xresd = self.xp.xpath2df(url, {
                'name'             : '//*[@id="page-wrapper"]/main/div[2]/div[3]/div[1]/h1/text()[2]',
                'symbol'           : '//*[@id="page-wrapper"]/main/div[2]/div[4]/div[1]/table[1]//tr[1]/td/text()',
                'trading'          : '//*[@id="page-wrapper"]/main/div[2]/div[4]/div[1]/table[1]//tr[2]/td/span/text()[2]',
                
                #'links-website'    : '//*[@id="page-wrapper"]/main/div[2]/div[4]/div[2]/div[1]/table//tr[1]/td/a/@href',
                #'links-blog'       : '//*[@id="page-wrapper"]/main/div[2]/div[4]/div[2]/div[1]/table//tr[2]/td/a/@href',
                #'links-whitepaper' : '//*[@id="page-wrapper"]/main/div[2]/div[4]/div[2]/div[1]/table//tr[3]/td/a/@href',
                #'links-facebook'   : '//*[@id="page-wrapper"]/main/div[2]/div[4]/div[2]/div[1]/table//tr[4]/td/a/@href',
                #'links-twitter'    : '//*[@id="page-wrapper"]/main/div[2]/div[4]/div[2]/div[1]/table//tr[5]/td/a/@href',
                #'links-linkedin'   : '//*[@id="page-wrapper"]/main/div[2]/div[4]/div[2]/div[1]/table//tr[6]/td/a/@href',
                #'links-slack'      : '//*[@id="page-wrapper"]/main/div[2]/div[4]/div[2]/div[1]/table//tr[7]/td/a/@href',
                #'links-telegram'   : '//*[@id="page-wrapper"]/main/div[2]/div[4]/div[2]/div[1]/table//tr[8]/td/a/@href',
                #'links-github'     : '//*[@id="page-wrapper"]/main/div[2]/div[4]/div[2]/div[1]/table//tr[9]/td/a/@href',
                
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
            #"""
            xresdlen = {}
            for j in xresd: xresdlen[j] = len(xresd[j])
            #xresdlen = [len(xresd[j]) for j in xresd]
            #print xresdlen
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
            #"""
            #print xresdlen
            #print xresd
            dftm = p.DataFrame(xresd, index=[i])
            # dates
            for j in dftm.index:
                try: dftm.loc[j, 'crowdsale-opening-date-ts'] = datetime.datetime.strptime(dftm.loc[j, 'crowdsale-opening-date'], '%d. %b %Y')
                except Exception as e: ''#self.qd.exception(e)
                try: dftm.loc[j, 'crowdsale-closing-date-ts'] = datetime.datetime.strptime(dftm.loc[j, 'crowdsale-closing-date'], '%d. %b %Y')
                except Exception as e: ''#self.qd.exception(e)
                try: dftm.loc[j, 'crowdsale-days'] = (dftm.loc[j, 'crowdsale-closing-date-ts'] - dftm.loc[j, 'crowdsale-opening-date-ts']).days
                except Exception as e: ''#self.qd.exception(e)
                try: dftm.loc[j, 'crowdsale-days-to-close'] = (datetime.datetime.now() - dftm.loc[j, 'crowdsale-closing-date-ts']).days
                except Exception as e: ''#self.qd.exception(e)

            #self.dfp = self.dfp.fillna(0)

            #with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
            #    print self.dfp
            self.dfp = self.dfp.combine_first(dftm)
            #print self.dfp.dtypes
            #print dftm.dtypes
            #dindx = self.dfp.index
            #dcols = self.dfp.index
            #self.dfp = combineDF3(self.dfp.to_dict(), dftm.to_dict())
            #self.dfp = p.DataFrame(self.dfp)
            with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
                #dff = self.dfp.set_index('symbol').combine_first(self.cmc.tickers())
                #dff = dftm.set_index('symbol').combine_first(self.cmc.tickers())
                #dff = dff[dff['type'] == 'ethereum']
                #dff = dff[dff['available_supply'] > 0]
                #dff = dff[dff['crowdsale-days'] > 0]
                #print dff
                #print self.dfp
                #print
                #self.dfp
                #print dftm#.transpose()
                #print dftm.transpose()
                ''
            #break
        #li = 'name backlinks domain-score github-starredby github-commits github-contributors github-forks github-openIssues github-watchings crowdsale-opening-date crowdsale-closing-date available_supply total_supply'.split()
        li = xresd.keys()
        #backlinks domain-score
        #links-blog links-facebook links-github links-twitter links-website links-whitepaper name symbol trading    
        for j in li:
            try:    dftm[j] = map(lambda x: x.strip(), dftm[j])
            except: ''            

    def underTheRadarTokens(self):
        # TokenMarket [UnderTheRadar Tokens]
        #self.allAssetsBlockchainTokenMarket()
        #dfp = self.allAssetsICOsBlockchain
        #with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
        #    print self.dfp
        dfp = self.dfp
        #self.dfp.to_csv('tokenmarket.csv', encoding='utf8')
        fi = 'name symbol trading type backlinks domain-score links-blog links-facebook links-github links-twitter links-website links-whitepaper github-starredby github-commits github-contributors github-forks github-openIssues github-watchings crowdsale-opening-date-ts crowdsale-closing-date-ts crowdsale-days crowdsale-days-to-close available_supply total_supply'
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
                #arr = map(lambda x: 0 if x == 'None' else x, arr)
                for x in range(len(arr)):
                    try:    x = x.strip()
                    except: ''
                    if x == 'None':
                        arr[x] = 0
                    else:
                        try:    arr[x] = arr[x].strip()
                        except: ''
                print arr
                print 
                arr = p.to_numeric(p.Series(arr))
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
            print dfr.ix[:,'symbol potentialPortfolioWeight'.split(' ')]#.head(20)
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

    def __init__(self, key=None, secret=None, exchange=None):
        self.qd = QoreDebug()
        self.debug = False
        if key:      self.key      = key.strip()
        if secret:   self.secret   = secret.strip()
        if exchange: self.exchange = exchange.strip()

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
        if self.exchange == 'poloniex':
            #sign = hmac.new(self.secret, digestmod=hl.sha512)
            #sign = _new(self.secret.encode('utf-8'), _urlencode(args).encode('utf-8'),_sha512)
            sen = self.secret.encode('utf-8')
            #print params
            lasd = urllib.urlencode(params)
            lasd = lasd.encode('utf-8')
            sign = hmac.new(sen, lasd, hl.sha512)
            #params = urllib.urlencode(params)
            #sign.update(params)
            return sign.hexdigest()

    #def getResponse():
    
    def requestAuthenticated(self, method=None, url=None, params={}, requestType='POST'):
        if method and self.exchange != 'poloniex':
            params.update({'method':method})
        if self.exchange == 'liqui':
            nonce = str(1)
        if self.exchange == 'bittrex':
            nonce = str(int(time.time() * 1000))
        if self.exchange == 'poloniex':
            nonce = str(int(time.time() * 1000000))
        params.update({'nonce':nonce})

        if self.exchange == 'liqui':
            params = urllib.urlencode(params)
            headers = {'Content-type': 'application/x-www-form-urlencoded',
                      'Key':  self.key,
                      'Sign': self.signHMAC512(params=params)}
        if self.exchange == 'bittrex':
            params = urllib.urlencode(params)
            headers = {'apisign': self.signHMAC512(msg='https://bittrex.com' + url)}
        if self.exchange == 'poloniex':
            #'Content-type': 'application/x-www-form-urlencoded',
            params['command'] = method
            payload = {}
            payload['url'] = url
            payload['data'] = params
            headers = {'Key':  self.key,
                       'Sign': self.signHMAC512(params=params)}
            payload['headers'] = headers
            params = urllib.urlencode(params).encode('utf-8')
            #params = payload
            #headers = payload
            """
            print '---'
            print 'url: %s' % url
            print 'headers: %s' % headers
            print 'params: %s' % params
            print 'payload: %s' % payload
            print '---'
            """
            
        if self.exchange == 'poloniex':
            ret = req.post(**payload)
            response = ret.text
            #sys.exit()
        else:
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
            #self.qd.exception(e)
            try:
                data = uj.loads(response.read())
            except:
                data = uj.loads(response)
        try:
            if self.debug:
                print data
            return data
        except Exception as e:
            print
            self.qd.exception(e)

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

class Poloniex(Exchange):

    def __init__(self, key=None, secret=None):
        Exchange.__init__(self, key, secret, exchange='poloniex')
        self.qd = QoreDebug()
        self.apiServer = 'poloniex.com'
        self.apiMethod = '/tradingApi'
        self.btc = 'DASH ETH FCT GNO LTC XMR REP XRP ZEC'.split(' ')
        self.periods = '1 5 15 30 60 240 14400'.split(' ')
        self.periods = [300, 900, 1800, 7200, 14400, 86400]
        #self.periods = [1, 5, 15, 30, 60, 3600, 14400, 86400]
        print self.periods

    def getInfo(self):
        params = {}
        data = self.requestAuthenticated(url='https://poloniex.com/tradingApi', method='returnBalances', params=params)
        field = 'balance'
        df = p.DataFrame(data, index=[field]).transpose()
        df[field] = p.to_numeric(df[field])
        for i in df[df[field] == 0].index:
            df = df.drop(i)
        #pf(df)
        return df

    def getPoloniexHistorical(self, symbol='BTC_XMR', period=14400, start=1405699200, end=9999999999, bars=15, cache=False):
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
        noCache = not cache
        li = apiRequest('https://poloniex.com/public', '?command=returnChartData&currencyPair=%s&start=%s&end=%s&period=%s' % (symbol, start, end, period), noCache=noCache)
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

    def getCurrencies(self, quote='ETH'):
        #li = apiRequest('https://poloniex.com/public', '?command=returnCurrencies')
        #li = apiRequest('https://poloniex.com/public', '?command=returnTicker')
        payload = {}
        payload['url'] = 'https://poloniex.com/public?command=returnTicker'
        ret = req.get(**payload)
        li = uj.loads(ret.text)

        df = p.DataFrame(li)
        df = df.transpose()
        df = df.sort_values(by='percentChange', ascending=False)
        for x in xrange(len(df.index)):
            sp = df.index[x]
            _quote = sp.split('_')[0]
            _base  = sp.split('_')[1]
            df.loc[sp, 'quote'] = _quote
            df.loc[sp, 'base']  = _base
            df.loc[sp, 'symbol']  = '%s/%s'%(_base, _quote)
        if quote != None and type(quote) == type(''):
            df = df[df['quote'] == quote]
        df['last'] = p.to_numeric(df['last'])
        return df

    def trade(self, pair=None, method='buy', rate=None, amount=None):
        params =   {
                    #'type':mtype,
                    'currencyPair': str(pair).upper(),
                    'rate': str(rate),
                    'amount': str(amount),
                    }
        data = self.requestAuthenticated(url='https://poloniex.com/tradingApi', method=method, params=params)
        try:
            df = p.DataFrame(data, index=[pair])#.transpose()
            print df
        except Exception as e:
            print e
            try: print data['error']
            except: ''
            return
        return df.transpose()


    def makeCurrencyTimeseriesTable(self, symbols, bars=15):
        li = symbols.split(' ')
        #li = 'BTC ETH EOS OMG'.split(' ')
        #li = map(lambda x: 'USDT_%s'%x, li)
        mdf = p.DataFrame()
        for i in range(len(li)):
            symbol = li[i]
            quote = symbol.split('_')[0]
            try:    base  = symbol.split('_')[1]
            except: base = ''
            if base == '':
                symbol = 'USDT_%s' % symbol
                li[i]  = symbol
            #try:    print '%s %s %s' % (quote, base, symbol)
            #except: print '%s %s' % (quote, symbol)
            try:
                df = self.getPoloniexHistorical(symbol=symbol, period=86400, bars=bars, cache=True)#.set_index('date')
                df = df.set_index('date').loc[:, 'close volume'.split(' ')]
                df[symbol] = df['close']
                #plt.plot(df['close'])
                #plt.show()
                #print df
                #print df
                #print df.shape
                mdf = mdf.combine_first(df.loc[:, [symbol]])
            except Exception as e:
                print '%s: %s' % (li[i], e)
                #print '%s %s' % (symbol, e)
                ''
            if base != '':
                #print symbol
                try: mdf[symbol] = mdf[symbol] * mdf['USDT_ETH']
                except:''
        """
        mdf = p.DataFrame()
        li = symbols.split(' ')
        #li = 'BTC ETH EOS OMG'.split(' ')
        #li = map(lambda x: 'USDT_%s'%x, li)
        for i in range(len(li)):
            symbol = li[i]
            quote = symbol.split('_')[0]
            try:    base  = symbol.split('_')[1]
            except: base = ''
            if base == '':
                symbol = 'USDT_%s' % symbol
                li[i]  = symbol
            #try:    print '%s %s %s' % (quote, base, symbol)
            #except: print '%s %s' % (quote, symbol)
            try:
                df = self.getPoloniexHistorical(symbol=symbol, period=86400, bars=bars, cache=True)#.set_index('date')
                df = df.set_index('date').loc[:, 'close volume'.split(' ')]
                df[symbol] = df['close']
                #plt.plot(df['close'])
                #plt.show()
                #print df
                mdf = mdf.combine_first(df.loc[:, [symbol]])
            except Exception as e:
                print e
                #print '%s %s' % (symbol, e)
                ''
            if base != '':
                #print symbol
                try: mdf[symbol] = mdf[symbol] * mdf['USDT_ETH']
                except:''
        """
        return mdf

    def allocations(self, quote, symbols='BTC ETH LTC XRP DASH XEM XMR MIOTA NEO ETH_OMG', bars=15, cache=True, balance=None):
        import matplotlib.pylab as plt
        from qoreliquid import normalizeme, sigmoidme
        import seaborn as sea
        sea.set()

        if balance == None:
            try:
                bdf = self.getBalanceTable(live=False, quote=quote)
                with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
                    print bdf
                balance = n.sum(bdf['balanceUSDT'].get_values())
            except Exception as e:
                print e
                balance = 100

        try:
            # equity allocations
            mdf = self.makeCurrencyTimeseriesTable(symbols, bars=bars)
            #mdf['sum'] = n.sum(mdf.get_values(), 1)
        
            # convert weight to percentage
            """for symbol in li:
                try:    mdf[symbol] = mdf[symbol] / mdf['sum']
                except: ''
            mdf = mdf.loc[:, li]"""
            
            mdf = normalizeme(mdf)
            mdf = sigmoidme(mdf)
            mdf = mdf.fillna(0)
    
            #mdf.loc['sum',:]  = n.sum(mdf.get_values(), 0)
            #mdf.loc[:, 'sum'] = n.sum(mdf.get_values(), 1)
            psum              = n.sum(mdf.get_values(), 1)
            for symbol in mdf.columns: mdf[symbol] = mdf[symbol] / psum
            # fix portfolio dilution on coin addition [for improved visualization in plot]
            dff = n.sum(n.array(mdf > 0, dtype=int), 1)
            mdf.loc[:, :] = (mdf.get_values().T * dff).T        
            #mdf = mdf.drop('sum', 1)
            pmdf = mdf
        except:
            import matplotlib.pylab as plt
            import seaborn as ss
            ss.set()    
            df0 = p.read_csv('/tmp/allocations2.csv', index_col=0)
            # fix portfolio dilution on coin addition [for improved visualization in plot]
            dff = n.sum(n.array(df0 > 0, dtype=int), 1)
            df1 = df0.copy()
            df0.loc[:, :] = (df0.get_values().T * dff).T
            with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
                print df1.tail(10)
                print df0.tail(10)
            plt.plot(df0)
            plt.legend(df0.columns, loc=2)
            plt.show()
            sys.exit()
                    
        # save to allocations.csv file
        ts = max(pmdf.index)
        pdf = pmdf.loc[[ts], :].transpose()
        #pdf['portPcnt'] = pdf[ts]
        pdf['quote'] = map(lambda x: x.split('_')[0], pdf.index)
        pdf['base']  = map(lambda x: x.split('_')[1], pdf.index)
        #pdf['usd'] = pdf[ts] * balance
        pdf = pdf.rename_axis({ts:'portPcnt'}, axis='columns')
        fname = '/tmp/allocations.csv'
        fname2 = '%s.%s'%(fname, int(time.time()))
        print '%s %s' % (fname, fname2)
        pdf.to_csv(fname)
        rdf = p.read_csv(fname, index_col=0)
        rdf.to_csv(fname2)
        pmdf.to_csv('/tmp/allocations2.csv')
        with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
            print pmdf#.tail(10)
            #print pmdf.dtypes
            #for symbol in pmdf.columns: pmdf[symbol] = pmdf[symbol] / psum
            plt.plot(pmdf.tail(100))
            plt.legend(pmdf.columns, loc=2)
            plt.show()
            ''
        return pmdf
    
    def _allToCoin(self, df, coin):
        df['portPcnt'] = 0
        df.loc[coin, 'portPcnt'] = 1
        return df

    def getBalanceTable(self, live=False, verbose=False, quote='ETH', allToCoin=None):
        df = self.getCurrencies(quote=quote)
        df = setIndex(df, 'base', 'symbol2')
        #df = self.getCurrencies(quote=None)
        dfbtc = self.getCurrencies(quote='BTC')
        dfbtc = setIndex(dfbtc, 'base', 'symbol2')
        df = df.combine_first(dfbtc)
        dfusdt = self.getCurrencies(quote='USDT')
        df['id'] = df.index
        pdf = p.read_csv('/tmp/allocations.csv', index_col=0)
        pdf = setIndex(pdf, 'base', 'symbol2')
        print pdf
        def nom(pmdf):
            pmdf = pmdf.transpose()
            ff = pmdf.index[0]
            psum = n.sum(pmdf, 1)
            psum = psum[ff]
            for symbol in pmdf.columns: pmdf.loc[ff,symbol] = pmdf.loc[ff,symbol] / psum
            pmdf = pmdf.transpose()
            return pmdf
        pdf = nom(pdf)
        df = df.combine_first(pdf)#.fillna(0)
        #df = df.set_index('base')
        bdf = self.getInfo()
        df = df.combine_first(bdf).fillna(0)
        df['lastUSDT'] = df['last'] * dfusdt.loc['USDT_ETH', 'last']
        df.loc['USDT', 'last'] = 1
        df.loc['USDT', 'lastUSDT'] = 1
        df['balanceUSDT'] = df['balance'] * df['lastUSDT']

        # fix balances
        for i in df[df['quote'] == 'USDT'].index:
            for j in dfusdt.columns:
                df.loc[i, j] = dfusdt.loc[df.loc[i, 'symbol2'], j]
                df.loc[i, 'lastUSDT'] = df.loc[i, 'last']
                df.loc[i, 'balanceUSDT'] = df.loc[i, 'balance'] * df.loc[i, 'lastUSDT']

        #df.loc['sum', 'balanceUSDT'] = n.sum(df['balanceUSDT'])
        
        if allToCoin != None:
            df = self._allToCoin(df, allToCoin)
        
        df['portBalanceUSDT'] = df['portPcnt'] * df['balanceUSDT'].sum()
        df['diffUSDT'] = df['portBalanceUSDT'] - df['balanceUSDT']
        #df['diffUSDT'] = df['usd'] - df['balanceUSDT']
        df['diffETH'] = df['diffUSDT'] / dfusdt.loc['USDT_ETH', 'last']
        df['diffBTC'] = df['diffUSDT'] / dfusdt.loc['USDT_BTC', 'last']
        df['diffQuote'] = df['diff%s'%quote] / df['last']
        df = df.fillna(0)
        df = df[(df['portPcnt'] > 0.0) | (df['balance'] > 0.0)]
        mdf = df.loc[:, 'symbol2 last diffQuote'.split(' ')].sort_values(by='diffQuote', ascending=True).set_index('symbol2')
        with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
            #print bdf
            #print pdf
            print df
            #print df.loc[:, 'quote symbol2 balanceUSDT usd diffUSDT diffETH diffQuote'.split(' ')]
            #print mdf
            ''
        for i in mdf.index:
            diffQuote = mdf.loc[i, 'diffQuote']
            method = 'buy' if diffQuote > 0 else 'sell'
            last = mdf.loc[i, 'last']
            if i != 0 and last != 0:
                if verbose:
                    print
                    print '=== %s' % i
                    #print mdf.loc[i, :]
                    print 'pair=%s method=%s rate=%s amount=%s' % (i, method, last, n.abs(diffQuote))
                if live:
                    self.trade(pair=i, method=method, rate=last, amount=n.abs(diffQuote))
                #break
                #time.sleep(1)
        print 'balance: %s' % n.sum(df['balanceUSDT'])
        return df

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
            self.qd.exception(e)

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
            
class EtherDelta:
    
    def parseEtherDeltaDump(self):
        import re
        fp = open('/mldev/bin/data/cache/coins/etherdelta.volume.tsv', 'r')
        res = fp.read()
        fp.close()
        #print res
        res = re.sub(re.compile(r'.*?Offer(.*?)(Token|Order|ORDER).*', re.S), '\\1', res)
        res = res.strip()
        return res
    
    def toMjson(self, df, fname):
        import ujson as uj
        df = df.fillna(0)
        try:
            df = df.set_index('symbol')
        except:
            ''
        tojson = df.transpose().to_dict()
        tojson = {'timestamp':time.time(), 'data':tojson}
        try:
            tojson = uj.dumps(tojson)
            fp = open(fname, 'a')
            fp.write('%s\n' % tojson)
            fp.close()
        except: ''

class Eveningstar:
    
    #https://eveningstar.io/my-portfolio/
    def __init__(self):
        self.qd = QoreDebug()
        self.fname = '/tmp/coins-eveningstar-export.csv'
        try:    self.df = p.read_csv(self.fname)
        except: self.df = p.DataFrame([])
    
    def exportPortfolio(self):
        try:    self.df.set_index('Asset Id').to_csv(self.fname, doublequote=True, quotechar='"', quoting=True, line_terminator='\r\n')
        except: ''            

    def addToPortFolio(self, assetId, quantity, costBasis):
        self.df.loc[len(self.df.index)+1, :] = p.Series({'Quantity': quantity, 'Cost Basis Each (USD)': costBasis, 'Asset Id': assetId})
        return self.df

#@profile
def getAdressInfoEthplorer(ethaddr, verbose=False, instruments=5, noCache=True, initialInvestment=0, model=None, allocationModel=None):
    
    if type(ethaddr) == type(''):
        ethaddr = ethaddr.split(' ')
    
    cmc = CoinMarketCap()
    pm = PortfolioModeler()
    
    eth = cmc.getTicker('ETH').set_index('symbol').transpose()
    ethusd = float(eth.loc['price_usd', 'ETH'])
    mdf0 = p.DataFrame([])
    dfp = pm.modelPortfolio(num=instruments, ethusd=ethusd, allocationModel=allocationModel)
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
                #print e
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
                dfp = pm.modelPortfolio(num=instruments, ethusd=ethusd, allocationModel=allocationModel)
                #df = df.combine_first(dfp)
                #df = pm.genPortfolio(df)
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
            #print mdf.sort_values(by='balance_usd', ascending=False)
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

        # filter invalid contracts
        ic = ['0xb04cfa8a26d602fb50232cee0daf29060264e04b']
        mdf0 = dfinfo.combine_first(mdf0)
        for x in mdf0.index:
            try: mdf0.loc[x, 'id4'] = '%s-%s' % (x, mdf0.loc[x, 'address'][0:8])
            except: ''
        for ici in ic:
            try:
                for x in list(mdf0[mdf0['address'] == ici].index):
                    mdf0 = mdf0.drop(x)
            except: 
                ''
        
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
            try:
                mdf0['balance_usd']
            except:
                print mdf0.fillna(0)
                return
            balanceUSDTotal = mdf0['balance_usd'].sum() #+ 89.736
            ethUSDTotal     = addressInfos['balance'].sum() * ethusd
            pc  = ((balanceUSDTotal + ethUSDTotal) / initialInvestment * 100)-100
            pc2 = (balanceUSDTotal + ethUSDTotal) - initialInvestment
            #for i3 in addressInfos.index:
            #    print mdf0[mdf0['ethaddr'] == i3]
            mdf0['ethUSDTotal'] = ethUSDTotal
            mdf0 = pm.genPortfolio(mdf0)
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
            f = '24h_volume_usd allocation avg balance balance_usd bid ethaddr holdersCount id2 id3 issuancesCount offer price_btc price_usd rank symbol t1 t2 volume portWeight portPcnt totalBalanceUsd portUsd portUnits unitsDiff balanceUsdDiff balanceETHDiff'.split()
            f = 'totalBalanceUsd 24h_volume_usd allocation avg balance balance_usd portUsd balancePortDiffUSD balancePerPort bid offer spread spreadPcnt spreadPcntA ethaddr holdersCount price_btc price_usd rank mname volume volumePerHolder holdersPerVolume portWeight portPcnt portUsd portUnits mname avg balance unitsDiff unitsDiffPerBalance balancePerUnitsDiff balanceByUnitsDiff balanceByUnitsDiff2 balanceByBalanceUsdDiff balanceUsdDiff balanceETHDiff t1'.split()
            f = ('id id2 id4 totalBalanceUsd totalBalanceEth balance_eth balance_usd currentPortPcnt avg price_eth arb1 mname sum mvp allocation portPcnt price_usd balance balance_eth balance_usd currentPortPcnt portPcnt portUsd balancePortDiffUSD balanceETHDiff balanceETHDiffCumsum balancePerPort bid offer spread spreadPcnt spreadPcntA ethaddr holdersCount price_btc price_usd rank mname 24h_volume_usd volume volumeETH volumeUSD volumePerHolder volumeETHPerHolder holdersPerVolume portWeight portPcnt portUsd portUnits mname sum avg balance balance_usd spreadPcnt avg unitsDiff balanceETHDiff ethaddr unitsDiffPerBalance balancePerUnitsDiff balanceByUnitsDiff balanceByUnitsDiff2 balanceByBalanceUsdDiff balanceUsdDiff balanceETHDiff %s' % pm.allocationModels).split()
            pm.printPortfolio(mdf0, f)
            print '---'
            print dfinfo
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

#%reload_ext autoreload
#%autoreload 2
from bitmex import *

def setIndex(df, to, oldIndex):
    df[oldIndex] = df.index
    df = df.set_index(to)
    return df

#@profile
def main():
    pl = Poloniex('M8YTJIKE-2EIE8VV2-7UP6Z9O0-PJNGRPV4', '')
    #pl.debugon()

    import argparse
    # source: https://docs.python.org/2/howto/argparse.html
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", '--verbose', help="turn on verbosity")
    parser.add_argument("-lm", '--listPortfolioModels', help="", action="store_true")
    parser.add_argument("-pm", '--setPortfolioModel', help="")
    parser.add_argument("-model", '--allocationModel', help="")
    parser.add_argument("-cu", '--currency', help="currency")
    parser.add_argument("-all2", '-a2', '--allToCoin', help="convert all coin to..")
    parser.add_argument("-l", '--live', help="go live and turn off dryrun", action="store_true")
    parser.add_argument("-pa", '--parse', help="go live and turn off dryrun", action="store_true")
    parser.add_argument("-p", '--portfolio', help="go live and turn off dryrun", action="store_true")
    parser.add_argument("-gp", '--genPortfolio', help="parseCoinMrketCap skipTo", action="store_true")
    parser.add_argument("-sk", '--parseCoinMarketCapSkipTo', help="parseCoinMrketCap skipTo")
    parser.add_argument("-b", '--balance', help="parseCoinMrketCap skipTo")
    parser.add_argument("-tm", '--tokenmarket', help="parseCoinMrketCap skipTo", action="store_true")
    parser.add_argument("-rad", '--underTheRadarTokens', help="parseCoinMrketCap skipTo", action="store_true")
    parser.add_argument("-r01", '--research01', help="parseCoinMrketCap skipTo", action="store_true")
    parser.add_argument("-eth", '--ethAccount', help="parseCoinMrketCap skipTo")
    parser.add_argument("-addr", '--ethAddress', help="parseCoinMrketCap skipTo")
    parser.add_argument("-num", '--instruments', help="parseCoinMrketCap skipTo")
    parser.add_argument("-bars", '--bars', help="bars")
    parser.add_argument("-r01b", '--research01bittrex', help="parseCoinMrketCap skipTo", action="store_true")
    parser.add_argument("-r03", '--research03', help="parseCoinMrketCap skipTo", action="store_true")
    parser.add_argument("-r04", '--research04', help="parseCoinMrketCap skipTo", action="store_true")
    parser.add_argument("-r05", '--research05', help="parseCoinMrketCap skipTo", action="store_true")
    parser.add_argument("-r06", '--research06', help="test 06", action="store_true")
    parser.add_argument("-r06a",'--research06a',help="test 06a",action="store_true")
    parser.add_argument("-r07", '--research07', help="test 07", action="store_true")
    parser.add_argument("-r08", '--research08', help="test 08", action="store_true")
    parser.add_argument("-r09", '--research09', help="test 09", action="store_true")
    parser.add_argument("-r10", '--research10', help="test 10 onexchange", action="store_true")
    parser.add_argument("-r11", '--research11', help="test 11", action="store_true")
    parser.add_argument("-r12", '--research12', help="test 12", action="store_true")
    parser.add_argument("-r13", '--research13', help="test 13", action="store_true")
    parser.add_argument("-r14", '--research14', help="test 14", action="store_true")
    parser.add_argument("-r15", '--research15', help="test 15", action="store_true")
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
    
    if args.research13:
        
        #print pl.trade(pair='ETH_ZRX', method='sell', rate=0.0006, amount=5)
        quote = args.currency # ETH or BTC
        live = args.live
        try:    allToCoin = args.allToCoin
        except: allToCoin = None
        df = pl.getBalanceTable(live=live, verbose=True, quote=quote, allToCoin=allToCoin)
        print 'allToCoin: %s' % allToCoin
        with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
            print df
    
    if args.research12:
        """import pkg_resources
        def ff(name):
            print '%s: %s' % (name, pkg_resources.get_distribution(name).version)
        ff('poloniex')
        ff('urllib3')
        import poloniex
        #from urllib import urlencode as _urlencode
        pl = poloniex.Poloniex('M8YTJIKE-2EIE8VV2-7UP6Z9O0-PJNGRPV4', '')
        print pl.returnBalances()        
        """
        #def main3():
    
        #cmc = CoinMarketCap()
        #df = cmc.tickers()
    
        bars = (365*4)
        #bars = 20
        #symbols = 'BTC ETH LTC XRP DASH XEM XMR MIOTA NEO'
        #symbols = 'BTC ETH ETH_OMG ETH_PLR ETH_PPT ETH_CDT ETH_ZRX ETH_PAY'
        
        # etherdelta
        #symbols = 'BTC ETH %s' % ' '.join(map(lambda x: 'ETH_%s'%x, list(p.read_csv('/tmp/symbols.txt', index_col=0)['0'].get_values()) ))
        
        # poloniex
        try:    quote=args.currency # ETH or BTC
        except: quote = 'ETH'
        if not quote in 'BTC ETH'.split(' '):
            print '-cu[currency] should == BTC | ETH'
            sys.exit()
        df = pl.getCurrencies(quote=quote)
        if quote == 'ETH':
            symbols = 'BTC ETH %s' 
        if quote == 'BTC':
            symbols = 'BTC %s'
        symbols = symbols % ' '.join(list(df.index))
        print symbols
        pdf = pl.allocations(quote, symbols=symbols, bars=bars)
        with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
            print pdf

    if not args.research11:
        cmc = CoinMarketCap()
        pm  = PortfolioModeler()
        #cmc.getTradableCoins()

    try:    instruments = int(args.instruments)
    except: instruments = 50

    try:    allocationModel = args.allocationModel
    except: allocationModel = None

    if args.listPortfolioModels:
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
    if args.tokenmarket or args.underTheRadarTokens:
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

        # other
        initialInvestment = 0
        if args.ethAccount == '0':
            getAdressInfoEthplorer([args.ethAddress.split(' ')], args.verbose, instruments=instruments, noCache=noCache, initialInvestment=initialInvestment, allocationModel=allocationModel)

        #ethaddress1 = '0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae'
        usdars = 16.72
        initialInvestment = (970.0+850+1800) / usdars
        otherInvestments = {
            'genesis': 230,
            'steemit SP': 25.0/1.3,
            'steemit SBD': 0,
            'steemit STEEM': 0,
        }

        try:    ethAccount = int(args.ethAccount)
        except: ethAccount = args.ethAccount
        
        if type(ethAccount) == type(''):
            getAdressInfoEthplorer(ethAccount.split(' '), args.verbose, instruments=instruments, noCache=noCache, initialInvestment=initialInvestment, allocationModel=allocationModel)
        else:
            if args.ethAccount == '1':
                getAdressInfoEthplorer([eth1_2, eth1_1], args.verbose, instruments=instruments, noCache=noCache, initialInvestment=initialInvestment, allocationModel=allocationModel)
            
            usdtwd = 30.41
            initialInvestment = 40000.0 / usdtwd
            if args.ethAccount == '2':
                getAdressInfoEthplorer(['', eth2_2, eth2_1], args.verbose, instruments=instruments, noCache=noCache, initialInvestment=initialInvestment, allocationModel=allocationModel)
            #print getTicker('bitcoin')    
    
            # ??? etherdelta
            #initialInvestment = 1
            if args.ethAccount == '3':
                getAdressInfoEthplorer([''], args.verbose, instruments=instruments, noCache=noCache, initialInvestment=initialInvestment, allocationModel=allocationModel)

    if args.research03:
        df1 = cmc.getTicker('PPT').set_index('symbol').transpose()
        print df1
    
    if args.genPortfolio:
        with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
            dfp = pm.modelPortfolio(num=instruments)
            gpdf = pm.genPortfolio(dfp)
            print dfp
            print gpdf
        #import qgrid
        #qgrid.show_grid()
        import dfgui
        dfgui.show(dfp)
    
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

        dfp = pm.modelPortfolio(df=df)
        #df = pm.genPortfolio(df, volume='Volume')

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

    if args.research06:
        cmc = CoinMarketCap()
        with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
            #print cmc.getTradableCoins(filterVolume=False)
            if args.currency:                
                print cmc.getCoinsExchanges(args.currency).transpose()
            else:
                print cmc.getCoinsExchanges('bitcoin').transpose()

    if args.research06a:
        cmc = CoinMarketCap()
        with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
            for i in 'tnt,adt,ppt'.split(','):
                cmc.resolveCoin(i)
                print cmc.resolvedCoin
            #print cmc.getTradableCoins(filterVolume=False)

    if args.research07:
        def tryGetCoinsOnExchange(exchange, args):
            try:
                df = cmc.getCoinsOnExchange(exchange=exchange, cache=args.cache)
            except:
                df = cmc.getCoinsOnExchange(exchange=exchange, cache=False)
            return df
        #df = cmc.getCoinsOnExchange(exchange='Bittrex', cache=False)#args.cache)
        #df = tryGetCoinsOnExchange('Bittrex', args)
        df = tryGetCoinsOnExchange('EtherDelta', args)
        #print df.sort_index()
        print df.sort_values(by='sum', ascending=True)
        
    if args.research08:
        from qore import XPath
        ethaddr = args.ethAddress
        url = 'https://etherscan.io/tokentxns?a=%s' % ethaddr
        #url = 'https://etherscan.io/tokentxns?a=%s&p=3' % ethaddr
        xp = XPath()
        xresd = xp.xpath2df(url, {
            'name' : '/html/body/div[1]/div[4]/div[2]/div/div/div/table//tr/td[7]/a/text()',
            'bal'  : '/html/body/div[1]/div[4]/div[2]/div/div/div/table//tr/td[6]/text()',
            #'href'       : '//*[@id="table-all-assets-wrapper"]/table/tbody/tr/td[4]/div[1]/a/@href',
            #'status'     : '//*[@id="table-all-assets-wrapper"]/table/tbody/tr/td[3]/span/text()',
            #'symbol'     : '//*[@id="table-all-assets-wrapper"]/table/tbody/tr/td[5]/text()',
            #'description': '//*[@id="table-all-assets-wrapper"]/table/tbody/tr/td[6]/text()',
            #'hot': '//*[@id="table-all-assets-wrapper"]/table/tbody/tr/td[4]/div[2]/text()',        
        })#, verbose=True)
        #print xresd
        for i in xresd.keys(): print 'len %s: %s' % (i, len(xresd[i]))
        #print p.DataFrame(xresd)

        import numba
        #@profile
        #@numba.jit(nopython=True)
        @numba
        def xresdFix(xresd):
            xresdlen = {}
            for j in xresd: xresdlen[j] = len(xresd[j])
            #xresdlen = [len(xresd[j]) for j in xresd]
            #print xresdlen
            xresdlen = p.DataFrame(xresdlen, index=['len'])
            xresdlen = xresdlen.transpose()
            xresdlen['max'] = n.max(xresdlen['len'])
            xresdlen['min'] = n.min(xresdlen['len'])
            xresdlen['diff'] = xresdlen['max'] - xresdlen['len']
            xresdlen['diffMin'] = n.abs(xresdlen['min'] - xresdlen['len'])
            #print xresdlen
            #print xresd
            for j in xrange(len(xresdlen['diff'])):
                try:
                    #print '%s %s' % (j, xresdlen['diff'][j])
                    if xresdlen['diff'][j] > 0:
                        print j
                        #xresdlen = xresdlen.drop(xresdlen.index[j])
                        xresd.pop(xresdlen.index[j])
                        #print p.DataFrame(xresd)
                except:
                    ''
            return xresd
            
        xresd = xresdFix(xresd)
        
        for i in xresd.keys(): print 'len %s: %s' % (i, len(xresd[i]))
                

        """
        Bought MSP at 0.06, sold at 0.25
        Bought BAT at 0.08, sold at 0.25
        Bought DNT at 0.017, sold at 0.147
        """

    if args.research09:
        
        """
        ev = Eveningstar()        
        #df.loc[2, :] = p.Series(se.to_dict())
        ev.addToPortFolio('tenx', 23.052199999999999, 0)
        ev.addToPortFolio('tenx', 23.052199999999999, 0)
        ev.addToPortFolio('tenx', 23.052199999999999, 0)
        ev.addToPortFolio('tenx', 23.052199999999999, 0)
        #df.loc[3, :] = p.Series({'Quantity': 23.052199999999999, 'Cost Basis Each (USD)': 0, 'Asset Id': 'tenx'})
        ev.exportPortfolio()
        print ev.df
        """
        
        #df = apiRequest('https://www.coinexchange.io/api/v1', '/getmarkets')
        df = apiRequest('https://www.coinexchange.io/api/v1', '/getmarketsummaries')

        print p.DataFrame(df)
        print p.DataFrame(df['result'])


    if args.research10:
        cmc = CoinMarketCap()
        cache=False
        df1 = cmc.getCoinsOnExchange(exchange='EtherDelta', cache=cache)
        df2 = cmc.getCoinsOnExchange(exchange='Poloniex', cache=cache)
        print '==='
        print df1.index
        print df2.index
        print '==='
        df3 = df2.loc[df1.index, :]
        print df3[df3['sum'] > 0]

    if args.research11:
        try:    symbol = args.currency
        except: symbol = 'BTC_XVC'
        try:    bars = int(args.bars)
        except: bars = 10
        
        #symbols = map(lambda x: 'BTC_%s'%x, 'XVC GAS EMC2 SBC'.split(' '))
        #print symbols

        pl = Poloniex()

        df = pl.getCurrencies()
        with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
            print df
        sys.exit()
        
        #def getPoloniexHistorical(self, symbol='BTC_XMR', period=14400, start=1405699200, end=9999999999, bars=15):
        #df = pl.getPoloniexHistorical(symbol=symbol, period=300, bars=bars).set_index('date')
        df = pl.getPoloniexHistorical(symbol=symbol, period=300, bars=15)#.set_index('date')
        df['symbol'] = symbol
        df = df.set_index('symbol')
        #df = df.tail(1)
        with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
            print df

    if args.research14:
        symbols='BTC ETH BTH XRP LTC DASH XEM MIOTA XMR NEO ETC'
        bars = 365*(2017-2008)
        mdf = pl.makeCurrencyTimeseriesTable(symbols, bars=bars)
        mdf.loc[:, mdf.columns] = mdf.get_values() * n.array([16588437,94831556, 38343841883])
        mdf['sum'] = n.sum(mdf.get_values(), 1)
        mdf.to_csv('/mldev/bin/data/cache/coins/marketcap.csv')
        with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
            print mdf


    if args.research15:
        from scipy import signal
        import matplotlib.pylab as plt
        def peaks(df, seekWidth):
            x = df.index
            y = df['sum'].get_values()
            #x = n.arange(0, n.pi, 0.05)
            #y = n.sin(x)
            peakind = signal.find_peaks_cwt(y, n.arange(1,seekWidth))
            #print peakind
            pdf = p.DataFrame()
            print '---'
            #print list(x[peakind])
            pdf['x'] = x[peakind]
            #print type(y)
            pdf['y'] = y[peakind]
            #print list(y[peakind])
            #print x
            print pdf
            df['sum'].plot(logy=True)
            plt.scatter(x[peakind], y[peakind])
            #plt.plot(x, y)
            #plt.legend(mdf.columns, loc=2)
            plt.show()
            #([32], array([ 1.6]), array([ 0.9995736]))
        """x = n.arange(0, n.pi, 0.05)
        y = n.sin(x)
        peaks(x, y)
        sys.exit()"""

        mdf = p.read_csv('/mldev/bin/data/cache/coins/marketcap.csv', index_col=0)
        try:    num = int(args.instruments)
        except: num = 10
        seekWidths = [2,3,5,8,13,21,34,55,89,144,233]
        """
        seekWidth = num
        mdf['sum'] = p.rolling_mean(mdf['sum'], seekWidth)
        #mdf['sum'].plot(logy=True)
        #plt.legend(mdf.columns, loc=2)
        #plt.show()
        #sys.exit()
        #peaks(mdf.index, mdf['sum'].get_values())
        peaks(mdf, seekWidth)
        #mdf['sum'] = 1/mdf['sum']
        #peaks(mdf, seekWidth)"""
        #sys.exit()
        for i in range(len(seekWidths)-1, -1, -1):
            print seekWidths[i]
            seekWidth = seekWidths[i]
            cmdf = mdf.copy()
            #cmdf['sum'] = p.rolling_mean(cmdf['sum'], seekWidth)
            cmdf['sum'] = cmdf['sum'].rolling(window=seekWidth).mean()
            #cmdf['sum'].plot(logy=True)
            #plt.legend(cmdf.columns, loc=2)
            #plt.show()
            #sys.exit()
            #peaks(cmdf.index, cmdf['sum'].get_values())
            peaks(cmdf, seekWidth)
            #cmdf['sum'] = 1/cmdf['sum']
            #peaks(cmdf, seekWidth)"""
        sys.exit()

        peaks(mdf.index, list(mdf['sum']))
        import matplotlib.pylab as plt
        plt.plot(mdf['sum'])
        plt.legend(mdf.columns, loc=2)
        plt.show()
        mdf['sum'].plot(logy=True)
        plt.legend(mdf.columns, loc=2)
        plt.show()
        sys.exit()

    # portfolio tokenization
    if args.research05:
        portfolioTokenization()

if __name__ == "__main__":
    main()
