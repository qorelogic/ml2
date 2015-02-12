#from numpy import *
import numpy as n
import pandas as p
import Quandl as q
import datetime as dd
import urllib2 as u
import html2text
import os, errno
import exceptions as ex
import re, sys

def debug(str, verbosity):
    if verbosity == 9:
        print str

def toCurrency(n):
    return '%2d' % n


"""
Created on Thu Nov 13 21:52:25 2014

@author: qore2
"""

import numpy as n
import pandas as p
from matplotlib.pylab import *

class PriceStudy:
    def __init__(self):
        self.tks = []
        
    def getPrices(self):
        self.tks = []
        self.tks.append('LBMA/GOLD') # Gold
        self.tks.append('DOE/RBRTE') # Europe Brent Crude Oil Spot Price FOB
        self.tks.append('CHRIS/CME_CL1') # Crude Oil Futures, Continuous Contract #1 (CL1) (Front Month)
        self.tks.append('BAVERAGE/USD') # USD/BITCOIN Weighted Price
        self.tks.append('BCHAIN/NTRAN')
        self.tks.append('BCHAIN/MKTCP')
        self.tks.append('BCHAIN/TOTBC')
        self.tks.append('BCHAIN/NTRAT')
        self.tks.append('BCHAIN/HRATE')
        self.tks.append('BCHAIN/ETRVU')
        self.tks.append('BCHAIN/NADDU')
        self.tks.append('BCHAIN/AVBLS')
        self.tks.append('BCHAIN/MIREV')
        d8 = getDataFromQuandl(self.tks, index_col=None, dataset='', verbosity=8)
        return d8
    
    def bitcoinStudy(self):
        d8 = self.getPrices()
        fig = plt.figure()
        #fig.add_subplot(111)
        
        d = normalizeme(d8.copy())
        d.plot(logy=False)
        
        d8.plot(logy=False)
        
        d8.plot(logy=True)
        
        d = normalizeme(d8.copy())
        d = sigmoidme(d)
        d.plot(logy=False)
        
        d = normalizeme(d8.copy())
        d = sigmoidme(d)
        d.plot(logy=False, style='.')
        
        d = normalizeme(d8.copy())
        d.plot(logy=True)
        
        show()


class FinancialModel:
    """The summary line for a class docstring should fit on one line.

    If the class has public attributes, they should be documented here
    in an ``Attributes`` section and follow the same formatting as a
    function's ``Args`` section.

    Attributes:
      attr1 (str): Description of `attr1`.
      attr2 (list of str): Description of `attr2`.
      attr3 (int): Description of `attr3`.

    """    
    def getRateFromProjectedAccruedment(from_capital, to_capital, period):
        """Example of docstring on the __init__ method.

        The __init__ method may be documented in either the class level
        docstring, or as a docstring on the __init__ method itself.

        Either form is acceptable, but the two should not be mixed. Choose one
        convention to document the __init__ method and be consistent with it.

        Note:
          Do not include the `self` parameter in the ``Args`` section.

        Args:
          param1 (str): Description of `param1`.
          param2 (list of str): Description of `param2`. Multiple
            lines are supported.
          param3 (int, optional): Description of `param3`, defaults to 0.

        """
        """
        vc = 100 * pow(1+50.0/100,2)
        vc = 1e9
        print vc
        period = 500
        print period
        """
        return 100 * (pow(float(to_capital)/from_capital, 1.0/period)-1)
    
    def compoundedPercentageIntegral(self, compoundedRate, period_integrals):
        return 100 * (pow(pow(1 + float(compoundedRate) / 100,1), 1 / float(period_integrals)) - 1)
        
    # wrapper for compoundedPercentageIntegral()
    def segmentCompundingPeriod(self, from_rate, intra_periods):
        return compoundedPercentageIntegral(from_rate, intra_periods)
    
    # 50, 1 => 50
    # 50, 2 => 125
    # 50, 3 => 237.5
    def rateToCompoundedPercentage(self, rate, period):
        return 100 * (pow(pow(1 + float(rate) / 100, period),float(1) / 1) - 1)
        
    def compoundVestedCapital(self, rate, period, initial_capital=100, shift=0):
        rate   = n.array(rate, dtype=float64)
        period = n.array(period)    
        
        if shift < 0:
            raise ex.IndexError('shift should be greater than 0. shift: '+str(shift))
        if shift > len(period):
            raise ex.IndexError('shift should be smaller than period length. shift: '+str(shift)+', period length: '+str(len(period)))
        
        # shift code
        try:        
            period = list(n.zeros(shift, dtype=int)) + list(period[0:len(period)-shift])
        except:
            ''
        
        return initial_capital * n.power(1 + rate.reshape(size(rate), 1) / 100, period)
        
    def mdrange(self, initial, space, end):
        return n.linspace(initial,end,(1.0/space)*end+1)
        
    def rateSpectra(self):
        rate   = self.mdrange(0, 0.1, 10)
        period = range(0, 200 + 1)
        plot(self.compoundVestedCapital(rate, period))
       
    def test(self):
        print self.compoundVestedCapital(50,2)
        print self.compoundVestedCapital(1,n.array([1,2,3]))
        print self.compoundVestedCapital(1,[1,2,3])
        print self.compoundVestedCapital(1,range(0,10))
        print self.compoundVestedCapital(range(0,10),range(0,10))
        #print self.rateCompoundedToPercentage(1,20)
        #print self.compoundedPercentageIntegral(rateCompoundedToPercentage(1,20), 20)
        #print self.compoundedPercentageIntegral(12, 20)

        r_day = fm.rateToCompoundedPercentage(1, 20)       
        vc = ic * pow(1+float(r_day)/100,20)
        print vc
        vc = fm.rateToCompoundedPercentage(r_day, 20)
        print vc
        r_month = 12
        vc = ic * pow(1+float(r_month)/100,1)
        print vc
        vc = fm.compoundVestedCapital(r_month, 1)[0][0]
        print vc

        n.linspace(0,1,100).T
        rate = range(0,23)
        period = range(0,100)
        rate   = n.array(rate, dtype=float64)
        period = n.array(period)    
        #res =  100 * n.power(1 + rate / 100, period.reshape(size(period), 1))
        res =  100 * n.power(1 + rate.reshape(size(rate), 1) / 100, period)
        print res


