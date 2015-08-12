
#from numpy import *
from qore import readcache, writecache, mkdir_p, QoreDebug
from pandas import read_csv as p_read_csv
from pandas import DataFrame as p_DataFrame
from pandas import Series as p_Series
from numpy import array as n_array
from numpy import sum as n_sum
from numpy import power as n_power
from numpy import mean as n_mean
from numpy import convolve as n_convolve
from numpy import std as n_std
from numpy import e as n_e
from numpy import log10 as n_log10
from numpy import ones as n_ones
from numpy import zeros as n_zeros
from numpy import ceil
from numpy import dot as n_dot
from numpy import divide as n_divide
from numpy import float16 as n_float16

import sys, oandapy
import datetime as dd
from matplotlib.pyplot import plot, legend, title, show
from IPython.display import display, clear_output

"""
from qore import *
from qore_qstk import *
from matplotlib.pylab import *

import numpy as n
import pandas as p
import Quandl as q
import datetime as dd
import urllib2 as u
import json as j
import html2text
import exceptions as ex
import re, sys
import StringIO as sio
import threading,time
import itertools as it


from IPython.display import display, clear_output
import time
import math

import plotly.plotly as py
from plotly.graph_objs import *

from selenium import webdriver
from selenium.selenium import selenium
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
import pandas as p
"""

def toCurrency(n):
    return '%2d' % n

"""
Created on Thu Nov 13 21:52:25 2014

@author: qore2
"""


class Selenium:

    def scrollToBottom(driver):
        # scroll to bottom of page
        # todo: go into loop until it reaches the end of the list
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
        #driver.execute_script("return window.screenTop;")
    
    def test():
        # Select the Python language option
        python_link = driver.find_elements_by_xpath('//*[@id="open-trades-holder"]/div[2]/div/div/div[1]/div[3]/div[1]/div/div/div[1]/div/a')[0]
        python_link.click()
        
        # Enter some text!
        text_area = driver.find_element_by_id('textarea')
        text_area.send_keys("print 'Hello,' + ' World!'")
        
        # Submit the form!
        submit_button = driver.find_element_by_name('submit')
        submit_button.click()
        
        # Make this an actual test. Isn't Python beautiful?
        #assert "Hello, World!" in driver.get_page_source()
        xp = '/html/body/div/table/tbody/tr/td/div[2]/table/tbody/tr/td[2]/div/pre'
        assert "Hello, World!" in driver.find_element_by_xpath(xp).text
        
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
        self.qd = QoreDebug()
        self.qd._getMethod()

        self.verbose = verbose

        co = p_read_csv(self.configfile, header=None)
        
        #env1=co.ix[0,1]
        #access_token1=co.ix[0,2]
        #self.oanda1 = oandapy.API(environment=env1, access_token=access_token1)
        
        env2=co.ix[1,1]
        access_token2=co.ix[1,2]
        self.oanda2 = oandapy.API(environment=env2, access_token=access_token2)
        
        #self.accid1 = self.oanda1.get_accounts()['accounts'][6]['accountId']
        #self.accid2 = self.oanda2.get_accounts()['accounts'][0]['accountId']

        #print 'using account: {0}'.format(self.accid1)
        
        #from selenium import webdriver
        #driver = webdriver.Chrome()
        self.et = Etoro()
        
        self.sw = StatWing()

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
        if type(targetPortfolio) != type(p_DataFrame([])):
            targetPortfolio = p_DataFrame(targetPortfolio).transpose()
        #print type(targetPortfolio)
        print 'live portfolio'
        print livePortfolio    
        if type(livePortfolio) != type(p_DataFrame([])):
            livePortfolio = p_DataFrame(livePortfolio).transpose()
        #print type(livePortfolio)
        
        print 'to trade'
        tt = p_DataFrame([list(targetPortfolio.ix[:,0].get_values()), list((targetPortfolio.ix[:,1] - livePortfolio.ix[:,1]).get_values())]).transpose()
        if returnList == True:
            [list(tt.transpose().get_values()[0]), list(tt.transpose().get_values()[1])]    
        else:
            return tt    
    #assert toTrade([['AAPL', 'BAC', 'BOA', 'DAL'], [930, 230, 109, 2130]], [['AAPL', 'BAC', 'BOA', 'DAL'], [1032, 123, 98, 9812]], returnList=True) == [['AAPL', 'BAC', 'BOA', 'DAL'], [102, -107, -11, 7682]]

    def getMeanPrice(self, instrument):
        self.qd._getMethod()
        
        pr0 = self.oanda1.get_prices(instruments=[instrument])['prices'][0]
        return n_mean([pr0['ask'], pr0['bid']])
    
    def prepTargetPortfolio(self):        
        self.qd._getMethod()
        
        """
        test
        """
        tarp = self.et.getTargetPortfolio('manapana')
        # source: http://pandas.pydata.org/pandas-docs/dev/indexing.html#the-where-method-and-masking
        #tarp = tarp.query('username == "noasnoas"')
        #print tarp
        tarp2 = [list(n_array(tarp.ix[:,'pair'].get_values(), dtype=str)), list(n_array(tarp.ix[:,'amount'].get_values(), dtype=str))]
        #print tarp
        #tarp = p_DataFrame(tarp).transpose()
        
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
        targetPortfolio2.ix[:,'take_profit'] = n_array(targetPortfolio2.ix[:,'take_profit'], dtype=float)
        targetPortfolio2.ix[:,'stop_loss']   = n_array(targetPortfolio2.ix[:,'stop_loss'],   dtype=float)
        targetPortfolio2 = polarizePortfolio(targetPortfolio2, 'risk2', 'amount', 'bias')
        
        # group positions by aggregate pairs
        # 
        # source: http://pandas.pydata.org/pandas-docs/dev/reshaping.html
        #print df.stack() #.groupby(level=1, axis=2)
        # source: http://bconnelly.net/2013/10/summarizing-data-in-python-with-pandas/
        df = targetPortfolio2.groupby('instrument')
        d0 = df['amount'].aggregate(n_sum)
        d1 = df['take_profit'].aggregate(n_mean)
        d2 = df['stop_loss'].aggregate(n_mean)
        print
        #print df.describe()
        df = p_DataFrame([d0, d1, d2]).transpose()
        return p_DataFrame(df)
        

    def prepSendToMarket(self, df):
        self.qd._getMethod()
        
        df2 = self.oanda2.get_positions(self.accid2)
        df2 = p_DataFrame(df2['positions']).sort('instrument', ascending=True).ix[:,['instrument','side','units']]
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
            amount     = int(ceil(n_abs(dfi['amount'])))
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
        #dfb = p_DataFrame(index=self.df.ix[0:len(self.df)-ct, 0].index)
        #dfb['a'] = self.df.ix[0:len(self.df)-ct, 0].get_values()
        #dfb['b'] = self.df.ix[ct:len(self.df), 0].get_values()
        #self.df.ix[:,0] = dfb['b']
        
        #print self.df
        y = self.df.ix[:, self.sw.keyCol].fillna(0)
        
        # shift to next bar close
        #y = list(self.sw.higherNextDay(y, self.sw.keyCol).get_values()); y.append(0)
        #y = list(self.sw.nextBar(self.df, self.sw.keyCol).get_values()); #y.append(0)
        #print self.df

        barsForward = 1
        y = list(self.sw.nextBar(self.df, self.sw.keyCol, barsForward=barsForward))
        self.df = self.df.ix[0:len(self.df)-barsForward,:]

        #self.df['y'] = y        
        #print p_DataFrame(self.df.ix[:,[self.sw.keyCol, 'y']])
        #import sys
        
        y = n_array(y)
        #print p_DataFrame(y)
        print y.shape
        
        self.loadTheta(iterations, pair=pair, granularity=granularity)
        
        self.sw.regression2(X=self.df.ix[0:len(self.df), :], y=y, iterations=iterations, alpha=alpha, initialTheta=self.sw.theta, viewProgress=False, showPlot=showPlot)
        
        self.saveTheta(self.sw.ml.iter, pair=pair, granularity=granularity)
        
    def loadTheta(self, iterations, pair='EURUSD', granularity='H4'):
        self.qd._getMethod()
    
        hdir  = '/mldev/bin/datafeeds/models/qorequant'
        fname = hdir+'/{0}-{1}.theta.csv'.format(pair, granularity)
        print fname
        iter  = 0
        
        try:
            df0 = p_read_csv(fname, index_col=0)
            #print df0#.get_values()
            print 'df0 load'
            #print df0
            iter = max(df0.index[df0.index < iterations])
            #print iter
            #print iterations - iter    
            initialTheta = df0.ix[iter, :]#.get_values()
            print 'loaded initialTheta..'
        except Exception as e:
            print e
            df0 = p_DataFrame()
            initialTheta = None
            
        self.sw.theta = initialTheta
        self.sw.ml.theta = initialTheta
        self.sw.ml.initialIter = iter
        self.sw.ml.iter = iter
        print self.sw.ml.initialIter
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
        
        hdir = '/mldev/bin/datafeeds/models/qorequant'
        fname = hdir+'/{0}-{1}.theta.csv'.format(pair, granularity)
        print fname
        
        mkdir_p(hdir)
        try:
            df0 = p_read_csv(fname, index_col=0)
            #print df0
        except Exception as e:
            print e
            df0 = p_DataFrame()
        print len(df0)
        #print self.sw.ml.theta.get_values()
        try:    theta = self.sw.ml.theta.get_values()
        except: theta = self.sw.ml.theta
        df = p_DataFrame(theta, index=list(self.dfdata.columns), columns=[self.sw.ml.iter]).transpose()
        #print df.ix[self.sw.ml.iter, :]#.get_values()
        #print self.sw.ml.theta
        
        df = df.combine_first(df0)
        #print df
        print df.transpose()
        print 'save theta'
        
        if self.verbose == True: 
            df.plot(legend=None, title='{0} {1} theta progression'.format(pair, granularity)); 
            show();
        df.to_csv(fname)        
    
    def predict(self, plotTitle='', wlen=2000, showPlot=True):
        self.qd._getMethod()
        
        data = self.df
        #self.sw.predictRegression2(mdf.ix[0:ldf-0, :], quiet=True)
        ldf = len(data.ix[:, self.sw.keyCol])
        
        """
        try:
            nprices = getPricesLatest(data, trueprices=True)
            data.ix[p_tslib.Timestamp('2015-06-10').date(), self.sw.relatedCols] = list(nprices.transpose().ix[0,:])
            #print data.ix[p_tslib.Timestamp('2015-06-10'), self.sw.relatedCols]
            #print data
            print nprices
        except Exception as e:
            print e
        """
        mdf = data
        #[mdf, dmean, dstd] = normalizeme(data, pinv=True)
        #tp = sw.predictRegression2(mdf.ix[0:ldf-i, :], quiet=False)
        tp = p_DataFrame(self.sw.predictRegression2(mdf.ix[:, :], quiet=True), index=data.index)
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
        
        curr1 = n_mean([float(eu[0]['ask']), float(eu[0]['bid'])])
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
            print p_DataFrame(tp.get_values(), index=self.oq.timestampToDatetimeFormat(self.oq.oandaToTimestamp(list(tp.index))), columns=[pair])
        
        if mode == 4:
            self.tradePrediction(pair, tp, risk=risk, stop=stop)
        

    # volume trades
    # source: http://stackoverflow.com/questions/13728392/moving-average-or-running-mean
    def runningMean(self, x, N):
        self.qd._getMethod()
        
        y = n_zeros((len(x),))
        for ctr in range(len(x)):
             y[ctr] = n_sum(x[ctr:(ctr+N)])
        return y/N
    
    # source: http://stackoverflow.com/questions/13728392/moving-average-or-running-mean
    
    def runningMeanFast(self, x, N):
        self.qd._getMethod()
        
        x = x.transpose().get_values()[0]
        return n_convolve(x, n_ones((N,))/N)[(N-1):]
    
    # visualize multi-pair volume
    def visualizeVolumeMultiPair(self, granularity = 'M30', pairs=[], tailn=400):
        self.qd._getMethod()
        
        df = p_DataFrame()
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
        #from numpy import tanh as n_tanh
        #df = n_tanh(df)
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
        #dff = p_DataFrame(df['candles'])
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
                pairs = list(p_DataFrame(self.oq.oanda2.get_positions(self.oq.aid)['positions']).ix[:,'instrument'].get_values())
            except:
                pairs = opairs
        
        for pair in pairs:
            try:    
                self.sweepCharts(pair=pair, granularity=granularity)
            except: ''
            #break


class FinancialModel:
    """The summary line for a class docstring should fit on one line.

    If the class has public attributes, they should be documented here
    in an ``Attributes`` section and follow the same formatting as a
    function's ``Args`` section.

    Attributes:
      attr1 (str): Description of `attr1`.
      attr2 (list of str): Description of `attr2`.
      attr3 (int): Description of `attr3`.

    """    
    def getRateFromProjectedAccruedment(from_capital, to_capital, period):
        """Example of docstring on the __init__ method.

        The __init__ method may be documented in either the class level
        docstring, or as a docstring on the __init__ method itself.

        Either form is acceptable, but the two should not be mixed. Choose one
        convention to document the __init__ method and be consistent with it.

        Note:
          Do not include the `self` parameter in the ``Args`` section.

        Args:
          param1 (str): Description of `param1`.
          param2 (list of str): Description of `param2`. Multiple
            lines are supported.
          param3 (int, optional): Description of `param3`, defaults to 0.

        """
        """
        vc = 100 * pow(1+50.0/100,2)
        vc = 1e9
        print vc
        period = 500
        print period
        """
        return 100 * (pow(float(to_capital)/from_capital, 1.0/period)-1)
    
    def compoundedPercentageIntegral(self, compoundedRate, period_integrals):
        return 100 * (pow(pow(1 + float(compoundedRate) / 100,1), 1 / float(period_integrals)) - 1)
        
    # wrapper for compoundedPercentageIntegral()
    def segmentCompundingPeriod(self, from_rate, intra_periods):
        return compoundedPercentageIntegral(from_rate, intra_periods)
    
    # 50, 1 => 50
    # 50, 2 => 125
    # 50, 3 => 237.5
    def rateToCompoundedPercentage(self, rate, period):
        return 100 * (pow(pow(1 + float(rate) / 100, period),float(1) / 1) - 1)
        
    def compoundVestedCapital(self, rate, period, initial_capital=100, shift=0):
        rate   = n_array(rate, dtype=float64)
        period = n_array(period)    
        
        if shift < 0:
            raise ex.IndexError('shift should be greater than 0. shift: '+str(shift))
        if shift > len(period):
            raise ex.IndexError('shift should be smaller than period length. shift: '+str(shift)+', period length: '+str(len(period)))
        
        # shift code
        try:        
            period = list(n_zeros(shift, dtype=int)) + list(period[0:len(period)-shift])
        except Exception as e:
            print e
            ''
        
        return initial_capital * n_power(1 + rate.reshape(size(rate), 1) / 100, period)
        
    def mdrange(self, initial, space, end):
        return n_linspace(initial,end,(1.0/space)*end+1)
        
    def rateSpectra(self):
        rate   = self.mdrange(0, 0.1, 10)
        period = range(0, 200 + 1)
        plot(self.compoundVestedCapital(rate, period))
       
    def test(self):
        print self.compoundVestedCapital(50,2)
        print self.compoundVestedCapital(1,n_array([1,2,3]))
        print self.compoundVestedCapital(1,[1,2,3])
        print self.compoundVestedCapital(1,range(0,10))
        print self.compoundVestedCapital(range(0,10),range(0,10))
        #print self.rateCompoundedToPercentage(1,20)
        #print self.compoundedPercentageIntegral(rateCompoundedToPercentage(1,20), 20)
        #print self.compoundedPercentageIntegral(12, 20)

        r_day = fm.rateToCompoundedPercentage(1, 20)       
        vc = ic * pow(1+float(r_day)/100,20)
        print vc
        vc = fm.rateToCompoundedPercentage(r_day, 20)
        print vc
        r_month = 12
        vc = ic * pow(1+float(r_month)/100,1)
        print vc
        vc = fm.compoundVestedCapital(r_month, 1)[0][0]
        print vc

        n_linspace(0,1,100).T
        rate = range(0,23)
        period = range(0,100)
        rate   = n_array(rate, dtype=float64)
        period = n_array(period)    
        #res =  100 * n_power(1 + rate / 100, period.reshape(size(period), 1))
        res =  100 * n_power(1 + rate.reshape(size(rate), 1) / 100, period)
        print res

