
import urllib2 as u
import json as j
import os, errno, sys
import logging
import re
import pandas as p
import traceback

hdir = '/ml.live/bin/data/cache'

from numpy import array as n_array
from numpy import rint as n_rint
from numpy import tanh as n_tanh
from numpy import power as n_power
from numpy import e as n_e
from numpy import string0 as n_string0

def debug(str, verbosity=8):
    #if verbosity == 9:
    if verbosity == 8:
        #print str
        logging.debug(str)

        return str

class QoreDebug:
    
    def __init__(self, on=False, stackTrace=False):
        self._on        = on
        self.stackTrace = stackTrace
        self.limit      = 100
        self._logging = logging
        #self._logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s')
        self._logging.basicConfig(filename='/tmp/qore.dev.log', level=logging.DEBUG)
        
    def on(self):
        self.debugOn()
        
    def off(self):
        self.debugOff()
        
    def debugOn(self):
        self._on = True
        
    def debugOff(self):
        self._on = False
        
    def stackTraceOn(self):
        self.stackTrace = True
        
    def stackTraceOff(self):
        self.stackTrace = False
        
    # source: http://stackoverflow.com/questions/5067604/determine-function-name-from-within-that-function-without-using-traceback
    def _getMethod(self):
        
        if self._on == True:
            print
            print '=== QoreDebug::Method ======================================'
            print '{1} for {0}():'.format(sys._getframe(1).f_code.co_name, 'call stack')
            if self.stackTrace == True:
                for i in range(2,10):
                    try:    print ' - {0}()'.format(sys._getframe(i).f_code.co_name)
                    except: break
            print '------------------------------'

    def printTraceBack(self):
        if self._on == True:
            print '=== QoreDebug::TracebackStart==============================='
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print "=== traceback: ==="
            traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
            print "=== exception: ==="
            traceback.print_exception(exc_type, exc_value, exc_traceback, limit=self.limit, file=sys.stdout)
            print '=== QoreDebug::TracebackEnd ================================'

    def logTraceBack(self, e, limit=100):
        self._on = True
        if self._on == True:
            self.log('', exception=True)
            self.log('=== QoreDebug::TracebackStart===============================', exception=True)
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.log("=== exception: ===", exception=True)
            self.log(e, exception=True)
            self.log("=== traceback: ===", exception=True)
            
            #fp = open('/tmp/qore.dev.log', 'a')
            #traceback.print_tb(exc_traceback, limit=1, file=fp)
            tb = traceback.extract_tb(exc_traceback, limit=self.limit)
            #self.log(tb, exception=True)
            #self.log('{0}{1}'.format('\n', p.DataFrame(tb)), exception=True)
            for i in tb: self.log(i, exception=True)
            self.log("=== print_stack: ===", exception=True)
            #traceback.print_exception(exc_type, exc_value, exc_traceback, limit=2, file=fp)
            stack = traceback.extract_stack(limit=limit)
            #self.log(stack, exception=True)
            #self.log('{0}{1}'.format('\n', p.DataFrame(stack)), exception=True)
            for i in stack: self.log(i, exception=True)
            self.log('=== QoreDebug::TracebackEnd ================================', exception=True)
            self.log('', exception=True)
            #fp.close()

    def log(self, str, verbosity=8, exception=False):
        if exception:
            self._logging.basicConfig(filename='/tmp/qore.dev.log', level=logging.ERROR)
        else:
            self._logging.basicConfig(filename='/tmp/qore.dev.log', level=logging.DEBUG)
        #if verbosity == 9:
        if verbosity == 8:
            #print str
            self._logging.debug(str)
    
            #return str
    
    def data(self, data, name=None, verbosity=8):
        self._logging.basicConfig(filename='/tmp/qore.dev.data.log', level=logging.INFO)
        #if verbosity == 9:
        if verbosity == 8:
            #print data
            if type(name) != type(None):
                self._logging.debug(name)
            self._logging.debug(data)
            #print 'maccount::'
            #print p.DataFrame(maccount.columns)
            #print maccount#.to_dict()
    
            #return str

    def exception(self, e, verbosity=8):
        #if verbosity == 9:
        if verbosity == 8:
            #self._logging.debug(e)
            self.logTraceBack(e)
            #return e
    
    def type(self, v):
        self.log('{0} {1}'.format(v, type(v)))
    
# source: http://stackoverflow.com/questions/60208/replacements-for-switch-statement-in-python
class switch(object):
    value = None
    def __new__(class_, value):
        class_.value = value
        return True

def case(*args):
    return any((arg == switch.value for arg in args))


