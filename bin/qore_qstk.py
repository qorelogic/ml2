# Portfolio Optimizer
# source: /coursera/compuinvesting-001/programming/QSTK-0.2.8/Examples/Basic/tutorial8.py

'''
(c) 2011, 2012 Georgia Tech Research Corporation
This source code is released under the New BSD license.  Please see
http://wiki.quantsoftware.org/index.php?title=QSTK_License
for license details.

Created on January, 24, 2013

@author: Sourabh Bajaj
@contact: sourabhbajaj@gatech.edu
@summary: Demonstrates the use of the CVXOPT portfolio optimization call.
'''

from qoreliquid import *

# QSTK Imports
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da

# Third Party Imports
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import re
import shutil as shu

# Creating an object of the dataaccess class with Yahoo as the source.
c_dataobj = da.DataAccess('Yahoo')

def getFrontier(na_data):
    '''Function gets a 100 sample point frontier for given returns'''

    # Special Case with fTarget=None, just returns average rets.
    (na_avgrets, na_std, b_error) = tsu.OptPort(na_data, None)

    # Declaring bounds on the optimized portfolio
    na_lower = np.zeros(na_data.shape[1])
    na_upper = np.ones(na_data.shape[1])

    # Getting the range of possible returns with these bounds
    (f_min, f_max) = tsu.getRetRange(na_data, na_lower, na_upper,
                            na_avgrets, s_type="long")

    # Getting the step size and list of returns to optimize for.
    f_step = (f_max - f_min) / 100.0
    lf_returns = [f_min + x * f_step for x in range(101)]

    # Declaring empty lists
    lf_std = []
    lna_portfolios = []

    # Calling the optimization for all returns
    for f_target in lf_returns:
        (na_weights, f_std, b_error) = tsu.OptPort(na_data, f_target,
                                na_lower, na_upper, s_type="long")
        lf_std.append(f_std)
        lna_portfolios.append(na_weights)

    return (lf_returns, lf_std, lna_portfolios, na_avgrets, na_std)

def searchSymbols(symbols):
    ls_all_syms = c_dataobj.get_all_symbols()
    mtc = []
    for i in ls_all_syms:
        for j in symbols:
            try:
                gr = (re.match(re.compile(r"(.*"+j+".*)", re.I), i)).group(1)
                mtc.append(gr)
            except AttributeError, e:
                    ''
    #print len(ls_all_syms)
    #for i in mtc:
    #    print i+': '+str(ls_all_syms.index(i))
    #print
    return mtc

def updatePrices(symbols):
    print 'updating symbols..'+str(symbols)
    #path = '/home/qore2/Desktop/qstk-data/data/'
    path = '/usr/local/lib/python2.7/dist-packages/QSTK-0.2.8-py2.7.egg/QSTK/QSData/Yahoo/'
    #ls_symbols = read_symbols('symbols.txt')
    get_yahoo_data(path, symbols)

def getDataSymbols(symbols, mode='normal', days=365 , dt_end=dt.datetime.now(), search=True, updatePrice=True):
    """
    mode = normal | testforward
    """
    if search == True:
        srcht = searchSymbols(symbols)
        print srcht
    else:
        srcht = symbols
    
    if updatePrice == True:
        updatePrices(symbols)
    
    # Start and End date of the charts    
    dt_start = dt_end - dt.timedelta(days=days)
    dt_test = dt_end + dt.timedelta(days=days)
    
    # We need closing prices so the timestamp should be hours=16.
    dt_timeofday = dt.timedelta(hours=16)
    
    # Get a list of trading days between the start and the end.
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)
    ldt_timestamps_test = du.getNYSEdays(dt_end, dt_test, dt_timeofday)
    
    sdf = {}
    #sdf = c_dataobj.get_data_hardread(ldt_timestamps, srcht, ['close'])[0]    
    #print srcht
    print 'Fetching '+str(days)+' days data prior to '+str(dt_end)
    sdf['df_close'] = c_dataobj.get_data(ldt_timestamps, srcht, "close")
    sdf['df_close'] = sdf['df_close'].bfill().ffill()

    if mode == 'normal':
        return sdf['df_close']

    if mode == 'testforward':
        print 'Fetching '+str(days)+' days data after '+str(dt_end)
        sdf['df_close_test'] = c_dataobj.get_data(ldt_timestamps_test, srcht, "close")
        sdf['df_close_test'] = sdf['df_close_test'].bfill().ffill()
        return sdf