class ml007:

    def __init__(self):
        self.qd = QoreDebug()
        self.qd._getMethod()

        self.J_history = []
        self.theta     = []
        self.initialIter = 0
        self.iter        = 0
        
    def computeCost_linearRegression(self, X, y, theta, m):
        #self.qd._getMethod()
        
        #print 'cost'
        #print X.shape
        #print type(X.shape)
        #print theta.shape
        o1 = 1.0/(2*m)
        p1 = n_dot(X,theta)
        o2 = n_sum(n_power(p1-y,2)) # J
        #print type(theta)
        ret = o1 * o2
        return ret
    
    #print computeCost( n_array([1, 2, 1, 3, 1, 4, 1, 5]).reshape(4,2), n_array([7, 6, 5, 4]).reshape(4,1), n_array([0.1,0.2]).reshape(2,1) )
    # 11.945
    #print computeCost( n_array([1,2,3,1,3,4,1,4,5,1,5,6]).reshape(4,3), n_array([7, 6, 5, 4]).reshape(4,1), n_array([0.1,0.2,0.3]).reshape(3,1))
    # 7.0175
    
    def gradientDescent_linearRegression(self, X, y, theta, alpha, num_iters, viewProgress=True, b=500, sw=None):
        self.qd._getMethod()
        
        mdf = X

        m = len(y)
        self.J_history = n_zeros(num_iters)
        self.theta = theta
        X = n_array(X)
        alpha_over_m = (float(alpha)/m)
        #try:
        for self.iter in range(self.initialIter, num_iters):
                self.theta = self.theta - alpha_over_m * n_dot((   n_dot(X, self.theta) - y).transpose(), X).transpose()
                #                              nx1   1xm mx1   mxn nx1      mx1           mxn
                #if viewProgress:
                #    if self.iter % b == 0:
                #        clear_output()
                #        print ''
                #        print 'theta:{0}'.format(self.theta)
                self.J_history[self.iter] = self.computeCost_linearRegression(X, y, self.theta, m)
                #if viewProgress:
                #    if self.iter % b == 0:
                #        print '1 J history:{0}'.format(self.J_history[self.iter])
                #        print '1 iter:{0}'.format(self.iter)
                #print type(self.J_history[self.iter])
                #if n_isnan(self.J_history[self.iter]):
                #    #plot(self.J_history); show();
                #    plt.scatter(self.iter, self.J_history); show();
                #    return [self.theta, self.J_history]
                if self.iter % b == 0:
                    if sw != None:
                        tp = sw.predictRegression2(mdf.ix[:, :], quiet=True)
                        tp = tp.reshape(1,len(tp))[:,len(tp)-2:]
                    print '{0}:{1} {2} {3} {4}'.format(self.pair, self.granularity, self.iter, self.J_history[self.iter], tp)
                    #print self.theta                    
                    clear_output()
                    
        #except Exception as e:
        #    print e
        if viewProgress: 
            if self.iter % b == 0:
                #clear_output()
                print '2 J history:{0}'.format(self.J_history[self.iter])
                print '2 iter:{0}'.format(self.iter)
        
        return [self.theta, self.J_history]
        
    #[theta, J_history] = gradientDescent(n_array([1,5,1,2,1,4,1,5]).reshape(4,2), n_array([1,6,4,2]).reshape(4,1), n_array([0,0]).reshape(2,1),0.01,1000);
    #print theta
    #print J_history
    #theta =
    #    5.2148
    #   -0.5733
    #>>J_hist(1)
    #ans  =  5.9794
    #>>J_hist(1000)
    #ans = 0.85426
    
    #[theta, J_hist] = gradientDescent(n_array([3,5,1,2,9,4,1,5]).reshape(4,2),n_array([1,6,4,2]).reshape(4,1), n_array([0,0]).reshape(2,1), 0.01,1000);
    #print theta
    #print J_hist
    #>>theta
    #theta =
    #    0.2588
    #    0.3999

    def costFunction_logisticRegression(self, theta, X, y):
        self.qd._getMethod()

        #%COSTFUNCTION Compute cost and gradient for logistic regression
        #%   J = COSTFUNCTION(theta, X, y) computes the cost of using theta as the
        #%   parameter for logistic regression and the gradient of the cost
        #%   w.r.t. to the parameters.
        
        #% Initialize some useful values
        m = len(y); #% number of training examples
        
        #% You need to return the following variables correctly 
        J = 0;
        grad = n_zeros(size(theta));
        
        #% ====================== YOUR CODE HERE ======================
        #% Instructions: Compute the cost of a particular choice of theta.
        #%               You should set J to the cost.
        #%               Compute the partial derivatives and set grad to the partial
        #%               derivatives of the cost w.r.t. each parameter in theta
        #%
        #% Note: grad should have the same dimensions as theta
        #%
        
        y = y.get_values()
        
        #J = (1/m)*sum(-y.*log(sigmoid(X*theta))-(1-y).*log(1-sigmoid(X*theta)));
        J = (1.0/m) * n_sum(-y *  n_log(sigmoidme(n_dot(X, theta))) - (1 - y) *     log(  1 - sigmoidme(n_dot(X, theta))  ) );
        #grad = (1/m)*sum((sigmoid(X*theta)-y).*X)
        grad = (1/m)*n_sum(n_dot((sigmoidme(n_dot(X, theta))-y), X))
        
        #% =============================================================
        
        #end
        
        return [J, grad]    
    
    #initial_theta = n_zeros(nn + 1);
    #initial_theta = n_zeros(nn);
    #initial_theta
    
    #[cost, grad] = costFunction(initial_theta, X, y);


