# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>


# QoreQuant
# compinvesting-001
# video 1 - 9 Computing inside a hedge fund .mp4

#qstrader.py
#qsoptimizer.py
#qsforecaster.py

#%reset

import pandas as p
import numpy as n
import time
from threading import Thread
from qoreliquid import *

# Trading Algorithm
class QsTrader(Thread):
    def __init__(self):
        Thread.__init__(self)
        # getters
        self.historical      = None
        self.targetPortfolio = None
        self.livePortfolio   = None
        
        # setters
        self.orders = None
        
    def run(self):
        while 1:
            #self.check()
            self.gotoMarket()
            time.sleep(1e-1)            
    
    def getHistoricalPriceData(self):
        ''
        
    # portfolio_X.h5
    def getTargetPortfolio(self):
        optimizer = QsOptimizer()
        self.targetPortfolio = optimizer.generateTargetPortfolio()
        return self.targetPortfolio
        
    # portfolio_LIVE.h5
    def getLivePortfolio(self):
        # live portfolio
        # todo: get live portfolio from broker (keep persistent connection)
        livePortfolio = p.DataFrame([100,-200,50,-500], index=['AAPL','BAC','BOA','DAL'], columns=['live_amount'])
        self.livePortfolio = livePortfolio
        return livePortfolio

    # orders_V.h5
    def generateOrders(self):
        fname = 'orders_V.csv'
        # orders
        indx = []        
        orders = p.DataFrame(n.zeros(len(indx)), index=indx, columns=['orders_amount'])
        self.orders = orders
        return orders

    def sendOrders(self):
        # send orders only if there are orders to send
        # else do nothing        
        if n.sum(n.array(self.orders)) != 0:
            print 'detected pending orders.'
            print self.orders
            print 'sending orders to market..'
            print
    
    def gotoMarket(self):
        targetPortfolio = self.getTargetPortfolio()
        #print 'target portfolio'
        #print targetPortfolio
        #print
        livePortfolio = self.getLivePortfolio()
        #print 'live portfolio'
        #print livePortfolio
        #print
        orders = self.generateOrders()
        #print 'orders'
        #print orders
        #print
        #self.sendOrders()
        
        pp = p.DataFrame()
        pp = pp.combine_first(targetPortfolio)
        pp = pp.combine_first(livePortfolio)
        pp = pp.combine_first(orders)
        pp['orders_amount'] = n.diff(n.array(pp.ix[:,['live_amount','target_amount']]))
        self.orders = pp.ix[:,'orders_amount'].fillna(0)        
        self.orders = self.orders.ix[list(n.nonzero(n.array(self.orders != 0, dtype=int))[0])]
        #print self.orders        
        self.sendOrders()

# Portfolio Optimizer
class QsOptimizer:
    def __init__(self):
        # getters
        self.livePortfolio   = None
        self.nDayForecast    = None
        self.riskConstraints = None
        
        # setters
        self.targetPortfolio = None
    
    def getLivePortfolio(self):
        trader = QsTrader()
        self.livePortfolio = trader.getLivePortfolio()
        
    def getNDayForecast(self):
        forecaster = QsForecaster()
        self.forecaster = forecaster.getNDayForecast()
        
    def getRiskConstraints(self):
        ''
        
    def generateTargetPortfolio(self):
        # target portfolio
        targetPortfolio = p.DataFrame([100,0,50,-550], index=['AAPL','BAC','BOA','DAL'], columns=['target_amount'])
        self.targetPortfolio = targetPortfolio
        return targetPortfolio

# Forecasting Algorithm
class QsForecaster:
        def __init__(self):
            # getters
            self.informationFeed   = None
            self.historical        = None
            self.machineLearning   = None
            
            # setters
            self.nDayForecast = None
        
        def getInformationFeed(self):
            ''
        
        def getHistorical(self):
            trader = QsTrader()
            self.historical = trader.getHistoricalPriceData()
        
        def getMachineLearning(self):
            
            qq = QoreQuant()
            #qq.main(mode=1, pair='EUR_USD', granularity='H4', iterations=10000, alpha=0.09, risk=1, stopLossPrice=[1.113, 1.10963, 1.10707, 1.0963][3], noUpdate=True)

            mode          = 0
            noUpdate      = mode
            pair          = ['EUR_USD', 'EUR_NZD', 'NZD_USD', 'USD_JPY', 'USD_CHF', 'AUD_JPY', 'GBP_USD', 'AUD_USD', 'USD_CAD', 'NZD_JPY'][0]
            granularity   = ['M5', 'H4', 'H1'][1]
            iterations    = 10000
            alpha         = 0.1
            risk          = 1
            stopLossPrice = [1.10682, 1.113, 1.10963, 1.10707, 1.0963][0]
            
            qq.main(mode=mode, pair=pair, granularity=granularity, iterations=iterations, alpha=alpha, risk=risk, stopLossPrice=stopLossPrice, noUpdate=noUpdate)
        
        def generateNDayForecast(self):
            ''
    
trader = QsTrader()
forecaster = QsForecaster()

def main():
    #trader.start()
    forecaster.getMachineLearning()

def test():
    trader.gotoMarket()

if __name__ == "__main__":
    main()
    #test()

