
#from numpy import *
from qore import *
from qore_qstk import *
from matplotlib.pylab import *

import numpy as n
import pandas as p
import Quandl as q
import datetime as dd
import urllib2 as u
import json as j
import html2text
import exceptions as ex
import re, sys
import StringIO as sio
import threading,time
import itertools as it

def toCurrency(n):
    return '%2d' % n

"""
Created on Thu Nov 13 21:52:25 2014

@author: qore2
"""

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

def normalizeme(dfr):
    return (dfr - n.mean(dfr))/n.std(dfr)

def normalizeme2(ds, index=None, columns=None):
    #print type(ds)
    ds = n.array(ds, dtype=float)
    if type(ds) == type(p.DataFrame([])):
    #    print '0'
        dss = ds.get_values()
        index = ds.index
        columns = ds.columns
    if type(ds) == type(n.array([])):
    #    print 't1'
        dss = ds
    if type(ds) == type([]):
    #    print 't2'
        dss = n.array(ds)
    #print type(dss)
    #import sys
    #sys.exit()
    #print ds[0]
    # call fillna(method='bfill') on dataset before calling this method
    
    dss = dss / dss[0]
    dss = p.DataFrame(dss, index=index, columns=columns)
    return dss

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

#quickPlot('GOOG/AMEX_OFI')
#quickPlot('BAVERAGE/USD')
def quickPlot(tks, headers=None, listcolumns=False, title=None):
    d = getDataFromQuandl(tks, index_col=0, dataset='', verbosity=3)
    if listcolumns:
        #print p.DataFrame(list(d.columns))
        for i in enumerate(list(d.columns)):
            print i
    d = d.bfill().ffill()
    d = normalizeme(d)
    d = sigmoidme(d)
    
    if type(headers) == type([]):
        d = d.ix[:, headers] #.transpose()
    
    d.plot(logy=False)
    if type(headers) == type([]):
        #hdrs = d.columns[headers]
        #hdrs = list(d.columns[headers])
        try:        
            hdrs = list(d.columns[[headers]])
            legend(hdrs, 2)
        except:
            ''
    #else:
    #    legend(None, 2)
    #print type(title)
    #if title:
    #    title(title)
    show()
    return d

def writeQuandlSearchLog(stri):
    suffix='.csv'
    path='data/quandl'
    fname = path+'/searches'+suffix    
    fp = open(fname,'a')
    fp.write(stri+"\n")
    fp.close()    
    #fp = open(fname)
    #print fp.read()
    #fp.close()
    
def searchQuandl(query, mode='manifest', headers=None, returndataset=False, cache=True, listcolumns=False):
    debug('searching: '+query, verbosity=9)
    suffix='.csv'
    path='data/quandl/searches/'
    fquery = re.sub(re.compile(r'\/'),'-',query)
    fname = path+fquery+suffix
    mkdir_p(path)
    import time as t
    tt = t.time()
    try:
        if cache == False:
            raise IOError
        fp = open(fname, 'r')
        res = j.loads(fp.read())
        fp.close()
        writeQuandlSearchLog(str(tt)+':cached:'+str(query)+' to '+fname)
    except IOError, e:
        try:
            writeQuandlSearchLog(str(tt)+':searched:'+str(query)+' to '+fname)
            res = q.search(query, verbose=False)
            fp = open(fname, 'w')
            fp.write(j.dumps(res))
            fp.close()
            print 'saved to: '+fname
        except q.DatasetNotFound, f:
            print f
    tks = []
    ds = None
    for i in res:
        #print i.keys()
        #print i
        tk = i['code']
        
        if mode == 'manifest':
            print tk
            print i['name']
            print i['desc']
            print '---------'
            print
            """
            try:
                dsg = getDataFromQuandl(tk, dataset='')
            except e:
                print e
            """
            #print i['freq']
            #print i['name']
            #print i['desc']
            #print
        if mode == 'plot':
            print tk
            #print i['desc']
            ds = quickPlot(str(tk.strip()), listcolumns=listcolumns, title=query)
        if mode == 'combineplot':
            tks.append(str(tk))
    if mode == 'combineplot':
        ds = quickPlot(tks, headers=headers, listcolumns=listcolumns, title=query)
    if returndataset == True:
        return ds
    else:
        return len(res)

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
        