class OandaQ:
    
    oanda2 = None
    
    def __init__(self, verbose=False, stats=False):
        self.qd = QoreDebug()
        self.qd._getMethod()
        
        self.verbose = verbose
        
        # get current quotes
        co = p_read_csv('/mldev/bin/datafeeds/config.csv', header=None)
        env2=co.ix[1,1]
        access_token2=co.ix[1,2]
        self.oanda2 = oandapy.API(environment=env2, access_token=access_token2)
    
        self.aid = self.oanda2.get_accounts()['accounts'][0]['accountId']
        #self.oanda2.create_order(aid, type='market', instrument='EUR_USD', side='sell', units=10)
        if stats == True:
            res = self.oanda2.get_trades(self.aid)
            if verbose:
                for i in res:
                    print p_DataFrame(res[i])
            
                print p_DataFrame(self.oanda2.get_account(self.aid), index=[0])
    
        self.dfa = {}
        
        self.granularityMap = {
            'S5' : 5, # seconds
            'S10' : 10, # seconds
            'S15' : 15, # seconds
            'S30' : 30, # seconds
            'M1' : 1 * 60, # minute
    
            'M2' : 2 * 60, # minutes
            'M3' : 3 * 60, # minutes
            'M4' : 4 * 60, # minutes
            'M5' : 5 * 60, # minutes
            'M10' : 10 * 60, # minutes
            'M15' : 15 * 60, # minutes
            'M30' : 30 * 60, # minutes
            'H1' : 1 * 3600, # hour
            'H2' : 2 * 3600, # hours
            'H3' : 3 * 3600, # hours
            'H4' : 4 * 3600, # hours
            'H6' : 6 * 3600, # hours
            'H8' : 8 * 3600, # hours
            'H12' : 12 * 3600, # hours
            'D' : 1 * 86400, # Day
            #Start of week alignment (default Friday)        
            'W' : 1 * 604800, # Week
            #Start of month alignment (First day of the month)        
            'M' : 1 * 2419200 # Month
        }

    def log(self, msg, printDot=False):
        if self.verbose == True: 
            print msg
        if printDot == True:
            print '.',
    
    def debug(self, msg):
        if self.verbose == True: 
            print msg
    
    def datetimeToTimestamp(self, ddt):
        self.qd._getMethod()

        def _datetimeToTimestamp(ddt):
            return (ddt - dd.datetime(1970, 1, 1)).total_seconds() / dd.timedelta(seconds=1).total_seconds()
        
        try:    tstmp = _datetimeToTimestamp(ddt)
        except Exception as e:
            print e
            tstmp = []
            for i in ddt: tstmp.append(_datetimeToTimestamp(i))
        return tstmp
        
    def timestampToDatetime(self, tst):
        self.qd._getMethod()

        def _timestampToDatetime(tst):
            return dd.datetime.fromtimestamp(tst)

        try:    ddt = _timestampToDatetime(tst)
        except Exception as e:
            print e
            ddt = []
            for i in tst: ddt.append(_timestampToDatetime(i))                
        return ddt
        
    """
    timestampToDatetimeFormat [1435942800.0, 1436130000.0, 1436144400.0, 1436158800.0, 1436173200.0, 1436187600.0, 1436202000.0, 1436216400.0, 1436230800.0, 1436245200.0]
    Out]:
    ['2015-07-03 14:00:00',
     '2015-07-05 18:00:00',
     '2015-07-05 22:00:00',
     '2015-07-06 02:00:00',
     '2015-07-06 06:00:00',
     '2015-07-06 10:00:00',
     '2015-07-06 14:00:00',
     '2015-07-06 18:00:00',
     '2015-07-06 22:00:00',
     '2015-07-07 02:00:00']
     """
    def timestampToDatetimeFormat(self, tst, fmt='%Y-%m-%d %H:%M:%S %Z'):
        self.qd._getMethod()

        def _timestampToDatetimeFormat(tst):
            w2 = dd.datetime.fromtimestamp(tst)
            return w2.strftime(fmt)
            #return dd.datetime.fromtimestamp(tst)

        try:    
            ddt = _timestampToDatetimeFormat(tst)
        except Exception as e:
            print e
            ddt = []
            for i in tst: ddt.append(_timestampToDatetimeFormat(i))                
        return ddt

    
    def oandaToTimestamp(self, ptime):
        self.qd._getMethod()
        
        def _oandaToTimestamp(ptime):
            dt = dd.datetime.strptime(ptime, '%Y-%m-%dT%H:%M:%S.%fZ')
            return (dt - dd.datetime(1970, 1, 1)).total_seconds() / dd.timedelta(seconds=1).total_seconds()
            
        try:
            tstmp = _oandaToTimestamp(ptime)
        except Exception as e:
            print e
            tstmp = []
            for i in ptime: tstmp.append(_oandaToTimestamp(i))                
        return tstmp

    def oandaToDatetime(self, ptime):
        self.qd._getMethod()
        return dd.datetime.strptime(ptime, '%Y-%m-%dT%H:%M:%S.%fZ')

    def trade(self, risk, stop, instrument, side, tp=None):
        self.qd._getMethod()
        """
        if instrument == 'eu':
            instrument = 'EUR_USD'
        if instrument == 'au':
            instrument = 'AUD_USD'
        if instrument == 'nu':
            instrument = 'NZD_USD'
        if instrument == 'ej':
            instrument = 'EUR_JPY'
        if instrument == 'uj':
            instrument = 'USD_JPY'
        """
        if side == 'b':
            side ='buy'
            self.buy(risk, stop, instrument=instrument, tp=tp)
        if side == 's':
            side ='sell'
            self.sell(risk, stop, instrument=instrument, tp=tp)
        
    def buy(self, risk, stop, instrument='EUR_USD', tp=None):
        self.qd._getMethod()
        
        self.order(risk, stop, 'buy', instrument=instrument, tp=tp)
        
    def sell(self, risk, stop, instrument='EUR_USD', tp=None):
        self.qd._getMethod()
        
        self.order(risk, stop, 'sell', instrument=instrument, tp=tp)

    def order(self, risk, stop, side, instrument='EUR_USD', tp=None, price=None, expiry=None):
        self.qd._getMethod()
        
        stop = abs(float(stop)) # pips
        risk = float(risk) # percentage risk
        
        #print self.oanda2.get_accounts()['accounts'][0]['accountId']
        acc = self.oanda2.get_account(self.aid)
        #mprice = self.oanda2.get_prices(instruments='EUR_USD')['prices'][0]['ask']
        #leverage = 50
        
        amount = self.calculateAmount(acc['marginAvail'], risk, stop)
        
        #print acc['marginAvail'] * float(leverage) / mprice
        #print acc
        #print mprice
        print amount
        
        prc = self.oanda2.get_prices(instruments=instrument)['prices'][0]
        
        limitprice = self.oanda2.get_prices(instruments='EUR_USD')['prices'][0]
                
        if side == 'buy':
            stopLoss   = prc['bid'] - float(stop) / 10000
            takeProfit = prc['bid'] + float(stop) / 10000
            print takeProfit
            limitprice = limitprice['bid']
        if side == 'sell':
            stopLoss = prc['ask'] + float(stop) / 10000
            takeProfit = prc['ask'] - float(stop) / 10000
            print takeProfit
            limitprice = limitprice['ask']
        if tp != None:
            takeProfit = tp
        else:
            takeProfit = None
        
        try:
            print 'attempting market order'
            order = self.oanda2.create_order(self.aid, type='market', instrument=instrument, side=side, units=amount, stopLoss=stopLoss, takeProfit=takeProfit)
            print 'market order success'
        except oandapy.OandaError, e:
            print 'attempting limit order'
            tti = dd.datetime.now()
            tti = tti+ dd.timedelta(days=30)
            tti = self.datetimeToTimestamp(tti)
            expiry = self.timestampToDatetimeFormat(tti, fmt='%Y-%m-%dT%H:%M:%S-3:00')
            #print e
            order = self.oanda2.create_order(self.aid, type='limit', expiry=expiry, price=limitprice, instrument=instrument, side=side, units=amount, stopLoss=stopLoss, takeProfit=takeProfit)
            print order
            print 'limit order success'

    def calculateAmount(self, bal, pcnt, stop):
        self.qd._getMethod()

        bal  = float(bal)
        lev  = 30.0
        stop = float(stop)
        openp = 1 #1.13024
        pcnt = float(pcnt)
        
        amount = bal * lev
        pl     = amount * ((openp + float(stop) / 10000.0) - openp )
        #pcnt   = 100.0*pl / bal
        
        amount = (pcnt * bal) / (100* ((openp + float(stop) / 10000.0) - openp ) )
        #amount = (pcnt * bal) / (100* ((openp - float(stop) / 10000.0) - openp ) )
        amount = abs(int(amount))
        print 'amount {0}'.format(amount)
        print 'pl {0}'.format(pl)
        print 'pcnt {0}'.format(pcnt)
        
        return amount
        
    def calculateStopLossFromPrice(self, pair, mprice):
        self.qd._getMethod()

        current = self.oanda2.get_prices(instruments=[pair])['prices'][0]['bid']
        mstop = (mprice-current) * 10000
        #print 'mstop {0}'.format(mstop)
        return mstop
        
    def generateRelatedColsFromOandaTickers(self, data, pair):
        self.qd._getMethod()
        
        if type(data) == type(None):
            print data
            raise ValueError('given input is none')
        
        # generate relatedCols from oandas tickers
        fname = '/mldev/bin/data/oanda/cache/instruments.csv'
        try:
            inst = readcache(fname)
        except Exception as e:
            print e
            inst = p_DataFrame(self.oanda2.get_instruments(self.aid)['instruments'])
            writecache(inst, fname)
        lse = []
        lsf = []
        for i in inst.ix[:, 'instrument']:

            ipair = i.replace('_', '')
            
            if pair[0:3] == ipair[0:3] or pair[0:3] == ipair[3:6]:
                lse.append('BNP.'+ipair+' - '+ipair[0:3]+'/'+ipair[3:6]+'_x')

            if pair[3:6] == ipair[0:3] or pair[3:6] == ipair[3:6]:
                lse.append('BNP.'+ipair+' - '+ipair[0:3]+'/'+ipair[3:6]+'_x')
                
            if pair[0:3] == ipair[0:3] and pair[3:6] == ipair[3:6]:
                lse.pop()
        for i in lse:
            try:    
                lsf.append(list(data.columns).index(i))
            except Exception as e:
                print e
                
        #for i in inst:
        #    print i['instrument']
        
        #print lsf
        try:
            lsf  = list(p_DataFrame(lsf).sort(0).transpose().get_values()[0])
        except KeyError, e:
            print e
        #print lsf
        return lsf
        
    def getPairsRelatedToOandaTickers(self, pair):
        self.qd._getMethod()
        
        # generate relatedCols from oandas tickers
        
        fname = '/mldev/bin/data/oanda/cache/instruments.csv'
        try:
            inst = readcache(fname)
        except Exception as e:
            print e     
            inst = p_DataFrame(self.oanda2.get_instruments(self.aid)['instruments'])
            writecache(inst, fname)

        lse = []
        lsf = []
        lsp = []
        for i in inst.ix[:, 'instrument']:

            ipair = i.replace('_', '')
            
            if pair[0:3] == ipair[0:3] or pair[0:3] == ipair[3:6]:
                lse.append('BNP.'+ipair+' - '+ipair[0:3]+'/'+ipair[3:6]+'_x')
                lsp.append([i, ipair])

            if pair[3:6] == ipair[0:3] or pair[3:6] == ipair[3:6]:
                lse.append('BNP.'+ipair+' - '+ipair[0:3]+'/'+ipair[3:6]+'_x')
                lsp.append([i, ipair])
                
        #print lse
        #print lsp
        
        r = {}
        r['lse'] = lse
        r['lsf'] = lsf
        r['lsp'] = lsp
        
        return r
    
    def getPricesLatest(self, data, sw, trueprices=False):
        self.qd._getMethod()
        
        ins = []
        pairs = []
        for i in list(data.ix[:, sw.relatedCols].columns):
            pair = re.sub(re.compile(r'.*?-\ (.*)_x'), '\\1', i).replace('/', '_')
            #print pair
            pr = p_DataFrame(self.oanda2.get_prices(instruments=[pair])['prices'])
            #print 
            ins.append(n_mean(pr.ix[0, ['bid', 'ask']].get_values()))
            pairs.append(pair)
        prices = p_DataFrame(ins, index=pairs)
        if trueprices:
            return prices
        #print #prices
        list(prices.ix[1:,0])#.insert(0,1)
        nprices = p_DataFrame([list(sw.theta), list(prices.ix[1:,0]) ]).transpose()
        #nprices = nprices.fillna(0)
        
        #prices.ix[1:,0], sw.dmean, sw.dstd] = normalizeme(prices.ix[1:,0], pinv=True)
        #rices.ix[1:,0] = sigmoidme(prices.ix[1:,0])
        nprices = p_DataFrame([list(sw.theta), list(prices.ix[1:,0]) ], columns=list(prices.index)).transpose()
        pr2 = list(nprices.ix[:,1])[0:10]
        pr2.insert(0,1)
        #print pr2
        #print 
        #print prices
        nprices[1] = pr2
        print nprices
        return nprices

    def oandaTransactionHistory(self, plot=True):
        self.qd._getMethod()

        # oanda transaction history (long-term)
        from pylab import rcParams
        rcParams['figure.figsize'] = 20, 5
        # oanda equity viz
        df0 = p_read_csv('/home/qore/sec-svn.git/assets/oanda/kpql/primary/statement.csv')
        #df0 = df0.ix[3000:, 'Balance']
        df0 = df0.sort(columns=['Transaction ID'])
        df0 = df0.ix[:, :]
        df0 = df0.set_index('Transaction ID')
        
        #dfn = df0.ix[:, 'Balance']
        #dfn = normalizeme(dfn)
        #dfn = sigmoidme(dfn)
        #dfn.plot(); show();
        #print df.ix[:,['Type','Currency Pair','Units','Balance','Interest','Pl']]
        
        # oanda transaction history (short-term)
        qqq = QoreQuant()
        df1 = p_DataFrame(qqq.oanda2.get_transaction_history(qqq.oq.aid)['transactions']).bfill()
        df1 = df1.sort('id', ascending=True)
        df1 = df1.set_index('id')
        
        #print df0.tail()
        #print dfn.tail()
        #print df0 #.transpose()
        #print df1
        
        df1['Balance'] = df1['accountBalance']
        #print df0.tail()
        #print df1.tail()
        #df = df0.combine_first(df1)
        df = df1.combine_first(df0)
        #print df.tail()
        #df.ix[:,['Balance','accountBalance']]
        
        #print 'long term'
        #df0.ix[:,'Balance'].plot(); show();
        #print 'short term'
        #df1['accountBalance'].plot(); show();
        #print 'merge'
        if plot == True:
            df.ix[:,'Balance'].plot(); show();
        return df
        
    def getHistoricalPrice(self, pair, granularity='S5', count=2, plot=True):
        self.qd._getMethod()
        
        df = self.oanda2.get_history(instrument=pair, count=count, granularity=granularity)
        #hed = ['closeAsk', 'closeBid', 'highAsk', 'highBid', 'lowAsk', 'lowBid', 'openAsk', 'openBid', 'volume']
        #hed = ['closeAsk', 'closeBid', 'highAsk', 'highBid', 'lowAsk', 'lowBid', 'openAsk', 'openBid']
        hed = ['closeAsk', 'closeBid', 'volume']
        df = p_DataFrame(df['candles'], dtype=n_float16)
        df = df.set_index('time')
        #print df
        df = df.ix[:,hed]
        #df = normalizeme(df)
        #df = sigmoidme(df)
        if plot == True:
            df.ix[:,:].plot(legend=False, title=pair); show();
        #print df
        
        return df
    
    def appendHistoricalPrice(self, df, pair, granularity='S5', plot=True, count=None):
        self.qd._getMethod()

        safeShift = 0
        
        ti = df.tail(1).index[0]
        ddt = self.datetimeToTimestamp(dd.datetime.now()) 
        #print ddt
        ddtdiff = ddt - self.oandaToTimestamp(ti) + (60*60*3)
        self.log('{0} seconds behind'.format(ddtdiff))
        self.log('{0} minutes behind'.format(ddtdiff / 60))
        if count == None:
            reqcount = int(ceil(ddtdiff / self.granularityMap[granularity])) + safeShift
        else:
            reqcount = count
        self.log(self.granularityMap[granularity])
        self.log('requesting {0} ticks'.format(reqcount))
        if safeShift > 0:
            plotHiPr = True
        else:
            plotHiPr = False

        if reqcount > 1:
            dfn = self.getHistoricalPrice(pair, count=reqcount, granularity=granularity, plot=plotHiPr)#.tail()
            #print df.tail()
            #print dfn.tail()
            dfc = df.combine_first(dfn)
            df = dfc
        
            if plot == True:
                #df.plot(); show();
                dfc.plot(title=pair); show();
            return dfc
        return df
        
    def updatePairGranularity(self, pair, granularity, noUpdate=False, plot=True):
        self.qd._getMethod()

        ob = ''
        #ob += '{0} {1}'.format(pair, granularity)
        fname = '/mldev/bin/data/oanda/ticks/{0}/{0}-{1}.csv'.format(pair, granularity)
        try:    
            self.dfa[pair][granularity]
        except Exception as e:
            print e
            # if dataframe not in memory
            self.log('{0} {1} dataframe not in memory'.format(pair, granularity))
            try:
                # read from csv
                self.dfa[pair][granularity] = p_read_csv(fname, index_col=0)
                ob += ' reading from {0} {1} {2}'.format(fname, pair, granularity)
                ob += ' len {0}.'.format(len(self.dfa[pair][granularity]))
            except KeyError, e:
                self.debug(e)
                self.dfa[pair] = {}
            except IOError, e:
                # if no csv file, initialize memory for the dataframe
                #print e
                self.dfa[pair] = {}
            except Exception as e:
                print e
                print 'exception {0}'.format(pair)
                
        # append to current dataframe in memory
        if noUpdate == False:
            self.log('{0} {1} attempting update {2}'.format(pair, granularity, noUpdate))
            self.log('{0} {1} updating'.format(pair, granularity))
            try:
                self.log('len {0} before append.'.format(len(self.dfa[pair][granularity])))
                self.dfa[pair][granularity] = self.appendHistoricalPrice(self.dfa[pair][granularity], pair, granularity=granularity, plot=plot)
                self.log('len {0} after append.'.format(len(self.dfa[pair][granularity])))
                self.log('appended to {0}'.format(pair))
                # if no dataframe in memory, download from data source
            except Exception as e:
                self.debug(e)
                try:
                    self.dfa[pair][granularity] = self.getHistoricalPrice(pair, count=5000, granularity=granularity, plot=plot)
                    self.log('got clean series {0}'.format(pair))
                except oandapy.OandaError, e:
                    self.debug(e)
        
        if noUpdate == False:
            try:
                # save to csv file
                li = fname.split('/'); li.pop(); hdir = '/'.join(li);
                mkdir_p(hdir)
                self.dfa[pair][granularity].to_csv(fname)
                #if plot == True:
                #    self.dfa[pair][granularity].plot(); show();
                self.log('saved {0} to {1}'.format(pair, fname))
            except KeyError, e:
                print e
        self.log(ob)
        #print self.dfa[pair][granularity]
        return self.dfa[pair][granularity]
        
    def updateBarsFromOanda(self, pair='EURUSD', granularities = 'H4', plot=True, noUpdate=False):
        self.qd._getMethod()

        pair = pair.replace('_', '') # remove the underscore
        relatedPairs = self.getPairsRelatedToOandaTickers(pair)        
        
        pairs = list(p_DataFrame(relatedPairs['lsp']).ix[:,0])
        #self.log(pairs)
        self.granularities = granularities.split(' ')
        for pair in pairs:
            self.log('')
            try:                self.dfa[pair]
            except KeyError, e: 
                self.dfa[pair] = {}; 
                self.debug(e)
            for granularity in self.granularities:
                self.updatePairGranularity(pair, granularity, noUpdate=noUpdate, plot=plot)
                
        #print self.dfa
        return self.dfa

    def prepareDfData(self, dfa):
        self.qd._getMethod()

        dfac = p_DataFrame()
        gran = self.granularities[0]
        
        try:
            for i in dfa:
                #dfa[i][gran][i+'closeAsk'] = dfa[i][gran]['closeAsk']
                #dfa[i][gran][i+'closeBid'] = dfa[i][gran]['closeBid']
                par = 'BNP.{0} - {1}_x'.format(i.replace('_', ''), i.replace('_', '/'))
                dfa[i][gran][par] = (dfa[i][gran]['closeAsk'] + dfa[i][gran]['closeBid']) / 2       
                #print dfa[i][gran].ix[:,[2,3]].tail(1)#.transpose()
                #dfac = dfac.combine_first(dfa[i][gran].ix[:,[2,3,4]]) #.tail(1)#.transpose()
                dfac = dfac.combine_first(dfa[i][gran].ix[:,[par]]) #.tail(1)#.transpose()
        except Exception as e:
            print e
            print gran+' granularity not available, please update for '+gran
        #dfac = normalizeme(dfac)
        #dfac = sigmoidme(dfac)
        #dfac = (1 - n_power(n_e, -dfac)) / (1 + n_power(n_e, -dfac)) # hyperbolic tangent, tanh
        #dfac = n_log(1 + n_power(n_e, dfac)) # relu
        #dfac = n_tanh(dfac) # tanh
        #dfac.plot(legend=False); show();
        #dfac
        
        #from qoreliquid import *
        #qq = QoreQuant()
        
        return dfac


# source: http://stackoverflow.com/questions/3949226/calculating-pearson-correlation-and-significance-in-python
def pearson_def(x, y):
    def average(x):
        assert len(x) > 0
        return float(sum(x)) / len(x)
    assert len(x) == len(y)
    n = len(x)
    assert n > 0
    avg_x = average(x)
    avg_y = average(y)
    diffprod = 0
    xdiff2 = 0
    ydiff2 = 0
    for idx in range(n):
        xdiff = x[idx] - avg_x
        ydiff = y[idx] - avg_y
        diffprod += xdiff * ydiff
        xdiff2 += xdiff * xdiff
        ydiff2 += ydiff * ydiff

    return diffprod / math.sqrt(xdiff2 * ydiff2)
#print pearson_def([1,2,3], [1,5,7])
#returns
#0.981980506062

def pcc(X, Y):
   ''' Compute Pearson Correlation Coefficient. '''
   # Normalise X and Y
   X -= X.mean(0)
   Y -= Y.mean(0)
   # Standardise X and Y
   X /= X.std(0)
   Y /= Y.std(0)
   # Compute mean product
   return n_mean(X*Y)
# Using it on a random example
#from random import random
#X = n_array([random() for x in xrange(100)])
#Y = n_array([random() for x in xrange(100)])
#pcc(X, Y)