def prefilter(ds):
    """
    if type(ds) == type(p.DataFrame([])):
        dss = ds.get_values()
        index = ds.index
        columns = ds.columns
    else:
        dss = ds
    """
    if type(ds) == type(p.DataFrame([])):
        dss = ds.bfill().ffill().get_values()
        index = ds.index
        columns = ds.columns
    else:
        ds = p.DataFrame(ds).bfill().ffill().get_values()
        dss = ds
    #print type(dss)
    #print ds[0]
    # call fillna(method='bfill') on dataset before calling this method
    return dss

def normalizeme2(ds, index, columns):
    dss = prefilter(ds)
    dss = p.DataFrame(dss / dss[0], index=index, columns=columns)
    #print dss
    return dss

def normalizeme(ds, index, columns):
    dss = prefilter(ds)
    return p.DataFrame((dss - n.mean(dss))/n.std(dss), index=index, columns=columns)

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

def fetchFromQuandlSP500():
    sp = p.read_csv('data/quandl/SP500.csv')
    #for i in list(sp.sort(columns='Name').ix[0:10,['Code']].get_values().reshape(1,15)[0]):
    for i in range(0, len(sp)):
        getDataFromQuandl(sp.ix[i,'Code'], dataset='SP500')

def quandlCode2DatasetCode(tk, hdir='./', include_path=True, suffix='.csv'):
    try:
        mt = re.match(re.compile(r'(.*)\/(.*)_(.*)', re.S), tk).groups()
        path = hdir+'/'+mt[0]+'/'+mt[1]
        if include_path:
            fname = path+'/'+mt[0]+'-'+mt[1]+'_'+mt[2]+suffix
        else:
            fname = mt[0]+'-'+mt[1]+'_'+mt[2]+suffix            
        #fname = path+'/'+mt[2]+'.csv'
    except:
        mt = re.match(re.compile(r'(.*)\/(.*)', re.S), tk).groups()
        path = hdir+'/'+mt[0]+'/'+mt[1]
        if include_path:
            fname = path+'/'+mt[0]+'-'+mt[1]+suffix
        else:
            fname = mt[0]+'-'+mt[1]+suffix
    return [fname,path]
        
