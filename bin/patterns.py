
import argparse
# source: https://docs.python.org/2/howto/argparse.html
parser = argparse.ArgumentParser()
parser.add_argument("-v", '--verbose', help="turn on verbosity", action="store_true")
parser.add_argument("-l", '--live', help="go live and turn off dryrun", action="store_true")
parser.add_argument("-a", '--analyze', help="go live and turn off dryrun", action="store_true")
parser.add_argument("-acc", '--account', help="account number")
parser.add_argument('-g', "-gearing", '--leverage', help="gearing or leverage, default=50")
parser.add_argument('-n', '--num', help="number of trades default=None")
parser.add_argument('-dp', '--diffpThreshold', help="trade only signals above a given threshold default=5")
#parser.add_argument("-c", '--connect', help="connect, v=Vultr", action="store_true")
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
rcParams['figure.figsize'] = 20, 5

import oandapy

co = p.read_csv('datafeeds/config.csv', header=None)

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
        for i in 'EUR_USD,GBP_USD,GBP_JPY,USD_CAD,EUR_AUD,USD_JPY,AUD_USD,AUD_JPY,CAD_JPY,EUR_CAD,EUR_CHF,EUR_GBP,NZD_JPY,NZD_USD,USD_CHF,CHF_JPY,USD_MXN'.split(','):
            dfu = dfu.combine_first(getc4(df, dfh, oanda2, instrument=i))
        fname = '/tmp/patterns.dfu.%s.csv' % time.time()
        dfu.to_csv(fname)
    else:
        dfu = p.read_csv(fname, index_col=0)
    dfu['diff'] = n.abs(dfu['buy'] - dfu['sell'])
    if verbose: print dfu.sort('diff', ascending=False)
    
    # In[ calculate period weights ]:
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
    if verbose: print pw
    
    with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
        cli = [0,1,2,3,4,5,6,7,8]
        mdfu = p.DataFrame(dfu.ix[:,cli].get_values() * pw['percent'].get_values(), index=dfu.index, columns=dfu.columns[cli])
        dfu  = mdfu.combine_first(dfu)
        posdf = dfu.ix[:,cli][dfu.ix[:,cli] > 0].fillna(0)
        negdf = dfu.ix[:,cli][dfu.ix[:,cli] < 0].fillna(0)
        dfu['buy'] = n.sum(posdf.get_values(), 1)
        dfu['sell'] = n.abs(n.sum(negdf.get_values(), 1))
        dfu['diff'] = n.abs(dfu['buy'] - dfu['sell'])
        if verbose:
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
    dfu2 = dfu[dfu['diffp'] > (float(diffpThreshold)/100)].sort('diff', ascending=False)
    # recalculate percentages [diffp]
    dfu2['diffp'] = (dfu2['diff'].get_values())/n.sum(dfu2['diff'].get_values())
    with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
        if verbose: print dfu2
    
    
    # In[ ]:
    
    orders = dfu2.ix[:, 'diff side diffp sidePolarity'.split(' ')]
    if verbose: 
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
        if verbose: 
            print '1broker orders:'
            print dfu3
    except Exception as e:
        print e
        print 'No'
        print
        
    verbose=args.verbose
    
    if args.account:
        try:
            dfu33 = rebalanceTrades(dfu2, oanda1, int(args.account), dryrun=dryrun, leverage=leverage, verbose=verbose)
        except oandapy.OandaError as e:
            print e
            print 'Try a different account number'
    else:
        fu33 = rebalanceTrades(dfu2, oanda2, accid, dryrun=dryrun, leverage=leverage, verbose=verbose)
        fu33 = rebalanceTrades(dfu2, oanda1, 801996, dryrun=dryrun, leverage=leverage, verbose=verbose)
        fu33 = rebalanceTrades(dfu2, oanda1, 135830, dryrun=dryrun, leverage=leverage, verbose=verbose)
        dfu33 = rebalanceTrades(dfu2, oanda1, 558788, dryrun=dryrun, leverage=leverage, verbose=verbose)

if __name__ == "__main__":
    
    if args.live:
        dryrun=False
    else:
        dryrun=True

    if args.leverage:
        leverage=int(args.leverage)
    else:
        leverage=50
        
    main(args, leverage=leverage, dryrun=dryrun)