class StatWing:
    
    def __init__(self):
        self.qd = QoreDebug()
        self.qd._getMethod()

        self.keyCol = ''
        self.relatedCols = []
        self.theta = n_array([])
        self.dmean = []
        self.dstd = []
        
        # for predict from theta
        self.nxps = []
        try:    self.oq = OandaQ()
        except Exception as e:
            print e
            print 'offline mode'
        #self.theta = p_read_csv('/mldev/bin/datafeeds/theta.csv', index_col=0)
        self.theta = p_DataFrame()
        self.ml = ml007()
        
    def nextBar(self, dfa, k, barsForward=3):
        self.qd._getMethod()
        
        dfc = p_DataFrame(dfa, index=dfa.index[0:len(dfa)-barsForward])
        #print type(dfc)
        a = dfa.ix[0:len(dfa)-barsForward, [k]].get_values()
        b = dfa.ix[barsForward:len(dfa),[k]].get_values()
        #print len(a)
        #print len(b)
        dfc['a'] = a
        dfc['b'] = b
        dfc['c'] = dfc['b']
        #print dfc.ix[1:len(dfa),['a','b','c']]
        return dfc['c']

    def higherNextDay(self, dfa, k):
        self.qd._getMethod()

        dfc = p_DataFrame(dfa, index=dfa.index[0:len(dfa)-1])
        print type(dfc)
        dfc['a'] = dfa.ix[0:len(dfa)-1, [k]].get_values()
        dfc['b'] = dfa.ix[1:len(dfa),[k]].get_values()
        dfc['c'] = list(n_array((dfc['b'] > dfc['a']), dtype=int))
        #print dfc['a']
        return dfc['c']
        #p_DataFrame(sw.higherPrev(df.ix[:, 0].get_values()))
    
    def lowerNextDay(self, dfa, k):
        self.qd._getMethod()

        dfc = p_DataFrame(dfa, index=dfa.index[0:len(dfa)-1], columns=dfa.columns)
        dfc['a'] = dfa.ix[0:len(dfa)-1, [k]].get_values()
        dfc['b'] = dfa.ix[1:len(dfa), [k]].get_values()
        dfc['c'] = n_array((dfc['b'] < dfc['a']), dtype=int)
        return dfc['c']
        #p_DataFrame(sw.higherPrev(df.ix[:, 0].get_values()))
    
    # export dataset to csv for analysis (statwing)
    def higherPrev(self, a):
        self.qd._getMethod()

        a = sigmoidme(a) > 0.5
        return n_array(a, dtype=int)
    
    def lowerPrev(self, a):
        self.qd._getMethod()

        a = sigmoidme(a) < 0.5
        return n_array(a, dtype=int)
    
    def exportToStatwing(self, de, currency_code):
        self.qd._getMethod()

        #dff = n_matrix('1;2;3;4;-4;-5;-3;2;9').A
        #print higherPrev(dff)
        #print lowerPrev(dff)
        s1 = 0
        de = de.fillna(0)
        de1 = de.ix[s1:,:]
        #de1 = sigmoidme(normalizeme(de1))
        de1 = p_DataFrame(de1)
        de1['hi'] = self.higherPrev(de.ix[s1:,0].diff())
        de1['lo'] = self.lowerPrev(de.ix[s1:,0].diff())
        #de1.to_csv('quandl-BNP-'+currency_code+'.csv', index=None)
        #de1.ix[:,:].plot(style='-'); show();
        #print de1
        return de1

    def getCol(self, col, df):
        self.qd._getMethod()

        if type(col) == type(0):
            column = df.columns[col]
        elif type(col) == type(''):
            column = col
        return column
    
    def describe(self, df, col):
        self.qd._getMethod()

        print 'Summary:'
        sample = df.ix[:,col]  
        c = ['Sample Size', 'Median',        'Average',      'Confidence Interval of Average',  'Standard Deviation', 'Minimum',      'Maximum',      'Sum']
        d = [len(sample),   n_median(sample),n_mean(sample), '0.53784 to 0.54679',                    n_std(sample),       n_min(sample), n_max(sample), n_sum(sample)]
        #110.279 to 110.636
        summary = p_DataFrame(d, index=c)#.transpose()
        print summary
        
        print 'Percentiles:'
        pctl = []
        for i in [0,1,5,10,25,50,75,90,95,99,100]:
            pctl.append(n_percentile(df.ix[:,1], i))
        print p_DataFrame(pctl, index=['0th (Minimum)', '1st','5th','10th','25th (Lower Quartile)','50th (Median)','75th (Upper Quartile)','90th','95th','99th','100th (Maximum)'])#.transpose()
        
        sample.hist(bins=100);
        xlabel(self.getCol(col, df))
        #ylabel('t2')
        show();
        
    def relate(self, sample, keyCol, relatedCol):
        self.qd._getMethod()

        #print n_corrcoef(sample.ix[:, keyCol], sample.ix[:, relatedCol])[0, 1]
        #print pearson_def(sample.ix[:, keyCol], sample.ix[:, relatedCol])
        # source: http://stackoverflow.com/questions/19428029/how-to-get-correlation-of-two-vectors-in-python
        from scipy.stats.stats import pearsonr, spearmanr
        ind = ['Pearson\'s r: ', 'Spearman\'s r: ']
        d = [pearsonr(sample.ix[:, keyCol], sample.ix[:, relatedCol]), spearmanr(sample.ix[:, keyCol], sample.ix[:, relatedCol])]
        print p_DataFrame(d, index=ind)
        
        x = sample.ix[:, relatedCol].fillna(0)
        y = sample.ix[:, keyCol].fillna(0)
        
        deg = 1
        weight = 1
        theta = n_polynomial.polynomial.polyfit(x,y,deg,weight)#w=weight of each observation)
        print 'theta:{0}'.format(theta)
        #p_DataFrame(theta[0] + theta[1] * n_array(range(0, int(n_max(x.ix[:,1]))))).plot()
        #p_DataFrame(theta[0] + theta[1] * n_array(range(0, ceil(n_max(x.get_values()))))).plot()
        #print [min(y), max(y)]
        #print [min(x), max(x)]
        #p_DataFrame(theta[0] + theta[1] * n_array( n_linspace(0, int(ceil(n_max(x.get_values()))), 5) )).plot()
        mini = int(ceil(n_min(x.get_values())))#-10
        maxi = int(ceil(n_max(x.get_values())))#+10
        plot(linspace(mini, maxi, 10), theta[0] + theta[1] * linspace(mini, maxi, 10), '-r');
        #p_DataFrame(theta[0] + theta[1] * n_array( n_linspace(mini, maxi, maxi-mini) )).plot()
        #p_DataFrame(theta[0] + theta[1] * n_array( n_linspace(-120, 60, 180) )).plot()
        
        #print n_linspace(int(ceil(n_max(x.get_values()))), int(ceil(n_max(x.get_values()))), 5)
        #print n_linspace(min(x)-10, int(ceil(n_max(x.get_values())))+10, len(x))
        
        scatter(x,y, vmin=0, vmax=(100));
        #print ceil(max(x))
        #scatter(sample.ix[:, relatedCol], sample.ix[:, keyCol]);
        xlabel(self.getCol(relatedCol, sample))
        ylabel(self.getCol(keyCol, sample))
        show();
    
    def fixColumns(self, data, relatedCols, keyCol):
        self.qd._getMethod()

        #print 'relatedCols'
        #print relatedCols
        
        #print 'keyCol'
        #print keyCol
        
        #print 'datavols'
        #print data.columns

        X = data.ix[:, relatedCols]
        #print type(X)
        #print X
        #print list(X.columns)
        X['bias'] = n_ones(len(data))
        Xc = X.columns.tolist()
        Xc.insert(0, Xc.pop())
        try:
        #print 'removing {0}'.format(keyCol)
        #print Xc
            Xc.remove(keyCol)
        except Exception as e:
            #print e
            ''
        X = X[Xc]
        #print list(X.columns)
        return X
    
    def regression(self, data, y, keyCol, relatedCols, initialTheta=None, iterations=1000, alpha=0.01, viewProgress=True, showPlot=True, verbose=False):
        self.qd._getMethod()

        data = data.fillna(0)
        #X = data.ix[:,0]; y = data.ix[:,1]
        #X = data.ix[:,2]; y = data.ix[:,1]
        ##X = data.ix[:,0]; 
        #y = data.ix[:,'hi']
        ##y = data.ix[:,0]
        m = len(data)
        
        #scatter(X,y, marker='x', c='r'); show();
        
        # gradient descent
        #plot(X,y,'.'); show();
        
        # 
        X = self.fixColumns(data, relatedCols, keyCol)
        
        #print y
        
        #initialTheta = None
        
        if type(initialTheta) == type(None):
            self.theta = n_zeros(len(X.columns))
            print 'theta initialized'
        else:
            print initialTheta
            print 'theta loaded'
            self.theta = initialTheta

        #print y.shape
        #print m
        #print 'test======'
        print 'data.shape: {0}'.format(data.shape)
        print 'X.shape: {0}'.format(X.shape)
        #print type(X)
        #print self.theta
        print 'theta.shape: {0}'.format(self.theta.shape)
        #print type(self.theta)
        #print X.columns
        #print self.theta.to_frame().columns
        self.theta = p_Series(self.theta).to_frame('o').fillna(0).combine_first(p_DataFrame(n_zeros(len(X.columns)), index=X.columns, columns=['o'])).ix[X.columns, 'o'].get_values()
        print self.theta
        print 'theta2.shape: {0}'.format(self.theta.shape)
        #print relatedCols
        #print len(relatedCols)
        #print self.theta.shape
        #print self.theta
        #print type(self.theta)
        #print '===='        
        #import sys
        #sys.exit()
        #raise(e)
        
        #theta = n_random.randn(len(X.columns))
        #print self.theta
        
        #% compute and display initial cost
        self.ml.computeCost_linearRegression(X, y, self.theta, len(y))
        
        #% run gradient descent
        [self.theta, self.J_hist] = self.ml.gradientDescent_linearRegression(X, y, self.theta, alpha, iterations, viewProgress=viewProgress, sw=self);
        
        if verbose == True:
            #% print theta to screen
            print 'Theta found by gradient descent: '
            #print '%f %f \n', theta(1), theta(2)
        
        jh = self.J_hist
        if verbose == True:
            print 'len cols'
            print len(X.columns)
            print self.ml.theta
            print jh[len(jh)-1]
        if showPlot == True:
            plot(jh, '-'); show();

        
        return self.ml.theta

    def predictRegression(self, te1, te2, mode=1):
        self.qd._getMethod()

        if len(te1) > len(te2):
            #te2.append(0)
            te2.insert(0,0)
        
        print te1
        print te2
        print '---'
        
        dp = p_DataFrame(te1)
        #print len(te1)
        #print te1
        #print len(te2)
        #print te2
        dp[1] = te2
        
        # get current quotes
        co = p_read_csv('datafeeds/config.csv', header=None)
        env2=co.ix[1,1]
        access_token2=co.ix[1,2]
        oanda2 = oandapy.API(environment=env2, access_token=access_token2)
        li = []
        if mode == 1: fl = 0; ll = len(dp.index)-1;
        if mode == 2: fl = 1; ll = len(dp.index);
        for i in list(dp.ix[:,1])[fl:ll]:
            if i != 'bias':
                try:
                    pai = "{0}_{1}".format(i[0:3], i[3:6])
                    response = oanda2.get_prices(instruments=pai)
                    prices = response.get("prices")
                    asking_price = prices[0].get("ask")
                    li.append(asking_price)
                except oandapy.OandaError, e:
                    print
                    print e
                    print
                    print 'The above pair is not available, please omit this pair before applying a regression.'
                    print 'The below output is not accurate and it only serves as an indication.'
                    print
                    li.append(0)
            else:
                li.append(1)
        #if len(te1) > len(te2):
        #li.append(1)
        li.insert(0,1)
        dp[2] = li
        print dp
        
        dn = n_array(dp.get_values()[:,[0,2]], dtype=float)
        #print dn
        n_dot(dn[:,0], dn[:,1])
        pred = n_sum(dn[:,0] * dn[:,1])
        print pred
        """
        predictions.append(pred)
        print p_DataFrame(predictions)
        plot(predictions); show();
        """
        
    # m2e() { fc="`echo "$1" | perl -pe 's/.xlsx/.csv/g'`"; echo $1; echo $fc; xlsx2csv $1 $fc; }    
    def statwingExportPredict(self, fns, ):
        self.qd._getMethod()

        for fn in fns:
            print '================================================='
            print fn
            print '================================================='
            
            fp = open(fn,'r')
            te = fp.read()
            te = re.match(re.compile(r'.*?= (.*?").*', re.S), te).groups()[0]#.replace('\n', '')
            #print te
            
            # weights
            #te1 = re.findall(re.compile(r'[\+\-]\s+\d+\.\d+', re.S), te)#.groups()[0]#.replace('\n', '')            
            te1 = re.findall(re.compile(r'([\+\-])\s+(\d+)(\.\d+)?', re.S), te)#.groups()[0]#.replace('\n', '')
            #print te1
            for i in xrange(len(te1)):
                te1[i] = ''.join(te1[i])
            
            # pairs 
            te2 = re.findall(re.compile(r'[A-Z]+\.([A-Z]+)', re.S), te)#.groups()[0]#.replace('\n', '')
            
            self.predictRegression(te1, te2)
            
    #def regression2(self, de=None, du=None, da=None):
    def regression2(self, X=None, y=None, iterations=1000, alpha=0.01, initialTheta=None, viewProgress=True, showPlot=True):
        self.qd._getMethod()

        #if X == None:
        #    X = getDatasetEUR()
        #if du == None:
        #    du = getDataUSD()
        #if da == None:
        #    da = getDataAUD()
        
        # last model
        # 1990-01-01 2015-05-20 inclusive
        
        #df1 = self.exportToStatwing(X,'EUR')
        #sw.exportToStatwing(du,'USD')
        #print df1
        
        #sw.relate(df1, 0, 3)
        
        #data = p_read_csv('/coursera/ml-007/programming-exercises/mlclass-ex1/ex1data1.txt', header=None)
        #data = p_read_csv('quandl-BNP-USD.csv')
        #data = p_read_csv('quandl-BNP-EUR.csv')
        #data = X.fillna(0).ix[:,data.columns]
        data = X.ix[X.index, X.columns].fillna(0)
        
        [data, self.dmean, self.dstd] = normalizeme(data, pinv=True)
        data = sigmoidme(data)
        [y, self.ymean, self.ystd] = normalizeme(y, pinv=True)
        y = sigmoidme(y)
        
        self.regression(data, y, self.keyCol, self.relatedCols, iterations=iterations, alpha=alpha, initialTheta=initialTheta, viewProgress=viewProgress, showPlot=showPlot)
        self.theta = self.ml.theta
        #p1 = list(data.columns[self.relatedCols])
        #print p1
        if showPlot:
            plot(data, '.'); show();

    def predictRegression2(self, data, quiet=False):
        self.qd._getMethod()

        #if len(self.theta) == 0:
        #    self.regression2(de=data)
        [data, self.dmean, self.dstd] = normalizeme(data, pinv=True)
        data = sigmoidme(data)

        # predict regression
        if quiet == False:
            print 'related cols'
            print self.relatedCols
            #print data
        #X = p_DataFrame(n_ones(len(data)), index=data.index).combine_first(data.ix[:, self.relatedCols].fillna(0))
        X = self.fixColumns(data, self.relatedCols, self.keyCol)
        if quiet == False:
            print list(X.columns)

        #s = len(X)-20
        s = len(X)-1
        #print X.ix[s:s+20, data.columns[[0]].insert(0,0)]
        #print X.ix[s+19,data.columns[self.relatedCols].insert(0,0)]
        #print theta
        #print 'shape theta'
        #print self.theta.shape
        #print len(self.relatedCols)
        ntheta = self.ml.theta.reshape(len(self.relatedCols),1)
        #ntheta = self.ml.theta.reshape(len(self.relatedCols)+1,1)
        #nX = X.ix[:,data.columns[self.relatedCols].insert(0,0)]
        nX = X
        #nX = X.ix[s,data.columns[self.relatedCols].insert(0,0)]
        
        if quiet == False:
            #print nX
            #print ntheta
            print 'theta shape:'
            print self.ml.theta.shape
            print self.ml.theta
            print 'X:'
            print X.shape
            print list(X.columns)
        
        predict = n_dot(nX, ntheta)
        if quiet == False:
            print ntheta
            print nX.ix[len(nX)-1, :]
        
        X.ix[:,data.columns[self.relatedCols].insert(0,0)]
        #self.ml.theta.reshape(len(self.relatedCols)+1,1)            
        
        #print self.dmean
        #print self.dstd
        predict = sigmoidmePinv(predict)
        predict = normalizemePinv(predict, self.ymean, self.ystd) #[self.keyCol]
        
        if quiet == False:
            #print self.dmean
            #print self.dstd
            #predict = sigmoidmePinv(predict)
            #predict = normalizemePinv(predict, self.dmean, self.dstd)[self.keyCol]
            print self.keyCol
            print predict
        return predict

    # real-time theta
    def predictFromTheta(self, df=None, nX=None, save=False):
        self.qd._getMethod()

        if type(nX) == type(None):
            nX = self.oq.getPricesLatest(df, self, trueprices=True)
            #print nX
        
        #print n_c_[n_ones(1), nX.ix[1:,:].get_values().T].T
        #print nX.shape
        #print n_dot(nX.T, theta)
        if type(self.theta) == type(p_DataFrame()):
            theta = self.theta.get_values()
        else:
            theta = self.theta
        nXbias = n_c_[n_ones(1), nX.ix[1:,:].get_values().T]
        #print nXbias
        #print theta
        #print nXbias.shape
        #print self.theta.shape
        
        val = 0
        try:
            val = n_dot( nXbias, self.theta )[0][0]
        except Exception as e:
            ''
            #print e
            #print 'eerr'
        if val != 0:
            self.nxps.append( val )
        
        if save == True:
            p_DataFrame(self.nxps).to_csv('/mldev/bin/datafeeds/nxps.csv')
        #plot(self.nxps);
        #show();
        #print self.nxps
        return val
 

class RealtimeChart:
    
    def __init__(self):
        
        ####
        # real time chart
        ####
        self.df = p_DataFrame()
        self.sw = StatWing()
        
        """
        # real time plot
        plt.axis([0, 2000, -0.41, -0.38])
        plt.ion()
        plt.show()
        """
        self.i = 0
        
        self.startPlotly()
        ####
        # end real time chart
        ####
        
    # source: http://stackoverflow.com/questions/4098131/how-to-update-a-plot-in-matplotlib
    def update(self, csvc):
        
        ####
        # real time chart
        ####
        self.df[csvc[0]] = [float(csvc[1])]
        nX =   self.df.transpose()
        y  = self.sw.predictFromTheta(nX=nX)
        
        try:
            imax = n_max(self.sw.nxps)
            imax = imax + n_std(self.sw.nxps)
        except Exception as e:
            print e
        try:
            imin = n_min(self.sw.nxps)
            imin = imin - n_std(self.sw.nxps)
        except Exception as e:
            print e
        """
        try:
            plt.axis([0, len(self.sw.nxps)+10, imin, imax])
        except Exception as e:
            print e
        plt.scatter(self.i, y)
        plt.draw()
        """
        if float(y) != 0:
            self.sendToPlotly(self.i, y)
        #time.sleedf
        
        self.i += 1
        ####
        # end real time chart
        ####
        
        #print nX 
        #time.sleep(0.9)
        #clear_output()
        
    def startPlotly(self):
        # auto sign-in with credentials or use py.sign_in()
        #py.sign_in('<plotly username>', '<plotly API key>')
        py.sign_in('cilixian', 'ks48f6mysz')
        trace1 = Scatter(
            x=[], 
            y=[], 
            #stream=dict(token='my_stream_id')
            stream=dict(token='dlun5nb9sr')
        )
        data = Data([trace1])
        py.plot(data)
        self.s = py.Stream('dlun5nb9sr')
        self.s.open()
        
    def sendToPlotly(self, x, y):
        #print 'x:'+str(x)
        print 'y:'+str(y)
        if self.i % 20 == 0:
             self.s.write(dict(x=x, y=y))
        #self.s.close()