def plotSymbols(symbols, normalize=False, sigmoid=False, search=False, updatePrices=False):
    sdf = getDataSymbols(symbols, search=search, updatePrice=updatePrices)
    if normalize:
        sdf = normalizeme(sdf)
    if sigmoid:
        sdf = sigmoidme(sdf)
    sdf.plot(); plt.legend(list(sdf.columns), 2); plt.show();

def calculateEfficientFrontier(ls_symbols, dt_end, days=100, updatePrices=False, annotate=False):

    # Creating an object of the dataaccess class with Yahoo as the source.
    c_dataobj = da.DataAccess('Yahoo')

    ls_all_syms = c_dataobj.get_all_symbols()
    # Bad symbols are symbols present in portfolio but not in all syms
    ls_bad_syms = list(set(ls_symbols) - set(ls_all_syms))
    for s_sym in ls_bad_syms:
        i_index = ls_symbols.index(s_sym)
        ls_symbols.pop(i_index)

    # Start and End date of the charts
    dt_start = dt_end - dt.timedelta(days=365)
    dt_test = dt_end + dt.timedelta(days=365)

    # We need closing prices so the timestamp should be hours=16.
    dt_timeofday = dt.timedelta(hours=16)

    # Get a list of trading days between the start and the end.
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)
    ldt_timestamps_test = du.getNYSEdays(dt_end, dt_test, dt_timeofday)

    # Reading just the close prices
    #df_close = c_dataobj.get_data(ldt_timestamps, ls_symbols, "close")
    #df_close_test = c_dataobj.get_data(ldt_timestamps_test, ls_symbols, "close")
    sdf = getDataSymbols(ls_symbols, mode='testforward', days=days, search=False, updatePrice=updatePrices, dt_end=dt_end)

    df_close = sdf['df_close']
    df_close_test = sdf['df_close_test']
    #df_close = getDataSymbols(ls_symbols)
    #df_close_test = getDataSymbols(ls_symbols)

    # Filling the data for missing NAN values
    #df_close = df_close.fillna(method='ffill')
    #df_close = df_close.fillna(method='bfill')
    #df_close_test = df_close_test.fillna(method='ffill')
    #df_close_test = df_close_test.fillna(method='bfill')

    # Copying the data values to a numpy array to get returns
    na_data = df_close.values.copy()
    na_data_test = df_close_test.values.copy()
    
    # Getting the daily returns
    tsu.returnize0(na_data)
    tsu.returnize0(na_data_test)
    
    # Calculating the frontier.
    (lf_returns, lf_std, lna_portfolios, na_avgrets, na_std) = getFrontier(na_data)
    (lf_returns_test, lf_std_test, unused, unused, unused) = getFrontier(na_data_test)
    
    #print pd.DataFrame(na_data)
    #return 1
    
    # Plotting the efficient frontier
    plt.clf()
    plt.plot(lf_std, lf_returns, 'b')
    #print str(lf_std) + ' ' + str(lf_returns)
    #print len(lf_std)
    #print len(lf_returns)
    #for i in range(0,len(lf_std)):
    #    print str(lf_std[i]) + ' ' + str(lf_returns[i])
    plt.plot(lf_std_test, lf_returns_test, 'r')
    
    
    # Plot where the efficient frontier would be the following year
    lf_ret_port_test = []
    lf_std_port_test = []
    for na_portfolio in lna_portfolios:
        na_port_rets = np.dot(na_data_test, na_portfolio)
        lf_std_port_test.append(np.std(na_port_rets))
        lf_ret_port_test.append(np.average(na_port_rets))
    
    plt.plot(lf_std_port_test, lf_ret_port_test, 'k')
    
    # Plot indivisual stock risk/return as green +
    #for i, f_ret in enumerate(na_avgrets):
    #    plt.plot(na_std[i], f_ret, 'g+')
    green1  = pd.DataFrame(na_avgrets, columns=['na_avgrets'], index=df_close.columns)
    green   = pd.DataFrame(na_std, columns=['na_std'], index=df_close.columns)
    ret = green1.combine_first(green)
    #print ret
    ret = ret.sort('na_std', ascending=True)
    #print ret1.ix[0:3]
    #print len(ret1)
    #plot(ret1['na_std'], ret1['na_avgrets'], '.'); show();
    
    for i, f_ret in enumerate(na_avgrets):
        plt.plot(na_std[i], f_ret, 'g+')
    plt.plot(na_std, na_avgrets, '.')
    # annotation -------------
    # source: http://stackoverflow.com/questions/5147112/matplotlib-how-to-put-individual-tags-for-a-scatter-plot
    if annotate == True:
        labels = [ls_symbols[i].format(i) for i in range(len(na_avgrets))]
        for label, x, y in zip(labels, na_std, na_avgrets):
            plt.annotate(
                label, 
                xy = (x, y), xytext = (-20, 20),
                textcoords = 'offset points', ha = 'right', va = 'bottom',
                bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.25),
                arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))
    # end annotation -------------
    
    # # Plot some arrows showing transistion of efficient frontier
    for i in range(0, 101, 10):
    #for i in range(0, 10, 1):
    #    print i
        #plt.plot(lf_std[i], lf_returns[i], lf_std_port_test[i] - lf_std[i], lf_ret_port_test[i] - lf_returns[i], color='r')
        plt.plot(lf_std_port_test[i], lf_ret_port_test[i], 'ok')
        plt.plot(lf_std[i], lf_returns[i], 'ok')
    
    # Labels and Axis
    plt.legend(['2014 Frontier', '2015 Frontier', 'Performance of \'14 Frontier in 2015'], loc='lower right')
    plt.title('Efficient Frontier For S&P 100 ')
    plt.ylabel('Expected Return')
    plt.xlabel('StDev')
    
    return ret

