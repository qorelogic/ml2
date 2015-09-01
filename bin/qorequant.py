
import sys
try: sys.path.index('/ml.dev/lib/oanda/oandapy')
except: sys.path.append('/ml.dev/lib/oanda/oandapy')

#from numpy import *
from numpy import divide as n_divide
from numpy import float16 as n_float16
from numpy import rint as n_rint
from numpy import c_ as n_c_
from numpy import min as n_min
from numpy import max as n_max
from numpy import tanh as n_tanh
from numpy import concatenate as n_concatenate

import plotly.plotly as py
from plotly.graph_objs import *

import os, sys, oandapy
import datetime as dd
from matplotlib.pyplot import plot, legend, title, show, imshow, tight_layout
from pylab import rcParams
from IPython.display import display, clear_output
import ujson as j

from qore import *
from qore_qstk import *
from oandaq import OandaQ
from matplotlib.pylab import *

import numpy as n
import pandas as p
import Quandl as q
import datetime as dd
import urllib2 as u
import html2text
import exceptions as ex
import re, sys
import StringIO as sio
import threading,time
import itertools as it

import oandapy

# -*- coding: utf-8 -*-
"""Example Google style docstrings.

This module demonstrates documentation as specified by the `Google Python
Style Guide`_. Docstrings may extend over multiple lines. Sections are created
with a section header and a colon followed by a block of indented text.

Example:
  Examples can be given using either the ``Example`` or ``Examples``
  sections. Sections support any reStructuredText formatting, including
  literal blocks::

      $ python example_google.py

Section breaks are created by simply resuming unindented text. Section breaks
are also implicitly created anytime a new section starts.

Attributes:
  module_level_variable (int): Module level variables may be documented in
    either the ``Attributes`` section of the module docstring, or in an
    inline docstring immediately following the variable.

    Either form is acceptable, but the two should not be mixed. Choose
    one convention to document module level variables and be consistent
    with it.

.. _Google Python Style Guide:
   http://google-styleguide.googlecode.com/svn/trunk/pyguide.html

"""
class QoreQuant():

    configfile       = '/mldev/bin/datafeeds/config.csv'
    quandlAuthtoken  = "WVsyCxwHeYZZyhf5RHs2"
        
    def setVerbose(self, verbose=False):
        self.verbose = verbose
        self.oq.verbose = self.verbose
        
    def __init__(self, verbose=False):

        self.thetaDir         = '/mldev/bin/data/oanda/qorequant'
        self.hdirDatapipeline = '/mldev/lib/crawlers/finance/dataPipeline.scrapy'

        self.qd = QoreDebug()
        self.qd._getMethod()

        self.verbose = verbose

        co = p.read_csv(self.configfile, header=None)
        
        env1=co.ix[0,1]
        access_token1=co.ix[0,2]
        self.oanda1 = oandapy.API(environment=env1, access_token=access_token1)
        
        env2=co.ix[1,1]
        access_token2=co.ix[1,2]
        self.oanda2 = oandapy.API(environment=env2, access_token=access_token2)
        
        self.accid1 = self.oanda1.get_accounts()['accounts'][6]['accountId']
        self.accid2 = self.oanda2.get_accounts()['accounts'][0]['accountId']

        #print 'using account: {0}'.format(self.accid1)
        
        #from selenium import webdriver
        #driver = webdriver.Chrome()
        self.et = Etoro()
        
        self.sw = StatWing(thetaDir=self.thetaDir)

        try:    self.oq = OandaQ(verbose=self.verbose)
        except Exception as e:
            print e
            print 'offline mode'
        
        self.dfdata = None
        
    def synchonizeTrades(self, dryrun=True):
        self.qd._getMethod()
        
        # send to market works
        username = 'manapana'
        save = True
        mode = 2
        try: print self.et.getEtoroTraderPositions(username, save=save, mode=mode)
        except Exception as e:
            print e
            print self.et.getEtoroTraderPositions('manapana', save=save, mode=mode)
        targetPortfolio2 = self.prepTargetPortfolio()
        df = self.generateTargetPortfolio(targetPortfolio2)
        df0 = self.prepSendToMarket(df)
        self.sendToMarket(df0, dryrun=dryrun)
        #self.et.etoroLogout()
        #self.et.quit()
    
    """
    targetPortfolio = [['AAPL', 'BAC', 'BOA', 'DAL'], [1032, 123, 98, 9812]]
    livePortfolio = [['AAPL', 'BAC', 'BOA', 'DAL'], [930, 230, 109, 2130]]
    """
    def toTrade(self, livePortfolio, targetPortfolio, returnList=False):
        self.qd._getMethod()
        
        print 'target portfolio'
        print targetPortfolio
        if type(targetPortfolio) != type(p.DataFrame([])):
            targetPortfolio = p.DataFrame(targetPortfolio).transpose()
        #print type(targetPortfolio)
        print 'live portfolio'
        print livePortfolio    
        if type(livePortfolio) != type(p.DataFrame([])):
            livePortfolio = p.DataFrame(livePortfolio).transpose()
        #print type(livePortfolio)
        
        print 'to trade'
        tt = p.DataFrame([list(targetPortfolio.ix[:,0].get_values()), list((targetPortfolio.ix[:,1] - livePortfolio.ix[:,1]).get_values())]).transpose()
        if returnList == True:
            [list(tt.transpose().get_values()[0]), list(tt.transpose().get_values()[1])]    
        else:
            return tt    
    #assert toTrade([['AAPL', 'BAC', 'BOA', 'DAL'], [930, 230, 109, 2130]], [['AAPL', 'BAC', 'BOA', 'DAL'], [1032, 123, 98, 9812]], returnList=True) == [['AAPL', 'BAC', 'BOA', 'DAL'], [102, -107, -11, 7682]]

    def getMeanPrice(self, instrument):
        self.qd._getMethod()
        
        pr0 = self.oanda1.get_prices(instruments=[instrument])['prices'][0]
        return n.mean([pr0['ask'], pr0['bid']])
    
    def prepTargetPortfolio(self):        
        self.qd._getMethod()
        
        """
        test
        """
        tarp = self.et.getTargetPortfolio('manapana')
        # source: http://pandas.pydata.org/pandas-docs/dev/indexing.html#the-where-method-and-masking
        #tarp = tarp.query('username == "noasnoas"')
        #print tarp
        tarp2 = [list(n.array(tarp.ix[:,'pair'].get_values(), dtype=str)), list(n.array(tarp.ix[:,'amount'].get_values(), dtype=str))]
        #print tarp
        #tarp = p.DataFrame(tarp).transpose()
        
        balance = 200
        
        # oanda account info
        self.accid1 = self.oanda1.get_accounts()['accounts'][6]['accountId']
        self.accid2 = self.oanda2.get_accounts()['accounts'][0]['accountId']
        self.balance1 = self.oanda1.get_account(self.accid1)['balance']
        self.balance2 = self.oanda2.get_account(self.accid2)['balance']
        
        for i in range(0,len(tarp.ix[:,1])):
            tarp.ix[i,'amount'] = float(str(tarp.ix[i,'amount']).replace('$', ''))
            #try:
            # infere leverage of the trade
            openp = float(tarp.ix[i,'open'])
            currentp = self.getMeanPrice(tarp.ix[i,'pair'].replace('/','_'))
            amount = float(tarp.ix[i,'amount'])
            gain = float(tarp.ix[i,'gain'].replace('$', ''))
            tarp.ix[i,'leverage'] = abs(floor((gain/(openp-currentp))/amount / 25)) * 25
            tarp.ix[i,'units0'] = amount * tarp.ix[i,'leverage']
            #except Exception as e:
            #    ''
            
            #tarp.ix[i,2] = float(str(tarp.ix[i,1])) / balance
            tarp.ix[i,'instrument'] = tarp.ix[i,'pair'].replace('/', '_')
            tarp.ix[i,'risk0'] = float(str(tarp.ix[i,'amount'])) * tarp.ix[i,'leverage'] / balance * 100
            tarp.ix[i,'risk1'] = ceil(float(str(tarp.ix[i,'risk0'])) / 100 * self.balance1)
            tarp.ix[i,'risk2'] = ceil(float(str(tarp.ix[i,'risk0'])) / 100 * self.balance2)
        print tarp
        #print
        targetPortfolio1 = tarp.ix[:,['instrument','bias','risk1','take_profit','stop_loss']]
        targetPortfolio2 = tarp.ix[:,['instrument','bias','risk2','take_profit','stop_loss']]
        
        #print "Account: {0}".format(self.accid1)
        #print targetPortfolio1
        #print
        #print "Account: {0}".format(self.accid2)
        #print targetPortfolio2
        
        return targetPortfolio2
    
    
    def generateTargetPortfolio(self, targetPortfolio2):
        self.qd._getMethod()
        
        #print "Account: {0}".format(self.accid1); print targetPortfolio1; print
        print "Account: {0}".format(self.accid2); #print targetPortfolio2; print
        targetPortfolio2.ix[:,'take_profit'] = n.array(targetPortfolio2.ix[:,'take_profit'], dtype=float)
        targetPortfolio2.ix[:,'stop_loss']   = n.array(targetPortfolio2.ix[:,'stop_loss'],   dtype=float)
        targetPortfolio2 = polarizePortfolio(targetPortfolio2, 'risk2', 'amount', 'bias')
        
        # group positions by aggregate pairs
        # 
        # source: http://pandas.pydata.org/pandas-docs/dev/reshaping.html
        #print df.stack() #.groupby(level=1, axis=2)
        # source: http://bconnelly.net/2013/10/summarizing-data-in-python-with-pandas/
        df = targetPortfolio2.groupby('instrument')
        d0 = df['amount'].aggregate(n.sum)
        d1 = df['take_profit'].aggregate(n.mean)
        d2 = df['stop_loss'].aggregate(n.mean)
        print
        #print df.describe()
        df = p.DataFrame([d0, d1, d2]).transpose()
        return p.DataFrame(df)
        

    def prepSendToMarket(self, df):
        self.qd._getMethod()
        
        df2 = self.oanda2.get_positions(self.accid2)
        df2 = p.DataFrame(df2['positions']).sort('instrument', ascending=True).ix[:,['instrument','side','units']]
        polarizePortfolio(df2, 'units', 'amount', 'side')
        
        df2 = df2.set_index('instrument').ix[:,['amount']] 
        df2 = df2.convert_objects(convert_numeric=True)
        df1 = df.ix[:,['amount']]
        #print df1
        #print
        #print df2
        #print type(df)
        #print type(df2)
        df0 =  df1 - df2
        #print df0
        #print df
        df0 = df0.combine_first(df)
        return df0

    def sendToMarket(self, df, dryrun=True):
        self.qd._getMethod()
        
        #pp0 = list(df.ix[:,'instrument'].get_values())
        #pp1 = list(df.ix[:,'amount'].get_values())
        #print pp0;
        #print pp1; print
        
        #print df
        #print df.index
        #print
        
        for i in df.index:
            dfi = df.ix[i,:]
            instrument = i
            amount     = int(ceil(n.abs(dfi['amount'])))
            if dfi['amount'] > 0:
                side = 'buy'
            elif dfi['amount'] < 0:
                side = 'sell'
            
            # send order to market
            #"""
            #instrument:* Required Instrument to open the order on.
            #units: Required The number of units to open order for.
            #side: Required Direction of the order, either 'buy' or 'sell'.
            #type: Required The type of the order 'limit', 'stop', 'marketIfTouched' or 'market'.
            #expiry: Required If order type is 'limit', 'stop', or 'marketIfTouched'. The order expiration time in UTC. The value specified must be in a valid datetime format.
            #price: Required If order type is 'limit', 'stop', or 
            #"""
            if amount > 0:
                print "order = self.oanda2.create_order({0}, type='market', instrument='{1}', side='{2}', units='{3}')".format(self.accid2, instrument, side, amount)
                if dryrun == False:
                    order = self.oanda2.create_order(self.accid2, type='market', instrument=instrument, side=side, units=amount)
            else:
                print 'Nothing to trade on {0}.'.format(i)
        print
        
    def updateDatasets(self, code, noUpdate=False):
        self.qd._getMethod()

        #self.da = getDataAUD(noUpdate=noUpdate)
        #self.dg = getDataGBP(noUpdate=noUpdate)
        #self.dj = getDataJPY(noUpdate=noUpdate)
        #self.db = getDataBitcoin(noUpdate=noUpdate)
        
        if code == 'EUR':
            self.de = getDatasetEUR(noUpdate=noUpdate)
            return self.de
        if code == 'USD':
            self.du = getDataJPY(noUpdate=noUpdate)
            return self.du
        
    def setDfData(self, dfdata):
        self.qd._getMethod()
        
        self.dfdata = dfdata
    
    def update(self, pair='EURUSD', granularity = None, noUpdate=False, plot=False):
        self.qd._getMethod()
        
        # update from data the source
        #self.granularityMap.keys()
        if granularity == None:
            self.oq.updateBarsFromOanda(pair=pair, granularities=' '.join(['D','H4','H1','M30','M15','M5','M1','S5','M','W']), plot=plot, noUpdate=noUpdate)
        else:
            self.oq.updateBarsFromOanda(pair=pair, granularities=' '.join([granularity]), plot=plot, noUpdate=noUpdate)
        self.setDfData(self.oq.prepareDfData(self.oq.dfa).bfill().ffill())
    
    def main(self, mode=1, pair='EUR_USD', granularity='H4', iterations=200, alpha=0.09, risk=1, stopLossPrice=None, noUpdate=False, showPlot=True):
        self.qd._getMethod()
        
        self.pair              = pair
        self.sw.pair           = pair
        self.sw.ml.pair        = pair
        
        self.granularity       = granularity
        self.sw.granularity    = granularity
        self.sw.ml.granularity = granularity
        
        #modes = ['train','predict','trade']
        #alpha = 0.09 # 0.3
        
        modes = ['train','predict','trade']
        mstop = None
        if stopLossPrice != None:
            mstop = self.oq.calculateStopLossFromPrice(pair, stopLossPrice)        
        
        self.update(pair=pair, granularity=granularity, noUpdate=noUpdate, plot=plot)
    
        if modes[mode] == 'train':
            mmode = 2
        if modes[mode] == 'predict':
            mmode = 3
        if modes[mode] == 'trade':
            mmode = 4
        try:
            self.forecastCurrency(mode=mmode, pair=pair, iterations=iterations, alpha=alpha, risk=risk, stop=mstop, granularity=granularity, showPlot=showPlot)
            #print self.oq.granularities[0]
        except KeyboardInterrupt, e:
            # save the theta state on keyboard interrupt (stop button)
            self.saveTheta(self.sw.ml.iter, pair=pair.replace('_', ''), granularity=granularity)
        
        if modes[mode] == 'train':
            self.forecastCurrency(mode=3, pair=pair, iterations=iterations, alpha=alpha, risk=risk, stop=mstop, granularity=granularity, showPlot=showPlot)
        
    def train(self, pair='EURUSD', iterations=10000, alpha=0.09, noUpdate=False, granularity='H4', showPlot=False):
        self.qd._getMethod()
        
        #pair = 'EURGBP'
        #pair = 'EURCHF'
        
        self.sw.keyCol = 'BNP.'+pair+' - '+pair[0:3]+'/'+pair[3:6]+'_x'
        
        #if type(self.dfdata) == type(None):
        #    self.dfdata = self.updateDatasets(pair[0:3], noUpdate=noUpdate)        
        self.update(pair=pair, granularity=granularity, noUpdate=noUpdate)

        #self.sw.relatedCols = [0, 1,2,3,6,9,8,5]
        #self.sw.relatedCols = [0, 1,2,3,6,8,5, 7,9,10,11,12,13,14,16,17]
        self.sw.relatedCols = self.sw.oq.generateRelatedColsFromOandaTickers(self.dfdata, pair)
        #self.sw.relatedCols = [0,1, 2, 3, 4, 5, 6, 7, 8, 13, 19]
        
        #
        #self.sw.relatedCols = range(1, 98)
        #self.sw.relatedCols = data.columns
        #self.sw.relatedCols = [0,1]
        
        #print self.dfdata.columns
        
        self.df = self.dfdata.ix[0:len(self.dfdata)-0, :].fillna(0)
        X = self.df.ix[0:len(self.df)]
        # shift keyCol up ct cells
        #ct = 5
        #dfb = p.DataFrame(index=self.df.ix[0:len(self.df)-ct, 0].index)
        #dfb['a'] = self.df.ix[0:len(self.df)-ct, 0].get_values()
        #dfb['b'] = self.df.ix[ct:len(self.df), 0].get_values()
        #self.df.ix[:,0] = dfb['b']
        
        #print self.df
        y = self.df.ix[:, self.sw.keyCol].fillna(0)
        
        # shift to next bar close
        #y = list(self.sw.higherNextDay(y, self.sw.keyCol).get_values()); y.append(0)
        #y = list(self.sw.nextBar(self.df, self.sw.keyCol).get_values()); #y.append(0)
        #print self.df

        barsForward = (13-6)*6
        barsForward = 1
        y = list(self.sw.nextBar(self.df, self.sw.keyCol, barsForward=barsForward))
        self.df = self.df.ix[0:len(self.df)-barsForward,:]

        #self.df['y'] = y        
        #print p.DataFrame(self.df.ix[:,[self.sw.keyCol, 'y']])
        #import sys
        
        y = n.array(y)
        #print p.DataFrame(y)
        print y.shape
        
        self.loadTheta(iterations, pair=pair, granularity=granularity)
        
        self.sw.regression2(X=self.df.ix[0:len(self.df), :], y=y, iterations=iterations, alpha=alpha, initialTheta=self.sw.theta, viewProgress=False, showPlot=showPlot)
        
        self.saveTheta(self.sw.ml.iter, pair=pair, granularity=granularity)
        
    def loadTheta(self, iterations, pair='EURUSD', granularity='H4'):
        self.qd._getMethod()
        fname = self.thetaDir+'/{0}-{1}.theta.csv'.format(pair, granularity)
        print fname
        iter  = 0
        
        try:
            self.df0 = p.read_csv(fname, index_col=0)
            #print self.df0#.get_values()
            #print 'self.df0 load'
            #print 'loadtheta iterations:{0}'.format(iterations)
            #print self.df0.index < iterations
            #print self.df0.index#[self.df0.index < iterations]
            try:
                iter = max(self.df0.index[self.df0.index < iterations])
                #print 'iter:{0}'.format(iter)
            except:
                iter = max(self.df0.index)
                #print 'last iteration:{0}'.format(iter)
            #print iterations - iter    
            initialTheta = self.df0.ix[iter, :]#.get_values()
            #print 'loaded initialTheta: {0}'.format(initialTheta.get_values())
        except Exception as e:
            print e
            self.df0 = p.DataFrame()
            initialTheta = None
            
        self.sw.theta = initialTheta
        self.sw.ml.theta = initialTheta
        self.sw.ml.initialIter = iter
        self.sw.ml.iter = iter
        #print self.sw.ml.initialIter
        #print self.sw.theta
        try: print len(self.sw.theta)
        except Exception as e:
            print e
   
    def saveTheta(self, iterations, pair='EURUSD', granularity='H4'):
        self.qd._getMethod()
        
        print 'saving theta @ {0} iterations {1}-{2}'.format(self.sw.ml.iter, pair, granularity)
        #print list(self.df.columns)
        #print 
        #print 
        #print len(list(self.dfdata.columns))
        
        fname = self.thetaDir+'/{0}-{1}.theta.csv'.format(pair, granularity)
        print fname
        
        mkdir_p(self.thetaDir)
        try:
            self.df0 = p.read_csv(fname, index_col=0)
            #print self.df0
        except Exception as e:
            print e
            self.df0 = p.DataFrame()
        print len(self.df0)
        #print self.sw.ml.theta.get_values()
        try:    theta = self.sw.ml.theta.get_values()
        except: theta = self.sw.ml.theta
        df = p.DataFrame(theta, index=list(self.dfdata.columns), columns=[self.sw.ml.iter]).transpose()
        #print df.ix[self.sw.ml.iter, :]#.get_values()
        #print self.sw.ml.theta
        
        df = df.combine_first(self.df0)
        #print df
        print df.transpose()
        print 'save theta'
        
        if self.verbose == True: df.plot(legend=None, title='{0} {1} theta progression'.format(pair, granularity)); show();
        df.to_csv(fname)        
    
    def predict(self, plotTitle='', wlen=2000, showPlot=True):
        self.qd._getMethod()
        
        data = self.df
        #self.sw.predictRegression2(mdf.ix[0:ldf-0, :], quiet=True)
        ldf = len(data.ix[:, self.sw.keyCol])
        
        """
        try:
            nprices = getPricesLatest(data, trueprices=True)
            data.ix[p.tslib.Timestamp('2015-06-10').date(), self.sw.relatedCols] = list(nprices.transpose().ix[0,:])
            #print data.ix[p.tslib.Timestamp('2015-06-10'), self.sw.relatedCols]
            #print data
            print nprices
        except Exception as e:
            print e
        """
        mdf = data
        #[mdf, dmean, dstd] = normalizeme(data, pinv=True)
        #tp = sw.predictRegression2(mdf.ix[0:ldf-i, :], quiet=False)
        tp = p.DataFrame(self.sw.predictRegression2(mdf.ix[:, :], quiet=True), index=data.index)
        #plot(self.de.ix[ldf-wlen: ldf, self.sw.keyCol])
        if self.verbose == True or showPlot == True: 
            plot(data.ix[ldf-wlen: ldf, self.sw.keyCol])
            plot(tp.ix[ldf-wlen: ldf, :], '.')
            legend(['price', 'tp'])
            title(plotTitle)
            show();
        #normalizemePinv(, dmean, dstd)
        return tp.ix[len(tp)-1:len(tp)-0, :]
    
    def tradePrediction(self, pair, tp, risk=1, stop=40):
        self.qd._getMethod()

        print pair
        pair = pair.replace('_','')
        print pair
        pair = pair[0:3]+'_'+pair[3:6]
        print pair
        eu =  self.oq.oanda2.get_prices(instruments=pair)['prices']
        
        curr1 = n.mean([float(eu[0]['ask']), float(eu[0]['bid'])])
        tp1 = float('%.5f' % tp.ix[len(tp)-1,0])
        print 'current: {0}'.format(curr1)
        print 'tp1: {0}'.format(tp1)
        if tp1 > curr1:
            self.oq.trade(risk, stop, pair, 'b', tp=tp1)
        if tp1 < curr1:
            self.oq.trade(risk, stop, pair, 's', tp=tp1)
    
    def forecastCurrency(self, mode=3, pair='EURUSD', granularity='H4', iterations=10000, alpha=0.09, risk=5, stop=20, showPlot=True):
        self.qd._getMethod()
        
        # 1: update 2: train, 3: predict, 4: trade
        print 'forecastCurrency: {0} {1}'.format(pair, granularity)  
        
        onErrorTrain = False # onErrorTrain swich
        pair = pair.replace('_', '') # remove the underscore
        
        try:    
            self.df
        except Exception as e:
            print e 
            onErrorTrain = True
        
        if mode == 1:
            self.updateDatasets('EUR', noUpdate=False)
            
        if mode == 2 or (onErrorTrain == True):
            #if mode != 4:
            self.train(pair=pair, iterations=iterations, alpha=alpha, noUpdate=True, granularity=granularity, showPlot=showPlot)
        
        if mode == 2 or mode == 3 or mode == 4:
            tp = self.predict(plotTitle=pair, showPlot=showPlot)
            self.predict(wlen=50, showPlot=showPlot)
            print 'Price forecast for {0} {1}'.format(pair, granularity)
            print p.DataFrame(tp.get_values(), index=self.oq.timestampToDatetimeFormat(self.oq.oandaToTimestamp(list(tp.index))), columns=[pair])
        
        if mode == 4:
            self.tradePrediction(pair, tp, risk=risk, stop=stop)
        

    # volume trades
    # source: http://stackoverflow.com/questions/13728392/moving-average-or-running-mean
    def runningMean(self, x, N):
        self.qd._getMethod()
        
        y = n.zeros((len(x),))
        for ctr in range(len(x)):
             y[ctr] = np.sum(x[ctr:(ctr+N)])
        return y/N
    
    # source: http://stackoverflow.com/questions/13728392/moving-average-or-running-mean
    
    def runningMeanFast(self, x, N):
        self.qd._getMethod()
        
        x = x.transpose().get_values()[0]
        return n.convolve(x, n.ones((N,))/N)[(N-1):]
    
    # visualize multi-pair volume
    def visualizeVolumeMultiPair(self, granularity = 'M30', pairs=[], tailn=400):
        self.qd._getMethod()
        
        df = p.DataFrame()
        period = 20
        #for i in self.oq.dfa:
        for i in pairs:
            #for j in self.oq.dfa[i]:
            #    print '{0} {1}'.format(i,j)
            #print '{0} {1}'.format(i,granularity)
            try:
                nl = '{0}:{1}'.format(i, granularity)
                nlma20 = '{0}:{1}:ma volume'.format(nl, period)
                self.oq.updatePairGranularity(i, granularity, noUpdate=False, plot=False)
                dfi = self.oq.dfa[i][granularity]#.ix[:,['volume']]
                dfi = dfi.sort(ascending=False)
                dfi[nlma20] = self.runningMeanFast(dfi.ix[:,['volume']], period)
                dfi = dfi.sort(ascending=True)
                dfi[nl] = dfi['volume']
                df = df.combine_first(dfi.ix[:,[nl, nlma20]])
            except Exception as e: print e
        df = normalizeme(df)
        df = df.tail(tailn)
        #print df.tail(2).transpose()
        df.plot(title='Multi-pair volume {0}'.format(granularity)).legend(bbox_to_anchor=(1.4, 1));# show();
        
        df = sigmoidme(df)
        #from numpy import tanh as n.tanh
        #df = n.tanh(df)
        df.plot(title='Multi-pair volume {0}'.format(granularity)).legend(bbox_to_anchor=(1.4, 1));# show();

    def vizVolume(self, fper=0, tper=2):
        self.qd._getMethod()
        
        for i in xrange(fper, tper+1):
            self.visualizeVolumeMultiPair(granularity=self.granularities[i], pairs=self.pairs)
            self.sweepChartsConstantGranularity(self.granularities[i], self.pairs, onlyTradedPairs=True)
            #break
        
    def visualizeVolume(self, dff, pair, granularity, tailn=400):
        self.qd._getMethod()
        
        period = 20
        dfa = dff.copy()
        dfa = dfa.sort(ascending=False)
        #dfa['ma {0} volume'.format(period)] = self.runningMean(dfa.ix[:,['volume']], period)
        dfa['ma {0} volume'.format(period)] = self.runningMeanFast(dfa.ix[:,['volume']], period)
        dfa['wqe'] = dfa.ix[:,'volume'] / dfa.ix[:, 'ma {0} volume'.format(period)]
        dfa = dfa.sort(ascending=True)
        
        dfa = normalizeme(dfa)
        dfa = sigmoidme(dfa)
        dfa = dfa.ix[20:, :].tail(tailn)
        #dfa.plot(title='{0} {1}'.format(pair, granularity)).legend(loc=2);
        dfa.plot(title='{0} {1}'.format(pair, granularity)).legend(bbox_to_anchor=(1.3, 1));
       
        #trade = raw_input('trade?: ')
        #trade
        
        #print dfa
    
    def sweepCharts(self, pair=None, granularity=None):
        self.qd._getMethod()
        
        #if pair == None:
           
        #df = self.oanda2.get_history(instrument=pair, count=count, granularity=granularity)
        #break
        #dff = p.DataFrame(df['candles'])
        dff = self.oq.updatePairGranularity(pair, granularity, noUpdate=False, plot=False)
        #return
        dff = dff.ix[:, 'closeAsk closeBid volume'.split(' ')]
        #print dff.tail(5)
        #dff = normalizeme(dff)
        #dff = sigmoidme(dff)
        #dff.plot(); show()
        self.visualizeVolume(dff, pair, granularity)
        #print dff
        #break
    
    def sweepChartsConstantPair(self):
        self.qd._getMethod()
        
        # contant pair, variable granularity
        pair = pairs[0]
        for granularity in granularities:
            #try:
            sweepCharts(pair=pair, granularity=granularity)
            #except: ''
    
    def sweepChartsConstantGranularity(self, granularity, pairs, onlyTradedPairs=False):
        self.qd._getMethod()
        
        # constant granularity, variable pair
        #granularity = granularities[5]
        opairs = pairs
        
        # view only pairs with open positions
        if onlyTradedPairs == True:
            try:
                pairs = list(p.DataFrame(self.oq.oanda2.get_positions(self.oq.aid)['positions']).ix[:,'instrument'].get_values())
            except:
                pairs = opairs
        
        for pair in pairs:
            try:    
                self.sweepCharts(pair=pair, granularity=granularity)
            except: ''
            #break

    def returnTraining(self, fname, showPlot=False):
        df = p.read_csv(fname, header=None)
        #print df.columns
        df = df.ix[:,[2,3,4]]
        #df.ix[:,[2]].plot()
        #df.ix[:,[3]].plot()
        #df.ix[:,[4]].plot()
        #print df
        #if showPlot == True: plt.scatter(df.ix[:,[3]], df.ix[:,[4]]); plt.show();
        if showPlot == True: df.ix[:,[4]].plot(); plt.show();
        #if showPlot == True: df.ix[:,[3,4]].plot(); plt.show();
        
        dfp = df
        df = normalizeme(df)
        #if showPlot == True: plt.scatter(df.ix[:,[3]], df.ix[:,[4]]); plt.show();
        #if showPlot == True: df.plot(); plt.show();
    
        df = sigmoidme(df)
        #if showPlot == True: plt.scatter(df.ix[:,[3]], df.ix[:,[4]]); plt.show();
        if showPlot == True: df.plot(); plt.show();
        #print dfp
        return dfp
    
    def viewTraining(self, pair, gran):
        #hdir = '/home/qore2/data-oanda/qorequant'
        hdir = '/ml.dev/bin/data/oanda/qorequant'
        fname = hdir+'/{0}-{1}.train.csv'.format(pair, gran)
        #print fname
        df = self.returnTraining(fname)
        dfn = df.ix[:,[3,4]]
        dfn = dfn.set_index(3).sort(ascending=False).tail(50)
        forecastPrice = list(dfn.tail(1).get_values())[0][0]
        #print '{0} {1} {2} {3}'.format(pair, gran, len(df), forecastPrice)
        columns = 'pair timeframe iterations forecast'.split(' ')
        manifest = p.DataFrame([pair, gran, len(df), forecastPrice], index=columns).transpose()
        #title('{0} {1} Forecast'.format(pair, gran))
        #dfn = normalizeme(dfn)
        #dfn = sigmoidme(dfn)
        #plot(dfn);
        #scatter(dfn.ix[:,3], dfn.ix[:,4])
        #legend(list(dfn.columns))
        #legend([df1.columns, df2.columns])
        #show();
        #print len(df)
        return [dfn, manifest]
    
    def showLevels(self):
        """
        merges all granularity forecasts onto a single plot
        """

        pa = 'EUR_USD GBP_USD AUD_USD USD_CAD USD_CHF NZD_USD'.split(' ')
        gr = 'D H4 H1 M30 M15'.split(' ')
        for i in xrange(len(pa)):
            dfs = p.DataFrame()
            for j in xrange(len(gr)):
                try:
                    training = self.viewTraining(pa[i], gr[j])
                    df = training[0]
                    manifest = training[1]
                    dfs = dfs.combine_first(manifest.set_index('timeframe'))
                    plot(df.get_values())
                except: 
                    ''
            try:
                dfs['timeframe'] = dfs.index # save the lost field before calling set_index()
                print dfs.set_index('forecast').sort(ascending=False)
            except: ''
            dfp = p.read_csv('/ml.dev/bin/data/oanda/ticks/{0}/{0}-M5.csv'.format(pa[i])).sort(ascending=True).tail(50).ix[:,'closeAsk']
            plot(dfp)
            title('{0} Forecast'.format(pa[i]))
            legend(gr)
            show();
            #break

    def analyseInvestingTechnical(self, showPlot=True):
        
        import ujson as j
        
        fname = self.hdirDatapipeline+'/investingTechnical_numbeo.csv'
        df = p.read_csv(fname)
        #print df.sort(['name','period'])
    
        #di = {'strong sell':0, 'sell':1, 'neutral':2, 'buy':3, 'strong buy':4}
        di = {'strong sell':-2, 'sell':-1, 'neutral':0, 'buy':1, 'strong buy':2}
        df['summaryCode'] = df['summary']
        li = list(df.ix[:,'summary'])
        for i in xrange(len(li)): df.ix[i,'summaryCode'] = di[li[i].lower()]
        sdf = df.pivot('name', 'period', 'summaryCode').transpose()
        #print sdf
        sdf = j.dumps(sdf.fillna(0).to_dict())
        #print repr(sdf)
        cdate = os.path.getctime(fname)
        fp = open(self.hdirDatapipeline+'/investingTechnical_numbeo.csv.log', 'a')
        fp.write('{0},{1}\n'.format(cdate,sdf))
        fp.close()
    
        dfa = df.set_index('name').ix[:,['period','summaryCode']]
        #dfa = normalizeme(dfa)
        #dfa = sigmoidme(dfa)
        #print dfa
        #if showPlot == True: scatter(dfa['period'], dfa['summaryCode']); show();
        #if showPlot == True: .plot(style='-'); show();
    
        dfs = df.pivot('name', 'period', 'summaryCode').transpose()
        nm = n.array(dfs, dtype=n.float16)
        #print nm
        header = n.concatenate([list(dfs.columns), n.sum(nm, 0)])
        print 
        header = p.DataFrame(header.reshape(2, header.shape[0] / 2)).transpose().set_index(0).transpose()
        print header
        if showPlot == True: 
            imshow(n.array(dfs, dtype=n.float16), extent=[1,7,1,9], aspect=0.517)
            #title('Manually Set Aspect')
            tight_layout()
            show()
    
        headerT = header.transpose()
        headerT[1] = n.array(headerT[1], dtype=n.float16)
        rcParams['figure.figsize'] = 7.8, 5
        #headerT = normalizeme(headerT)
        #headerT = n.tanh(headerT)
        if showPlot == True: 
            headerT.plot(); show()
        
        return header
        
if __name__ == "__main__":
    print 'stub'