def getDataFromQuandl(tk, dataset='', index_col=None, verbosity=1, plot=False):
    # if string
    df = p.DataFrame([])
    
    if type(tk) == type(''):
        debug('fetching '+tk, verbosity=verbosity)
        [fname, path] = quandlCode2DatasetCode(tk, hdir='data/quandl/'+dataset, include_path=True, suffix='.csv')
        mkdir_p(path) # alternative python3: os.makedirs(path, exist_ok=True)
        
        try:
            df = p.read_csv(fname, index_col=index_col)
        except IOError, e:
            try:
                df = q.get(tk)
                df.to_csv(fname)
                print 'saved to: '+fname
            except q.DatasetNotFound, f:
                print f
        if index_col == None:
            df = df.set_index(df.columns[0])
    
    # if list
    if type(tk) == type([]):
        # concatenate ticker code to column value
        dfs = []
        for i in range(0, len(tk)):
            dfs.append(getDataFromQuandl(tk[i], index_col=0, dataset='', verbosity=8))
            #tk[i] = quandlCode2DatasetCode(tk[i], include_path=False, suffix='')[0]
            r1 = n.array([tk[i]+' '], dtype=object)
            r2 = n.array(list(dfs[i].columns), dtype=object)
            dfs[i].columns = r1+r2
            #print list(dfs[i].columns)    
        for i in range(0, len(dfs)):
            df = df.combine_first(dfs[i])
    
    if plot == True:
        df.plot(); show();
    return df
    
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


def getDatasetEUR():
    pa = ''
    # 2
    pa += 'EURUSD EURJPY EURGBP EURCHF EURCAD EURAUD EURNZD EURSEK EURNOK EURBRL EURCNY EURRUB EURINR EURTRY EURTHB EURIDR EURMYR EURMXN EURARS EURDKK EURILS EURPHP'
    # 3
    pa += ' EURDKK EURHUF EURISK EURNOK EURSEK EURCHF EURTRY EURGBP'
    # 4
    pa += ' EURALL EURBAM EURBGN EURHRK EURCZK EURMKD EURPLN EURRON EURRSD'
    # 5
    pa += ' EURAMD EURAZN EURBYR EURGEL EURKZT EURKGS EURLVL EURLTL EURMDL EURRUB EURTJS EURTMT EURUAH EURUZS'
    # 6
    pa += ' EURBND EURKHR EURCNY EURHKD EURIDR EURJPY EURLAK EURMYR EURMNT EURMMK EURKPW EURPHP EURSGD EURKRW EURTHB EURVND'
    # 7
    pa += ' EURAFN EURBDT EURBTN EURINR EURLKR EURMVR EURNPR EURPKR'
    # 8
    pa += ' EURDZD EURBHD EURDJF EUREGP EURIRR EURIQD EURILS EURJOD EURKWD EURLBP EURLYD EURMAD EUROMR EURQAR EURSAR EURSYP EURTND EURAED EURYER'
    # 9
    pa += ' EURAOA EURBIF EURXOF EURBWP'
    # 10
    pa += ' EURXAF EURCDF EURKMF EURCVE EURETB EURGHS EURGNF EURGMD EURKES EURLRD EURLSL EURMGA EURMZN EURMRO EURMUR EURMWK EURNAD EURNGN EURRWF EURSDG EURSLL EURSOS EURSTD EURSZL EURSCR EURTZS EURUGX EURZAR EURZMW'
    # 11
    pa += ' EURUSD EURCAD EURMXN'
    # 12
    pa += ' EURXCD EURBSD EURBBD EURCUP EURDOP EURHTG EURJMD EURTTD'
    # 13
    pa += ' EURBZD EURCRC EURGTQ EURHNL EURNIO EURPAB'
    # 14
    pa += ' EURARS EURBOB EURBRL EURCLP EURCOP EURGYD EURPYG EURPEN EURSRD EURUYU EURVEF'
    # 15
    pa += ' EURAUD EURFJD EURNZD EURPGK EURWST EURSBD EURTOP EURVUV'
    
    de = getDataFromQuandlBNP(pa, 'EUR')
    return de