def getEfficientFrontierCharts(dt_end, calculateHowMany=None, printHowMany=None, fname='tutorial3portfolio.csv', days=365, annotate=False):
    sp500 = p.read_csv('data/quandl/SP500.csv')
    print len(sp500)
    if calculateHowMany == None:
        calculateHowMany = len(sp500)
    tiks = list(sp500.ix[:,'Ticker'][0:calculateHowMany])
    print len(tiks)
    print tiks
    out = calculateEfficientFrontier(tiks, dt_end, days=days, annotate=annotate)
    #print out
    #df9 = list(out.index[[0,len(out.index)-25]])
    #print df9
    
    if printHowMany == None:
        printHowMany = len(out)
    efficientFrontier = out.ix[0:printHowMany,:]
    #print list(efficientFrontier.index)
    #df9 = getDataSymbols(df9, search=False, updatePrice=True)
    #print df9
    #print sharpe(df9.ix[:,0])
    #df9c = getDataSymbols(df9, search=False, updatePrice=False)
    #print sharpe(df9c.ix[:,'ACE'])
    #plotSymbols(list(efficientFrontier.index), normalize=True)
    
    #out2 = calculateEfficientFrontier(list(efficientFrontier.index), days=365*5)
    #print out2
    
    out2List = list(efficientFrontier.index)
    #out2List.append('MSFT')
    print out2List
    out2 = efficientFrontier.copy()
    #out2['alloc'] = out2.ix[:,'na_std']/n.sum(out2.ix[:,'na_std'])
    out2['alloc'] = (1-out2.ix[:,'na_std'])/n.sum(1-out2.ix[:,'na_std'])
    print len(out2)
    print out2
    
    # copy previous allocation file to archive
    tct = os.path.getmtime(fname)
    dtnow = dt.datetime.fromtimestamp(tct)
    tstm = dt.datetime.strftime(dtnow, '%Y%m%d-%H%M%S')
    fname2 = fname+'.'+tstm+'.csv'
    shu.copy2(fname, fname2)

    print out2.ix[:,'alloc'].to_csv(fname)
    
    return out2
    
    #plotSymbols(out2List, normalize=True)
    
    """
    # Test calculateEfficientFrontier() with sample tickers    
    srch = ['AMD', 'MS', 'APL', 'NVD']
    #tiks = searchSymbols(srch)
    #tiks    
    #print list(tiks)
    
    #tiks = searchSymbols(srch)
    #df1_close = getDataSymbols(srch)
    #plotSymbols(srch, normalize=True, sigmoid=True)
    
    #sdf = getDataSymbols(list(tiks), mode='test', days=10)
    #print sdf['df_close']
    #print sdf['df_close_test']
    
    #out = calculateEfficientFrontier(list(tiks), days=365)
    
    srch = searchSymbols(srch)
    #df1_close = getDataSymbols(srch)
    #plotSymbols(srch, normalize=True, sigmoid=True)
    #print (srch)
    out = calculateEfficientFrontier(srch)
    print out
    """


