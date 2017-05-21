# -*- coding: utf-8 -*-
#%reload_ext autoreload
#%autoreload 2
import argparse
# source: https://docs.python.org/2/howto/argparse.html
parser = argparse.ArgumentParser()
parser.add_argument("-v", '--verbose', help="turn on verbosity")
parser.add_argument("-b", '-bal', '--balance', help="turn on verbosity")
parser.add_argument("-l", '-lev', '--leverage', help="turn on verbosity")
parser.add_argument("-min", '--minimal', help="", action="store_true")
args = parser.parse_args()

import sys
def defp(pt):
    try:    sys.path.index(pt)
    except: sys.path.append(pt)
defp('/ml.dev/bin')
defp('/ml.dev/lib/oanda/oandapy')
import oandapyV20
import pandas as p
import numpy as n
import oandapy
import os

from qoreliquid import Patterns
@profile
def main():
    co = p.read_csv('/mldev/bin/datafeeds/config.csv', header=None)
    loginIndex = 2
    
    # compute metatrader portfolio
    def usage():
        print 'usage: -b <balance> -l <leverage> [-min]'
    try:
        balance  = float(args.balance)
    except Exception as e:
        #print e
        usage()
        sys.exit()
    try:
        leverage = int(args.leverage)
    except Exception as e:
        #print e
        usage()
        sys.exit()
    try:
        # auto select patterns file
        cmd = 'ls -t /ml.dev/bin/data/oanda/cache/patterns/patterns.portfolioMetatrader.* 2> /dev/null'
        fname = os.popen(cmd).read().strip().split('\n')[0]
        print 'Reading from: %s' % fname
    except Exception as e:
        print e
        usage()
        sys.exit()
    pa = Patterns(loginIndex=loginIndex)
    df = p.read_csv(fname, index_col=[0])
    df = pa.computePortfolioMetatrader(df, balance=balance, leverage=leverage, method='etoro')
    with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
        if args.minimal:
            fields = 'side lots lotsEtoro minimumLeverageEtoro unitsEtoro amount2Metatrader side diffp lots'.split(' ')
            #fields = 'side lots lotsEtoro minimumLeverageEtoro unitsEtoro balanceMetatrader leverageMetatrader allMarginMetatrader amount2Metatrader closeTradePLMetatrader side diffp lots'.split(' ')
        else:
            fields = 'side lots lotsEtoro _lotsEtoroRT _lotsEtoroRT2 _diffpLotsEtoro _minimumLeverageEtoro2 minimumLeverageEtoro unitsEtoro amount2Metatrader diffp lots'.split(' ')
        df = df.ix[:, fields]
        #df = df.sort_index()
        df = df.sort_values(by='diffp', ascending=False)
        print df
        
main()