def getDataUSD():
    pa = ''
    # 2
    pa += ' USDEUR USDJPY USDGBP USDCHF USDCAD USDAUD USDNZD USDSEK USDNOK USDBRL USDCNY USDRUB USDINR USDTRY USDTHB USDIDR USDMYR USDMXN USDARS USDDKK USDILS USDPHP'
    # 3
    pa += ' USDEUR USDDKK USDHUF USDISK USDNOK USDSEK USDCHF USDTRY USDGBP'
    # 4
    pa += ' USDALL USDBAM USDBGN USDHRK USDCZK USDMKD USDPLN USDRON USDRSD'
    # 5
    pa += ' USDAMD USDAZN USDBYR USDGEL USDKZT USDKGS USDLVL USDLTL USDMDL USDRUB USDTJS USDTMT USDUAH USDUZS'
    # 6
    pa += ' USDBND USDKHR USDCNY USDHKD USDIDR USDJPY USDLAK USDMYR USDMNT USDMMK USDKPW USDPHP USDSGD USDKRW USDTHB USDVND'
    # 7
    pa += ' USDAFN USDBDT USDBTN USDINR USDLKR USDMVR USDNPR USDPKR'
    # 8
    pa += ' USDDZD USDBHD USDDJF USDEGP USDIRR USDIQD USDILS USDJOD USDKWD USDLBP USDLYD USDMAD USDOMR USDQAR USDSAR USDSYP USDTND USDAED USDYER'
    # 9
    pa += ' USDAOA USDBIF USDXOF USDBWP'
    # 10
    pa += ' USDXAF USDCDF USDKMF USDCVE USDETB USDGHS USDGNF USDGMD USDKES USDLRD USDLSL USDMGA USDMZN USDMRO USDMUR USDMWK USDNAD USDNGN USDRWF USDSDG USDSLL USDSOS USDSTD USDSZL USDSCR USDTZS USDUGX USDZAR USDZMW'
    # 11
    pa += ' USDCAD USDMXN'
    # 12
    pa += ' USDXCD USDBSD USDBBD USDCUP USDDOP USDHTG USDJMD USDTTD'
    # 13
    pa += ' USDBZD USDCRC USDGTQ USDHNL USDNIO USDPAB'
    # 14
    pa += ' USDARS USDBOB USDBRL USDCLP USDCOP USDGYD USDPYG USDPEN USDSRD USDUYU USDVEF'
    # 15
    pa += ' USDAUD USDFJD USDNZD USDPGK USDWST USDSBD USDTOP USDVUV'
    
    du = getDataFromQuandlBNP(pa, 'USD')
    return du