def portfolioBacktester(fname='tutorial3portfolio.csv', dt_end=dt.datetime.now(), days=1095):
    # Portfolio Backtester
    # Tips for accessing historical data via DataAccess + a quick and dirty portfolio back test
    # source: http://wiki.quantsoftware.org/index.php?title=QSTK_Tutorial_3
    
    import QSTK.qstkutil.qsdateutil as du
    import QSTK.qstkutil.tsutil as tsu
    import QSTK.qstkutil.DataAccess as da
    import datetime as dt
    import matplotlib.pyplot as plt
    import pandas as pd
    import numpy as np
    
    """
    csv = " ""symbol, allocation
    SPY,0.3
    GABBABOOM,0.2
    GLD,0.3
    7ABBA, 0.2
    " ""
    fname = 'tutorial3portfolio.csv'
    fp = open(fname, 'w')
    fp.write(csv)
    fp.close()
    """
    #print df_alloc.ix[len(df_alloc)-1,:].to_csv(fname)
    
    #Reading in the portfolio description
    
    #NumPy provides a nice utility, loadtxt() for reading in CSV formatted data files. 
    #Here's the code for reading in the portfolio:
    skiprows = 0
    na_portfolio = np.loadtxt(fname, dtype='S5,f4', delimiter=',', comments="#", skiprows=skiprows)
    #os.remove(fname)
    print pd.DataFrame(na_portfolio)
    
    #The second line (dtype=) defines the format for each column. I think the other arguments are self explanatory. 
    #Now let's take a look at what we get back from this read:
    #[('SPY', 0.30000001192092896) ('GABBA', 0.20000000298023224),('GLD', 0.30000001192092896) ('7ABBA', 0.20000000298023224)]
    #Later on it will be helpful if our data is sorted by symbol name, so we'll do that next:
    na_portfolio = sorted(na_portfolio, key=lambda x: x[0])
    #print p.DataFrame(na_portfolio)
    #Which prints out:
    #[('7ABBA', 0.20000000298023224), ('GABBA', 0.20000000298023224), ('GLD', 0.30000001192092896), ('SPY', 0.30000001192092896)]
    #Now we build two lists, one that contains the symbols and one that contains the allocations:
    ls_port_syms = []
    lf_port_alloc = []
    for port in na_portfolio:
        ls_port_syms.append(port[0])
        lf_port_alloc.append(port[1])
    print ls_port_syms
    updatePrices(ls_port_syms)
    #Checking for spurious symbols and removing them
    #
    #Now we're going to benefit from the horsepower of our DataAccess class and Python's set operations. 
    #First step is to see which symbols are available, then intersect that list with the symbols in our portfolio:
    c_dataobj = da.DataAccess('Yahoo')
    ls_all_syms = c_dataobj.get_all_symbols()
    ls_bad_syms = list(set(ls_port_syms) - set(ls_all_syms))
    #The second line above returns a list of all symbols available to us in the "Yahoo" data store. 
    #On the third line above we convert the list of all symbols, and the list of symbols in our portfolio into sets, 
    #then remove the symbols not present in the ls_all_syms but present in the ls_port_syms. These are the bad symbols.
    
    if len(ls_bad_syms) != 0:
            print "Portfolio contains bad symbols : ", ls_bad_syms
    #The above code results in the following print out:
    #Portfolio contains bad symbols : ['7ABBA', 'GABBA']
    #Now we'll remove those bad symbols from our portfolio:
    for s_sym in ls_bad_syms:
        i_index = ls_port_syms.index(s_sym)
        ls_port_syms.pop(i_index)
        lf_port_alloc.pop(i_index)
    #Configuring times and reading the data
    #
    #The list portsyms now contains the proper list of valid symbols, so we can ask DataAccess to return them 
    #for us with out blowing up. First we must set up the time boundaries as below:
    #dt_end = dt.datetime(2015, 1, 1)
    #dt_end = dt.datetime.now()
    dt_start = dt_end - dt.timedelta(days=days)
    dt_timeofday = dt.timedelta(hours=16)
    
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)
    
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    
    ldf_data = c_dataobj.get_data(ldt_timestamps, ls_port_syms, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))
    #The code above reads in the data for the symbols in our portfolio between the dates of Jan 1, 2011, 
    #back to 1095 days before that (3 years).
    #Now, a quick and dirty back test
    #
    #Note: this example computes portfolio returns assuming daily rebalancing. For coursera homework 1, 
    #you should not assume daily rebalancing.
    #The first step is to prep the data. We make a copy of our closing prices in to "rets", 
    #fill the data forward, then convert it into daily returns:
    df_rets = d_data['close'].copy()
    df_rets = df_rets.fillna(method='ffill')
    df_rets = df_rets.fillna(method='bfill')
    
    na_rets = df_rets.values
    na_rets = p.DataFrame(na_rets).fillna(0).get_values()
    #print 'na_rets'; print p.DataFrame(na_rets)
    tsu.returnize0(na_rets)
    # fixes the portfolio nan issue
    na_rets = p.DataFrame(na_rets).fillna(0).get_values()
    #print 'na_rets2'; print p.DataFrame(na_rets)
    #Note that we extracted an ndarray from "close" (a pandas DataFrame), so we're now no longer benefitting 
    #from DataFrame features. You should consult other locations on this site for details on fill forward 
    #and converting into daily returns. For our combined portfolio we'll assume the combined return for each day 
    #is a sum of the returns for each equity weighted by the allocation. We can quickly compute the daily returns 
    #and the cumulative returns as follows:
    na_portrets = np.sum(na_rets * lf_port_alloc, axis=1)
    #print 'na_portrets'; print na_portrets
    na_port_total = np.cumprod(na_portrets + 1)
    #print 'na_port_total'; print na_port_total
    #In a similar manner we can compute the returns of the individual components as follows:
    na_component_total = np.cumprod(na_rets + 1, axis=0)
    #That's it for the "back test." porttot contains the total returns for our combined portfolio.
    #Plotting the results
    
    #Our combined portfolio (and component equities).
    plt.clf()
    fig = plt.figure()
    fig.add_subplot(111)
    plt.plot(ldt_timestamps, na_component_total, alpha=0.4)
    plt.plot(ldt_timestamps, na_port_total)
    ls_names = ls_port_syms
    ls_names.append('Portfolio')
    plt.title('Portfolio Allocations incl. assets');
    plt.legend(ls_names,2)
    plt.ylabel('Cumulative Returns')
    plt.xlabel('Date'); plt.show();
    fig.autofmt_xdate(rotation=45);    
    plt.plot(ldt_timestamps, na_port_total);
    plt.title('Portfolio Allocations ex. assets');
    plt.legend(['SP 500','Portfolio'],2);
    plt.show();
    
    # show the S&P500 and VIX
    dt_start0  = dt.datetime.strftime(dt_start, '%Y-%m-%d')
    dt_end0    = dt.datetime.strftime(dt_end, '%Y-%m-%d')
    #dt_start0  = dt.datetime.strftime(dt.datetime(2012,01,01), '%Y-%m-%d')
    #dt_end0    = dt.datetime.strftime(dt.datetime(2015,01,01), '%Y-%m-%d')
    #dt_start = dt.datetime.strptime(dt_start0, "%Y-%m-%d")
    #dt_end   = dt.datetime.strptime(dt_end0, "%Y-%m-%d")
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt.timedelta(hours=16))
    #print ldt_timestamps
    print len(ldt_timestamps)
    #z = getDataFromQuandl('YAHOO/INDEX_GSPC', dataset='').set_index('Date').ix[dt_start0:dt_end0,['Close']]
    z = getDataFromQuandl(['YAHOO/INDEX_GSPC','YAHOO/INDEX_VIX'], dataset='').bfill().ffill().ix[dt_start0:dt_end0,['YAHOO/INDEX_GSPC Close', 'YAHOO/INDEX_VIX Close']]  #.set_index('Date')
    #z['Portfolio'] = na_port_total
    dt_timeofday_na_port_total = dt.timedelta(hours=0)
    ldt_timestamps_na_port_total = du.getNYSEdays(dt_start, dt_end, dt_timeofday_na_port_total)
    z2 = p.DataFrame(na_port_total, index=ldt_timestamps_na_port_total, columns=['Portfolio'])
    z = z.combine_first(z2).bfill().ffill()
    z = normalizeme(z)
    #z = sigmoidme(z)
    plot(z.index, z)
    #legend(['Portfolio',z.columns[0], z.columns[1]],2)
    legend(z.columns,2)
    #z = getDataFromQuandl('YAHOO/INDEX_VIX', dataset='').set_index('Date').ix[dt_start0:dt_end0,['Close']]
    #print len(z)
    #z = normalizeme(z)
    #z = sigmoidme(z)
    #plot(ldt_timestamps, z)
    
    #plt.savefig('tutorial3.pdf', format='pdf')

