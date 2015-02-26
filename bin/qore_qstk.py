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

def getDataSymbols(symbols, mode='normal', days=365 , search=True):
    """
    mode = normal | testforward
    """
    if search == True:
        srcht = searchSymbols(symbols)
        print srcht
    else:
        srcht = symbols
    
    # Start and End date of the charts    
    #dt_end = dt.datetime(2010, 1, 1)
    dt_end = dt.datetime(2010, 2, 20)
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
    sdf['df_close']      = c_dataobj.get_data(ldt_timestamps, srcht, "close")
    sdf['df_close']      = sdf['df_close'].bfill().ffill()

    if mode == 'normal':
        return sdf['df_close']

    if mode == 'testforward':
        print 'getting past data from..'+str(dt_end)
        sdf['df_close_test'] = c_dataobj.get_data(ldt_timestamps_test, srcht, "close")
        print 'getting future data from..'+str(dt_end)
        sdf['df_close_test'] = sdf['df_close_test'].bfill().ffill()
        return sdf

def plotSymbols(symbols, normalize=False, sigmoid=False, search=False):
    sdf = getDataSymbols(symbols, search=search)
    if normalize:
        sdf = normalizeme(sdf)
    if sigmoid:
        sdf = sigmoidme(sdf)
    sdf.plot(); plt.legend(list(sdf.columns), 2); plt.show();

def calculateEfficientFrontier(ls_symbols, days=100):
    #print ls_symbols
    # Reading just the close prices
    #df_close = c_dataobj.get_data(ldt_timestamps, ls_symbols, "close")
    #df_close_test = c_dataobj.get_data(ldt_timestamps_test, ls_symbols, "close")
    sdf = getDataSymbols(ls_symbols, mode='testforward', days=days, search=False)

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