def cleanJsonContent(t):
    return re.sub(re.compile(r'[\s]+'), ' ', ''.join(t.split('\n')))

def fetchFromCache(url):
    # from cache file
    #mkdir_p(hdir)
    fp = open(hdir+'/'+u.quote(url,''), 'r')
    r = fp.read()
    fp.close()
    return r

def fetchURL(url, mode='json', cachemode='w', fromCache=False):
    import requests as req
    # mode = json | html
    try:
        if fromCache == True:
            debug('fetchURL(): '+url)
            ret = fetchFromCache(url)
        else:
            debug('fetchURL(fetchedFromCache): '+url)
            # method 1 urllib2
            #response = u.urlopen(url)
            #ret = response.read()
            
            # method 2 requests
            # source: http://docs.python-requests.org/en/master/
            r = req.get(url)
            ret = r.text
            
            # cache to file
            mkdir_p(hdir)
            fname = hdir+'/'+u.quote(url,'')
            debug('fetchURL(): caching to file: '+fname)
            fp = open(fname, cachemode)
            if mode == 'json':
                ret = cleanJsonContent(ret)
            fp.write(ret+'\n')
            fp.close()
        
        if mode == 'json':
            debug('fetchURL(): json format: '+url)
            ret = j.loads(ret)
        return ret
    except u.URLError, e:
        debug(e)        
    except NameError, e:
        debug(e)

# getWebContentToText
def lynxDump2(url):
    response = u.urlopen(url)
    html = response.read()
    html = html.decode('utf-8')
    return html2text.html2text(html)

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

def readcache(fname):
    return p.read_csv(fname, index_col=0)

def writecache(df, fname):
    mkdir_p(os.path.dirname(fname))
    df.to_csv(fname)
    
def cacheme(cmd, fname):
    try:
        df = readcache(fname)
    except:
        
        exec('df = '+cmd)
        writecache(df, fname)
    return df


#for i in range(len(allPositions2['noasnoas'])):
#    try:
#        allPositions2['noasnoas'][str(i)] = allPositions2['noasnoas'].pop(i)
#    except:
#        ''
#print allPositions2
#print j.dumps(allPositions2)

# source: http://gotoanswer.stanford.edu/?q=Recursive+depth+of+python+dictionary
#Be sure to assign the result of the recursive call to depth. Also, as @amit says, 
# consider using max so that you can handle dicts with multiple key value pairs (a treelike structure).
#>>> myDict = {'leve1_key1': {'level2_key1': 
#               {'level3_key1': {'level4_key_1': 
#                  {'level5_key1':   'level5_value1'}}}}}
#>>> dict_depth(myDict)
#5
def dict_depth(d, depth=0):
    if not isinstance(d, dict) or not d:
        return depth
    return max(dict_depth(v, depth+1) for k, v in d.iteritems())

#You should store the value retured from the recursive call, 
# and return the max value found, otherwise - you are calling the recursive 
# function without doing anything with the returned value! [and returning 0 as expected, since it was never changed]
def dict_depth(d, depth=0):
    ret = depth 
    for i in d.keys():
        if type(d[i]) is dict:
            newDict = d[i]
            ret = max(dict_depth(newDict, depth+1),ret) #finding max and storing it
    return ret #returning the max found

def convertDictKeysToString(dt, depth=2):
    if dict_depth(dt) == 1:
        for i in dt.keys(): 
            dt[i] = ({str(k): v for k, v in dt[i].iteritems()})
    if dict_depth(dt) == 2:
        for i in dt.keys():
            for j in dt[i].keys():
                dt[i][j] = ({str(k): v for k, v in dt[i][j].iteritems()})
    return dt

#alp = convertDictKeysToString(allPositions2)
#alp = j.dumps(alp)
#print alp

#positions = et.getEtoroTraderPositions('noasnoas', )