def getDataAUD():
    pa = ''
    # 2
    pa += ' AUDEUR AUDJPY AUDGBP AUDCHF AUDCAD AUDUSD AUDNZD AUDSEK AUDNOK AUDBRL AUDCNY AUDRUB AUDINR AUDTRY AUDTHB AUDIDR AUDMYR AUDMXN AUDARS AUDDKK AUDILS AUDPHP'
    # 3
    pa += ' AUDEUR AUDDKK AUDHUF AUDISK AUDNOK AUDSEK AUDCHF AUDTRY AUDGBP'
    # 4
    pa += ' AUDALL AUDBAM AUDBGN AUDHRK AUDCZK AUDMKD AUDPLN AUDRON AUDRSD'
    # 5
    pa += ' AUDAMD AUDAZN AUDBYR AUDGEL AUDKZT AUDKGS AUDLVL AUDLTL AUDMDL AUDRUB AUDTJS AUDTMT AUDUAH AUDUZS'
    # 6
    pa += ' AUDBND AUDKHR AUDCNY AUDHKD AUDIDR AUDJPY AUDLAK AUDMYR AUDMNT AUDMMK AUDKPW AUDPHP AUDSGD AUDKRW AUDTHB AUDVND'
    # 7
    pa += ' AUDAFN AUDBDT AUDBTN AUDINR AUDLKR AUDMVR AUDNPR AUDPKR'
    # 8
    pa += ' AUDDZD AUDBHD AUDDJF AUDEGP AUDIRR AUDIQD AUDILS AUDJOD AUDKWD AUDLBP AUDLYD AUDMAD AUDOMR AUDQAR AUDSAR AUDSYP AUDTND AUDAED AUDYER'
    # 9
    pa += ' AUDAOA AUDBIF AUDXOF AUDBWP'
    # 10
    pa += ' AUDXAF AUDCDF AUDKMF AUDCVE AUDETB AUDGHS AUDGNF AUDGMD AUDKES AUDLRD AUDLSL AUDMGA AUDMZN AUDMRO AUDMUR AUDMWK AUDNAD AUDNGN AUDRWF AUDSDG AUDSLL AUDSOS AUDSTD AUDSZL AUDSCR AUDTZS AUDUGX AUDZAR AUDZMW'
    # 11
    pa += ' AUDUSD AUDCAD AUDMXN'
    # 12
    pa += ' AUDXCD AUDBSD AUDBBD AUDCUP AUDDOP AUDHTG AUDJMD AUDTTD'
    # 13
    pa += ' AUDBZD AUDCRC AUDGTQ AUDHNL AUDNIO AUDPAB'
    # 14
    pa += ' AUDARS AUDBOB AUDBRL AUDCLP AUDCOP AUDGYD AUDPYG AUDPEN AUDSRD AUDUYU AUDVEF'
    # 15
    pa += ' AUDFJD AUDNZD AUDPGK AUDWST AUDSBD AUDTOP AUDVUV'
    # 16
    #pa += ' /BITCOIN/MTGOXAUD /WGC/GOLD_DAILY_AUD'
    
    da = getDataFromQuandlBNP(pa, 'AUD')

class CryptoCoinBaseClass:
    
    def __init__(self):
        ''
        
class CoinMarketCap:
    
    def __init__(self):
        ''

    def updateData(self):
        # source: http://coinmarketcap-nexuist.rhcloud.com/
        t = fetchURL('http://coinmarketcap-nexuist.rhcloud.com/api/all', cachemode='a', fromCache=False, mode='json')