def polarizePortfolio(df, fromCol, toCol, biasCol):
    """Adds an extra polarization column that separates fromCol between positive and negative
according to the status of the given bias column, the new values are placed ino toCol.

Parameters
----------
df : pandas DataFrame
fromCol : The originating column values to copy
toCol : The column to paste values into. 
        The values are converted to +ive or -ive (negative or positive) 
        according to the bias value of the respecoq.trade(1, 20, 'eu', 's')tive row.
biasCol : The column to check for bias

Example
-------
>>> df = p_DataFrame([['a','b','c'],['buy','sell','sell'],[1,2,3]], index=['pair', 'bias', 'amount']).transpose()
>>> print df
  pair  bias amount
0    a   buy      1
1    b  sell      2
2    c  sell      3

>>> print polarizePortfolio(df, 'amount', 'amountPol', 'bias')
  pair  bias amount  amountPol
0    a   buy      1          1
1    b  sell      2         -2
2    c  sell      3         -3


Applications
------------
This function can be called to generate a polarized target portfolio.
"""
    for i in range(len(df[biasCol])):
        if df.ix[i, biasCol].lower() == 'sell':
            df.ix[i, toCol] = df.ix[i, fromCol] * -1
        elif df.ix[i, biasCol].lower() == 'buy':
            df.ix[i, toCol] = df.ix[i, fromCol] * 1
    return df

def normalizeme(dfr, pinv=False):
    
    nmean = n_mean(dfr, axis=0)
    nstd = n_std(dfr, axis=0)
    #nmean = n_mean(dfr)
    #nstd = n_std(dfr)
    dfr = (dfr - nmean) / nstd
    #dfr = n_divide((dfr - nmean), nstd)
    if pinv == False:
        return dfr
    else:
        return [dfr, nmean, nstd]

def normalizemePinv(dfr, mean, std):
    
    #print (n_dot(data.get_values(),  dst['mean'].get_values().reshape(len(dst), 1) )) + dst['std']
    #print (n_dot(data.get_values(),  dmean.get_values().reshape(len(dst), 1) )) + dstd.get_values()
    ##print type(data)
    #print (data)
    ##print type(dmean)
    #print (dmean)
    ##print type(dstd)
    #print (dstd)
    #print (n_dot(n_array(data), dmean.reshape(len(dst), 1) )) + dstd
    
    dfr = (dfr * std) + mean
    return dfr

def normalizeme2(ds, index=None, columns=None):
    
    #ds = n_array(ds, dtype=float)
    if type(ds) == type(p_DataFrame([])):
        #print '0'
        dss = ds.get_values()
        index = ds.index
        columns = ds.columns
    if type(ds) == type(n_array([])):
    #    print 't1'
        dss = ds
    if type(ds) == type([]):
    #    print 't2'
        dss = n_array(ds, dtype=float)
    #print type(dss)
    #import sys
    #sys.exit()
    #print ds[0]
    # call fillna(method='bfill') on dataset before calling this method
    
    dss = dss / dss[0]
    dss = p_DataFrame(dss, index=index, columns=columns)
    return dss

def sigmoidme(dfr):
    return 1.0 / (1 + pow(n_e,-dfr))

def sigmoidmePinv(sigdfr):
    #sigdfr = sigdfr.fillna(0).get_values()
    #sigdfr = 1.0 / (1 + pow(n_e,-dfr))
    #return pow(n_e,-dfr) = (1.0 / pinv) - 1
    #return log10((1.0 / dfr.get_values()) - 1)
    #return n_log10((1.0/sigdfr)-1)/n_log10(n_e)
    #pow(n_e,-dfr) = (1.0 / pinv) - 1
    #/ n_log(n_e)
    return -n_divide(n_log10((n_divide(1.0, sigdfr))-1), n_log10(n_e))

def sharpe(dfr):
    ''

"""
def toCurrency(n):
    return '%2d' % n

def normalizeme(dfr):
    return ((dfr - mean(dfr))/std(dfr))

def sigmoidme(dfr):
    return 1.0 / (1 + pow(e,-dfr))

def sharpe(dfr):
    ''
"""

#quickPlot('GOOG/AMEX_OFI')
#quickPlot('BAVERAGE/USD')
def quickPlot(tks, headers=None, listcolumns=False, title=None):
    d = getDataFromQuandl(tks, index_col=0, dataset='', verbosity=3)
    if listcolumns:
        #print p_DataFrame(list(d.columns))
        for i in enumerate(list(d.columns)):
            print i
    d = d.bfill().ffill()
    d = normalizeme(d)
    d = sigmoidme(d)
    
    if type(headers) == type([]):
        d = d.ix[:, headers] #.transpose()
    
    d.plot(logy=False)
    if type(headers) == type([]):
        #hdrs = d.columns[headers]
        #hdrs = list(d.columns[headers])
        try:        
            hdrs = list(d.columns[[headers]])
            legend(hdrs, 2)
        except Exception as e:
            print e
    #else:
    #    legend(None, 2)
    #print type(title)
    #if title:
    #    title(title)
    show()
    return d

def writeQuandlSearchLog(stri):
    suffix='.csv'
    path='data/quandl'
    fname = path+'/searches'+suffix    
    fp = open(fname,'a')
    fp.write(stri+"\n")
    fp.close()    
    #fp = open(fname)
    #print fp.read()
    #fp.close()
    
def searchQuandl(query, mode='manifest', headers=None, returndataset=False, cache=True, listcolumns=False):
    debug('searching: '+query, verbosity=9)
    suffix='.csv'
    path='data/quandl/searches/'
    fquery = re.sub(re.compile(r'\/'),'-',query)
    fname = path+fquery+suffix
    mkdir_p(path)
    import time as t
    tt = t.time()
    try:
        if cache == False:
            raise IOError
        fp = open(fname, 'r')
        res = j.loads(fp.read())
        fp.close()
        writeQuandlSearchLog(str(tt)+':cached:'+str(query)+' to '+fname)
    except IOError, e:
        try:
            writeQuandlSearchLog(str(tt)+':searched:'+str(query)+' to '+fname)
            res = q.search(query, verbose=False)
            fp = open(fname, 'w')
            fp.write(j.dumps(res))
            fp.close()
            print 'saved to: '+fname
        except q.DatasetNotFound, f:
            print f
    tks = []
    ds = None
    for i in res:
        #print i.keys()
        #print i
        tk = i['code']
        
        if mode == 'manifest':
            print tk
            print i['name']
            print i['desc']
            print '---------'
            print
            """
            try:
                dsg = getDataFromQuandl(tk, dataset='')
            except e:
                print e
            """
            #print i['freq']
            #print i['name']
            #print i['desc']
            #print
        if mode == 'plot':
            print tk
            #print i['desc']
            ds = quickPlot(str(tk.strip()), listcolumns=listcolumns, title=query)
        if mode == 'combineplot':
            tks.append(str(tk))
    if mode == 'combineplot':
        ds = quickPlot(tks, headers=headers, listcolumns=listcolumns, title=query)
    if returndataset == True:
        return ds
    else:
        return len(res)

def fetchFromQuandlSP500():
    sp = p_read_csv('data/quandl/SP500.csv')
    #for i in list(sp.sort(columns='Name').ix[0:10,['Code']].get_values().reshape(1,15)[0]):
    for i in range(0, len(sp)):
        getDataFromQuandl(sp.ix[i,'Code'], dataset='SP500')

def quandlCode2DatasetCode(tk, hdir='./', include_path=True, suffix='.csv'):
    try:
        mt = re.match(re.compile(r'(.*)\/(.*)_(.*)', re.S), tk).groups()
        path = hdir+'/'+mt[0]+'/'+mt[1]
        if include_path:
            fname = path+'/'+mt[0]+'-'+mt[1]+'_'+mt[2]+suffix
        else:
            fname = mt[0]+'-'+mt[1]+'_'+mt[2]+suffix            
        #fname = path+'/'+mt[2]+'.csv'
    except Exception as e:
        print e
        mt = re.match(re.compile(r'(.*)\/(.*)', re.S), tk).groups()
        path = hdir+'/'+mt[0]+'/'+mt[1]
        if include_path:
            fname = path+'/'+mt[0]+'-'+mt[1]+suffix
        else:
            fname = mt[0]+'-'+mt[1]+suffix
    return [fname,path]
        
def getDataFromQuandl(tk, dataset='', index_col=None, verbosity=1, plot=False, style='-', columns=['Close'], tail=False):
    # if string
    df = p_DataFrame([])
    
    if type(tk) == type(''):
        debug('fetching '+tk, verbosity=verbosity)
        [fname, path] = quandlCode2DatasetCode(tk, hdir='data/quandl/'+dataset, include_path=True, suffix='.csv')
        mkdir_p(path) # alternative python3: os.makedirs(path, exist_ok=True)
        
        try:
            df = p_read_csv(fname, index_col=index_col)
        except IOError, e:
            try:
                df = q.get(tk)
                df.to_csv(fname)
                print 'saved to: '+fname
            except q.DatasetNotFound, f:
                print f
        if index_col == None:
            df = df.set_index(df.columns[0])
    
    # if list
    if type(tk) == type([]):
        # concatenate ticker code to column value
        dfs = []
        for i in range(0, len(tk)):
            dfs.append(getDataFromQuandl(tk[i], index_col=0, dataset='', verbosity=8))
            #tk[i] = quandlCode2DatasetCode(tk[i], include_path=False, suffix='')[0]
            r1 = n_array([tk[i]+' '], dtype=object)
            r2 = n_array(list(dfs[i].columns), dtype=object)
            dfs[i].columns = r1+r2
            #print list(dfs[i].columns)    
        for i in range(0, len(dfs)):
            df = df.combine_first(dfs[i])
    #if type(columns) == type([]):
    cols = []
    if type(tk) == type([]):
        for i in xrange(len(tk)):
            cols.append("{0} {1}".format(tk[i], columns))
        df = df.ix[:,cols]
    
    if tail > 0:
        df = df.ix[:,:].tail(tail)
    if plot == True:
        df.plot(style=style); show();
    return df
    
# source: https://www.quandl.com/c/markets/exchange-rates-versus-eur
# quandl js parser: for (var i = 2; i<=15; i++) {var buff = ''; $($x('//*[@id="ember894"]/div['+i+']/table/tbody/tr/td[3]/a/@href')).each(function(e,o) {buff += ' '+o.value.replace(/\/CURRFX\//g, '');}); console.log('# '+i); console.log('pa += \''+buff+'\'');}

# source: https://www.quandl.com/c/usa/usa-currency-exchange-rate
# quandl js parser: for (var i = 2; i<=15; i++) {var buff = ''; $($x('//*[@id="ember894"]/div['+i+']/table/tbody/tr/td[3]/a/@href')).each(function(e,o) {buff += ' '+o.value.replace(/\/CURRFX\//g, '');}); console.log('# '+i); console.log('pa += \''+buff+'\'');}

# getDataFromQuandlBNP(pa, curr)
def getDataFromQuandlBNP(pa, curr, authtoken=None, noUpdate=False): # curr = EUR || USD, etc.
    pa = pa.split(' ')
    
    tk = []
    tl = []
    for i in pa:
        tk.append('BNP/'+i)
        tl.append('BNP.'+i+' - '+i[0:3]+'/'+i[3:6])
    #print tk
    #print tl
    
    fname = '/mldev/bin/data/quandl/BNP.'+curr+'.csv'
    #print fname
    try:
        da = p_read_csv(fname, index_col=0)
        
        # if column mismatch then update from source instead of caching
        """
        if len(tk) != len(da.columns):
            print len(tk)
            print len(da.columns)
            print 'tickers and columns not matching'
            print tk
            print list(da.columns)
            raise IOError
        """
        if noUpdate == True:
            raise IOError
        
        print 'updating..'
        #trim_start = str(list(da.tail(1).ix[:,0])[0])
        trim_start = da.index[len(da)-1]
        trim_end = str(dd.datetime.today().year).zfill(4) + '-' + str(dd.datetime.today().month).zfill(2) + '-' + str(dd.datetime.today().day).zfill(2)
        print trim_start
        print trim_end
        ts = trim_start.split('-')
        te = trim_end.split('-')
        #print ts
        #print te
        #a = dd.date(int(ts[0]), int(ts[1]), int(ts[2])-1)
        
        
        
        # source: http://stackoverflow.com/questions/1506901/cleanest-and-most-pythonic-way-to-get-tomorrows-date
        a = dd.date(int(ts[0]), int(ts[1]), int(ts[2])) - dd.timedelta(1) # minus 1 day
        #b = dd.date(int(te[0]), int(te[1]), int(te[2]))
        b = dd.date(int(te[0]), int(te[1]), int(te[2])) + dd.timedelta(1) # plus 1 day
        print 'a {0}'.format(a)
        print 'b {0}'.format(b)
        days = (b-a).days        
        print days
        
        nowp             = dd.datetime.now()
        #lastp            = dd.datetime(nowp.year, nowp.month, nowp.day-1, 18)
        lastp            = dd.datetime(nowp.year, nowp.month, nowp.day, 18) - dd.timedelta(1)
        secondsfromlastp = (nowp - lastp).total_seconds()
        print lastp
        print nowp
        print secondsfromlastp
        if secondsfromlastp > 86400: # 60 * 60 * 24 hardcoded
            print 'update'
        #return        
        if days > 0:
            qq = QoreQuant()            
            print 'fetching from {0} to {1}'.format(a, b)
            print 'greater than 0 days'
            #d = q.get(tk[0:2], authtoken=authtoken, trim_start=a, trim_end=b)
            #d = q.get(tk[0:2], authtoken=authtoken, transformation="diff")
            #d = q.get(tk[0:2], authtoken=authtoken, collapse="annual")
            d = q.get(tk, authtoken=qq.quandlAuthtoken, rows=days, sort_order='desc', trim_start=a, trim_end=b).sort(ascending=True)
            print d
            
            # combine the cache and new data into one dataset
            d = da.combine_first(d)
            d.to_csv('data/quandl/BNP.'+curr+'.csv')
        else:
            print 'equal 0 days'
            d = da
    except IOError, e:
        print e
        print 'getting from quandl..'
        print 'get all from quandl'
        #d = q.get(tk, authtoken=authtoken)
        #d = q.get(tk, returns="numpy")
        #d = q.get(["NSE/OIL.4","WIKI/AAPL.1"])
        #d = q.get("NSE/OIL", trim_start="yyyy-mm-dd", trim_end="yyyy-mm-dd")
        #print d
        #d.to_csv('data/quandl/BNP.'+curr+'.csv')
        
        print 'reading from '+fname
        d = p_read_csv(fname, index_col=0)
        
    #plot(d.ix[:,tl])
    #print d.columns
    print 'cols1'
    
    return d

def testMicrofinance():
    fm = FinancialModel()
    #fm.test()
    
    years    = 4
    months   = 12 * years + 1
    days     = 250 * years + 1
    ic       = 100
    myrates  = []
    
    # 12% monthly
    myrates.append(12)
    # 1% daily, monthly equivalent
    myrates.append(fm.rateToCompoundedPercentage(1, 20))
    # 7% APR monthly equivalent
    myrates.append(fm.rateToCompoundedPercentage(fm.compoundedPercentageIntegral(7, 250), 20))
    
    myratetitles = []
    
    periods = n_array(range(0,months))
    df = p_DataFrame(periods)
    myratetitles.append('period')
    for i in xrange(0,len(myrates)):
        myratetitles.append('vested_'+str(int(myrates[i]))+'_monthly')
        df[myratetitles[i]] = fm.compoundVestedCapital(myrates[i], periods)[0]
    
    print df
    
    plot(df)
    print myratetitles
    legend(myratetitles, 2)
    
    """
    plot(vc)
    title('Vested Capital')
    show()
    """