def prepTestDataFrame(df, verbose=0):
    """Prepares a pandas DataFrame for the test suite. Converts the 2D matrix to a 1D vector
returning a one-line python list that can be copy/pasted to the assertion line.

Parameters:
-----------
df : a pandas DataFrame
verbose : accepts int
          Set the verbosity level to 0 or 1. This prints the assertion string to stdout
           so that you can copy the assertion to a test file.
               
Examples:
---------
>>> df = p.DataFrame([['a','b','c'],['buy','sell','sell'],[1,2,3]], index=['pair', 'bias', 'amount']).transpose()
>>> prepTestDataFrame(df, verbose=1)
DataFrame=
  pair  bias amount
0    a   buy      1
1    b  sell      2
2    c  sell      3

Copy assertion line and example DataFrame to a test file:
assert prepTestDataFrame(df) == ['a', 'buy', 1, 'b', 'sell', 2, 'c', 'sell', 3]

Pasting the following lines 
to test_example.py:

df = p.DataFrame([['a','b','c'],['buy','sell','sell'],[1,2,3]], index=['pair', 'bias', 'amount']).transpose()
assert prepTestDataFrame(df) == ['a', 'buy', 1, 'b', 'sell', 2, 'c', 'sell', 3]
"""
    h = len(df.index)
    w = len(df.columns)
    forAssertion = list((df.get_values().reshape(1, h * w))[0])
    
    if verbose == 1:
        print
        print 'DataFrame='
        print df
        print
        print 'Copy assertion line and example DataFrame to your test file:'
        print "assert prepTestDataFrame(df) == {0}".format(forAssertion)
    
    return forAssertion


class XPath:
    ## xpath class ##
    def fixNewlines(self, item, field, kw='\n'):
        try:
            li = item[field]
            li = p.DataFrame(li)
            #srch = li[li[0] == kw]
            srch = li[p.Series(map(lambda x: True if x.strip() == kw.strip() else False, li[0]), index=li.index)]
            #print srch
            for i in list(srch.index):
                li = li.drop(i)
            li[0] = map(lambda x: x.strip(), li[0])
            li[0] = map(lambda x: x.replace(kw, ''), li[0])
            #print li
            item[field] = list(li[0])
        except Exception as e:
            #print e
            ''
        return item
    
    def fixItemsearchReplace(self, item, field, regex, replace):
        import re
        try:
            li = item[field]
            li = p.DataFrame(li)
            li[0] = map(lambda x: x.strip(), li[0])
            li[0] = map(lambda x: re.sub(re.compile(regex), replace, x), li[0])
            #print li
            item[field] = list(li[0])
        except Exception as e:
            #print e
            ''
        return item
    
    """
    xcols = {
        'host'   : '//div/div//table//tr//td[1]/text()',
        'port'   : '//div/div//table//tr//td[2]/text()',
        'anon'   : '//div/div//table//tr//td[4]/text()',
        'speed'  : '//div/div//table//tr//td[5]/text()',
        'check'  : '//div/div//table//tr//td[6]/text()',
    }
    """
    def xpath2df(self, url, xcols):
        import requests as req
        from lxml import html
        res = req.get(url)
        tree = html.fromstring(res.text)
        #print res.text
        xresd = {}
        for i in range(len(xcols.keys())):
            xk = xcols.keys()
            xv = xcols.values()
            xresd.update({xk[i]:tree.xpath(xv[i])})
        return xresd
    ## end xpath class ##

    def x2(self, url, xpath):
        import requests as req
        from lxml import html
        res = req.get(url)
        tree = html.fromstring(res.text)
        #print res.text
        xresd = {}
        xresd.update({'name':tree.xpath(xpath)})
        return xresd
    
class QoreScrapy:
    def makeItems(self, df, itemClass):
        items = []
        df = p.DataFrame.from_dict(df, orient='index').transpose().fillna('')
        for i in xrange(len(df)):
            ct = []
            for j in xrange(len(df.ix[i,:])):
                k = list(df.keys())[j]                
                v = df.ix[i,k].replace("\'","\\'")
                pair = "{0}='{1}'".format(k, v.encode('utf-8'))
                ct.append(pair)
            # import the item class
            exec('import {0}'.format(re.sub(re.compile(r'(.*?)\..*'), '\\1', itemClass)))
            # append to items
            try:
                exec('items.append({0})'.format("{0}({1})".format(itemClass, ", ".join(ct))))
            except:
                print itemClass
                print ct
        return items

