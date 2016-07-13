
import argparse
# source: https://docs.python.org/2/howto/argparse.html
parser = argparse.ArgumentParser()
parser.add_argument("-v", '--verbose', help="turn on verbosity")
parser.add_argument("-l", '--live', help="go live and turn off dryrun", action="store_true")
parser.add_argument("-hh", '--history', help="history", action="store_true")
parser.add_argument("-hf", '--historyFilename', help="history file name")
parser.add_argument("-a", '--analyze', help="go live and turn off dryrun", action="store_true")
parser.add_argument("-acc", '--account', help="account number")
parser.add_argument('-g', "-gearing", '--leverage', help="gearing or leverage, default=50")
parser.add_argument('-n', '--num', help="number of trades default=None")
parser.add_argument('-dp', '--diffpThreshold', help="trade only signals above a given threshold default=5")
#parser.add_argument("-c", '--connect', help="connect, v=Vultr", action="store_true")
parser.add_argument("-i", '--interactive', help="Interactive Loop", action="store_true")
parser.add_argument("-ni", '--noInteractive', help="No interactive Q&A", action="store_true")
parser.add_argument("-nid", '--noInteractiveDeleverage', help="No interactive Q&A for the deleverage option", action="store_true")
parser.add_argument("-nil", '--noInteractiveLeverage', help="No interactive Q&A for the deleverage option", action="store_true")
parser.add_argument("-nif", '--noInteractiveFleetingProfits', help="No interactive Q&A for the fleeting profits routine", action="store_true")
args = parser.parse_args()

import sys
try: sys.path.index('/ml.dev/bin/datafeeds')
except: sys.path.append('/ml.dev/bin/datafeeds')

import numpy as n
import sys
try: sys.path.index('/ml.dev/bin/datafeeds')
except: sys.path.append('/ml.dev/bin/datafeeds')

import numpy as n
import pandas as p
#mport Quandl as q
from Quandl import Quandl as q
import datetime as dd
from qoreliquid import *
import talib as talib
from matplotlib import pyplot as plt
from pylab import rcParams
#get_ipython().magic(u'pylab inline')
#rcParams['figure.figsize'] = 20, 5

import oandapy

co = p.read_csv('/mldev/bin/datafeeds/config.csv', header=None)

env1=co.ix[0,1]
access_token1=co.ix[0,2]
oanda1 = oandapy.API(environment=env1, access_token=access_token1)

env2=co.ix[1,1]
access_token2=co.ix[1,2]
oanda2 = oandapy.API(environment=env2, access_token=access_token2)

acc = oanda2.get_accounts()['accounts']
accid = acc[0]['accountId']
#print 'using account: {0}'.format(accid)