def testGetDataFromQuandl():
    tks = []
    tks.append('LBMA/GOLD') # Gold
    tks.append('DOE/RBRTE') # Europe Brent Crude Oil Spot Price FOB
    tks.append('CHRIS/CME_CL1') # Crude Oil Futures, Continuous Contract #1 (CL1) (Front Month)
    tks.append('BAVERAGE/USD') # USD/BITCOIN Weighted Price
    #d = q.get(tks)
    d8 = getDataFromQuandl(tks, index_col=0, dataset='', verbosity=8)
    #d8.plot()
    #show()
    print d8.bfill().ffill()


def getDatasetEUR(noUpdate=False, returnPairs=False):
    pa = ''
    # 2
    pa += 'EURUSD EURJPY EURGBP EURCHF EURCAD EURAUD EURNZD EURSEK EURNOK EURBRL EURCNY EURRUB EURINR EURTRY EURTHB EURIDR EURMYR EURMXN EURARS EURDKK EURILS EURPHP'
    # 3
    pa += ' EURDKK EURHUF EURISK EURNOK EURSEK EURCHF EURTRY EURGBP'
    # 4
    pa += ' EURALL EURBAM EURBGN EURHRK EURCZK EURMKD EURPLN EURRON EURRSD'
    # 5
    pa += ' EURAMD EURAZN EURBYR EURGEL EURKZT EURKGS EURLVL EURLTL EURMDL EURRUB EURTJS EURTMT EURUAH EURUZS'
    # 6
    pa += ' EURBND EURKHR EURCNY EURHKD EURIDR EURJPY EURLAK EURMYR EURMNT EURMMK EURKPW EURPHP EURSGD EURKRW EURTHB EURVND'
    # 7
    pa += ' EURAFN EURBDT EURBTN EURINR EURLKR EURMVR EURNPR EURPKR'
    # 8
    pa += ' EURDZD EURBHD EURDJF EUREGP EURIRR EURIQD EURILS EURJOD EURKWD EURLBP EURLYD EURMAD EUROMR EURQAR EURSAR EURSYP EURTND EURAED EURYER'
    # 9
    pa += ' EURAOA EURBIF EURXOF EURBWP'
    # 10
    pa += ' EURXAF EURCDF EURKMF EURCVE EURETB EURGHS EURGNF EURGMD EURKES EURLRD EURLSL EURMGA EURMZN EURMRO EURMUR EURMWK EURNAD EURNGN EURRWF EURSDG EURSLL EURSOS EURSTD EURSZL EURSCR EURTZS EURUGX EURZAR EURZMW'
    # 11
    pa += ' EURUSD EURCAD EURMXN'
    # 12
    pa += ' EURXCD EURBSD EURBBD EURCUP EURDOP EURHTG EURJMD EURTTD'
    # 13
    pa += ' EURBZD EURCRC EURGTQ EURHNL EURNIO EURPAB'
    # 14
    pa += ' EURARS EURBOB EURBRL EURCLP EURCOP EURGYD EURPYG EURPEN EURSRD EURUYU EURVEF'
    # 15
    pa += ' EURAUD EURFJD EURNZD EURPGK EURWST EURSBD EURTOP EURVUV'
    
    if returnPairs == True:
        return pa
    else:
        return getDataFromQuandlBNP(pa, 'EUR', noUpdate=noUpdate)

def getDataUSD(noUpdate=False):
    pa = ''
    # 2
    pa += ' USDEUR USDJPY USDGBP USDCHF USDCAD USDAUD USDNZD USDSEK USDNOK USDBRL USDCNY USDRUB USDINR USDTRY USDTHB USDIDR USDMYR USDMXN USDARS USDDKK USDILS USDPHP'
    # 3
    pa += ' USDEUR USDDKK USDHUF USDISK USDNOK USDSEK USDCHF USDTRY USDGBP'
    # 4
    pa += ' USDALL USDBAM USDBGN USDHRK USDCZK USDMKD USDPLN USDRON USDRSD'
    # 5
    pa += ' USDAMD USDAZN USDBYR USDGEL USDKZT USDKGS USDLVL USDLTL USDMDL USDRUB USDTJS USDTMT USDUAH USDUZS'
    # 6
    pa += ' USDBND USDKHR USDCNY USDHKD USDIDR USDJPY USDLAK USDMYR USDMNT USDMMK USDKPW USDPHP USDSGD USDKRW USDTHB USDVND'
    # 7
    pa += ' USDAFN USDBDT USDBTN USDINR USDLKR USDMVR USDNPR USDPKR'
    # 8
    pa += ' USDDZD USDBHD USDDJF USDEGP USDIRR USDIQD USDILS USDJOD USDKWD USDLBP USDLYD USDMAD USDOMR USDQAR USDSAR USDSYP USDTND USDAED USDYER'
    # 9
    pa += ' USDAOA USDBIF USDXOF USDBWP'
    # 10
    pa += ' USDXAF USDCDF USDKMF USDCVE USDETB USDGHS USDGNF USDGMD USDKES USDLRD USDLSL USDMGA USDMZN USDMRO USDMUR USDMWK USDNAD USDNGN USDRWF USDSDG USDSLL USDSOS USDSTD USDSZL USDSCR USDTZS USDUGX USDZAR USDZMW'
    # 11
    pa += ' USDCAD USDMXN'
    # 12
    pa += ' USDXCD USDBSD USDBBD USDCUP USDDOP USDHTG USDJMD USDTTD'
    # 13
    pa += ' USDBZD USDCRC USDGTQ USDHNL USDNIO USDPAB'
    # 14
    pa += ' USDARS USDBOB USDBRL USDCLP USDCOP USDGYD USDPYG USDPEN USDSRD USDUYU USDVEF'
    # 15
    pa += ' USDAUD USDFJD USDNZD USDPGK USDWST USDSBD USDTOP USDVUV'
    
    du = getDataFromQuandlBNP(pa, 'USD', noUpdate=noUpdate)
    return du

def getDataJPY(noUpdate=False):
    pa = ''
    # 2
    pa += ' USDJPY AUDJPY CADJPY CHFJPY EURJPY HKDJPY GBPJPY NZDJPY SGDJPY TRYJPY ZARJPY '
    
    res = getDataFromQuandlBNP(pa, 'JPY', noUpdate=noUpdate)
    return res

def getDataAUD(noUpdate=False):
    pa = ''
    # 2
    pa += ' AUDEUR AUDJPY AUDGBP AUDCHF AUDCAD AUDUSD AUDNZD AUDSEK AUDNOK AUDBRL AUDCNY AUDRUB AUDINR AUDTRY AUDTHB AUDIDR AUDMYR AUDMXN AUDARS AUDDKK AUDILS AUDPHP'
    # 3
    pa += ' AUDEUR AUDDKK AUDHUF AUDISK AUDNOK AUDSEK AUDCHF AUDTRY AUDGBP'
    # 4
    pa += ' AUDALL AUDBAM AUDBGN AUDHRK AUDCZK AUDMKD AUDPLN AUDRON AUDRSD'
    # 5
    pa += ' AUDAMD AUDAZN AUDBYR AUDGEL AUDKZT AUDKGS AUDLVL AUDLTL AUDMDL AUDRUB AUDTJS AUDTMT AUDUAH AUDUZS'
    # 6
    pa += ' AUDBND AUDKHR AUDCNY AUDHKD AUDIDR AUDJPY AUDLAK AUDMYR AUDMNT AUDMMK AUDKPW AUDPHP AUDSGD AUDKRW AUDTHB AUDVND'
    # 7
    pa += ' AUDAFN AUDBDT AUDBTN AUDINR AUDLKR AUDMVR AUDNPR AUDPKR'
    # 8
    pa += ' AUDDZD AUDBHD AUDDJF AUDEGP AUDIRR AUDIQD AUDILS AUDJOD AUDKWD AUDLBP AUDLYD AUDMAD AUDOMR AUDQAR AUDSAR AUDSYP AUDTND AUDAED AUDYER'
    # 9
    pa += ' AUDAOA AUDBIF AUDXOF AUDBWP'
    # 10
    pa += ' AUDXAF AUDCDF AUDKMF AUDCVE AUDETB AUDGHS AUDGNF AUDGMD AUDKES AUDLRD AUDLSL AUDMGA AUDMZN AUDMRO AUDMUR AUDMWK AUDNAD AUDNGN AUDRWF AUDSDG AUDSLL AUDSOS AUDSTD AUDSZL AUDSCR AUDTZS AUDUGX AUDZAR AUDZMW'
    # 11
    pa += ' AUDUSD AUDCAD AUDMXN'
    # 12
    pa += ' AUDXCD AUDBSD AUDBBD AUDCUP AUDDOP AUDHTG AUDJMD AUDTTD'
    # 13
    pa += ' AUDBZD AUDCRC AUDGTQ AUDHNL AUDNIO AUDPAB'
    # 14
    pa += ' AUDARS AUDBOB AUDBRL AUDCLP AUDCOP AUDGYD AUDPYG AUDPEN AUDSRD AUDUYU AUDVEF'
    # 15
    pa += ' AUDFJD AUDNZD AUDPGK AUDWST AUDSBD AUDTOP AUDVUV'
    # 16
    #pa += ' /BITCOIN/MTGOXAUD /WGC/GOLD_DAILY_AUD'
    
    da = getDataFromQuandlBNP(pa, 'AUD', noUpdate=noUpdate)
    
def quandlSweepDatasources():
    import StringIO as sio
    df = p_read_csv('/mldev/lib/crawlers/finance/quandl.scrapy/datasources_quandl.csv')
    print df['code']
    #print df.ix[:,['name','code','datasets','url']]
    return 
    for i in xrange(len(df.ix[:,['code']])):
        dsets = int(floor(float(df.ix[i,'datasets'].replace(',','')) / 300))
        print dsets
        for j in xrange(dsets):
            print i
            print j
            break
            url = 'http://www.quandl.com/api/v2/datasets.csv?query=*&source_code={0}&per_page=300&page={1}&auth_token=WVsyCxwHeYZZyhf5RHs2'
            print 'fetching url:'+url
            c = fetchURL(url.format(df.ix[i,['code']]['code'], j), mode='')
            """
            s = sio.StringIO()
            s.write(c)
            s.seek(0)
            print p_read_csv(s)
            """
            #fp = open('', 'a')
            #fp.write(c+'\n')
            #c.split('\n')      
            break

def quandlGetDatasetSourceList(source_code, pg=1):    
    dsets = fetchURL('http://www.quandl.com/api/v2/datasets.json?query=*&source_code='+source_code+'&per_page=300&page='+str(pg))
    print dsets.keys()
    print dsets['sources']
    #print dsets['sources']['datasets_count']
    print dsets['sources'][0]['datasets_count']
    return dsets

def quandlGetPreMunge(c, fromCol=None, toCol=None):
    d = q.get(c, authtoken="WVsyCxwHeYZZyhf5RHs2")
    print c
    print list(d.columns)
    d = normalizeme(d)
    d = sigmoidme(d)
    if fromCol != None and toCol != None:
        d[toCol] = d.ix[:,[fromCol]]
    print '----'
    return d

class CryptoCoinBaseClass:
    
    def __init__(self):
        ''
        
class CoinMarketCap:
    
    def __init__(self):
        ''

    def updateData(self):
        # source: http://coinmarketcap-nexuist.rhcloud.com/
        t = fetchURL('http://coinmarketcap-nexuist.rhcloud.com/api/all', cachemode='a', fromCache=False, mode='json')