import ujson as js
class DataPipeline:
    
    def __init__(self):
        self.z = ZZZ()
        self.z.initServer()
    
    #@profile
    def getEquity(self, i, fname, returnDataframe=False):
        #import pandas_finance as pf
        from pandas_finance import Equity
        aapl = Equity(i)
        #print p.DataFrame(aapl)
        #aapl
        #res = {}
        res = {'symbol': i, 'annual_dividend': '', 'dividend_yield': '', 'price': ''}
        try:    res.update({'annual_dividend': aapl.annual_dividend})
        except: ''
        try:    res.update({'dividend_yield' : aapl.dividend_yield})
        except: ''
        try:    res.update({'price'          : aapl.price})
        except: ''
        try:    res.update({'options'        : aapl.options})
        except: ''
        #    #aapl.hist_vol(30)
        #    #aapl.rolling_hist_vol(30)
        #except: ''
        jres = js.dumps(res)
        self.z.send(jres)
        #res = p.DataFrame(res, index=[i])
        #print res
        #df = df.combine_first(res)
        #df.to_csv(fname)
        #return df
    
    def receiveEquity(self, num):
        print 'receiveEquity()'
        self.z.initClient()
        import ujson as js
        df = p.DataFrame()
        i = 0
        while True:
            data = self.z.socketClient.recv(0)
            data = js.loads(data.replace('tester ', ''))
            #print data
            dfm = p.DataFrame(data, index=[data['symbol']])
            df = df.combine_first(dfm)
            if i == num-1:
                #print 'breaking out'
                print df.sort_values(by='dividend_yield', ascending=False)
                print
                break
            i += 1
        return df

    def populateTickers(self, live, num=10):
        import pandas as p
        #ti = 'AAPL T FB PG'.split(' ')
        df = p.DataFrame()
        tdf = p.read_csv('/ml.dev/lib/DataPipeline/tickers_numbeo.csv')
        tdf = tdf[tdf['exchange'] == 'NYSE'].sort_values(by='symbol')
        fname = 'tickers-fundamentals.csv'
            
        if live == 1:
            from multiprocessing.pool import ThreadPool
            pool = ThreadPool(processes=20)
            async_result = pool.apply_async(self.receiveEquity, [num])
            #import threading            
            #t = threading.Thread(target=self.receiveEquity, args=[num])
            #t.daemon = False
            #t.start()
            for i in list(tdf['symbol'])[0:num]:
            #    print i
            #for i in ti:
                #print i
                #print 't: %s' % i

                async_result = pool.apply_async(self.getEquity, [i, fname, False])
                #async_result = pool.map_async(t3, [i])
                #async_result = pool.imap_unordered(t3, [i])
                #return_val   = async_result.get()
                #print return_val[0]

                #t = threading.Thread(target=self.getEquity, args=[i, fname, False])
                #t.daemon = False
                #t.start()
                #print
                #df = getEquity(i, True)
            pool.close()
        #self.z.socket.close()

        if live == 0:
            df = p.read_csv(fname)

        return df

import zmq
class ZZZ:
    
    def __init__(self):
        self.ctx = zmq.Context()
        
    def initServer(self):
        # server
        self.socketServer = self.ctx.socket(zmq.PUB)
        url = 'tcp://*:3343'
        #try:
        self.socketServer.bind(url)
        #except Exception as e:
        #    print e
    
    def initClient(self):
        # client
        self.socketClient = self.ctx.socket(zmq.SUB)
        url = 'tcp://localhost:3343'
        self.socketClient.connect(url)
        self.socketClient.setsockopt(zmq.SUBSCRIBE, 'tester')

    def sendm(self):
        for i in range(10000):
            self.socketServer.send('%s %s' % ('tester', randint(1,10000000)))

    def send(self, txt):
        self.socketServer.send('%s %s' % ('tester', txt))

    def receive(self):
        while True:
            print self.socketClient.recv(0)

    def t3(self, tn):
        import time as tt
        self.send(tn)
        #tt.sleep(n.random.randint(5))
        #print 'p: %s' % tn
        tt.sleep(tn)
        return 'r: %s' % tn



def babysitTrades2(qq, acc):
    #acc = qq.oq.oanda2.get_account(qq.oq.aid)
    bal = acc['balance']

    relatedPairs = qq.oq.getPairsRelatedToOandaTickers('EUR_USD')
    pairs = list(n_array(p.DataFrame(relatedPairs['lsp']).ix[:,0], dtype=n_string0))
    prices = p.DataFrame(qq.oq.oanda2.get_prices(instruments=','.join(pairs))['prices'])
    cupris = prices.set_index('instrument').ix['EUR_USD',['ask','bid']].transpose().describe()['top']#.ix['EUR_USD',:]

    trades = p.DataFrame(qq.oq.oanda2.get_trades(qq.oq.aid)['trades'])
    trades['cprice'] = cupris
    pl = (trades['price'] - cupris) * trades['units'] * cupris
    trades['pl'] = pl
    trades['pips'] = (trades['price'] - cupris) * 10000
    trades['pcnt'] = pl / bal * 100

    print list((trades['instrument'] == 'EUR_USD').index)
    for i in xrange(len(trades)):
        trade = trades.ix[i,:]
        pl = trade['pl']
        #print trade
        if pl > 0:
            print pl
            print 'setting trailstop'
            tid = trade['id']
            #qq.oq.oanda2.modify_trade(qq.oq.aid, tid, trailingStop=10)
        else:
            print 'trailstop too small, patience!'
            
        #break
    print trades.transpose()