def getDatasetSymbol(symbol, dt_end=dt.datetime.now(), days=365*2, hours=16):
    c_dataobj = da.DataAccess('Yahoo', verbose=True)
    dt_timeofday = dt.timedelta(hours=hours)
    dt_end = dt.datetime(2010, 2, 20)
    dt_start = dt_end - dt.timedelta(days=days)
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)
    ret = c_dataobj.get_data(ldt_timestamps, [symbol], "close")
    return ret

def trollPlots():
    print out
    lsstk = []
    for i in out.index:
        lsstk.append(i)
        #print lsstk
        plotSymbols((lsstk), normalize=True)
    
    #df9 = list(out.index[[0,len(out.index)-25]])
    #df9 = list(out.index[lsstk])
    #df9 = getDataSymbols(df9, search=False, updatePrice=True)
    #print df9
    #print sharpe(df9.ix[:,0])
    #plotSymbols(list(out.index[[0,len(out.index)-25]]), normalize=True)
    #plotSymbols(list(out.index[lsstk]), normalize=True)

# -----------------------------------------

'''
Pulling Yahoo CSV Data
from: YahooDataPull.py
'''

import urllib2
import urllib
import datetime
import os
import QSTK.qstkutil.DataAccess as da

def get_yahoo_data(data_path, ls_symbols):
    '''Read data from Yahoo
    @data_path : string for where to place the output files
    @ls_symbols: list of symbols to read from yahoo
    '''
    # Create path if it doesn't exist
    if not (os.access(data_path, os.F_OK)):
        os.makedirs(data_path)

    ls_missed_syms = []
    # utils.clean_paths(data_path)   

    _now = datetime.datetime.now()
    # Counts how many symbols we could not get
    miss_ctr = 0
    for symbol in ls_symbols:
        # Preserve original symbol since it might
        # get manipulated if it starts with a "$"
        symbol_name = symbol
        if symbol[0] == '$':
            symbol = '^' + symbol[1:]

        symbol_data = list()
        # print "Getting {0}".format(symbol)

        try:
            params = urllib.urlencode ({'a':0, 'b':1, 'c':2000, 'd':_now.month-1, 'e':_now.day, 'f':_now.year, 's': symbol})
            url = "http://ichart.finance.yahoo.com/table.csv?%s" % params
            url_get = urllib2.urlopen(url)
            
            header = url_get.readline()
            symbol_data.append (url_get.readline())
            while (len(symbol_data[-1]) > 0):
                symbol_data.append(url_get.readline())

            # The last element is going to be the string of length zero. 
            # We don't want to write that to file.
            symbol_data.pop(-1)
            #now writing data to file
            f = open (data_path + symbol_name + ".csv", 'w')

            #Writing the header
            f.write (header)

            while (len(symbol_data) > 0):
                f.write (symbol_data.pop(0))

            f.close()

        except urllib2.HTTPError:
            miss_ctr += 1
            ls_missed_syms.append(symbol_name)
            print "Unable to fetch data for stock: {0} at {1}".format(symbol_name, url)
        except urllib2.URLError:
            miss_ctr += 1
            ls_missed_syms.append(symbol_name)
            print "URL Error for stock: {0} at {1}".format(symbol_name, url)

    print "All done. Got {0} stocks. Could not get {1}".format(len(ls_symbols) - miss_ctr, miss_ctr)
    return ls_missed_syms