class btce(CryptoCoinBaseClass):
    def getTicker(self, code):
        # eg. code = btc_usd
        url = 'https://btc-e.com/api/3/ticker/'+code
        r = fetchURL(url, mode='json')
        #print r
        ky = r[code].keys()
        #print ky
        #print r[code].values()
        r = p.DataFrame(r[code].values(), index=ky, columns=[code]).transpose()
        return r.ix[:,['sell','buy','last','vol','vol_cur']].transpose()
    
    def getRarestCryptoCoins(self):
        # linked from: http://crypt.la/2013/12/14/list-of-the-fastest-cryptocurrencies/
        # source: http://crypt.la/2013/12/16/list-of-the-top-25-rarest-cryptocurrencies/
        t = """Currency	Code	Total Circulation 
Onecoin	ONC	1
Bestcoin	BEST	1,000,000
Cryptogenic Bullion	CGB	1,000,000
GoldPressedLatinum	GPL	1,000,000
Peoplecoin	PPL	1,440,000
CryptoBuck	BUK	10,000,000
Mincoin	MNC	10,000,000
Ecocoin	ECO	10,200,000
CrimeCoin	CRM	100,000
ProtoShares	PTS	2,000,000
Sauron Rings	SAU	20,000
BitGem	BTG	23,000
Unobtanium	UNO	250,000
Jupitercoin	JPC	3,700,000
Cryptobits	CYB	4,000,000
Anoncoin	ANC	4,200,000
Diamond	DMD	4,300,000
ExtremeCoin	EXC	5,000,000
Basecoin	BAC	6,000,000
Frozen	FZ	7,700,000
Doubloons	DBL	8,000,000
Bitbar	BTB	8,500
PhilosopherStone	PHS	8,891,840
Lovercoin	LVC	9,000,000
"""
        print t
    
    def getFastestCryptoCoins(self):
        # linked from: http://bitcoin.stackexchange.com/questions/24636/fastest-cryptocurrency
        # source: http://crypt.la/2013/12/14/list-of-the-fastest-cryptocurrencies/
        t = """Coin	Symbol	Confirmations Required	Transaction Speed (in seconds)
Fastcoin	FST	4	48
Worldcoin	WDC	4	60
Krugercoin	KGC	6	90
Richcoin	RCH	3	90
Realcoin	REC	3	90
Digitalcoin	DGC	5	100
Emerald	EMD	5	100
Xencoin	XNC	5	100
Asiccoin	ASC	4	120
Infinitecoin	IFC	4	120
Alphacoin	ALP	5	150
Elephantcoin	ELP	5	150
Quarkcoin	QRK	5	150
Valuecoin	VLC	5	150
Argentum	ARG	5	160
Hypercoin	HYC	4	160
Colossuscoin	COL	7	175
Casinocoin	CSC	6	180
Franko	FRK	6	180
Orbitcoin	ORB	6	180
Florincoin	FLO	5	200
Stablecoin	SBC	5	200
Galaxycoin	GLX	7	210
Zetacoin	ZET	7	210
Anoncoin	ANC	6	240
Novacoin	NVC	4	240
Yacoin	YAC	4	240
Globalcoin	GLC	7	280
Bbqcoin	BQC	5	300
Elacoin	ELC	5	300
Ezcoin	EZC	5	300
Grandcoin	GDC	7	315
Spots	SPT	5	350
Diamond	DMD	6	360
Datacoin	DTC	6	360
Lebowskis	LBW	6	360
Redcoin	RED	6	360
Primecoin	XPM	6	360
Netcoin	NET	7	420
Nanotoken	NAN	5	450
Powercoin	PWC	10	450
Cryptogenicbullion	CGB	8	480
Terracoin	TRC	4	480
Americancoin	AMC	4	600
Litecoin	LTC	4	600
Nibble	NIB	4	600
Feathercoin	FTC	5	750
Megacoin	MEC	5	750
Nucoin	NUC	5	750
Phenixcoin	PXC	5	750
Deutsche eMark	DEM	7	840
Noirbits	NRB	7	840
Cosmoscoin	CMC	5	1050
Betacoin	BET	5	1200
Tagcoin	TAG	5	1200
Weedcoin	WEC	5	1200
Unobtanium	UNO	7	1260
Cinnamoncoin	CIN	5	1500
Craftcoin	CRC	5	1500
Protoshares	PTS	6	1800
Bitbar	BTB	4	2400
Bitcoin	BTC	4	2400
Bitgem	BTG	4	2400
Peercoin	PPC	6	3600
"""
        tis = p.read_csv(sio.StringIO(t), delimiter='\t', index_col=0).ix[:,[0,1,2]]
        tis = tis.sort('Transaction Speed (in seconds)', ascending=True)
        #print tis.ix[0:3,[0,2]]
        #print tis
        tis = list(tis.ix[:,[0]].transpose().get_values()[0])
        """
        for i in list(n.array(self.pk, dtype=string0)):
            print i.split('_')
            for j in range(0,len(fastestCoins)):
                #print type(fastestCoins[j])
                try:
                    fc = fastestCoins[j].lower()
                    #print 'fastest:'+fc
                    #if i[0:3] == fc:
                    #    print i[0:3]
                    #if i[4:7] == fc:
                    #    print i[4:7]
                except:
                    ''
        """
        return tis
    
    def __init__(self):
        self.pk = []
        self.exchanges = ['ex1','ex2','ex3','ex4']; #print exchanges;
        self.check()

    def check(self):
        if len(self.pk) == 0: self.getCurrencies()
    
    def getCurrencies(self):
        url = 'https://btc-e.com/api/3/info'
        r = fetchURL(url, mode='json')

        try:
            #print p.DataFrame(list(r['pairs']['ltc_gbp']))
            pk = r['pairs'].keys()
            pv = r['pairs'].values()
            #print pk
            li = []
            for i in pv:
                li.append(i.values())
            li = p.DataFrame(li, index=pk, columns=pv[0].keys())
            self.pk = pk
            return li
            #pk = p.DataFrame(pk, index=pk, columns=['pair'])
            #print pk
            #print pk.combine_first(li)
            #print r
        except TypeError, e:
            debug(e)
    
    def getRatesOnExchange(self):
        self.check()
        pc = p.DataFrame()
        for i in self.pk:
            debug(i)
            try:
                ti = self.getTicker(i); #print ti.transpose()
                pc = pc.combine_first(ti)
            except:
                ''
        #print pc
        return pc.transpose()
    
    def getDepth(self, code, doPlot=True):
        debug('Starting getTDepth: '+code)
        # eg. code = btc_usd
        url = 'https://btc-e.com/api/3/depth/'+code
        r = fetchURL(url, mode='json')
        #print r
        try:        
            ky = r[code].keys()    
            #print ky
            rb = p.DataFrame(r[code]['bids'], columns=['bp','ba'])
            ra = p.DataFrame(r[code]['asks'], columns=['ap','aa'])
            #print rb
            #print ra
            r = rb.combine_first(ra)
            #r = r.ix[:,[]]
            if doPlot == True:
                r1 = r
                r1 = r1.ix[:,['ap','bp']]
                plot(r1); title(code+' orders'); legend(r1.columns,2); show()
        
                r2 = r
                r2 = normalizeme(r2)
                r2 = sigmoidme(r2)
                r2 = r2.ix[:,:]
                plot(r2); title(code+' orders'); legend(r2.columns,2); show()
            debug('Ending getDepth:'+code)
            return r
        except TypeError, e:
            debug(e)

    def parseTrades(self, r, code, doPlot=True):
        #print r
        try:
            ky = r[code][0].keys()
            #print ky
            li = []
            for i in r[code]:
                li.append(i.values())
            ro = p.DataFrame(li, columns=ky)
            r = ro.ix[:,['price','amount']]
            #print r
            """
            rb = p.DataFrame(r[code]['bids'], columns=['bp','ba'])
            ra = p.DataFrame(r[code]['asks'], columns=['ap','aa'])
            print rb
            print ra
            r = rb.combine_first(ra)
            print r
            #r = r.ix[:,[]]
            """
            r1 = r
        #    r1 = normalizeme(r1)
        #    r1 = sigmoidme(r1)
            if doPlot == True:
                r1 = r1.ix[:,['price']]
                plot(r1); title(code+' trades'); legend(r1.columns,2); show()
            debug('Ending getTrades:'+code)
            return ro
        except TypeError, e:
            debug(e)
    
    def getTrades(self, code, doPlot=True):
        debug('Starting getTrades: '+code)
        # eg. code = btc_usd
        url = 'https://btc-e.com/api/3/trades/'+code
        r = fetchURL(url, mode='json', cachemode='a')
        #r = fetchFromCache(url)
        ro = self.parseTrades(r, code, doPlot)
        return ro

    def getArbTable(self, pk):
        self.check()
        arbtable1 = n.random.randn(len(pk)*len(self.exchanges)).reshape(len(pk),len(self.exchanges));
        return arbtable1

    def getArbRates(self, doPlot=False):
        #print pk
        arbtable1 = self.getArbTable(self.pk)
        rarb = p.DataFrame(arbtable1, index=self.pk, columns=self.exchanges);
        #print rarb; print;
        
        ms = []
        arbHdr = ['sell','buy','arbitrageRate']
        arbRates = p.DataFrame([])
        for i in range(0,len(self.pk)):
        #for i in range(0,2):
            ind = i
            debug(self.pk[ind])
            m = rarb.ix[self.pk[ind]]
            debug(m)
            m = p.DataFrame(n.array(m).reshape(len(m),1) / n.array(m) * 100 - 100, index=self.exchanges, columns=self.exchanges); 
            debug(m); debug('');
            m1 = n.max(m,0); #print m1;
            exhds = list(m1.index)
            #print (n.nonzero(m == m1))
            #print (n.nonzero(m1 == n.max(m1)))
            maxIndx = n.max(n.nonzero(m1 == n.max(m1)))
            maxNum = n.max(m1,0); #print maxNum;
            indx = (n.nonzero(n.array(m == maxNum, dtype=int)))
            arbRate = p.DataFrame([exhds[indx[0][0]], exhds[indx[1][0]], maxNum], index=arbHdr, columns=[self.pk[ind]])
            arbRates = arbRates.combine_first(arbRate)
            debug(arbRate.transpose())
            #m = normalizeme(m)
            if doPlot == True:
                plot(m,'-')
                #scatter(m)
                title(self.pk[ind]); legend(m.columns,2); show();
            ms.append(m.get_values().tolist())
        #print ms
        #scatter(ms[0],ms[1]); show();
        debug(arbRates.transpose())
        return arbRates
        
    def getFastestCryptoCoinArbitrage(self):
        # show the fastest coin to arbitrage
        try:
            arr
        except:
            arr = self.getMostProfitablePair()
        arrSortedAR = arr.sort('arbitrageRate', ascending=False)
        print p.DataFrame(arrSortedAR.ix[list(arrSortedAR.ix[:,'p1']).index(self.p1), :]).transpose(); print
        print p.DataFrame(arrSortedAR.ix[list(arrSortedAR.ix[:,'p2']).index(self.p2), :]).transpose()
    
    def getMostProfitablePair(self):
        fastestCoins = self.getFastestCryptoCoins()
        fcs = []
        try:
            arbRates
        except:
            arbRates = self.getArbRates()
        arr = arbRates.transpose()
        po1 = []; po2 = []
        for row in (n.array(arr.index, dtype=string0)):
            po1.append(row[0:3])
            po2.append(row[4:7])
        arr['p1'] = po1
        arr['p2'] = po2
        for i in range(0,len(arr)):
            #if arr.ix[i,'p1']
            try: arr.ix[i,'p11'] = fastestCoins.index(arr.ix[i,'p1'].upper())
            except: ''
            try: arr.ix[i,'p22'] = fastestCoins.index(arr.ix[i,'p2'].upper())
            except: ''
        arr1 = arr.sort('p11', ascending=True);
        arr2 = arr.sort('p22', ascending=True);
        self.p1 = arr1.ix[0,'p1']; debug(self.p1)
        self.p2 = arr2.ix[0,'p2']; debug(self.p2)
        debug(arr)
        return arr
    
    def updateData(self):
        # Create threads
        # source: http://pymotw.com/2/threading/
        for i in self.pk:                
            t0 = threading.Thread(target=self.getCurrencies)
            t0.daemon = False
            t0.start()
            t1 = threading.Thread(target=self.getRatesOnExchange)
            t1.daemon = False
            t1.start()
            t2 = threading.Thread(target=self.getTrades, args=(i, False,))
            t2.daemon = False
            t2.start()
            t3 = threading.Thread(target=self.getDepth, args=(i, False,))
            t3.daemon = False
            t3.start()
           #print "Error: unable to start thread"
        #while 1:
        #   pass