class btce(CryptoCoinBaseClass):
    def getTicker(self, code):
        # eg. code = btc_usd
        url = 'https://btc-e.com/api/3/ticker/'+code
        r = fetchURL(url, mode='json')
        #print r
        ky = r[code].keys()
        #print ky
        #print r[code].values()
        r = p_DataFrame(r[code].values(), index=ky, columns=[code]).transpose()
        return r.ix[:,['sell','buy','last','vol','vol_cur']].transpose()
    
    def getRarestCryptoCoins(self):
        # linked from: http://crypt.la/2013/12/14/list-of-the-fastest-cryptocurrencies/
        # source: http://crypt.la/2013/12/16/list-of-the-top-25-rarest-cryptocurrencies/
        t = """Currency	Code	Total Circulation 
Onecoin	ONC	1
Bestcoin	BEST	1,000,000
Cryptogenic Bullion	CGB	1,000,000
GoldPressedLatinum	GPL	1,000,000
Peoplecoin	PPL	1,440,000
CryptoBuck	BUK	10,000,000
Mincoin	MNC	10,000,000
Ecocoin	ECO	10,200,000
CrimeCoin	CRM	100,000
ProtoShares	PTS	2,000,000
Sauron Rings	SAU	20,000
BitGem	BTG	23,000
Unobtanium	UNO	250,000
Jupitercoin	JPC	3,700,000
Cryptobits	CYB	4,000,000
Anoncoin	ANC	4,200,000
Diamond	DMD	4,300,000
ExtremeCoin	EXC	5,000,000
Basecoin	BAC	6,000,000
Frozen	FZ	7,700,000
Doubloons	DBL	8,000,000
Bitbar	BTB	8,500
PhilosopherStone	PHS	8,891,840
Lovercoin	LVC	9,000,000
"""
        print t
    
    def getFastestCryptoCoins(self):
        # linked from: http://bitcoin.stackexchange.com/questions/24636/fastest-cryptocurrency
        # source: http://crypt.la/2013/12/14/list-of-the-fastest-cryptocurrencies/
        t = """Coin	Symbol	Confirmations Required	Transaction Speed (in seconds)
Fastcoin	FST	4	48
Worldcoin	WDC	4	60
Krugercoin	KGC	6	90
Richcoin	RCH	3	90
Realcoin	REC	3	90
Digitalcoin	DGC	5	100
Emerald	EMD	5	100
Xencoin	XNC	5	100
Asiccoin	ASC	4	120
Infinitecoin	IFC	4	120
Alphacoin	ALP	5	150
Elephantcoin	ELP	5	150
Quarkcoin	QRK	5	150
Valuecoin	VLC	5	150
Argentum	ARG	5	160
Hypercoin	HYC	4	160
Colossuscoin	COL	7	175
Casinocoin	CSC	6	180
Franko	FRK	6	180
Orbitcoin	ORB	6	180
Florincoin	FLO	5	200
Stablecoin	SBC	5	200
Galaxycoin	GLX	7	210
Zetacoin	ZET	7	210
Anoncoin	ANC	6	240
Novacoin	NVC	4	240
Yacoin	YAC	4	240
Globalcoin	GLC	7	280
Bbqcoin	BQC	5	300
Elacoin	ELC	5	300
Ezcoin	EZC	5	300
Grandcoin	GDC	7	315
Spots	SPT	5	350
Diamond	DMD	6	360
Datacoin	DTC	6	360
Lebowskis	LBW	6	360
Redcoin	RED	6	360
Primecoin	XPM	6	360
Netcoin	NET	7	420
Nanotoken	NAN	5	450
Powercoin	PWC	10	450
Cryptogenicbullion	CGB	8	480
Terracoin	TRC	4	480
Americancoin	AMC	4	600
Litecoin	LTC	4	600
Nibble	NIB	4	600
Feathercoin	FTC	5	750
Megacoin	MEC	5	750
Nucoin	NUC	5	750
Phenixcoin	PXC	5	750
Deutsche eMark	DEM	7	840
Noirbits	NRB	7	840
Cosmoscoin	CMC	5	1050
Betacoin	BET	5	1200
Tagcoin	TAG	5	1200
Weedcoin	WEC	5	1200
Unobtanium	UNO	7	1260
Cinnamoncoin	CIN	5	1500
Craftcoin	CRC	5	1500
Protoshares	PTS	6	1800
Bitbar	BTB	4	2400
Bitcoin	BTC	4	2400
Bitgem	BTG	4	2400
Peercoin	PPC	6	3600
"""
        tis = p_read_csv(sio.StringIO(t), delimiter='\t', index_col=0).ix[:,[0,1,2]]
        tis = tis.sort('Transaction Speed (in seconds)', ascending=True)
        #print tis.ix[0:3,[0,2]]
        #print tis
        tis = list(tis.ix[:,[0]].transpose().get_values()[0])
        """
        for i in list(n_array(self.pk, dtype=string0)):
            print i.split('_')
            for j in range(0,len(fastestCoins)):
                #print type(fastestCoins[j])
                try:
                    fc = fastestCoins[j].lower()
                    #print 'fastest:'+fc
                    #if i[0:3] == fc:
                    #    print i[0:3]
                    #if i[4:7] == fc:
                    #    print i[4:7]
                except Exception as e:
                    print e
        """
        return tis
    
    def __init__(self):
        self.pk = []
        self.exchanges = ['ex1','ex2','ex3','ex4']; #print exchanges;
        self.check()

    def check(self):
        if len(self.pk) == 0: self.getCurrencies()
    
    def getCurrencies(self):
        url = 'https://btc-e.com/api/3/info'
        r = fetchURL(url, mode='json')

        try:
            #print p_DataFrame(list(r['pairs']['ltc_gbp']))
            pk = r['pairs'].keys()
            pv = r['pairs'].values()
            #print pk
            li = []
            for i in pv:
                li.append(i.values())
            li = p_DataFrame(li, index=pk, columns=pv[0].keys())
            self.pk = pk
            return li
            #pk = p_DataFrame(pk, index=pk, columns=['pair'])
            #print pk
            #print pk.combine_first(li)
            #print r
        except TypeError, e:
            debug(e)
    
    def getRatesOnExchange(self):
        self.check()
        pc = p_DataFrame()
        for i in self.pk:
            debug(i)
            try:
                ti = self.getTicker(i); #print ti.transpose()
                pc = pc.combine_first(ti)
            except Exception as e:
                print e
        #print pc
        return pc.transpose()
    
    def getDepth(self, code, doPlot=True):
        debug('Starting getTDepth: '+code)
        # eg. code = btc_usd
        url = 'https://btc-e.com/api/3/depth/'+code
        r = fetchURL(url, mode='json')
        #print r
        try:        
            ky = r[code].keys()    
            #print ky
            rb = p_DataFrame(r[code]['bids'], columns=['bp','ba'])
            ra = p_DataFrame(r[code]['asks'], columns=['ap','aa'])
            #print rb
            #print ra
            r = rb.combine_first(ra)
            #r = r.ix[:,[]]
            if doPlot == True:
                r1 = r
                r1 = r1.ix[:,['ap','bp']]
                plot(r1); title(code+' orders'); legend(r1.columns,2); show()
        
                r2 = r
                r2 = normalizeme(r2)
                r2 = sigmoidme(r2)
                r2 = r2.ix[:,:]
                plot(r2); title(code+' orders'); legend(r2.columns,2); show()
            debug('Ending getDepth:'+code)
            return r
        except TypeError, e:
            debug(e)

    def parseTrades(self, r, code, doPlot=True):
        #print r
        try:
            ky = r[code][0].keys()
            #print ky
            li = []
            for i in r[code]:
                li.append(i.values())
            ro = p_DataFrame(li, columns=ky)
            r = ro.ix[:,['price','amount']]
            #print r
            """
            rb = p_DataFrame(r[code]['bids'], columns=['bp','ba'])
            ra = p_DataFrame(r[code]['asks'], columns=['ap','aa'])
            print rb
            print ra
            r = rb.combine_first(ra)
            print r
            #r = r.ix[:,[]]
            """
            r1 = r
        #    r1 = normalizeme(r1)
        #    r1 = sigmoidme(r1)
            if doPlot == True:
                r1 = r1.ix[:,['price']]
                plot(r1); title(code+' trades'); legend(r1.columns,2); show()
            debug('Ending getTrades:'+code)
            return ro
        except TypeError, e:
            debug(e)
    
    def getTrades(self, code, doPlot=True):
        debug('Starting getTrades: '+code)
        # eg. code = btc_usd
        url = 'https://btc-e.com/api/3/trades/'+code
        r = fetchURL(url, mode='json', cachemode='a')
        #r = fetchFromCache(url)
        ro = self.parseTrades(r, code, doPlot)
        return ro

    def getArbTable(self, pk):
        self.check()
        arbtable1 = n_random.randn(len(pk)*len(self.exchanges)).reshape(len(pk),len(self.exchanges));
        return arbtable1

    def getArbRates(self, doPlot=False):
        #print pk
        arbtable1 = self.getArbTable(self.pk)
        rarb = p_DataFrame(arbtable1, index=self.pk, columns=self.exchanges);
        #print rarb; print;
        
        ms = []
        arbHdr = ['sell','buy','arbitrageRate']
        arbRates = p_DataFrame([])
        for i in range(0,len(self.pk)):
        #for i in range(0,2):
            ind = i
            debug(self.pk[ind])
            m = rarb.ix[self.pk[ind]]
            debug(m)
            m = p_DataFrame(n_array(m).reshape(len(m),1) / n_array(m) * 100 - 100, index=self.exchanges, columns=self.exchanges); 
            debug(m); debug('');
            m1 = n_max(m,0); #print m1;
            exhds = list(m1.index)
            #print (n_nonzero(m == m1))
            #print (n_nonzero(m1 == n_max(m1)))
            maxIndx = n_max(n_nonzero(m1 == n_max(m1)))
            maxNum = n_max(m1,0); #print maxNum;
            indx = (n_nonzero(n_array(m == maxNum, dtype=int)))
            arbRate = p_DataFrame([exhds[indx[0][0]], exhds[indx[1][0]], maxNum], index=arbHdr, columns=[self.pk[ind]])
            arbRates = arbRates.combine_first(arbRate)
            debug(arbRate.transpose())
            #m = normalizeme(m)
            if doPlot == True:
                plot(m,'-')
                #scatter(m)
                title(self.pk[ind]); legend(m.columns,2); show();
            ms.append(m.get_values().tolist())
        #print ms
        #scatter(ms[0],ms[1]); show();
        debug(arbRates.transpose())
        return arbRates
        
    def getFastestCryptoCoinArbitrage(self):
        # show the fastest coin to arbitrage
        try:
            arr
        except Exception as e:
            print e
            arr = self.getMostProfitablePair()
        arrSortedAR = arr.sort('arbitrageRate', ascending=False)
        print p_DataFrame(arrSortedAR.ix[list(arrSortedAR.ix[:,'p1']).index(self.p1), :]).transpose(); print
        print p_DataFrame(arrSortedAR.ix[list(arrSortedAR.ix[:,'p2']).index(self.p2), :]).transpose()
    
    def getMostProfitablePair(self):
        fastestCoins = self.getFastestCryptoCoins()
        fcs = []
        try:
            arbRates
        except Exception as e:
            print e
            arbRates = self.getArbRates()
        arr = arbRates.transpose()
        po1 = []; po2 = []
        for row in (n_array(arr.index, dtype=string0)):
            po1.append(row[0:3])
            po2.append(row[4:7])
        arr['p1'] = po1
        arr['p2'] = po2
        for i in range(0,len(arr)):
            #if arr.ix[i,'p1']
            try: arr.ix[i,'p11'] = fastestCoins.index(arr.ix[i,'p1'].upper())
            except Exception as e:
                print e
            try: arr.ix[i,'p22'] = fastestCoins.index(arr.ix[i,'p2'].upper())
            except Exception as e:
                print e
        arr1 = arr.sort('p11', ascending=True);
        arr2 = arr.sort('p22', ascending=True);
        self.p1 = arr1.ix[0,'p1']; debug(self.p1)
        self.p2 = arr2.ix[0,'p2']; debug(self.p2)
        debug(arr)
        return arr
    
    def updateData(self):
        # Create threads
        # source: http://pymotw.com/2/threading/
        for i in self.pk:                
            t0 = threading.Thread(target=self.getCurrencies)
            t0.daemon = False
            t0.start()
            t1 = threading.Thread(target=self.getRatesOnExchange)
            t1.daemon = False
            t1.start()
            t2 = threading.Thread(target=self.getTrades, args=(i, False,))
            t2.daemon = False
            t2.start()
            t3 = threading.Thread(target=self.getDepth, args=(i, False,))
            t3.daemon = False
            t3.start()
           #print "Error: unable to start thread"
        #while 1:
        #   pass

class CryptoCoin:
    
    def __init__(self):
        ''
    
    def updateData(self):
        
        b = btce()
        b.updateData()
        
        sh = ShapeShift()
        sh.updateData()
        
        # coinmarket updater
        c = CoinMarketCap()
        c.updateData()

class ShapeShift(CryptoCoinBaseClass):
    def __init__(self):
        ''
    
    def updateData(self):
        urls = 'btc, ltc, ppc, drk, doge, nmc, ftc, blk, nxt, btcd, qrk, rdd, nbt'
        url = re.sub(re.compile(r',', re.S), '', urls).split(' ')
            
        """
        abc = 'a b c d e f g h i j k l m n o p q r s t u v w x y z'.split(' ')
        #rin = p_DataFrame(n_int0(n_abs(n_random.randn(26)*10)))
        abc = list(it.permutations(abc, 3))
        abc = n_array(abc).tolist()
        li = []
        for i in abc[0:10]:
            li.append(''.join(i))
        """
        
        def fetchURLThread(url):
            try:
                debug('fetching:'+url)
                fetchURL(url, cachemode='a')
            except Exception as e:
                print e
        
        li = url
        li = list(it.permutations(li, 2))
        li = n_array(li).tolist()
        lis = []
        for i in li:
            lis.append('_'.join(i))
        for i in lis:
            # doc source: https://shapeshift.io/api.html#rate
            """
            url: shapeshift.io/rate/<pair>
            method: GET
            
            <pair> is any valid coin pair such as btc_ltc or ltc_btc
            
            Success Output:
              
                {
                    "pair" : "btc_ltc",
                    "rate" : "70.1234"
                }
            """
            url = 'http://shapeshift.io/rate/'+i
            t = threading.Thread(target=fetchURLThread, args=[url])
            t.daemon = False
            t.start()
            
    def depositLimit():
        # source: https://shapeshift.io/api.html#deposit-limit
        """
        url: shapeshift.io/limit/<pair>
        method: GET
        
        <pair> is any valid coin pair such as btc_ltc or ltc_btc
        
        Success Output:
            {
                "pair" : "btc_ltc",
                "limit" : "1.2345"
            }
        """
        ''
        
    def recentTransactionsList(self):
        # source: https://shapeshift.io/api.html#recent-list
        """
        url: shapeshift.io/recenttx/<max>
        method: GET
        
        <max> is an optional maximum number of transactions to return.
        If <max> is not specified this will return 5 transactions.
        Also, <max> must be a number between 1 and 50 (inclusive).
        
        Success Output:
            [
                {
                curIn : <currency input>,
                curOut: <currency output>,
                amount: <amount>,
                timestamp: <time stamp>     //in seconds
                },
                ...
            ]
        """
        ''
        
    def statusOfDepositToAddress(self):
        # source: https://shapeshift.io/api.html#status-deposit
        """
        url: shapeshift.io/txStat/<address>
        method: GET
        
        <address> is the deposit address to look up.
        
        Success Output:  (various depending on status)
        
        Status: No Deposits Received
            {
                status:"no_deposits",
                address:<address>           //matches address submitted
            }
        
        Status: Received (we see a new deposit but have not finished processing it)
            {
                status:"received",
                address:<address>           //matches address submitted
            }
        
        Status: Complete
        {
            status : "complete",
            address: <address>,
            withdraw: <withdrawal address>,
            incomingCoin: <amount deposited>,
            incomingType: <coin type of deposit>,
            outgoingCoin: <amount sent to withdrawal address>,
            outgoingType: <coin type of withdrawal>,
            transaction: <transaction id of coin sent to withdrawal address>
        }
        
        Status: Failed
        {
            status : "failed",
            error: <Text describing failure>
        }
        
        *Note: this can still get the normal style error returned. For example if request is made without an address.
        """
    
    def timeRemainingOnFixedAmountTransaction(self):
        # source: https://shapeshift.io/api.html#timeremaining
        """
        url: shapeshift.io/timeremaining/<address>
        method: GET
        
        <address> is the deposit address to look up.
        
        Success Output:
        
            {
                status:"pending",
                seconds_remaining: 600
            }
        
        The status can be either "pending" or "expired".
        If the status is expired then seconds_remaining will show 0.
        """
    
######

# source: https://gist.github.com/hugs/830011
# To install the Python client library:
# pip install -U selenium
 
# Import the Selenium 2 namespace (aka "webdriver")