@profile
def main(args, leverage=10, dryrun=True, verbose=False):
    # In[ ]:
    
    """
    #oanda1.get_accounts()
    targetSalaryPerSecond = (40e3 / (60*60*24*260))
    asddf = p.DataFrame(oanda1.get_trades(558788)['trades'])#.set_index('instrument')#.ix[:,'side units'.split(' ')]
    asddf['timeu'] = oq.oandaToTimestamp(asddf['time'])
    asddf['timeage'] = time.time() - n.array(oq.oandaToTimestamp(asddf['time']))
    asddf['targetSalaryPerSecond'] = targetSalaryPerSecond * asddf['timeage']
    asddf.ix[:, 'time timeu timeage targetSalaryPerSecond'.split(' ')]
    """
    
    # In[ ]:
    
    
    
    
    import os
    cmd = 'ls -t /tmp/patterns*'
    fname = os.popen(cmd).read().strip().split('\n')[0]
    dfh = {}
    df = p.DataFrame()
    if args.analyze:
        dfu = p.DataFrame()
        from multiprocessing.pool import ThreadPool
        pool = ThreadPool(processes=270)
        instruments = p.DataFrame(oanda2.get_instruments(accid)['instruments']).set_index('instrument')
        symbols = instruments.index
        #symbols = 'EUR_USD,GBP_USD,GBP_JPY,USD_CAD,EUR_AUD,USD_JPY,AUD_USD,AUD_JPY,CAD_JPY,EUR_CAD,EUR_CHF,EUR_GBP,NZD_JPY,NZD_USD,USD_CHF,CHF_JPY'.split(',')
        print ','.join(symbols)
        for i in symbols:
            #dfu0 = getc4(df, dfh, oanda2, instrument=i)
            async_result = pool.apply_async(getc4, [df, dfh, oanda2, i])
            dfu0   = async_result.get()
            dfu  = dfu.combine_first(dfu0)
            #if int(verbose) >= 3:
            print
            print dfu
        pool.close()
	    #break
        fname = '/tmp/patterns.dfu.%s.csv' % time.time()
        dfu.to_csv(fname)
    else:
        dfu = p.read_csv(fname, index_col=0)
    dfu['diff'] = n.abs(dfu['buy'] - dfu['sell'])
    if int(verbose) > 5:
        print dfu.sort('diff', ascending=False)
    
    # In[ calculate period weights ]:
    @profile
    def periodWeightsTable():
        p0 = [1, 5, 15, 30, 60, 240, 1440, 1440*5, 1440*20]
        p1 = n.array(range(1, len(p0)+1))
        pp = p.DataFrame(p1, columns=[0])
        #pp(:,3) = pp(:,2)./power(pp(:,1), 3)
        pp['period'] = p0
        pp['weight'] = pp.ix[:,1] / n.power(pp.ix[:,0], 3)
        pp['percent'] = pp['weight'] / n.sum(pp['weight'])
        #pp.ix[:,[0,'weight']].plot()
        #pp
        return pp.set_index(0)
    pw = periodWeightsTable()
    if int(verbose) > 5: print pw
    
    with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
        cli = [0,1,2,3,4,5,6,7,8]
        mdfu = p.DataFrame(dfu.ix[:,cli].get_values() * pw['percent'].get_values(), index=dfu.index, columns=dfu.columns[cli])
        dfu  = mdfu.combine_first(dfu)
        posdf = dfu.ix[:,cli][dfu.ix[:,cli] > 0].fillna(0)
        negdf = dfu.ix[:,cli][dfu.ix[:,cli] < 0].fillna(0)
        dfu['buy'] = n.sum(posdf.get_values(), 1)
        dfu['sell'] = n.abs(n.sum(negdf.get_values(), 1))
        dfu['diff'] = n.abs(dfu['buy'] - dfu['sell'])
        if int(verbose) > 5:
            print
            print 'pw'
            print pw#['weight']
            print
            print 'element-wise *'
            print posdf
            print negdf
            print 
            print dfu.sort('diff', ascending=False)
    
    #sys.exit()
    
    if args.diffpThreshold: diffpThreshold=int(args.diffpThreshold)
    else:                   diffpThreshold=5

    dfu['diff'] = n.abs(dfu['buy'].get_values() - dfu['sell'].get_values())
    dfu['diffp'] = (dfu['diff'].get_values())/n.sum(dfu['diff'].get_values())
    dfu['side'] = map(lambda x: 'buy' if x == 1 else 'sell', (n.array((dfu['buy'].get_values() - dfu['sell'].get_values()) > 0, dtype=int)))
    dfu['sidePolarity'] = map(lambda x: 1 if x == 1 else -1, (n.array((dfu['buy'].get_values() - dfu['sell'].get_values()) > 0, dtype=int)))
    
    # set the percentage threshold
    dfu2 = dfu[dfu['diffp'] > (float(diffpThreshold)/100)].sort_values(by='diff', ascending=False)
    # recalculate percentages [diffp]
    dfu2['diffp'] = (dfu2['diff'].get_values())/n.sum(dfu2['diff'].get_values())
    with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
        if verbose: print dfu2
    
    
    # In[ ]:
    
    orders = dfu2.ix[:, 'diff side diffp sidePolarity'.split(' ')]
    if int(verbose) > 5: 
        print 'Oanda orders:'
        print orders
        print
    
    ps = """AUD/NZD
    AUD/USD
    EUR/CHF
    EUR/GBP
    EUR/JPY
    EUR/NOK
    EUR/SEK
    EUR/USD
    GBP/USD
    NZD/USD
    USD/CAD
    USD/CHF
    USD/CNH
    USD/JPY
    USD/RUB""".replace('/', '_')
    #print ps
    
    psdf = p.DataFrame(ps.split('\n'))
    psdf['1'] = 1
    psdf = psdf.set_index(0)
    # list only 1broker pairs in the orderbook
    oneBrokerOrderbook = psdf.ix[list(orders.index), :]
    #print oneBrokerOrderbook[oneBrokerOrderbook['1'] == 1]
    #print oneBrokerOrderbook
    #print
    try:
        dfu3 = orders.ix[oneBrokerOrderbook[oneBrokerOrderbook['1'] == 1].index, :]
        
        # recalculate percentages [diffp]
        dfu3['diffp'] = (dfu3['diff'].get_values())/n.sum(dfu3['diff'].get_values())
        if int(verbose) > 5:
            print '1broker orders:'
            print dfu3
    except Exception as e:
        print e
        print 'No'
        print
        
    verbose                 = args.verbose
    noInteractive           = args.noInteractive
    noInteractiveLeverage   = args.noInteractiveLeverage
    noInteractiveDeleverage = args.noInteractiveDeleverage
    noInteractiveFleetingProfits = args.noInteractiveFleetingProfits
    
    oq = OandaQ(verbose=False)

    if args.account:
        try:
            dfu33 = rebalanceTrades(oq, dfu2, oanda1, int(args.account), dryrun=dryrun, leverage=leverage, verbose=verbose, noInteractive=noInteractive, noInteractiveLeverage=noInteractiveLeverage, noInteractiveDeleverage=noInteractiveDeleverage, noInteractiveFleetingProfits=noInteractiveFleetingProfits)
        except oandapy.OandaError as e:
            print e
            print 'Try a different account number'
    else:
        fu33 = rebalanceTrades(oq, dfu2, oanda2, accid, dryrun=dryrun, leverage=leverage, verbose=verbose, noInteractive=noInteractive, noInteractiveLeverage=noInteractiveLeverage, noInteractiveDeleverage=noInteractiveDeleverage, noInteractiveFleetingProfits=noInteractiveFleetingProfits)
        fu33 = rebalanceTrades(oq, dfu2, oanda1, 801996, dryrun=dryrun, leverage=leverage, verbose=verbose, noInteractive=noInteractive, noInteractiveLeverage=noInteractiveLeverage, noInteractiveDeleverage=noInteractiveDeleverage, noInteractiveFleetingProfits=noInteractiveFleetingProfits)
        fu33 = rebalanceTrades(oq, dfu2, oanda1, 135830, dryrun=dryrun, leverage=leverage, verbose=verbose, noInteractive=noInteractive, noInteractiveLeverage=noInteractiveLeverage, noInteractiveDeleverage=noInteractiveDeleverage, noInteractiveFleetingProfits=noInteractiveFleetingProfits)
        dfu33 = rebalanceTrades(oq, dfu2, oanda1, 558788, dryrun=dryrun, leverage=leverage, verbose=verbose, noInteractive=noInteractive, noInteractiveLeverage=noInteractiveLeverage, noInteractiveDeleverage=noInteractiveDeleverage, noInteractiveFleetingProfits=noInteractiveFleetingProfits)

