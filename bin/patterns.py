
import argparse
# source: https://docs.python.org/2/howto/argparse.html
parser = argparse.ArgumentParser()
parser.add_argument("-l", '--live', help="go live and turn off dryrun", action="store_true")
parser.add_argument("-a", '--analyze', help="go live and turn off dryrun", action="store_true")
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


def main():
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
    print dfu
    
    # In[ ]:
    
    dfu['diff'] = n.abs(dfu['buy'].get_values() - dfu['sell'].get_values())
    dfu['diffp'] = (dfu['diff'].get_values())/n.sum(dfu['diff'].get_values())
    dfu['side'] = map(lambda x: 'buy' if x == 1 else 'sell', (n.array((dfu['buy'].get_values() - dfu['sell'].get_values()) > 0, dtype=int)))
    dfu['sideBool'] = map(lambda x: 1 if x == 1 else -1, (n.array((dfu['buy'].get_values() - dfu['sell'].get_values()) > 0, dtype=int)))
    
    dfu2 = dfu[dfu['diffp'] > (5.0/100)].sort('diff', ascending=False)
    # recalculate percentages [diffp]
    dfu2['diffp'] = (dfu2['diff'].get_values())/n.sum(dfu2['diff'].get_values())
    with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
        print dfu2
    
    
    # In[ ]:
    
    orders = dfu2.ix[:, 'diff side diffp sideBool'.split(' ')]
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
    dfu3 = orders.ix[oneBrokerOrderbook[oneBrokerOrderbook['1'] == 1].index, :]
    
    # recalculate percentages [diffp]
    dfu3['diffp'] = (dfu3['diff'].get_values())/n.sum(dfu3['diff'].get_values())
    print '1broker orders:'
    print dfu3
    
    fu33 = rebalanceTrades(dfu2, oanda2, accid, dryrun=dryrun)
    dfu33 = rebalanceTrades(dfu2, oanda1, 558788, dryrun=dryrun)

if __name__ == "__main__":
    
    if args.live:
        dryrun=False
    else:
        dryrun=True
        
    main()