class Etoro():
    def __init__(self):
        self.driver = None        
        self.fname_trader_positions = 'etoro-trader-positions.json'
        
    def disableImages(self):
        ## get the Firefox profile object
        firefoxProfile = FirefoxProfile()
        ## Disable CSS
        #firefoxProfile.set_preference('permissions.default.stylesheet', 2)
        ## Disable images
        firefoxProfile.set_preference('permissions.default.image', 2)
        ## Disable Flash
        firefoxProfile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
        ## Set the modified profile while creating the browser object 
        #self.browserHandle = webdriver.Firefox(firefoxProfile)
        return firefoxProfile

    def getURL(self, url):
        """Gets a url (selenium.get) specified by the url param if the url is not the current url."""
        
        if self.driver.current_url != url:
            print "getting: {0}".format(self.driver.current_url)
            self.driver.get(url)
    
    def start(self):
        """
        checks whether the browser is running, returns boolean
        """
        # iPhone
        #driver = webdriver.Remote(browser_name="iphone", command_executor='http://172.24.101.36:3001/hub')
        # Android
        #driver = webdriver.Remote(browser_name="android", command_executor='http://127.0.0.1:8080/hub')
        # Google Chrome 
        #driver = webdriver.Chrome()
        # Firefox 
        #FirefoxProfile fp = new FirefoxProfile();
        #fp.setPreference("webdriver.load.strategy", "unstable");
        #WebDriver driver = new FirefoxDriver(fp);
        
        #driver = webdriver.Firefox(firefox_profile=self.disableImages())
        driver = webdriver.Firefox()
        
        self.driver = driver
        
    def isLoggedIn(self):
        from selenium.common.exceptions import NoSuchElementException
        try:
            self.et.driver.find_element_by_xpath('//*[@id="layouts"]/div/header/div/div[2]/div[1]/div[2]/b')
            return False
        except NoSuchElementException, e:
            return True
            #print e
        except Exception as e:
            print e
            return False
    
    def etoroLogout():
        link = self.driver.find_elements_by_xpath('//*[contains(@class, "ob-crown-user-drop-logout-a")]')[0]
        link.click()
    
    def etoroLogin(self, verbose=False):
        flow = []
        co = p_read_csv('config.csv', header=None)
        username = co.ix[3,1]
        passwd = co.ix[3,2]
        print username
        print passwd
        self.check()
        try:
            # find element in loggedout template
            python_link = self.driver.find_elements_by_xpath('//*[@id="layouts"]/div/header/div/div[2]/div[1]/div[2]/b')[0]
            if verbose == True: flow.append(1);
        except IndexError, e:
            if verbose == True: flow.append(2);
            try:
                # find element in loggedin template        
                #python_link = self.driver.find_elements_by_xpath('//span[@class="ob-crown-user-name ob-drop-icon"]')[0]
                self.driver.find_elements_by_xpath('//*[contains(@class, "ob-crown-user-drop-logout-a")]')[0]
                #python_link = self.driver.find_elements_by_xpath('//*[@id="layouts"]/div/header/div/div[2]/div[1]/div[2]/div[1]/span')[0]
                if verbose == True: flow.append(3);
            except IndexError, f:
                if verbose == True: flow.append(4);
                self.driver.get('https://openbook.etoro.com/manapana/portfolio/open-trades/')
        try:
            if verbose == True: flow.append(5);
            python_link = self.driver.find_elements_by_xpath('//*[@id="layouts"]/div/header/div/div[2]/div[1]/div[2]/b')[0]
            python_link.click()
            
            # Enter some text!
            text_area = self.driver.find_elements_by_xpath('//*[@id="layouts"]/div/header/div/div[2]/div[1]/div[2]/div/form/input[1]')[0]
            text_area.send_keys(username)
            
            text_area = self.driver.find_elements_by_xpath('//*[@id="layouts"]/div/header/div/div[2]/div[1]/div[2]/div/form/input[2]')[0]
            text_area.send_keys(passwd)
            
            # Submit the form!
            submit_button = self.driver.find_elements_by_xpath('//*[@id="layouts"]/div/header/div/div[2]/div[1]/div[2]/div/form/div[1]/div/input')[0]
            #submit_button = driver.find_element_by_name('submit')
            submit_button.click()
        except Exception as e:
            print e
            if verbose == True: flow.append(6);
        if verbose == True: flow.append(7);
            
        if verbose == True: print flow
        
        from test_qoreliquid import assertSequenceEqual
        """
        flow:
        """
        try: assertSequenceEqual(flow, [2, 3, 5, 6, 7]) #logged in
        except AssertionError, e: ''#print e
        try: assertSequenceEqual(flow, [1,5,7])         #logged out
        except AssertionError, e: ''#print e
        try: assertSequenceEqual(flow, [2, 4, 5, 6, 7]) #logged in on remote page
        except AssertionError, e: ''#print e
        try: assertSequenceEqual(flow, [2, 4, 5, 7])    #logged in on remote page
        except AssertionError, e: ''#print e
            
        return flow
        
    def quit(self):
        # Close the browser!
        try:
            self.driver.quit()
            self.driver = None
            
        except Exception as e:
            print e
            self.driver = None
        if self.driver == None:
            return True
        else:
            return False
    
    def find_elements_by_xpath_return_list(self, xp, column):
        els = []
        for i in self.driver.find_elements_by_xpath(xp):
            #print i.text
            els.append(i.text)
        try:
            return p_DataFrame(els, columns=[column])
        except Exception as e:
            print e
    
    # todo:
    #https://openbook.etoro.com/markets/stocks/
    
    def getEtoroDiscoverPeople(self, driver=None):
        self.check()
        if driver != None:
            self.driver = driver
        lss = []
        
        xps = """username /html/body/div[2]/div[3]/div[2]/table/tbody/tr/td[1]/div/div[2]/div[1]/a
name /html/body/div[2]/div[3]/div[2]/table/tbody/tr/td[1]/div/div[2]/div[2]
country /html/body/div[2]/div[3]/div[2]/table/tbody/tr/td[1]/div/div[2]/div[3]/div[2]
copiers /html/body/div[2]/div[3]/div[2]/table/tbody/tr/td[2]
weeklyDrawdown /html/body/div[2]/div[3]/div[2]/table/tbody/tr/td[3]
dailyDrawdown /html/body/div[2]/div[3]/div[2]/table/tbody/tr/td[4]
profitableWeeks /html/body/div[2]/div[3]/div[2]/table/tbody/tr/td[5]
gain /html/body/div[2]/div[3]/div[2]/table/tbody/tr/td[6]"""
        ##########
        xps = xps.split('\n')
        for i in xrange(len(xps)):
            iss = xps[i].split(' ')
            lss.append(self.find_elements_by_xpath_return_list(iss[1], iss[0]))
            
        # combine all into a dataframe
        df = p_DataFrame(range(len(lss[0])))
        for i in lss:
            df[i.columns[0]] = i
        return df
    
    def check(self):        
        if type(self.driver) == type(None): 
            self.start()
            return True
        else:
            return True
        
    def getEtoroTraderPositions(self, username, save=True, mode=1):
        """
        mode= 1 or 2
        mode=1 OpenBook mode, able to obtain position trade data from all traders 
               within the OpenBook system. Does not include trade size (amount)
        mode=2 Copy trader mode, as mode=1 with the addition of trade size (amount)
        """        
        self.check()

        def xpathsSplitAndCombine(xps):
            """
            xps = xps.split('\n')
            for i in xrange(len(xps)):
                iss = xps[i].split(' ')
                iss[1] = re.sub(re.compile(r'<space>'), ' ', iss[1])
                #print iss
                try:
                    ilss = self.find_elements_by_xpath_return_list(iss[1], iss[0])
                    print len(ilss)
                    lss.append(ilss)
                except Exception as e:
                    print e
            """
            xps = xps.split('\n')
            for i in xrange(len(xps)):
                iss = xps[i].split(' ')
                iss[1] = re.sub(re.compile(r'<space>'), ' ', iss[1])
                try:
                    #print "{1}::  len iss: {0}".format(len(iss), iss[0])
                    if len(iss) == 2:
                        ilss = self.find_elements_by_xpath_return_list(iss[1], iss[0])
                        #print 'q1'
                    if len(iss) == 3:
                        iss1 = " ".join(iss[1:])
                        ilss = self.find_elements_by_xpath_return_list(iss1, iss[0])
                        #print 'q2'
                    print "{1} {0}".format(iss, len(ilss))
                    #print
                    lss.append(ilss)
                except IndexError, e:
                    print "e1:"
                    print e
            return lss

        def combineAllListsIntoPandasDataframe(lss):
            """
            # combine all into a dataframe
            #print lss
            df = None
            try:
                df = p_DataFrame(range(len(lss[0])))
                for i in lss:
                    df[i.columns[0]] = i
            except TypeError, e:
                print e
            """
            # combine all lists into a dataframe
            #print lss
            df = p_DataFrame(range(len(lss[0])))
            for i in lss:
                try:
                    df[i.columns[0]] = i
                except AttributeError, e:
                    print "{0}: {1}".format(i, e)
            return df
        
        if mode == 2:
            self.etoroLogin(verbose=True)
            self.getURL('https://openbook.etoro.com/{0}/portfolio/open-trades/'.format(username))
            
            lss = []
            xps = """pair //*[@id="open-trades-holder"]/div[2]/div/div/div[1]/div/div[1]/div/div/div[1]/div/a
bias //*[@id="open-trades-holder"]/div[2]/div/div/div[1]/div/div[1]/div/div/div[1]/div/strong
amount //*[contains(@class,<space>"user-table-cell<space>uttc-3")]
take_profit //*[contains(@class, "info-row-close-reason")][2]
stop_loss //*[contains(@class, "info-row-close-reason")][1]
time //*[@id="open-trades-holder"]/div[2]/div/div/div[1]/div/div[1]/div/div/div[3]/div/span
username //*[@id="open-trades-holder"]/div[2]/div/div/div[1]/div/div[2]/a
open //*[contains(@class,<space>"user-table-cell<space>uttc-4")]
netprofit //*[contains(@class,<space>"user-table-cell<space>uttc-5")]
gain //*[contains(@class,<space>"user-table-cell<space>uttc-5")]"""
            lss = xpathsSplitAndCombine(xps)
            df  = combineAllListsIntoPandasDataframe(lss)
            
        if mode == 1:
            self.driver.get('https://openbook.etoro.com/{0}/portfolio/open-trades/'.format(username))
            
            lss = []

            xps = """pair //*[@id="open-trades-holder"]/div[2]/div/div/div[1]/div/div[1]/div/div/div[1]/div/a
bias //*[@id="open-trades-holder"]/div[2]/div/div/div[1]/div/div[1]/div/div/div[1]/div/strong
take_profit //*[@id="open-trades-holder"]/div[2]/div/div/div[1]/div/div[1]/div/div/div[2]/div/span[2]
stop_loss //*[@id="open-trades-holder"]/div[2]/div/div/div[1]/div/div[1]/div/div/div[2]/div/span[1]
time //*[@id="open-trades-holder"]/div[2]/div/div/div[1]/div/div[1]/div/div/div[3]/div/span
open //*[@id="open-trades-holder"]/div[2]/div/div/div[1]/div[@class="user-table-row<space>{0}"]/div[3]
gain //*[@id="open-trades-holder"]/div[2]/div/div/div[1]/div[@class="user-table-row<space>{0}"]/div[4]""".format(username)
            lss = xpathsSplitAndCombine(xps)
            df  = combineAllListsIntoPandasDataframe(lss)
                
        # cleanup tables
        for i in range(len(df.ix[:,0])):
            try:
                col = 'take_profit'; df.ix[i,col] = re.match(re.compile(r'.*?([\d\.]+)'), df.ix[i,col]).groups()[0]
            except Exception as e:
                print e
            try:
                col = 'stop_loss'; df.ix[i,col] = re.match(re.compile(r'.*?([\d\.]+)'), df.ix[i,col]).groups()[0]
            except Exception as e:
                print e
            try:
                col = 'amount'; df.ix[i,col] = re.match(re.compile(r'.*?([\d\.]+)'), df.ix[i,col]).groups()[0]
            except Exception as e:
                print e
            try:
                col = 'netprofit'; df.ix[i,col] = re.match(re.compile(r'.*?([\d\.]+)'), df.ix[i,col]).groups()[0]
            except Exception as e:
                print e
            try:
                col = 'gain'; df.ix[i,col] = re.match(re.compile(r'(-?[\d\.]+).*'), df.ix[i,col]).groups()[0]
            except Exception as e:
                print e
            
        # remove the extra table column
        df = df.ix[:,list(df.columns[1:])]            
            
        if save == True:
            try:
                allPositions2 = p_read_json(self.fname_trader_positions)
                #print allPositions2
            except ValueError, e:
                allPositions2 = p_DataFrame()
                allPositions2.to_json(self.fname_trader_positions)
                #print allPositions2
                #print e
                
            fp = open(self.fname_trader_positions, 'r')
            allPositions2 = j.loads(fp.read())
            fp.close()
            
            #print allPositions2
            #print
            
            positions = df            
            #print positions
            #print positions.to_dict()
            allPositions2[username] = positions.to_dict()
            #allPositions2.to_json(self.fname_trader_positions)
            allPositions2 = convertDictKeysToString(allPositions2)
            #print j.dumps(allPositions2)
            
            fp = open(self.fname_trader_positions, 'w')
            fp.write(j.dumps(allPositions2))
            fp.close()        
            
        return df
        
    # get target portfolio from etoro user
    def getTargetPortfolio(self, username=None):
        fname = self.fname_trader_positions
        fp = open(fname, 'r')
        em = fp.read()
        em = j.loads(em)
        #for i in em:
        #    print p_DataFrame(em[i])
        target = p_DataFrame([])
        if username == None:
            for i in em:
                emi = p_DataFrame(em[i])
                #print emi
                target['pair'] = emi['pair']
                target['bias'] = emi['bias']
                target['take_profit'] = emi['take_profit']
                target['stop_loss'] = emi['stop_loss']
                target['amount'] = emi['amount']
                print target
                print
        if type(username) == type(''):
            #print username
            #for i in em:
            #    print i
            emi = p_DataFrame(em[username])
            #print emi
            try:
                target['pair'] = emi['pair']
            except KeyError, e:
                print e
            try:
                target['bias'] = emi['bias']
            except KeyError, e:
                print e
            try:
                target['take_profit'] = emi['take_profit']
            except KeyError, e:
                print e
            try:
                target['stop_loss'] = emi['stop_loss']
            except KeyError, e:
                print e
            try:
                target['amount'] = emi['amount']
            except KeyError, e:
                print e
            try:
                target['open'] = emi['open']
            except KeyError, e:
                print e
            try:
                target['gain'] = emi['gain']
            except KeyError, e:
                print e
            try:
                target['username'] = emi['username']
            except KeyError, e:
                print e
            return target
            #except KeyError, e:
            #    #print 'No username {0} found.'.format(username)
            #    print e
            #    ''

class Bancor:
    def getBancorYear(self, fname):    
        return int(re.match(re.compile(r'(.*)_([\d]{4}).*'), fname).groups()[1])
    
    def cleanBancorDate(self, dat, year):
        dat = re.match(re.compile(r'([\d]{2})\/([\d]{2})'), dat).groups()
        return dd.datetime(year, int(dat[1]), int(dat[0]))
    
    def cleanBancorNumber(self, n):
        try:
            #print n
            n = re.sub(re.compile(r'(.*)\,([\d]{2})'), '\\1_\\2', n)
            #print n
            n = re.sub(re.compile(r'\.'), '', n)
            n = re.sub(re.compile(r'\,'), '', n)
            #print n
            n = re.sub(re.compile(r'\_'), '.', n)
            #print n
            return float(n)
        #float(str(n).replace(',', ''))
        except Exception as e:
            print e
            return n
        #return n
    
    # requires pdf conversion to text via pdftotext -raw <fname.pdf>
    def parseBancorStatments(self, fname, mode=2, idx=[[15,76,137,198,259], [45,106,167,228,262]]):
        """
        mode = 1 # manifest
        mode = 2 # manifest
        """
        print fname
        res = open(fname, 'r').read().split('\n')
        if mode == 4:
            for i in res:
                print i
        idx = p_DataFrame(idx)
        p0 = p_DataFrame()
        if mode == 1:
            print idx.transpose().get_values()
            print n_diff(idx)
            print idx[0]
            for [i, j] in enumerate(res):
                print "{0} {1}".format(i,j)
        for i in idx:
            p0 = p0.combine_first(p_DataFrame(res).ix[idx[i][0]:idx[i][1],:])
        ms = []
        for i in list(p0.get_values()):
            if mode == 4:
                print i[0]
            try:
                #m = re.match(re.compile(r'([\d\/]+)[\s]+([\w\s\.\%\d]+?)[\s]+([\d\,^%]+)(.*)'), i[0]).groups()
                #m = re.match(re.compile(r'([\d\/]+)[\s]+(.+?)[\s]+([\.\d\,^\%]+)(.*)'), i[0]).groups()
                #m = re.match(re.compile(r'([\d\/]+)[\s]+(.+)[\s]+([\.\d\,^\%]+)[\s]+([\d\,]+)'), i[0]).groups()
                m = re.match(re.compile(r'([\d\/]+)[\s]+(.+)[\s]([\.\d\,^\%]+)[\s]([\d\,]+)'), i[0]).groups()
                if mode == 3:
                    #print i[0]
                    print m
                ms.append(m)
            except AttributeError, e:
                if mode == 1:
                    print i[0]
                #print e
                ''
        ms = p_DataFrame(ms, columns=['Fecha', 'Concepto/Empresa', 'Debito/Credito', 'Saldo'])
        for i in range(len(ms.ix[:,2])):
            ms.ix[i,0] = self.cleanBancorDate(ms.ix[i,0], self.getBancorYear(fname))
            ms.ix[i,2] = self.cleanBancorNumber(ms.ix[i,2])
            ms.ix[i,3] = self.cleanBancorNumber(ms.ix[i,3])
        #print ms
        pres = p_DataFrame(res).ix[:,:]
        ms = ms.set_index('Fecha')
        #ms.ix[:,'Saldo'].plot(); show();
        #print ms
        return ms
        print '==========================================================================================='
        print '==========================================================================================='

    
    def discoverInvestors(self):
        self.qq.et.driver.get('https://beta.etoro.com/discover/?culture=en-gb')
        
        # click on Search
        #python_link = self.et.driver.find_elements_by_xpath('/html/body/div[3]/div/div[3]/a/span')[0]
        #python_link.click()
        
        # Click on Trending Investors
        try:
            python_link = self.et.driver.find_elements_by_xpath('/html/body/div[3]/div/div[5]/div[1]/table/tbody/tr/td[3]/div/a/span/span')[0]
            python_link.click()
        except Exception as e:
            print e
            pass
        
        # clear the filters
        #python_link = driver.find_elements_by_xpath('/html/body/div[2]/div[3]/div[1]/div[2]/div[12]')[0]
        #python_link.click()
    
if __name__ == "__main__":
    print 'stub'
    #testMicrofinance()
    #testGetDataFromQuandl()
    #print normalizeme2([1423,2342,2343,23441,1235,1236,7123,8123,913])
    #print normalizeme2([3345,3422,3453,344,345,635,7345,8234,2349])
    #print list(normalizeme2([9,8,7,6,5,4,3,2,1]).transpose().get_values()[0])
    #nnn = normalizeme2([1423,2342,2343,23441,1235,1236,7123,8123,913])
    #print list(nnn.transpose().get_values()[0])
    #import doctest; print doctest.testmod()
    #debug('test', 9)
    
    #qu = 'Building Permits canada'
    #qu = 'argentina inflation'
    #qu = 'non farm'
    #searchQuandl(qu)
    
    #headers = [0,1]
    #headers = None
    #searchQuandl('tesla', mode='combineplot', returndataset=False, headers=headers, listcolumns=True)
