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

"""
import pandas as p
import numpy as n
import time
"""
from qoreliquid import QoreQuant
from threading import Thread
import sys, traceback

def rawInput(msg, options, option=None):
    for i in xrange(len(options)): print '{0} {1}'.format(i, options[i])
    while True:
        try:
            if option == None:
                option = int(raw_input(msg))
            if option in xrange(len(options)):
                break
        except:
            pass
        print 'Try again'
    return option

def argvOrRawInput(msg, options, argv):
    try:
        option = int(sys.argv[argv])
        option = rawInput(msg, options, option=option)
    except Exception as e:
        print e
        option = rawInput(msg, options)
    return option

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
            self.qq = QoreQuant(verbose=True)
        
        def getInformationFeed(self):
            ''
        
        def getHistorical(self):
            trader = QsTrader()
            self.historical = trader.getHistoricalPriceData()
        
        def getMachineLearning(self):
            
            pairs         = ['EUR_USD', 'GBP_USD', 'AUD_USD', 'NZD_USD', 'NZD_EUR', 'USD_JPY',  'USD_CHF', 'USD_CAD','GBP_JPY', 'EUR_NZD', 'GBP_NZD', 'AUD_JPY', 'AUD_NZD', 'NZD_JPY']
            pairs         = ['EUR_USD', 'GBP_USD', 'AUD_USD','EUR_JPY', 'GBP_JPY','USD_JPY']
            granularities = [ 'D','H4','H1','M30','M15','M5','M1','S10','S5']
            iterations    = 300000
            alpha         = 0.125
            risk          = 1
            plot          = False
            stopLossPrice = [0.73745, 0.73488, 1.07978, 1.5617, 1.1024, 1.10965, 1.102, 1.10682, 1.113, 1.10963, 1.10707, 1.0963][0]
            
            #modes = ['train','predict','trade']
            modes = 'update train trade'.split(' ')

            mode        = argvOrRawInput('select number: ', modes, 1)
            pair        = argvOrRawInput('select number: ', pairs, 2)
            granularity = argvOrRawInput('select number: ', granularities, 3)
            
            print "{0} {1} {2}".format(modes[mode], pairs[pair], granularities[granularity])

            if mode == 0: noUpdate = False
            if mode == 1 or mode == 2: noUpdate = True

            if mode == 2:
                stopLossPrice = float(raw_input('stopLossPrice: '))
                risk          = float(raw_input('risk: '))

            pair          = pairs[pair]
            granularity   = granularities[granularity]
            #%prun self.qq.main(mode=mode, pair=pair, granularity=granularity, iterations=iterations, alpha=alpha, risk=risk, stopLossPrice=stopLossPrice, noUpdate=noUpdate, plot=plot)
            #%lprun -f self.qq.main -f self.qq.update -f self.qq.oq.updateBarsFromOanda -f self.qq.oq.appendHistoricalPrice self.qq.main(mode=mode, pair=pair, granularity=granularity, iterations=iterations, alpha=alpha, risk=risk, stopLossPrice=stopLossPrice, noUpdate=noUpdate, plot=plot)
            self.qq.main(mode=mode, pair=pair, granularity=granularity, iterations=iterations, alpha=alpha, risk=risk, stopLossPrice=stopLossPrice, noUpdate=noUpdate, showPlot=plot)

            #self.qq.oq.getPairsRelatedToOandaTickers(pair.replace('_',''))
            self.qq.predict(wlen=50)
        
        def generateNDayForecast(self):
            ''
    
trader = QsTrader()
forecaster = QsForecaster()

def do_work( forever = True):
    while True:
        try:
            forecaster.getMachineLearning()
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print "*** print_tb:"
            traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
            print "*** print_exception:"
            traceback.print_exception(exc_type, exc_value, exc_traceback,
                                      limit=2, file=sys.stdout)

def do_work_debug( forever = True):
    while True:
        forecaster.getMachineLearning()

def main():
    trader.start()

def test():
    trader.gotoMarket()

if __name__ == "__main__":
    #main()
    #test()

    #do_work( True)
    do_work_debug( True)
