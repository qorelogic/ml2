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
import pandas as p
import oandapy
co = p.read_csv('/mldev/bin/datafeeds/config.csv', header=None)
loginIndex = 2

# compute metatrader portfolio
from qoreliquid import Patterns
def usage():
    print 'usage: <balance> <leverage> <patterns file>'
try:
    balance  = float(sys.argv[1])
except Exception as e:
    print e
    usage()
    sys.exit()
try:
    leverage = int(sys.argv[2])
except Exception as e:
    print e
    usage()
    sys.exit()
try:
    #fname = '/mldev/bin/data/oanda/cache/patterns/patterns.portfolioMetatrader.1485150677.45.csv'
    fname = sys.argv[3]
except Exception as e:
    print e
    usage()
    sys.exit()
pa = Patterns(loginIndex=loginIndex)
df = p.read_csv(fname, index_col=[0])
df = pa.computePortfolioMetatrader(df, balance=balance, leverage=leverage)
import numpy as n
df['lots'] = n.round(df['lots'], 2)
with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
    print df.ix[:, 'side lots balanceMetatrader leverageMetatrader allMarginMetatrader amount2Metatrader closeTradePLMetatrader side diffp lots'.split(' ')].sort_index()
