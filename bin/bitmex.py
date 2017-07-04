
#"""
import argparse
# source: https://docs.python.org/2/howto/argparse.html
parser = argparse.ArgumentParser()
parser.add_argument("-v", '--verbose', help="turn on verbosity")
parser.add_argument("-l", '--live', help="go live and turn off dryrun", action="store_true")
parser.add_argument("-pa", '--parse', help="go live and turn off dryrun", action="store_true")
parser.add_argument("-p", '--portfolio', help="go live and turn off dryrun", action="store_true")
parser.add_argument("-sk", '--parseCoinMarketCapSkipTo', help="parseCoinMrketCap skipTo")
parser.add_argument("-b", '--balance', help="parseCoinMrketCap skipTo")

args = parser.parse_args()

import sys
try: sys.path.index('/ml.dev/bin/datafeeds')
except: sys.path.append('/ml.dev/bin/datafeeds')
#"""
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
        df = p.DataFrame(li)
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
        btc = 'DASH ETH FCT GNO LTC XMR REP XRP ZEC'.split(' ')
        periods = '1 5 15 30 60 240 14400'.split(' ')
        periods = [300, 900, 1800, 7200, 14400, 86400]
        #periods = [1, 5, 15, 30, 60, 3600, 14400, 86400]
        print periods
        from matplotlib import pyplot as plt
        from pylab import rcParams
        import seaborn as sns
        sns.set()
        #%pylab inline
        rcParams['figure.figsize'] = 30, 5
        btc_usd = 2400
        for i in btc:
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

# cypto api 
exchangePriority = {
'Bittrex':3,
'Cryptopia':1,
'Novaexchange':2,
'Poloniex':5,
'YoBit':4
}

