#from numpy import *
import numpy as n
import pandas as p
import Quandl as q
import datetime as dd
import urllib2 as u
import html2text

def toCurrency(n):
    return '%2d' % n

def normalizeme(dfr):
    return ((dfr - n.mean(dfr))/n.std(dfr))

def sigmoidme(dfr):
    return 1.0 / (1 + pow(n.e,-dfr))

def sharpe(dfr):
    ''

"""
def toCurrency(n):
    return '%2d' % n

def normalizeme(dfr):
    return ((dfr - mean(dfr))/std(dfr))

def sigmoidme(dfr):
    return 1.0 / (1 + pow(e,-dfr))

def sharpe(dfr):
    ''
"""

# source: https://www.quandl.com/c/markets/exchange-rates-versus-eur
# quandl js parser: for (var i = 2; i<=15; i++) {var buff = ''; $($x('//*[@id="ember894"]/div['+i+']/table/tbody/tr/td[3]/a/@href')).each(function(e,o) {buff += ' '+o.value.replace(/\/CURRFX\//g, '');}); console.log('# '+i); console.log('pa += \''+buff+'\'');}

# source: https://www.quandl.com/c/usa/usa-currency-exchange-rate
# quandl js parser: for (var i = 2; i<=15; i++) {var buff = ''; $($x('//*[@id="ember894"]/div['+i+']/table/tbody/tr/td[3]/a/@href')).each(function(e,o) {buff += ' '+o.value.replace(/\/CURRFX\//g, '');}); console.log('# '+i); console.log('pa += \''+buff+'\'');}

# getDataFromQuandl(pa, curr)
def getDataFromQuandl(pa, curr): # curr = EUR || USD, etc.
    pa = pa.split(' ')
    
    tk = []
    tl = []
    for i in pa:
        tk.append('BNP/'+i)
        tl.append('BNP.'+i+' - '+i[0:3]+'/'+i[3:6])
    #print tk
    #print tl
    
    authtoken="WVsyCxwHeYZZyhf5RHs2"
    fname = 'data/quandl/BNP.'+curr+'.csv'
    print fname
    try:
        da = p.read_csv(fname, index_col=0)
        
        # if column mismatch then update from source instead of caching
        if len(tk) != len(da.columns):
            raise IOError
        
        print 'updating..'
        import datetime as dd
        #trim_start = str(list(da.tail(1).ix[:,0])[0])
        trim_start = da.index[len(da)-1]
        trim_end = str(dd.datetime.today().year).zfill(4) + '-' + str(dd.datetime.today().month).zfill(2) + '-' + str(dd.datetime.today().day).zfill(2)
        #print trim_start
        #print trim_end
        ts = trim_start.split('-')
        te = trim_end.split('-')
        #print ts
        #print te
        a = dd.date(int(te[0]), int(te[1]), int(te[2]))
        b = dd.date(int(ts[0]), int(ts[1]), int(ts[2]))
        days = (a-b).days
        print days
        if days > 0:
            print 'greater than 0 days'
            #d = q.get(tk[0:2], authtoken=authtoken, trim_start=trim_start, trim_end=trim_end)
            #d = q.get(tk[0:2], authtoken=authtoken, transformation="diff")
            #d = q.get(tk[0:2], authtoken=authtoken, collapse="annual")
            d = q.get(tk, authtoken=authtoken, rows=days, sort_order='desc').sort(ascending=True)
            
            # combine the cache and new data into one dataset
            d = da.combine_first(d)
            d.to_csv('data/quandl/BNP.'+curr+'.csv')
        else:
            print 'equal 0 days'
            d = da
    except IOError, e:
        print 'getting from quandl..'
        d = q.get(tk, authtoken=authtoken)
        #d = q.get(tk, returns="numpy")
        #d = q.get(["NSE/OIL.4","WIKI/AAPL.1"])
        #d = q.get("NSE/OIL", trim_start="yyyy-mm-dd", trim_end="yyyy-mm-dd")
        #print d
        d.to_csv('data/quandl/BNP.'+curr+'.csv')
        print e
        
    #plot(d.ix[:,tl])
    
    return d

# getWebContentToText
def lynxDump2(url):
    response = u.urlopen(url)
    html = response.read()
    html = html.decode('utf-8')
    return html2text.html2text(html)