if __name__ == "__main__":
    
    if args.leverage:
        leverage=int(args.leverage)
    else:
        leverage=50

    if args.account:
        account=int(args.account)
    else:
        account=558788

    def plotTransactionHistory(acc, oaoa):
        th = oaoa.get_transaction_history(acc)
        df = p.DataFrame()
        for i in th['transactions']:
            df = df.combine_first(p.DataFrame(i, index=[i['id']]).transpose())           
        df = df.transpose()
        #print df
        plot(df.ix[:,'accountBalance'].ffill()); show()

    """
    try:
        main(args, leverage=leverage, dryrun=dryrun)
    except Exception as e:
        qd.printTraceBack()
        print e
    """
    
    while True:
        print 'receiving feed..'
        if args.interactive:
            usage = 'usage: a=analyze, d=deleverage, l=leverage, f=fleetingProfits, ?=help'
            args = parser.parse_args()
            print usage
            mode = raw_input('mode ?: ')
            if mode == 'a': # analyze mode
                args.analyze = True
                args.live = False
            if mode == 'd': # deleverage mode (risk-off / remove from positions)
                args.live = True
                args.noInteractiveDeleverage = True
            if mode == 'l': # leverage mode (risk-on / add to positions)
                args.live = True
                args.noInteractiveLeverage = True
            if mode == 'f': # fleetingProfits mode (tp / take profits)
                args.live = True
                args.noInteractiveFleetingProfits = True
            if mode == '?' or mode == 'help': # help
                print usage
                break
            if int(args.verbose) >= 5:
                print 'mode: %s' % mode
                print 'live: %s' % args.live
                print 'noInteractiveLeverage: %s' % args.noInteractiveLeverage
                print 'noInteractiveDeleverage: %s' % args.noInteractiveDeleverage
                print 'noInteractiveFleetingProfits: %s' % args.noInteractiveFleetingProfits

        if args.live:
            dryrun=False
        else:
            dryrun=True
        if int(args.verbose) >= 5:
            print 'dryrun: %s' % dryrun
        
        try:
            if args.history:
                #plotTransactionHistory(account, oanda1)
                try:
                    try:
                        historyFilename = args.historyFilename
                    except:
                        historyFilename = '/home/qore2/Desktop/f566016f51bde41a6c6fd2b4ec74cd82.csv'
                    df = p.read_csv(historyFilename)
                    dfi = df.sort('Transaction ID', ascending=True)
                except:
                    dfi = p.DataFrame([])
                with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
                    print dfi#.columns
                    dfii = dfi.ix[:,'Transaction ID;Balance;Time (UTC)'.split(';')]#.tail(5)#.transpose()
                    #dfii['time'] = oq.oandaToTimestamp(dfii['Time (UTC)'])
                    dfp = dfii.ix[:,['Balance','Time (UTC)']].set_index('Time (UTC)')
                    dfp.plot()
                    show()
            else:
                main(args, leverage=leverage, dryrun=dryrun)
        except Exception as e:
            print e
        if not args.interactive:
            break
