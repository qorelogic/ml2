
import re

def searchSymbols(symbols):
    #len(ls_all_syms)
    #ls_all_syms.index('AAPL')
    mtc = []
    for i in ls_all_syms:
        for j in symbols:
            try:
                mtc.append((re.match(re.compile(r".*"+j+".*", re.I), i)).group())
            except:
                ''
    return mtc    

def getDataSymbols(symbols):
    srcht = searchSymbols(symbols)
    #print srcht
    
    # Start and End date of the charts
    days = 365 * 10
    #dt_end = dt.datetime(2010, 1, 1)
    dt_end = dt.datetime(2015, 2, 20)
    dt_start = dt_end - dt.timedelta(days=days)
    dt_test = dt_end + dt.timedelta(days=days)
    
    # We need closing prices so the timestamp should be hours=16.
    dt_timeofday = dt.timedelta(hours=16)
    
    # Get a list of trading days between the start and the end.
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)
    ldt_timestamps_test = du.getNYSEdays(dt_end, dt_test, dt_timeofday)
    
    #sdf = c_dataobj.get_data_hardread(ldt_timestamps, srcht, ['close'])[0]
    sdf = c_dataobj.get_data(ldt_timestamps, srcht, "close")
    
    sdf = sdf.bfill().ffill()
    return sdf

def plotSymbols(symbols, normalize=False, sigmoid=False):
    sdf = getDataSymbols(symbols)
    if normalize:
        sdf = normalizeme(sdf)
    if sigmoid:
        sdf = sigmoidme(sdf)
    sdf.plot(); legend(list(sdf.columns), 2); show();

def calculateEfficientFrontier(ls_symbols):
    #print ls_symbols
    # Reading just the close prices
    #df_close = c_dataobj.get_data(ldt_timestamps, ls_symbols, "close")
    #df_close_test = c_dataobj.get_data(ldt_timestamps_test, ls_symbols, "close")
    df_close = getDataSymbols(ls_symbols)
    df_close_test = getDataSymbols(ls_symbols)    
    
    # Filling the data for missing NAN values
    df_close = df_close.fillna(method='ffill')
    df_close = df_close.fillna(method='bfill')
    df_close_test = df_close_test.fillna(method='ffill')
    df_close_test = df_close_test.fillna(method='bfill')
    
    # Copying the data values to a numpy array to get returns
    na_data = df_close.values.copy()
    na_data_test = df_close_test.values.copy()
    
    print p.DataFrame(na_data)
    # Getting the daily returns
    tsu.returnize0(na_data)
    tsu.returnize0(na_data_test)
    
    # Calculating the frontier.
    (lf_returns, lf_std, lna_portfolios, na_avgrets, na_std) = getFrontier(na_data)
    
    return 1
    
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
    for i, f_ret in enumerate(na_avgrets):
        print str(i) + str(na_avgrets[i]) + ' ' + str(f_ret)
        plt.plot(na_std[i], f_ret, 'g+')
    #plt.plot(na_std, na_avgrets, '.')
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
    #return ret
