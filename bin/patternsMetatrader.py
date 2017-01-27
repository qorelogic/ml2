
# -*- coding: utf-8 -*-
#%reload_ext autoreload
#%autoreload 2
import sys
def defp(pt):
    try:    sys.path.index(pt)
    except: sys.path.append(pt)
defp('/ml.dev/bin')
defp('/ml.dev/lib/oanda/oandapy')
import oandapyV20
import oandapyV20.endpoints.accounts as accounts
import oandapyV20.endpoints.trades as trades
import oandapyV20.endpoints.positions as positions
from oandapyV20.endpoints.pricing import PricingStream
from oandapyV20.endpoints.accounts import AccountSummary
import pandas as p
import oandapy
from matplotlib import pyplot as plt
from pylab import rcParams
#%pylab inline
rcParams['figure.figsize'] = 20, 5
accountID = "101-004-1984564-001"
co = p.read_csv('/mldev/bin/datafeeds/config.csv', header=None)
loginIndex = 4
env0=co.ix[loginIndex,1]
access_token0=co.ix[loginIndex,2]
oanda0 = oandapy.API(environment=env0, access_token=access_token0)
#client = API(access_token=access_token, headers={"Content-Type": "application/json"})
client = oandapyV20.API(access_token=access_token0)
#client = oandapyV20.API(access_token=access_token0, environment="live")
#client = oandapyV20.API(access_token=access_token0, environment="practice")
#client = oandapyV20.API(access_token=access_token0)
#client.api_url = 'https://test.com'
co
#for i in co[2]: print i


# compute metatrader portfolio
from qoreliquid import Patterns
pa = Patterns()
df = p.read_csv('/mldev/bin/data/oanda/cache/patterns/patterns.portfolioMetatrader.1485150677.45.csv', index_col=[0])
df = pa.computeMetraderData(df, balance=140.65, leverage=500)
import numpy as n
df['lots'] = n.round(df['lots'], 2)
with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
    print df.ix[:, 'side lots balanceMetatrader leverageMetatrader allMarginMetatrader amount2Metatrader closeTradePLMetatrader side diffp lots'.split(' ')].sort_index()
