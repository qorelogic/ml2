
import pandas as p
import numpy as n
from qoreliquid import pf

import requests as req
import ujson as js
import datetime
from oandaq import OandaQ

import numpy as n
import calendar, datetime, time

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

def getPoloniexHistorical(symbol='BTC_XMR', period=14400, start=1405699200, end=9999999999, bars=15):
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

import hashlib as hl
import hmac
import urllib
import httplib
import ujson as uj

class Exchange:

    def signHMAC512(self, params):
        #p1 = {'a':'1', 'b':'2'}
        #p1 = params
        #p1.update({'nonce':str(1)})
        #li = []
        #for i in zip(p1.keys(), p1.values()):
        #    li.append('='.join(i))
        #p1p = '&'.join(li)
        #ahash = hm.sha512(p1p)
        #return ahash.hexdigest()
        H = hmac.new(self.secret, digestmod=hl.sha512)
        #params = urllib.urlencode(params)
        H.update(params)
        return H.hexdigest()

    #def getResponse():
    
    def requestAuthenticated(self, method=None, url=None, params={}, requestType='POST'):
        if method:
            params.update({'method':method})
        params.update({'nonce':str(1)})
        params = urllib.urlencode(params)

        headers = {'Content-type': 'application/x-www-form-urlencoded',
                  'Key':           self.key,
                  'Sign':          self.signHMAC512(params)}
        """
        if method != None:
            url = method
        print 'url:%s' % url
        conn = httplib.HTTPSConnection(self.apiServer)
        conn.request(requestType, url, params, headers)
        response = conn.getresponse()
        """

        conn = httplib.HTTPSConnection(self.apiServer)
        if url:
            conn.request(requestType, url, params, headers)
        else:
            conn.request(requestType, self.apiMethod, params, headers)
        response = conn.getresponse()

        print response.msg
        print response.status
        print response.reason
        print response.read()

        #print dir(response)

        print 'params:'
        print params
        print
        print 'headers:'
        print headers

        try:
            data = uj.load(response)
            #print data
            return data
        except Exception as e:
            print response.msg
            print response.status
            print response.reason
            print response.read()
            #print dir(response)

            print 'params:'
            print params
            print
            print 'headers:'
            print headers

            print
            print e

class Liqui(Exchange):
    
    def __init__(self, key, secret):
        self.key    = key
        self.secret = secret
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
        self.key    = key
        self.secret = secret
        self.apiServer = 'bittrex.com' # https://bittrex.com/api/v1.1/account/getbalances?apikey=apikey
        self.apiMethod = '/api/v1.1'

    def getInfo(self):
        #import drest
        data = self.requestAuthenticated(url='/api/v1.1/account/getbalances', requestType='GET')
        df = p.DataFrame(data['return'])#.transpose()
        #pf(df)
        return df

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

    nu = 150
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
    """
    print makeTimeseriesTimestampRange(timestamp=1495209642, period=300, bars=nu)['range']