class CryptoCoin:
    
    def __init__(self):
        ''
    
    def updateData(self):
        
        b = btce()
        b.updateData()
        
        sh = ShapeShift()
        sh.updateData()
        
        # coinmarket updater
        c = CoinMarketCap()
        c.updateData()

class ShapeShift(CryptoCoinBaseClass):
    def __init__(self):
        ''
    
    def updateData(self):
        urls = 'btc, ltc, ppc, drk, doge, nmc, ftc, blk, nxt, btcd, qrk, rdd, nbt'
        url = re.sub(re.compile(r',', re.S), '', urls).split(' ')
            
        """
        abc = 'a b c d e f g h i j k l m n o p q r s t u v w x y z'.split(' ')
        #rin = p.DataFrame(n.int0(n.abs(n.random.randn(26)*10)))
        abc = list(it.permutations(abc, 3))
        abc = n.array(abc).tolist()
        li = []
        for i in abc[0:10]:
            li.append(''.join(i))
        """
        
        def fetchURLThread(url):
            try:
                debug('fetching:'+url)
                fetchURL(url, cachemode='a')
            except:
                ''
        
        li = url
        li = list(it.permutations(li, 2))
        li = n.array(li).tolist()
        lis = []
        for i in li:
            lis.append('_'.join(i))
        for i in lis:
            # doc source: https://shapeshift.io/api.html#rate
            """
            url: shapeshift.io/rate/<pair>
            method: GET
            
            <pair> is any valid coin pair such as btc_ltc or ltc_btc
            
            Success Output:
              
                {
                    "pair" : "btc_ltc",
                    "rate" : "70.1234"
                }
            """
            url = 'http://shapeshift.io/rate/'+i
            t = threading.Thread(target=fetchURLThread, args=[url])
            t.daemon = False
            t.start()
            
    def depositLimit():
        # source: https://shapeshift.io/api.html#deposit-limit
        """
        url: shapeshift.io/limit/<pair>
        method: GET
        
        <pair> is any valid coin pair such as btc_ltc or ltc_btc
        
        Success Output:
            {
                "pair" : "btc_ltc",
                "limit" : "1.2345"
            }
        """
        ''
        
    def recentTransactionsList(self):
        # source: https://shapeshift.io/api.html#recent-list
        """
        url: shapeshift.io/recenttx/<max>
        method: GET
        
        <max> is an optional maximum number of transactions to return.
        If <max> is not specified this will return 5 transactions.
        Also, <max> must be a number between 1 and 50 (inclusive).
        
        Success Output:
            [
                {
                curIn : <currency input>,
                curOut: <currency output>,
                amount: <amount>,
                timestamp: <time stamp>     //in seconds
                },
                ...
            ]
        """
        ''
        
    def statusOfDepositToAddress(self):
        # source: https://shapeshift.io/api.html#status-deposit
        """
        url: shapeshift.io/txStat/<address>
        method: GET
        
        <address> is the deposit address to look up.
        
        Success Output:  (various depending on status)
        
        Status: No Deposits Received
            {
                status:"no_deposits",
                address:<address>           //matches address submitted
            }
        
        Status: Received (we see a new deposit but have not finished processing it)
            {
                status:"received",
                address:<address>           //matches address submitted
            }
        
        Status: Complete
        {
            status : "complete",
            address: <address>,
            withdraw: <withdrawal address>,
            incomingCoin: <amount deposited>,
            incomingType: <coin type of deposit>,
            outgoingCoin: <amount sent to withdrawal address>,
            outgoingType: <coin type of withdrawal>,
            transaction: <transaction id of coin sent to withdrawal address>
        }
        
        Status: Failed
        {
            status : "failed",
            error: <Text describing failure>
        }
        
        *Note: this can still get the normal style error returned. For example if request is made without an address.
        """
    
    def timeRemainingOnFixedAmountTransaction(self):
        # source: https://shapeshift.io/api.html#timeremaining
        """
        url: shapeshift.io/timeremaining/<address>
        method: GET
        
        <address> is the deposit address to look up.
        
        Success Output:
        
            {
                status:"pending",
                seconds_remaining: 600
            }
        
        The status can be either "pending" or "expired".
        If the status is expired then seconds_remaining will show 0.
        """
    
if __name__ == "__main__":
    print 'stub'
    #testMicrofinance()
    #testGetDataFromQuandl()
    #print normalizeme2([1423,2342,2343,23441,1235,1236,7123,8123,913])
    #print normalizeme2([3345,3422,3453,344,345,635,7345,8234,2349])
    #print list(normalizeme2([9,8,7,6,5,4,3,2,1]).transpose().get_values()[0])
    #nnn = normalizeme2([1423,2342,2343,23441,1235,1236,7123,8123,913])
    #print list(nnn.transpose().get_values()[0])
    #import doctest; print doctest.testmod()
    #debug('test', 9)
    
    #qu = 'Building Permits canada'
    #qu = 'argentina inflation'
    #qu = 'non farm'
    #searchQuandl(qu)
    
    #headers = [0,1]
    #headers = None
    #searchQuandl('tesla', mode='combineplot', returndataset=False, headers=headers, listcolumns=True)