def getDataFromQuandl(tk, dataset, index_col=None, verbosity=1):
    # if string
    if type(tk) == type(''):
        debug('fetching '+tk, verbosity=verbosity)
        [fname, path] = quandlCode2DatasetCode(tk, hdir='data/quandl/'+dataset, include_path=True, suffix='.csv')
        mkdir_p(path) # alternative python3: os.makedirs(path, exist_ok=True)
        
        df = p.DataFrame([])
        
        try:
            df = p.read_csv(fname, index_col=index_col)
        except IOError, e:
            try:
                df = q.get(tk)
                df.to_csv(fname)
                print 'saved to: '+fname
            except q.DatasetNotFound, f:
                print f
        return df
    
    # if list
    if type(tk) == type([]):
        # concatenate ticker code to column value
        dfs = []
        mfs = p.DataFrame()
        for i in range(0, len(tk)):
            dfs.append(getDataFromQuandl(tk[i], index_col=0, dataset='', verbosity=8))
            #tk[i] = quandlCode2DatasetCode(tk[i], include_path=False, suffix='')[0]
            r1 = n.array([tk[i]+' '], dtype=object)
            r2 = n.array(list(dfs[i].columns), dtype=object)
            dfs[i].columns = r1+r2
            #print list(dfs[i].columns)    
        for i in range(0, len(dfs)):
            mfs = mfs.combine_first(dfs[i])
        return mfs
    
# source: https://www.quandl.com/c/markets/exchange-rates-versus-eur
# quandl js parser: for (var i = 2; i<=15; i++) {var buff = ''; $($x('//*[@id="ember894"]/div['+i+']/table/tbody/tr/td[3]/a/@href')).each(function(e,o) {buff += ' '+o.value.replace(/\/CURRFX\//g, '');}); console.log('# '+i); console.log('pa += \''+buff+'\'');}

# source: https://www.quandl.com/c/usa/usa-currency-exchange-rate
# quandl js parser: for (var i = 2; i<=15; i++) {var buff = ''; $($x('//*[@id="ember894"]/div['+i+']/table/tbody/tr/td[3]/a/@href')).each(function(e,o) {buff += ' '+o.value.replace(/\/CURRFX\//g, '');}); console.log('# '+i); console.log('pa += \''+buff+'\'');}

# getDataFromQuandlBNP(pa, curr)
def getDataFromQuandlBNP(pa, curr): # curr = EUR || USD, etc.
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

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

def testMicrofinance():
    fm = FinancialModel()
    #fm.test()
    
    years    = 4
    months   = 12 * years + 1
    days     = 250 * years + 1
    ic       = 100
    myrates  = []
    
    # 12% monthly
    myrates.append(12)
    # 1% daily, monthly equivalent
    myrates.append(fm.rateToCompoundedPercentage(1, 20))
    # 7% APR monthly equivalent
    myrates.append(fm.rateToCompoundedPercentage(fm.compoundedPercentageIntegral(7, 250), 20))
    
    myratetitles = []
    
    periods = n.array(range(0,months))
    df = p.DataFrame(periods)
    myratetitles.append('period')
    for i in xrange(0,len(myrates)):
        myratetitles.append('vested_'+str(int(myrates[i]))+'_monthly')
        df[myratetitles[i]] = fm.compoundVestedCapital(myrates[i], periods)[0]
    
    print df
    
    plot(df)
    print myratetitles
    legend(myratetitles, 2)
    
    fm = FinancialModel()
    r = fm.compoundVestedCapital(1, range(0,10), initial_capital=1, shift=3)
    #r = fm.compoundVestedCapital(1, range(0,10), initial_capital=1, shift=-4)
    #r = fm.compoundVestedCapital(1, range(0,10), initial_capital=1, shift=40)
    print p.DataFrame(r).transpose()
    """
    plot(vc)
    title('Vested Capital')
    show()
    """

def testGetDataFromQuandl():
    tks = []
    tks.append('LBMA/GOLD') # Gold
    tks.append('DOE/RBRTE') # Europe Brent Crude Oil Spot Price FOB
    tks.append('CHRIS/CME_CL1') # Crude Oil Futures, Continuous Contract #1 (CL1) (Front Month)
    tks.append('BAVERAGE/USD') # USD/BITCOIN Weighted Price
    #d = q.get(tks)
    d8 = getDataFromQuandl(tks, index_col=0, dataset='', verbosity=8)
    #d8.plot()
    #show()
    print d8.bfill().ffill()

if __name__ == "__main__":
    #print 'stub'
    #testMicrofinance()
    #testGetDataFromQuandl()
    #ps = PriceStudy()
    #ps.bitcoinStudy()
    #print ps.getPrices()