def read_symbols(s_symbols_file):
    '''Read a list of symbols'''
    ls_symbols = []
    ffile = open(s_symbols_file, 'r')
    for line in ffile.readlines():
        str_line = str(line)
        if str_line.strip(): 
            ls_symbols.append(str_line.strip())
    ffile.close()
    return ls_symbols 

def update_my_data():
    '''Update the data in the root dir'''
    c_dataobj = da.DataAccess('Yahoo', verbose=True)
    s_path = c_dataobj.rootdir
    ls_symbols = c_dataobj.get_all_symbols()
    ls_missed_syms = get_yahoo_data(s_path, ls_symbols)
    # Making a second call for symbols that failed to double check
    get_yahoo_data(s_path, ls_missed_syms)
    return
    
def generateQstkSymbolsTxt():
    # generate qstools/symbols.txt (required for the yahoo pull prices script)
    #fname = '/usr/local/lib/python2.7/dist-packages/QSTK-0.2.8-py2.7.egg/QSTK/qstktools/symbols.txt'
    fname = '/home/qore2/Desktop/qstk-data/symbols.txt'
    df9 = p.DataFrame(c_dataobj.get_all_symbols(), index=None).transpose()
    df9 = list(df9.get_values()[0])
    n.savetxt(fname, df9, fmt='%s', delimiter=',', )


def main():
    '''Main Function'''
    path = './'
    ls_symbols = read_symbols('symbols.txt')
    get_yahoo_data(path, ls_symbols)

#if __name__ == '__main__':
#    main()