def apiRequest(baseurl, query, method='GET'):
    #import drest
    #api = drest.API(baseurl)
    #response = api.make_request(method, query)
    #res = response.data

    #import drest
    import ujson as uj
    # source: https://stackoverflow.com/questions/27118086/maintain-updated-file-cache-of-web-pages-in-python
    import requests as req, requests_cache
    requests_cache.install_cache('scraper_cache', backend='sqlite', expire_after=3600*24)
    #baseurl = 'http://api.coinmarketcap.com/'
    #method  = '/v1/ticker/'
    #api = drest.API(baseurl)
    #response = api.make_request(method, query)
    #res = response.data
    resp = req.get('%s%s' % (baseurl, query))
    res = resp.text
    res = uj.loads(res)
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
            'YoBit':4
        }
        self.parseCoinMarketCapSkipTo = 0
        pass

    #@profile
    def tickers(self):
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
        for i, v in enumerate(self.dfc['id']):#[0:20]:
            print '%s: %s' % (i, v);
            if i >= self.parseCoinMarketCapSkipTo:
                dfxs = dfxs.combine_first(self.getExchanges(v))
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
        df = df[df['price_usd'] <= 0.1]
        df = df[df['24h_volume_usd'] >= 100000]
        try:
            df = df.drop('FEDS')
        except:
            ''
    
        df = df.ix[:, c]
        df = df.sort_values(by='24h_volume_usd', ascending=False)
        df = df.sort_values(by='percent_change_24h', ascending=False)
    
        self.df = df

    #@profile
    def generatePortfolio(self, bal=165.11):
        try:
            self.df
        except:
            self.getTradableCoins()
        df = self.df
        # portfolio

        #df['portPcnt']         =      df['price_usd'] / df['price_usd'].sum() * 1
        #df['portPcnt']         =      (df['24h_volume_usd'] / df['price_usd']) / ((df['24h_volume_usd'] / df['price_usd'])).sum() * 1
        df['portPcnt']         =      (df['price_usd'] / df['24h_volume_usd']) / (df['price_usd'] / df['24h_volume_usd']).sum() * 1
        #df['portPcntPinv']     =   1 - df['portPcnt']
        df['portPcntPinv']     =   1 / df['portPcnt'] # df['portPcnt']
        df['portPcntPinv2']    =   df['portPcntPinv'] / df['portPcntPinv'].sum() * 100
        df['portAmount']       =  df['portPcntPinv2'] * bal / 100
        df['portAmount_usd']   =  df['portPcntPinv2'] * bal / 100
        df['portAmount_units'] = df['portAmount_usd'] / df['price_usd']
        df['at'] = df['available_supply'] / df['total_supply']
        df['mv'] = df['24h_volume_usd'] / df['market_cap_usd']
    
        c = '24h_volume_usd id market_cap_usd name percent_change_24h percent_change_7d price_btc price_usd portPcnt portPcntPinv portPcntPinv2 portAmount_usd portAmount_units'.split(' ')    
        c = '24h_volume_usd name percent_change_24h percent_change_7d price_usd portPcnt portPcntPinv portPcntPinv2 portAmount_usd portAmount_units'.split(' ')    
        c = '24h_volume_usd name percent_change_24h percent_change_7d price_usd portPcnt portPcntPinv portPcntPinv2 portAmount_usd portAmount_units'.split(' ')
        df = df.sort_values(by='portPcntPinv2', ascending=False)
    
        # tradableCoins2
        tradableCoins = self.tradableCoins
        #print list(tradableCoins.index)
        tradableCoins2 = df.set_index('id').ix[list(tradableCoins.index), c]
        tradableCoins2 = tradableCoins2.combine_first(tradableCoins)
        tradableCoins2 = tradableCoins2[tradableCoins2['portAmount_units'] > 0].sort_values(by='portAmount_units', ascending=False)
    
        with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
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
        c = 'symbol exchangeId 24h_volume_usd name available_supply total_supply at mv market_cap_usd percent_change_24h percent_change_7d price_usd portPcnt portPcntPinv portPcntPinv2 portAmount_usd portAmount_units Poloniex YoBit'.split(' ')
        #c = 'name price_usd portPcntPinv2 portAmount_usd portAmount_units Poloniex YoBit'.split(' ')
        with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
            sb = '24h_volume_usd portAmount_usd mv market_cap_usd'.split(' ')[3]
            dfv = df.fillna(0).ix[:, c].sort_values(by=sb, ascending=False)
            dfv = dfv[dfv['24h_volume_usd'] > 0]
            print dfv
        #print xresd
        #print p.DataFrame(xresd)
        self.df = df
        return df

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
        for i in lili[0:5]:
    
            url = '%s' % self.dfp.ix[self.dfp.index[i], 'href'] 
            print '%s %s' % (i, url)
            #"""
            xresd = self.xp.xpath2df(url, {
                'name'       : '//*[@id="page-wrapper"]/main/div[2]/div[3]/div[1]/h1/text()[2]',
                'symbol'     : '//*[@id="page-wrapper"]/main/div[2]/div[4]/div[1]/table[1]//tr[1]/td/text()',
                'trading'    : '//*[@id="page-wrapper"]/main/div[2]/div[4]/div[1]/table[1]//tr[2]/td/span/text()[2]',
                'links-website'    : '//*[@id="page-wrapper"]/main/div[2]/div[4]/div[2]/div[1]/table//tr[1]/td/a/@href',
                'links-blog'       : '//*[@id="page-wrapper"]/main/div[2]/div[4]/div[2]/div[1]/table//tr[2]/td/a/@href',
                'links-whitepaper' : '//*[@id="page-wrapper"]/main/div[2]/div[4]/div[2]/div[1]/table//tr[3]/td/a/@href',
                'links-facebook'   : '//*[@id="page-wrapper"]/main/div[2]/div[4]/div[2]/div[1]/table//tr[4]/td/a/@href',
                'links-twitter'    : '//*[@id="page-wrapper"]/main/div[2]/div[4]/div[2]/div[1]/table//tr[5]/td/a/@href',
                'links-linkedin'   : '//*[@id="page-wrapper"]/main/div[2]/div[4]/div[2]/div[1]/table//tr[6]/td/a/@href',
                'links-slack'      : '//*[@id="page-wrapper"]/main/div[2]/div[4]/div[2]/div[1]/table//tr[7]/td/a/@href',
                'links-telegram'   : '//*[@id="page-wrapper"]/main/div[2]/div[4]/div[2]/div[1]/table//tr[8]/td/a/@href',
                'links-github'     : '//*[@id="page-wrapper"]/main/div[2]/div[4]/div[2]/div[1]/table//tr[9]/td/a/@href',
                'domain-score'     : '//*[@id="page-wrapper"]/main/div[2]/div[4]/div[2]/table[2]//tr[1]/td/text()[1]',
                'backlinks'        : '//*[@id="page-wrapper"]/main/div[2]/div[4]/div[2]/table[2]//tr[2]/td/text()[1]',
                'github-starredby' : '//*[@id="page-wrapper"]/main/div[2]/div[4]/div[1]/div[3]/table//tr[1]/td/text()',
                'github-watchings' : '//*[@id="page-wrapper"]/main/div[2]/div[4]/div[1]/div[3]/table//tr[2]/td/text()',
                'github-contributors' : '//*[@id="page-wrapper"]/main/div[2]/div[4]/div[1]/div[3]/table//tr[2]/td/text()',
                'github-forks'        : '//*[@id="page-wrapper"]/main/div[2]/div[4]/div[1]/div[3]/table//tr[3]/td/text()',
                'github-commits'      : '//*[@id="page-wrapper"]/main/div[2]/div[4]/div[1]/div[3]/table//tr[4]/td/text()',
                'github-openIssues'   : '//*[@id="page-wrapper"]/main/div[2]/div[4]/div[1]/div[3]/table//tr[5]/td/text()',
            })
            #"""
            #print xresd
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
            li = 'name backlinks domain-score github-starredby github-commits github-contributors github-forks github-openIssues github-watchings'.split()    
            #backlinks domain-score
            #links-blog links-facebook links-github links-twitter links-website links-whitepaper name symbol trading    
            for j in li:
                try:    dftm[j] = map(lambda x: x.strip(), dftm[j])
                except: ''
            self.dfp = self.dfp.combine_first(dftm)
            with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
                #print dftm#.transpose()
                #print dftm.transpose()
                ''
            #break


    def underTheRadarTokens(self):
        # TokenMarket [UnderTheRadar Tokens]
        dfp = self.allAssetsICOsBlockchain
        #self.dfp.to_csv('tokenmarket.csv', encoding='utf8')
        fi = 'name symbol trading type backlinks domain-score links-blog links-facebook links-github links-twitter links-website links-whitepaper github-starredby github-commits github-contributors github-forks github-openIssues github-watchings'
        li = 'backlinks domain-score github-starredby github-commits github-contributors github-forks github-openIssues github-watchings'.split(' ')
        dfp = dfp.fillna(0)
        for i in li:
            try: dfp[i] = p.to_numeric(dfp[i])
            except Exception as e: 
                #print '%s %s' % (i,e)
                ''
        #print dfp.dtypes
        with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
            dfm = dfp.ix[:, fi.split()].sort_values(by='github-starredby').set_index('symbol')
            #print dfm
            ''
            df1 = self.allAssetsICOsBlockchain.set_index('name')
            df1['symbol'] = self.allAssetsICOsBlockchain.index
            dfm = dfm.set_index('name').combine_first(df1)
            #print ' '.join(list(dfm.columns))
            ff = '24h_volume_usd available_supply backlinks domain-score github-commits github-contributors github-forks github-openIssues github-starredby github-watchings id last_updated links-blog links-facebook links-github links-twitter links-website links-whitepaper market_cap_usd name percent_change_1h percent_change_24h percent_change_7d price_btc price_usd rank total_supply trading type'
            ff = 'symbol 24h_volume_usd available_supply backlinks domain-score github-commits github-contributors github-forks github-openIssues github-starredby github-watchings id last_updated market_cap_usd name percent_change_1h percent_change_24h percent_change_7d price_btc price_usd rank total_supply trading type'
            ff = 'X3 X X2 symbol backlinks domain-score github-commits github-contributors github-forks github-openIssues github-starredby github-watchings id  links-github type'
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
            dfm['X'] = dfm['github-commits'].get_values() / dfm['github-contributors'].get_values()
            dfm['X2'] = dfm['github-openIssues'].get_values() / dfm['github-forks'].get_values()
            dfm['X3'] = dfm['X2'].get_values() / dfm['X'].get_values()    
            #sortby='github-commits'
            sortby='X3'
            #print dfm.dtypes
            dfr = dfm
            for i in dfr[dfr['github-commits'] == 10].index: dfr = dfr.drop(i)
            dfr = dfr.ix[:,ff.split(' ')].fillna(0).sort_values(by=sortby, ascending=False)
            #print dfr
            ff = 'X3 weight' # to publish
            dfr = dfm.ix[:,ff.split(' ')].fillna(0).sort_values(by=sortby, ascending=False)
            for i in dfr[dfr['X3'] == n.inf].index: dfr = dfr.drop(i)
            dfr['potentialPortfolioWeight'] = dfr['X3'] / dfr['X3'].head(20).sum()
    
            import datetime, time
    
            # UnderTheRadar Suggestions
            print '== UnderTheRadar::tokens [%s]' % datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d')
            print '====================================='
            print
            print '== OpenSource Token Suggestions:'
            print '== FutureTokens  [Untradable::pre&postICO]'
            print
            print dfr.ix[:,['potentialPortfolioWeight']].head(20)
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
        except:
            ''

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

if __name__ == "__main__":

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




