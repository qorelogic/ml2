
from oandaq import OandaQ

#from numpy import *
#from numpy import divide as n_divide
#from numpy import float16 as n_float16
#from numpy import rint as n_rint
#from numpy import c_ as n_c_
#from numpy import min as n_min
#from numpy import max as n_max
#from numpy import tanh as n_tanh
#from numpy import concatenate as n_concatenate

#from pandas import read_csv as p_read_csv

import plotly.plotly as py
from plotly.graph_objs import *

#import os
import datetime as dd
#from matplotlib.pyplot import plot, legend, title, show #, imshow, tight_layout
#from matplotlib.pylab import *
#from pylab import rcParams
#from IPython.display import display, clear_output
import ujson as ujson

from qore import *
#from qore_qstk import *

import numpy as n
import pandas as p
#import Quandl as q
#import datetime as dd
#import urllib2 as u
#import html2text
import exceptions as ex
import re, sys
import StringIO as sio
import threading,time
import itertools as it

import oandapy

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
        rate   = n.array(rate, dtype=float64)
        period = n.array(period)    
        
        if shift < 0:
            raise ex.IndexError('shift should be greater than 0. shift: '+str(shift))
        if shift > len(period):
            raise ex.IndexError('shift should be smaller than period length. shift: '+str(shift)+', period length: '+str(len(period)))
        
        # shift code
        try:        
            period = list(n.zeros(shift, dtype=int)) + list(period[0:len(period)-shift])
        except Exception as e:
            print e
            ''
        
        return initial_capital * n.power(1 + rate.reshape(size(rate), 1) / 100, period)
        
    def mdrange(self, initial, space, end):
        return n.linspace(initial,end,(1.0/space)*end+1)
        
    def rateSpectra(self):
        rate   = self.mdrange(0, 0.1, 10)
        period = range(0, 200 + 1)
        plot(self.compoundVestedCapital(rate, period))
       
    def test(self):
        print self.compoundVestedCapital(50,2)
        print self.compoundVestedCapital(1,n.array([1,2,3]))
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

        n.linspace(0,1,100).T
        rate = range(0,23)
        period = range(0,100)
        rate   = n.array(rate, dtype=float64)
        period = n.array(period)    
        #res =  100 * n.power(1 + rate / 100, period.reshape(size(period), 1))
        res =  100 * n.power(1 + rate.reshape(size(rate), 1) / 100, period)
        print res

#from IPython.display import display, clear_output
#import time
class ml007:

    def __init__(self, thetaDir=None):
        self.qd = QoreDebug()
        self.qd._getMethod()

        self.J_history = []
        self.theta     = []
        self.initialIter = 0
        self.iter        = 0

        self.thetaDir = thetaDir
        
    def computeCost_linearRegression(self, X, y, theta, m):
        #self.qd._getMethod()
        
        #print 'cost'
        #print X.shape
        #print type(X.shape)
        #print theta.shape
        o1 = 1.0/(2*m)
        p1 = n.dot(X,theta)
        o2 = n.sum(n.power(p1-y,2)) # J
        #print type(theta)
        ret = o1 * o2
        return ret
    
    #print computeCost( n.array([1, 2, 1, 3, 1, 4, 1, 5]).reshape(4,2), n.array([7, 6, 5, 4]).reshape(4,1), n.array([0.1,0.2]).reshape(2,1) )
    # 11.945
    #print computeCost( n.array([1,2,3,1,3,4,1,4,5,1,5,6]).reshape(4,3), n.array([7, 6, 5, 4]).reshape(4,1), n.array([0.1,0.2,0.3]).reshape(3,1))
    # 7.0175
    
    def gradientDescent_linearRegression(self, X, y, theta, alpha, num_iters, viewProgress=True, b=500, sw=None):
        self.qd._getMethod()
        
        mdf = X

        m = len(y)
        self.J_history = n.zeros(num_iters)
        self.theta = theta
        X = n.array(X)
        alpha_over_m = (float(alpha)/m)
        #try:
        for self.iter in range(self.initialIter, num_iters):
                self.theta = self.theta - alpha_over_m * n.dot((   n.dot(X, self.theta) - y).transpose(), X).transpose()
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
                #if n.isnan(self.J_history[self.iter]):
                #    #plot(self.J_history); show();
                #    plt.scatter(self.iter, self.J_history); show();
                #    return [self.theta, self.J_history]
                if self.iter % b == 0:
                    if sw != None:
                        tp = sw.predictRegression2(mdf.ix[:, :], quiet=True)
                        tp = tp.reshape(1,len(tp))[:,len(tp)-1:]
                    print '{0}:{1} {2} {3} {4}'.format(self.pair, self.granularity, self.iter, self.J_history[self.iter], tp)
                    fp = open(self.thetaDir+'/{0}-{1}.train.csv'.format(self.pair, self.granularity), 'a')
                    csv = ','.join([self.pair, self.granularity, str(self.iter), str(self.J_history[self.iter]), str(list(tp[0])[0])])
                    fp.write(csv+'\n')
                    fp.close()
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
        
    #[theta, J_history] = gradientDescent(n.array([1,5,1,2,1,4,1,5]).reshape(4,2), n.array([1,6,4,2]).reshape(4,1), n.array([0,0]).reshape(2,1),0.01,1000);
    #print theta
    #print J_history
    #theta =
    #    5.2148
    #   -0.5733
    #>>J_hist(1)
    #ans  =  5.9794
    #>>J_hist(1000)
    #ans = 0.85426
    
    #[theta, J_hist] = gradientDescent(n.array([3,5,1,2,9,4,1,5]).reshape(4,2),n.array([1,6,4,2]).reshape(4,1), n.array([0,0]).reshape(2,1), 0.01,1000);
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
        grad = n.zeros(size(theta));
        
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
        J = (1.0/m) * n.sum(-y *  n.log(sigmoidme(n.dot(X, theta))) - (1 - y) *     log(  1 - sigmoidme(n.dot(X, theta))  ) );
        #grad = (1/m)*sum((sigmoid(X*theta)-y).*X)
        grad = (1/m)*n.sum(n.dot((sigmoidme(n.dot(X, theta))-y), X))
        
        #% =============================================================
        
        #end
        
        return [J, grad]    
    
    #initial_theta = n.zeros(nn + 1);
    #initial_theta = n.zeros(nn);
    #initial_theta
    
    #[cost, grad] = costFunction(initial_theta, X, y);


# source: http://stackoverflow.com/questions/3949226/calculating-pearson-correlation-and-significance-in-python
import math
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

import numpy as np
def pcc(X, Y):
   ''' Compute Pearson Correlation Coefficient. '''
   # Normalise X and Y
   X -= X.mean(0)
   Y -= Y.mean(0)
   # Standardise X and Y
   X /= X.std(0)
   Y /= Y.std(0)
   # Compute mean product
   return np.mean(X*Y)
# Using it on a random example
#from random import random
#X = np.array([random() for x in xrange(100)])
#Y = np.array([random() for x in xrange(100)])
#pcc(X, Y)

class StatWing:
    
    def __init__(self, thetaDir=None):
        self.qd = QoreDebug()
        self.qd._getMethod()

        self.thetaDir = thetaDir
        self.keyCol = ''
        self.relatedCols = []
        self.theta = n.array([])
        self.dmean = []
        self.dstd = []
        
        # for predict from theta
        self.nxps = []
        try:    self.oq = OandaQ()
        except Exception as e:
            print e
            print 'offline mode'
        #self.theta = p.read_csv('/mldev/bin/datafeeds/theta.csv', index_col=0)
        self.theta = p.DataFrame()
        self.ml = ml007(thetaDir=self.thetaDir)
        
    def nextBar(self, dfa, k, barsForward=3):
        self.qd._getMethod()
        
        dfc = p.DataFrame(dfa, index=dfa.index[0:len(dfa)-barsForward])
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

    def higherNextDay(self, dfa, k, barsForward=1):
        return self.higherNextBars(dfa, k, barsForward=barsForward)
        
    def higherNextBars(self, dfa, k, barsForward=1):
        self.qd._getMethod()

        dfc = p.DataFrame(dfa, index=dfa.index[0:len(dfa)-barsForward])
        print type(dfc)
        dfc['a'] = dfa.ix[0:len(dfa)-barsForward, [k]].get_values()
        dfc['b'] = dfa.ix[barsForward:len(dfa),[k]].get_values()
        dfc['c'] = list(n.array((dfc['b'] > dfc['a']), dtype=int))
        #print dfc['a']
        return dfc['c']
        #p.DataFrame(sw.higherPrev(df.ix[:, 0].get_values()))
    
    def lowerNextDay(self, dfa, k, barsForward=1):
        return self.lowerNextBars(dfa, k, barsForward=barsForward)
        
    def lowerNextBars(self, dfa, k, barsForward=1):
        self.qd._getMethod()

        dfc = p.DataFrame(dfa, index=dfa.index[0:len(dfa)-barsForward], columns=dfa.columns)
        dfc['a'] = dfa.ix[0:len(dfa)-barsForward, [k]].get_values()
        dfc['b'] = dfa.ix[barsForward:len(dfa), [k]].get_values()
        dfc['c'] = n.array((dfc['b'] < dfc['a']), dtype=int)
        return dfc['c']
        #p.DataFrame(sw.higherPrev(df.ix[:, 0].get_values()))
    
    # export dataset to csv for analysis (statwing)
    def higherPrev(self, a):
        self.qd._getMethod()

        a = sigmoidme(a) > 0.5
        return n.array(a, dtype=int)
    
    def lowerPrev(self, a):
        self.qd._getMethod()

        a = sigmoidme(a) < 0.5
        return n.array(a, dtype=int)
    
    def exportToStatwing(self, de, currency_code):
        self.qd._getMethod()

        #dff = n.matrix('1;2;3;4;-4;-5;-3;2;9').A
        #print higherPrev(dff)
        #print lowerPrev(dff)
        s1 = 0
        de = de.fillna(0)
        de1 = de.ix[s1:,:]
        #de1 = sigmoidme(normalizeme(de1))
        de1 = p.DataFrame(de1)
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
        d = [len(sample),   n.median(sample),n.mean(sample), '0.53784 to 0.54679',                    n.std(sample),       n.min(sample), n.max(sample), n.sum(sample)]
        #110.279 to 110.636
        summary = p.DataFrame(d, index=c)#.transpose()
        print summary
        
        print 'Percentiles:'
        pctl = []
        for i in [0,1,5,10,25,50,75,90,95,99,100]:
            pctl.append(n.percentile(df.ix[:,1], i))
        print p.DataFrame(pctl, index=['0th (Minimum)', '1st','5th','10th','25th (Lower Quartile)','50th (Median)','75th (Upper Quartile)','90th','95th','99th','100th (Maximum)'])#.transpose()
        
        sample.hist(bins=100);
        xlabel(self.getCol(col, df))
        #ylabel('t2')
        show();
        
    def relate(self, sample, keyCol, relatedCol):
        self.qd._getMethod()

        #print n.corrcoef(sample.ix[:, keyCol], sample.ix[:, relatedCol])[0, 1]
        #print pearson_def(sample.ix[:, keyCol], sample.ix[:, relatedCol])
        # source: http://stackoverflow.com/questions/19428029/how-to-get-correlation-of-two-vectors-in-python
        from scipy.stats.stats import pearsonr, spearmanr
        ind = ['Pearson\'s r: ', 'Spearman\'s r: ']
        d = [pearsonr(sample.ix[:, keyCol], sample.ix[:, relatedCol]), spearmanr(sample.ix[:, keyCol], sample.ix[:, relatedCol])]
        print p.DataFrame(d, index=ind)
        
        import numpy as np
        x = sample.ix[:, relatedCol].fillna(0)
        y = sample.ix[:, keyCol].fillna(0)
        
        deg = 1
        weight = 1
        theta = np.polynomial.polynomial.polyfit(x,y,deg,weight)#w=weight of each observation)
        print 'theta:{0}'.format(theta)
        #p.DataFrame(theta[0] + theta[1] * n.array(range(0, int(n.max(x.ix[:,1]))))).plot()
        #p.DataFrame(theta[0] + theta[1] * n.array(range(0, ceil(n.max(x.get_values()))))).plot()
        #print [min(y), max(y)]
        #print [min(x), max(x)]
        #p.DataFrame(theta[0] + theta[1] * n.array( n.linspace(0, int(ceil(n.max(x.get_values()))), 5) )).plot()
        mini = int(ceil(n.min(x.get_values())))#-10
        maxi = int(ceil(n.max(x.get_values())))#+10
        plot(linspace(mini, maxi, 10), theta[0] + theta[1] * linspace(mini, maxi, 10), '-r');
        #p.DataFrame(theta[0] + theta[1] * n.array( n.linspace(mini, maxi, maxi-mini) )).plot()
        #p.DataFrame(theta[0] + theta[1] * n.array( n.linspace(-120, 60, 180) )).plot()
        
        #print n.linspace(int(ceil(n.max(x.get_values()))), int(ceil(n.max(x.get_values()))), 5)
        #print n.linspace(min(x)-10, int(ceil(n.max(x.get_values())))+10, len(x))
        
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
        X['bias'] = n.ones(len(data))
        Xc = X.columns.tolist()
        Xc.insert(0, Xc.pop())
        try:
        #print 'removing {0}'.format(keyCol)
        #print Xc
            Xc.remove(keyCol)
        except Exception as e:
            e
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
        #m = len(data)
        
        #scatter(X,y, marker='x', c='r'); show();
        
        # gradient descent
        #plot(X,y,'.'); show();
        
        # 
        X = self.fixColumns(data, relatedCols, keyCol)
        
        #print y
        
        #initialTheta = None
        
        if type(initialTheta) == type(None):
            self.theta = n.zeros(len(X.columns))
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
        self.theta = p.Series(self.theta).to_frame('o').fillna(0).combine_first(p.DataFrame(n.zeros(len(X.columns)), index=X.columns, columns=['o'])).ix[X.columns, 'o'].get_values()
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
        
        #theta = n.random.randn(len(X.columns))
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
        
        dp = p.DataFrame(te1)
        #print len(te1)
        #print te1
        #print len(te2)
        #print te2
        dp[1] = te2
        
        # get current quotes
        co = p.read_csv('datafeeds/config.csv', header=None)
        env1=co.ix[1,1]
        access_token1=co.ix[1,2]
        oanda1 = oandapy.API(environment=env1, access_token=access_token1)
        li = []
        if mode == 1: fl = 0; ll = len(dp.index)-1;
        if mode == 2: fl = 1; ll = len(dp.index);
        for i in list(dp.ix[:,1])[fl:ll]:
            if i != 'bias':
                try:
                    pai = "{0}_{1}".format(i[0:3], i[3:6])
                    response = oanda1.get_prices(instruments=pai)
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
        
        dn = n.array(dp.get_values()[:,[0,2]], dtype=float)
        #print dn
        n.dot(dn[:,0], dn[:,1])
        pred = n.sum(dn[:,0] * dn[:,1])
        print pred
        """
        predictions.append(pred)
        print p.DataFrame(predictions)
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
        
        #data = p.read_csv('/coursera/ml-007/programming-exercises/mlclass-ex1/ex1data1.txt', header=None)
        #data = p.read_csv('quandl-BNP-USD.csv')
        #data = p.read_csv('quandl-BNP-EUR.csv')
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
        #X = p.DataFrame(n.ones(len(data)), index=data.index).combine_first(data.ix[:, self.relatedCols].fillna(0))
        X = self.fixColumns(data, self.relatedCols, self.keyCol)
        if quiet == False:
            print list(X.columns)

        #s = len(X)-20
        #s = len(X)-1
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
        
        predict = n.dot(nX, ntheta)
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
        
        #print n.c_[n.ones(1), nX.ix[1:,:].get_values().T].T
        #print nX.shape
        #print n.dot(nX.T, theta)
        #if type(self.theta) == type(p.DataFrame()):
        #    theta = self.theta.get_values()
        #else:
        #    theta = self.theta
        nXbias = n.c_[n.ones(1), nX.ix[1:,:].get_values().T]
        #print nXbias
        #print theta
        #print nXbias.shape
        #print theta.shape
        
        val = 0
        try:
            nd = n.dot( nXbias, self.theta )
            try:    val = nd[0][0]
            except: val = nd[0]
            #print nd
        except Exception as e:
            ''
            print e
            #print 'eerr'
        #print val
        if val != 0:
            self.nxps.append( val )
        
        if save == True:
            p.DataFrame(self.nxps).to_csv('/mldev/bin/datafeeds/nxps.csv')
        #plot(self.nxps);
        #show();
        #print self.nxps
        return val
 

#import plotly.plotly as py
#from plotly.graph_objs import *
class RealtimeChart:
    
    def __init__(self):
        self.qd = QoreDebug()
        self.qd._getMethod()
        
        ####
        # real time chart
        ####
        self.df = p.DataFrame()
        
        self.qq = QoreQuant()
        self.qq.loadTheta(0)
        
        self.sw = self.qq.sw
        
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
        
    def getInstruments(self):
        rs = list(self.qq.sw.theta.index)
        for i in xrange(len(rs)):
            rs[i] = rs[i].split(' ')[2].split('_')[0].replace('/','_')
        return ','.join(rs)
    
    # source: http://stackoverflow.com/questions/4098131/how-to-update-a-plot-in-matplotlib
    def update(self, csvc):
        self.qd._getMethod()
        
        ####
        # real time chart
        ####
        #print csvc
        self.df[csvc[0]] = [float(csvc[1])]
        #print self.df
        nX =   self.df.transpose()
        
        y  = self.sw.predictFromTheta(nX=nX)
        
        try:
            imax = n.max(self.sw.nxps)
            imax = imax + n.std(self.sw.nxps)
        except Exception as e:
            print 'exception:1'
            print e
        try:
            imin = n.min(self.sw.nxps)
            imin = imin - n.std(self.sw.nxps)
        except Exception as e:
            print 'exception:2'
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
        self.qd._getMethod()
        
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
        self.qd._getMethod()

        print 'x:{0}, y:{1}'.format(x, y)
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
>>> df = p.DataFrame([['a','b','c'],['buy','sell','sell'],[1,2,3]], index=['pair', 'bias', 'amount']).transpose()
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

# show the whole dataframe (untruncated)
def displayDataFrame(df, truncate=False):
    if truncate == False:
        with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
            print df
    else:
        print df

# wrapper for displayDataFrame(df, truncate=False)
def pf(df):
    displayDataFrame(df, truncate=False)

def normalizeme(dfr, pinv=False):
    
    nmean = n.mean(dfr, axis=0)
    nstd = n.std(dfr, axis=0)
    #nmean = n.mean(dfr)
    #nstd = n.std(dfr)
    dfr = (dfr - nmean) / nstd
    #dfr = n.divide((dfr - nmean), nstd)
    if pinv == False:
        return dfr
    else:
        return [dfr, nmean, nstd]

def normalizemePinv(dfr, mean, std):
    
    #print (n.dot(data.get_values(),  dst['mean'].get_values().reshape(len(dst), 1) )) + dst['std']
    #print (n.dot(data.get_values(),  dmean.get_values().reshape(len(dst), 1) )) + dstd.get_values()
    ##print type(data)
    #print (data)
    ##print type(dmean)
    #print (dmean)
    ##print type(dstd)
    #print (dstd)
    #print (n.dot(n.array(data), dmean.reshape(len(dst), 1) )) + dstd
    
    dfr = (dfr * std) + mean
    return dfr

def normalizeme2(ds, index=None, columns=None):
    
    #ds = n.array(ds, dtype=float)
    if type(ds) == type(p.DataFrame([])):
        #print '0'
        dss = ds.get_values()
        index = ds.index
        columns = ds.columns
    if type(ds) == type(n.array([])):
    #    print 't1'
        dss = ds
    if type(ds) == type([]):
    #    print 't2'
        dss = n.array(ds, dtype=float)
    #print type(dss)
    #import sys
    #sys.exit()
    #print ds[0]
    # call fillna(method='bfill') on dataset before calling this method
    
    dss = dss / dss[0]
    dss = p.DataFrame(dss, index=index, columns=columns)
    return dss

def sigmoidme(dfr):
    return 1.0 / (1 + pow(n.e,-dfr))

def sigmoidmePinv(sigdfr):
    #sigdfr = sigdfr.fillna(0).get_values()
    #sigdfr = 1.0 / (1 + pow(n.e,-dfr))
    #return pow(n.e,-dfr) = (1.0 / pinv) - 1
    #return log10((1.0 / dfr.get_values()) - 1)
    #return n.log10((1.0/sigdfr)-1)/n.log10(n.e)
    #pow(n.e,-dfr) = (1.0 / pinv) - 1
    #/ n.log(n.e)
    return -n.divide(n.log10((n.divide(1.0, sigdfr))-1), n.log10(n.e))

def tanhme(dfr):
    return n.tanh(dfr)

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
        #print p.DataFrame(list(d.columns))
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
        res = ujson.loads(fp.read())
        fp.close()
        writeQuandlSearchLog(str(tt)+':cached:'+str(query)+' to '+fname)
    except IOError:
        try:
            writeQuandlSearchLog(str(tt)+':searched:'+str(query)+' to '+fname)
            res = q.search(query, verbose=False)
            fp = open(fname, 'w')
            fp.write(ujson.dumps(res))
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
    sp = p.read_csv('data/quandl/SP500.csv')
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
    df = p.DataFrame([])
    
    if type(tk) == type(''):
        debug('fetching '+tk, verbosity=verbosity)
        [fname, path] = quandlCode2DatasetCode(tk, hdir='data/quandl/'+dataset, include_path=True, suffix='.csv')
        mkdir_p(path) # alternative python3: os.makedirs(path, exist_ok=True)
        
        try:
            df = p.read_csv(fname, index_col=index_col)
        except IOError:
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
            r1 = n.array([tk[i]+' '], dtype=object)
            r2 = n.array(list(dfs[i].columns), dtype=object)
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
        da = p.read_csv(fname, index_col=0)
        
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
            from qorequant import QoreQuant
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
        d = p.read_csv(fname, index_col=0)
        
    #plot(d.ix[:,tl])
    #print d.columns
    print 'cols1'
    
    return d

def testMicrofinance():
    fm = FinancialModel()
    #fm.test()
    
    years    = 4
    months   = 12 * years + 1
    #days     = 250 * years + 1
    #ic       = 100
    myrates  = []
    
    # 12% monthly
    myrates.append(12)
    # 1% daily, monthly equivalent
    myrates.append(fm.rateToCompoundedPercentage(1, 20))
    # 7% APR monthly equivalent
    myrates.append(fm.rateToCompoundedPercentage(fm.compoundedPercentageIntegral(7, 250), 20))
    
    myratetitles = []
    
    periods = n.array(range(0,months))
    df = p.DataFrame(periods)
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
    return da
    
def quandlSweepDatasources():
    #import StringIO as sio
    df = p.read_csv('/mldev/lib/crawlers/finance/quandl.scrapy/datasources_quandl.csv')
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
            """
            c = fetchURL(url.format(df.ix[i,['code']]['code'], j), mode='')
            s = sio.StringIO()
            s.write(c)
            s.seek(0)
            print p.read_csv(s)
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
    
    

#import numba
#@numba.jit(nopython=True)
#@profile
def combineDF(df1, df2):
    df1 = p.DataFrame(df1)
    df2 = p.DataFrame(df2)
    df = p.concat([df1, df2], axis=1)

    #print '------'
    #print df1
    #print df2
    #print '------'
    return df

# g: python combine two dictionaries by key, source: http://stackoverflow.com/questions/5946236/how-to-merge-multiple-dicts-with-same-key
#@profile
def combineDF2(df1, df2):
    ds = [df1, df2]
    df = {}
    for k in df1.iterkeys():
        df[k] = tuple(df[k] for df in ds)
    df = p.DataFrame(df)
    #print '------'
    #print df1
    #print df2
    #print '------'
    return df
    
#from collections import defaultdict
# g: python combine two dictionaries by key, source: http://stackoverflow.com/questions/5946236/how-to-merge-multiple-dicts-with-same-key
#@profile
def combineDF3(df1, df2):
    #df1 = {1: 2, 3: 4}
    #df2 = {1: 6, 3: 7}
    #df = defaultdict(list)
    df = {}
    for d in (df1, df2): # you can list as many input dicts as you want here
        for key, value in d.iteritems():
            #df[key].append(value)
            df.update({key:value})
    #df = p.DataFrame(df)
    #qd.data(df)
    #sys.exit()
    #print '------'
    #print df1
    #print df2
    #print '------'
    return df

def pairwise_python(X):
    M = X.shape[0]
    N = X.shape[1]
    D = np.empty((M, M), dtype=np.float)
    for i in range(M):
        for j in range(M):
            d = 0.0
            for k in range(N):
                tmp = X[i, k] - X[j, k]
                d += tmp * tmp
            D[i, j] = np.sqrt(d)
    print D
    return D
#%timeit pairwise_python(X)

def test_numba():
    from numba import double
    from numba.decorators import jit, autojit
    pairwise_numba = autojit(pairwise_python)
    X = n.random.random((1000, 3))
    pairwise_numba(X)
#    %timeit pairwise_numba(X)

def test_cython():
    print 'test'

    
class Patterns:

    def __init__(self, loginIndex=5):
        
        from oandapyV20 import API

        self.qd = QoreDebug()
        self.qd.on()

        co, loginIndex, env0, access_token0, oanda0 = getConfig(loginIndex=loginIndex)
        #print 'access_token0 %s' % access_token0        
        self.client = API(access_token=access_token0)

        self._accountList = self.accountList()
        self.hdirMonitor = '/mldev/bin/data/oanda/cache/monitor'
        mkdir_p(self.hdirMonitor)
        
    def accountList(self):

        import oandapyV20.endpoints.accounts as accounts
        r = accounts.AccountList()
        try:
            rv = self.client.request(r)
            return p.DataFrame(rv['accounts'])
        except Exception as e:
            self.qd.exception(e)
        return p.DataFrame([])

    def sendEmail(self, textFilename, toEmailAddress):
        # Import smtplib for the actual sending function
        import smtplib
        
        # Import the email modules we'll need
        from email.mime.text import MIMEText
        
        # Open a plain text file for reading.  For this example, assume that
        # the text file contains only ASCII characters.
        fp = open(textFilename, 'rb')
        # Create a text/plain message
        msg = MIMEText(fp.read())
        fp.close()
        
        # me == the sender's email address
        me = 'mailer@qoreliquid'
        # you == the recipient's email address
        msg['Subject'] = 'The contents of %s' % textFilename
        msg['From'] = me
        msg['To'] = toEmailAddress
        
        # Send the message via our own SMTP server, but don't include the
        # envelope header.
        try:
            s = smtplib.SMTP('localhost')
            s.sendmail(me, [toEmailAddress], msg.as_string())
            s.quit()
        except:
            return

    #@profile
    def visualizeAccounts(self):
        import matplotlib.pylab as plt
        
        fn = 'monitorAccountsMarginCloseout.jsonm'
        
        #fn = 'monitorAccountsProfitableTradesPLP.jsonm'
        #fn = 'monitorAccountsProfitableTradesPLP.stats.jsonm'
        #fn = 'monitorAccountsProfitableTradesPLN.jsonm'
        #fn = 'monitorAccountsProfitableTradesPLN.stats.jsonm'
        
        fp = open(self.hdirMonitor+'/'+fn)
        fn = fp.read().split('\n')
        fp.close()
        accid = '101-004-1984564-012'
        mdf = p.DataFrame()
        dif1  = mdf.to_dict()
        lfn = len(fn)
        for i in range(lfn)[lfn-500:lfn]:
            try:
                res = j.loads(fn[i])
                #print res['data']
                df = p.DataFrame(res['data'])#.ix[accid, :]
                df['id'] = df.index
                df['ts'] = res['time']
                df['mid'] = map(lambda x: '%s-%s' % (df.ix[x, 'ts'], df.ix[x, 'id']), df.index)
                df = df.set_index('mid')
                #with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
                #    print df
                    #print df.to_dict()
                df = df.transpose()
            except:
                ''
            #mdf = mdf.combine_first(df)
            dif1 = combineDF3(dif1, df.to_dict())
            #dif1 = combineDF3(dif1, {'mid': df.to_dict()})
            #mdf = combineDF(mdf, df)
            if i % 100 == 0:
                print '%s of %s [%s%s]' % (i, lfn, float(i)/lfn*100, '%') #df.to_dict()
            #mdf = p.concat([mdf, df], axis=1)
        
        #try:    
        mdf = p.DataFrame(dif1)
        mdf = mdf.transpose()
        #except: df1 = p.DataFrame(dif1, index=[granularity])
        with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
            #print mdf
            #mdf = mdf[mdf['id'] == accid].sort_values(by='ts')
            #print mdf.dtypes
            #mval = 'marginCloseoutPercent'
            #mval = 'balance'
            #mval = 'resettablePLPcnt'
            #mval = 'netAssetValue'
            mval = 'unrealizedPLPcnt'
        
            #mval = 'dfgMean'
            #mval = 'dfgStddev'
        
            mdf = mdf.pivot('ts', 'id', mval)
        
            #print mdf
            #print 
            #dfstdev = p.DataFrame(n.std(mdf.get_values(), 0), index=mdf.columns)#.transpose()
            #print dfstdev
            #print mdf.dtypes
            #mdf = mdf.ix[:,'resettablePLPcnt'.split(' ')]
            mdf = mdf.sort_index()
            mdf = normalizeme(mdf)
            #mdf = sigmoidme(mdf)
            #fields = '101-004-1984564-005 101-004-1984564-012 101-004-1984564-013'.split(' ')
            fields = mdf.columns
            mdf = mdf.ix[:, fields]
        
            #x = np.arange(len(fields))
            #plt.axes(xticks=x, yscale='log')
            #ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda i, loc: fields[int(i)]))
            #plt.plot(dfstdev)
            plt.plot(mdf)
            plt.title(mval)
            plt.legend(fields, 2)
        
            plt.show()
    
    def monitorAccountsMarginCloseout(self):

        import oandapyV20.endpoints.accounts as accounts
        from oandapyV20.exceptions import V20Error
        #from matplotlib.pylab import plot

        # monitor accounts: margin closeout watcher
        p.set_option('display.float_format', lambda x: '%.3f' % x)
        mfdf = p.DataFrame()
        
        for i in self._accountList['id']:
            #print '========== %s' % i
            r = accounts.AccountDetails(accountID=i)
            try:
                rv = self.client.request(r)        
                #print float(rv['account']['marginCloseoutPercent']) * 100
                #print json.dumps(rv['account'], indent=4)        
                with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
                    #print '===='
                    mmdf = p.DataFrame(rv).ix['marginCloseoutPercent balance marginAvailable unrealizedPL resettablePL'.split(' '),'account']#.transpose()
                    mmdf['id'] = i
                    mmdf = p.DataFrame(mmdf)
                    mmdf[i] = mmdf['account']
                    mfdf = mfdf.combine_first(mmdf)            
                    #print p.DataFrame(rv)
                    #print p.DataFrame(rv['account']['positions'])            
                    #print
                    #print 'positions long'
                    try: pldf = p.DataFrame(rv['account']['positions'][1]['long'], index=[i])
                    except: ''
                    #mfdf = mfdf.combine_first(pldf.transpose())
                    #print pldf
                    #print
                    #print 'positions short'
                    try: psdf = p.DataFrame(rv['account']['positions'][1]['short'], index=[i])
                    except: ''
                    #mfdf = mfdf.combine_first(psdf.transpose())
                    #print psdf
                    #print
            except V20Error as e:
                self.qd.exception(e)
                """
                print("OOPS: {:d} {:s}".format(e.code, e.msg))
                print 'args: %s' % e.args
                print 'code: %s' % e.code
                print 'message: %s' % e.message
                print 'msg: %s' % e.msg
                """
                if e.code == 403:
                    """
                    print 'You received a 403 because the token being used in this v20 REST call is from the legacy REST API.'
                    print 'You needs to revoke this token and then generate a new one, and this will work with both the legacy and v20 REST calls.'
                    print 'source: https://github.com/bm842/Brokers/issues/3'            
                    """
            except Exception as e:
                self.qd.exception(e)
    
        with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
            mfdf = mfdf.drop('id')
            #mfdf = mfdf.set_index('id')
            mfdf = mfdf.transpose()
            mfdf = mfdf.drop('account')
            mfdf['marginCloseoutPercent'] = p.to_numeric(mfdf['marginCloseoutPercent'])
            mfdf['unrealizedPL']          = p.to_numeric(mfdf['unrealizedPL'])
            mfdf['balance']               = p.to_numeric(mfdf['balance'])
            mfdf['resettablePL']          = p.to_numeric(mfdf['resettablePL'])
            mfdf['initialCapital']        = mfdf['balance'] - mfdf['resettablePL']
            mfdf.ix['101-004-1984564-007', 'initialCapital2'] = 1000000000
            """
            mfdf['initialCapital2'] = p.Series({
                '101-004-1984564-007':1000000000,
                '101-004-1984564-001':1312.852,
                #'101-004-1984564-00':,
                #'101-004-1984564-00':,
                #'101-004-1984564-00':,
                #'101-004-1984564-00':,
                #'101-004-1984564-00':,
                #'101-004-1984564-00':,
                #'101-004-1984564-00':,
            })
            """
            mfdf['marginCloseoutPercent'] = mfdf['marginCloseoutPercent'] * 100
            mfdf['netAssetValue']         = mfdf['balance'] + mfdf['unrealizedPL'] 
            mfdf['unrealizedPLPcnt']      = mfdf['unrealizedPL'] / mfdf['balance'] * 100
            #mfdf['resettablePLPcnt']     = mfdf['resettablePL'] / (mfdf['balance'] - mfdf['resettablePL']) * 100
            mfdf['resettablePLPcnt']      = mfdf['balance'] / (mfdf['balance'] - mfdf['resettablePL']) * 100 - 100
            mfdf['marginUnrealized']      = mfdf['marginCloseoutPercent'] / mfdf['unrealizedPLPcnt']
            mfdf['marginUnrealized2']     = mfdf['unrealizedPLPcnt'] / mfdf['marginCloseoutPercent']
            mfdf['netPLPcnt']             = mfdf['resettablePLPcnt'] + mfdf['unrealizedPLPcnt']
            mfdf['netPLP']                = mfdf['resettablePL'] + mfdf['unrealizedPL']
            mfdf['resettablePLLossGainPcnt'] = 100 / (100 + mfdf['resettablePLPcnt']) * 100 - 100
            mfdf['unrealizedPLLossGainPcnt'] = 100 / (100 + mfdf['unrealizedPLPcnt']) * 100 - 100
            #fieldsMfdf = mfdf.columns
            fieldsMfdf = 'resettablePLPcnt resettablePLLossGainPcnt balance initialCapital initialCapital2 netAssetValue unrealizedPL unrealizedPLPcnt unrealizedPLLossGainPcnt resettablePL resettablePLPcnt netPLP netPLPcnt marginUnrealized marginUnrealized2 marginAvailable marginCloseoutPercent'.split(' ')

            # write to log
            import ujson as json
            import time
            mtime = time.time()
            di = {'time':mtime, 'data':mfdf.ix[:, fieldsMfdf].to_dict()}
            di = json.dumps(di)
            # append to jsonm file
            fp = open('%s/%s.jsonm' % (self.hdirMonitor, 'monitorAccountsMarginCloseout'), 'a')
            fp.write('%s\n' % di)
            fp.close()

            # write to txt file
            fname = '%s/%s.txt' % (self.hdirMonitor, 'monitorAccountsMarginCloseout')
            fp = open(fname, 'a')
            fp.write('%s\n' % mfdf.ix[:, fieldsMfdf].sort_values(by='netPLPcnt', ascending=False))
            fp.close()
            
            toEmailAddress = '???'
            self.sendEmail(fname, toEmailAddress)

            print mfdf.ix[:, fieldsMfdf].sort_values(by='marginCloseoutPercent')
            print mfdf.ix[:, fieldsMfdf].sort_values(by='netPLPcnt', ascending=False)
            print mfdf.ix[:, fieldsMfdf].sort_values(by='resettablePLPcnt', ascending=False)
            print mfdf.ix[:, fieldsMfdf].sort_values(by='marginUnrealized', ascending=False)
            print mfdf.ix[:, fieldsMfdf].sort_values(by='unrealizedPL', ascending=False)
            print mfdf.sort_values(by='resettablePL', ascending=False)

            #plot(mfdf.ix['101-004-1984564-001 101-004-1984564-002 101-004-1984564-003 101-004-1984564-004 101-004-1984564-005 101-004-1984564-008 101-004-1984564-009'.split(' '),'marginCloseoutPercent'])    


    def monitorAccountsProfitableTrades(self, verbose=False, closeProfitableTrades=False, account=None, closeProfitableTradesThreshold=0.69):

        import oandapyV20.endpoints.accounts as accounts
        from oandapyV20.exceptions import V20Error
        from multiprocessing.pool import ThreadPool

        # monitor accounts: profitable trades watcher
        mfdf = p.DataFrame()
        plpmdf = {} #p.DataFrame()
        plnmdf = {} #p.DataFrame()
        
        prices = self.getPrices()
        for i in self._accountList['id']:
            if verbose:
                self.qd.data(i, name='==========')
            #print 'NAV %s:' % rv['account']['NAV']
            r = accounts.AccountDetails(accountID=i)
            try:
                rv = self.client.request(r)        
                #print float(rv['account']['marginCloseoutPercent']) * 100
                with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
                    #print '===='             
                    mmdf = p.DataFrame(rv).ix['marginCloseoutPercent balance marginAvailable unrealizedPL resettablePL'.split(' '),'account']#.transpose()
                    mmdf['id'] = i
                    mmdf = p.DataFrame(mmdf)
                    mmdf[i] = mmdf['account']
                    mfdf = mfdf.combine_first(mmdf)            
    
                    # monitor positions
                    #apdf = p.DataFrame(rv['account']['positions'])
                    #apdf['unrealizedPL'] = p.to_numeric(apdf['unrealizedPL'])
                    #print apdf.ix[:, 'instrument pl resettablePL unrealizedPL'.split(' ')].set_index('instrument').sort_values(by='unrealizedPL', ascending=False)            
    
                    # monitor trades
                    apdf = p.DataFrame(rv['account']['trades'])
                    apdf['unrealizedPL'] = p.to_numeric(apdf['unrealizedPL'])
                    apdf['price']        = p.to_numeric(apdf['price'])
                    apdf['unrealizedPLPcnt'] = apdf['unrealizedPL'] / float(rv['account']['NAV']) * 100
                    apdf = apdf.ix[:, 'id instrument pl price currentPrice resettablePL unrealizedPL unrealizedPLPcnt'.split(' ')]#.set_index('instrument')
                    for k in apdf.index:
                        inst = apdf.ix[k, 'instrument']
                        apdf.ix[k, 'currentPrice'] =  prices.ix[inst, 'avg']
                    apdf['profitPcnt'] = n.abs(apdf['currentPrice'] / apdf['price'] * 100 - 100)
                    
                    # positive trades
                    plpdf = apdf[apdf['unrealizedPL'] > 0]
                    plpdf = plpdf[plpdf['profitPcnt'] > 0.1].set_index('id')
                    plpdf = plpdf.sort_values(by='profitPcnt', ascending=False)
                    if verbose:
                        self.qd.data(plpdf, name='plpdf 001')
                    plpdfSum = plpdf.ix[:, 'unrealizedPL unrealizedPLPcnt'.split(' ')].sum().to_dict()
                    plpmdf.update({i:plpdfSum})

                    # negative trades
                    plpndf = apdf[apdf['unrealizedPL'] < 0]
                    plpndf = plpndf[plpndf['profitPcnt'] < 0.1].set_index('id')
                    plpndf = plpndf.sort_values(by='profitPcnt', ascending=False)
                    if verbose:
                        self.qd.data(plpndf, name='plndf 002')
                    plndfSum = plpndf.ix[:, 'unrealizedPL unrealizedPLPcnt'.split(' ')].sum().to_dict()
                    plnmdf.update({i:plndfSum})

                    if closeProfitableTrades and (account == None or account == i):
                        pool = ThreadPool(processes=270)
                        for k in plpdf.index:
                            async_result = pool.apply_async(self.closeTrade, [i, k])
                            res = async_result.get()
                            #self.closeTrade(i, k)
                        pool.close()

                #print json.dumps(rv['account'], indent=4)
                #print json.dumps(rv['account']['positions'], indent=4)
                #print json.dumps(rv['account']['trades'], indent=4)
            except V20Error as e:
                self.qd.exception(e)
            except Exception as e:
                self.qd.exception(e)
        with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
            mfdf = mfdf.drop('id')
            mfdf = mfdf.transpose()
            mfdf = mfdf.drop('account')
            mfdf['marginCloseoutPercent'] = p.to_numeric(mfdf['marginCloseoutPercent'])
            mfdf['unrealizedPL']          = p.to_numeric(mfdf['unrealizedPL'])
            mfdf['balance']               = p.to_numeric(mfdf['balance'])
            mfdf['resettablePL']          = p.to_numeric(mfdf['resettablePL'])
            mfdf['marginCloseoutPercent'] = mfdf['marginCloseoutPercent'] * 100
            mfdf['unrealizedPLPcnt']      = mfdf['unrealizedPL'] / mfdf['balance'] * 100
            mfdf['resettablePLPcnt']      = mfdf['resettablePL'] / (mfdf['balance'] - mfdf['resettablePL']) * 100
            #print mfdf.sort_values(by='marginCloseoutPercent')
            #print mfdf.sort_values(by='resettablePLPcnt', ascending=False)

            def displayData(df, name=None):
                import ujson as json
                import time
                mtime = time.time()
                df['realizedTheoreticalPLPcnt'] = df['resettablePLPcnt'] * (100 + df['unrealizedPLPcnt']) / 100
                print df.ix[:, 'unrealizedPL unrealizedPLPcnt resettablePLPcnt realizedTheoreticalPLPcnt marginCloseoutPercent'.split(' ')]
                print
                # write to log
                di = {'time':mtime, 'data':df.to_dict()}
                di = json.dumps(di)
                fp = open('%s/%s.jsonm'%(self.hdirMonitor, name), 'a')
                fp.write('%s\n' % di)
                fp.close()

                dfgm = p.DataFrame([])

                df['id']  = df.index
                df['gid'] = map(lambda x: x.split('-')[2], df.index)
                dfg = df.groupby('gid')
                dfgStddevUpper = dfg.mean() + dfg.std()
                dfgStddevUpper['dfgStddevUpper'] = dfgStddevUpper['unrealizedPLPcnt']
                dfgm = dfgm.combine_first(dfgStddevUpper)

                dfgMean        = dfg.mean()
                dfgMean['dfgMean'] = dfgMean['unrealizedPLPcnt']
                dfgm = dfgm.combine_first(dfgMean)

                dfgStddevLower = dfg.mean() - dfg.std()
                dfgStddevLower['dfgStddevLower'] = dfgStddevLower['unrealizedPLPcnt']
                dfgm = dfgm.combine_first(dfgStddevLower)

                dfgStddev = dfg.std()
                dfgStddev['dfgStddev'] = dfgStddev['unrealizedPLPcnt']
                dfgm = dfgm.combine_first(dfgStddev)

                fields = 'dfgStddevUpper dfgMean dfgStddevLower dfgStddev'.split(' ')
                print dfgm.ix[:, fields]
                # write to log
                di = {'time':mtime, 'data':dfgm.ix[:, fields].to_dict()}
                di = json.dumps(di)
                fp = open('%s/%s.stats.jsonm'%(self.hdirMonitor, name), 'a')
                fp.write('%s\n' % di)
                fp.close()
                #print dfg.describe()

            plpmdf = p.DataFrame(plpmdf).transpose()
            plnmdf = p.DataFrame(plnmdf).transpose()
            plpmdf = plpmdf.combine_first(mfdf)
            plnmdf = plnmdf.combine_first(mfdf)
            plpmdf = plpmdf.sort_values(by='unrealizedPLPcnt', ascending=False)
            plnmdf = plnmdf.sort_values(by='unrealizedPLPcnt', ascending=False)
            # close trade if above a specified threshold
            for i in plpmdf.index:
                if plpmdf.ix[i, 'unrealizedPLPcnt'] >= closeProfitableTradesThreshold:
                    closeProfitableTrades                  = True
                    #monitorAccountsProfitableTradesVerbose = False
                    #if args.account:
                    #      account = args.account
                    #else: account= None
                    # bind accid variable to account connecting - ca with cpt options
                    account = i
                    self.monitorAccountsProfitableTrades(verbose=False, closeProfitableTrades=closeProfitableTrades, account=account)
            # print dataframes
            if verbose:
                print
                print '== Monitor UnrealizedPL and UnrealizedPL% (+trades)'
                displayData(plpmdf, name='monitorAccountsProfitableTradesPLP')
                print
                print '== Monitor UnrealizedPL and UnrealizedPL% (-trades)'
                displayData(plnmdf, name='monitorAccountsProfitableTradesPLN')

        #plot(mfdf.ix['101-004-1984564-001 101-004-1984564-002 101-004-1984564-003 101-004-1984564-004 101-004-1984564-005 101-004-1984564-008 101-004-1984564-009'.split(' '),'marginCloseoutPercent'])    

    def closeTrade(self, accountID, tradeID):

        import oandapyV20.endpoints.trades as trades
        try:
            print 'closing trade: %s %s' % (accountID, tradeID)
            self.qd.data('closing trade: %s %s' % (accountID, tradeID))
            data = {}
            r = trades.TradeClose(accountID=accountID, tradeID=tradeID, data=data)
            self.client.request(r)
            self.qd.data(r.response, name='closeTrade:: 002')
        except Exception as e:        
            self.qd.exception(e)
    
    def getPrices(self):
        import oandapyV20.endpoints.pricing as pricing
        symbols  = 'AUD_CAD,AUD_CHF,AUD_HKD,AUD_JPY,AUD_NZD,AUD_SGD,AUD_USD,CAD_CHF,CAD_HKD,CAD_JPY,CAD_SGD,CHF_HKD,CHF_JPY,CHF_ZAR,EUR_AUD,EUR_CAD,EUR_CHF,EUR_DKK,EUR_GBP,EUR_HKD,EUR_HUF,EUR_JPY,EUR_NOK,EUR_NZD,EUR_PLN,EUR_SEK,EUR_SGD,EUR_TRY,EUR_USD,EUR_ZAR,GBP_AUD,GBP_CAD,GBP_CHF,GBP_HKD,GBP_JPY,GBP_NZD,GBP_PLN,GBP_SGD,GBP_USD,GBP_ZAR,HKD_JPY,NZD_CAD,NZD_CHF,NZD_HKD,NZD_JPY,NZD_SGD,NZD_USD,SGD_CHF,SGD_HKD,SGD_JPY,TRY_JPY,USD_CAD,USD_CHF,USD_CNH,USD_CZK,USD_DKK,USD_HKD,USD_HUF,USD_JPY,USD_MXN,USD_NOK,USD_PLN,USD_SEK,USD_SGD,USD_THB,USD_TRY,USD_ZAR,ZAR_JPY'
        #.split(',')
        #print symbols
        params = {"instruments": symbols}
        #params = {"instruments": "EUR_USD,EUR_JPY"}
        r = pricing.PricingInfo(accountID='101-004-1984564-001', params=params)
        try:
            rv = self.client.request(r)
        except Exception as e:
            self.qd.exception(e)
        with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
            instruments = p.DataFrame(r.response['prices']).set_index('instrument').transpose()
            instruments = instruments.ix['closeoutAsk closeoutBid'.split(' '), :].transpose()
            instruments['closeoutAsk'] = p.to_numeric(instruments['closeoutAsk'])
            instruments['closeoutBid'] = p.to_numeric(instruments['closeoutBid'])
            instruments['avg'] = (instruments['closeoutAsk'] + instruments['closeoutBid'])/2
            #print instruments
        return instruments

    def computePortfolioMetatrader(self, dfu33, balance=None, leverage=None, method="metatrader"):
        if balance: balance = balance
        else:       balance = 110.81
        if leverage: leverage = leverage
        else:       leverage = 500.0
        dfu33['balanceMetatrader'] = balance
        dfu33['leverageMetatrader'] = leverage
        
        def calcLots(dfu33, method):
            dfu33 = dfu33.copy()
            # ---======
            dfu33['allMarginMetatrader'] = dfu33['balanceMetatrader'] * dfu33['leverageMetatrader']
            dfu33['amount2Metatrader'] = dfu33['allMarginMetatrader'] * dfu33['diffp']
            dfu33['lots']      = n.round(dfu33['amount2Metatrader'] / 100000.0, 2)
    
            # rebalance for etoro
            if method == "etoro":
                dfu33['diffp'] = p.to_numeric(dfu33['diffp'])
                dfu33['leverageEtoro'] = 25
                dfu33['maxLeverageEtoro'] = n.round(dfu33['amount2Metatrader'] / dfu33['leverageEtoro'], 2)
                
                li = n.array([1,2,5,10,25,50,100,200,400])
                for i in dfu33['maxLeverageEtoro'].index:
                    try:    dfu33.ix[i, 'minimumLeverageEtoro'] =  n.max(li[li < dfu33.ix[i, 'maxLeverageEtoro']])
                    except: ''
                dfu33['lotsEtoro'] = n.round(dfu33['amount2Metatrader'] / dfu33['minimumLeverageEtoro'], 2)
                dfu33['unitsEtoro'] = n.round(dfu33['minimumLeverageEtoro'] * dfu33['lotsEtoro'], 2)
            # ---======
            return dfu33
        
        dfu33 = calcLots(dfu33, method)

        if method == "etoro":
            _lotsEtoroRT = 0
            for i in dfu33['lotsEtoro'].index:
                if _lotsEtoroRT + float(dfu33.ix[i, 'lotsEtoro']) <= balance:
                    _lotsEtoroRT += float(dfu33.ix[i, 'lotsEtoro'])
                    try:
                        dfu33.ix[i, '_lotsEtoroRT']  = _lotsEtoroRT
                        dfu33.ix[i, '_lotsEtoroRT2'] = dfu33.ix[i, 'lotsEtoro']
                    except: ''
            dfu33['_lotsEtoroRT2']     = dfu33['_lotsEtoroRT2'].fillna(0)
            dfu33['_boolLotsEtoroRT2'] = dfu33['_lotsEtoroRT2'] > 0
            dfu33['_diffpLotsEtoro']   = dfu33.ix[list(dfu33['_boolLotsEtoroRT2']), 'diffp']
            dfu33['diffp']             = dfu33['_diffpLotsEtoro'] / n.sum(dfu33['_diffpLotsEtoro'])
            
            dfu33 = dfu33[dfu33['_boolLotsEtoroRT2'] == True]
            dfu33 = calcLots(dfu33, method)

            dfu33['_minimumLeverageEtoro2'] = dfu33['unitsEtoro'] / dfu33['_lotsEtoroRT2']
            
            dfu33_etoro = dfu33[dfu33['diffp'] >= 0.06].copy()
            self.qd.printf(True)
            self.qd.data('              balance: %s' % balance)
            self.qd.data('    sum _lotsEtoroRT2: %s' % n.sum(dfu33['_lotsEtoroRT2']))
            self.qd.data('            sum diffp: %s' % n.sum(dfu33['diffp']))
            self.qd.data('  sum _diffpLotsEtoro: %s' % n.sum(dfu33['_diffpLotsEtoro']))
            self.qd.data('        sum lotsEtoro: %s' % n.sum(dfu33['lotsEtoro']))
            self.qd.data('       sum unitsEtoro: %s' % n.sum(dfu33['unitsEtoro']))
            self.qd.data('sum amount2Metatrader: %s' % n.sum(dfu33['amount2Metatrader']))
            self.qd.data('   balance * leverage: %s' % (balance * leverage))
            self.qd.printf(False)
        return dfu33

    def cacheOandapyV20Request(self, r, fname, age=30000):
        import os, time, requests
        import ujson as j
        
        def makeRequest(r):
            # read/download
            print 'requesting..'
            co = p.read_csv('/mldev/bin/datafeeds/config.csv', header=None)
            loginIndex = 2
            env0=co.ix[loginIndex,1]
            access_token0=co.ix[loginIndex,2]
            client = oandapyV20.API(access_token=access_token0)
            #print client.request(r)
            rv = client.request(r)
            # write to cache file
            fp = open(fname, 'w')
            fp.write(j.dumps(rv))
            fp.close()
            return rv
        
        def cacheRequest(r):
            print 'caching..'
            # cache
            fp = open(fname, 'r')
            rv = fp.read()
            rv = j.loads(rv)
            fp.close()
            return rv
    
        try:
            stat = os.stat(fname)
            if time.time() - stat.st_mtime >= age:
                return makeRequest(r)
            else:
                return cacheRequest(r)
        except:
            return makeRequest(r)
    

    def getTransactions(self, accountID):
        params = {
                  #"to": 400,
                  "to": df.ix[0,'lastTransactionID'],
                  "from": 1
        }
        r = trans.TransactionIDRange(accountID=accountID, params=params)
        client.request(r)
        #print p.DataFrame(r.response)
        df = p.DataFrame()
        with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
            for i in r.response['transactions']:
                try:
                    #print i
                    #print len(i)
                    #print i.keys()
                    #print i.values()
                    dfi = p.DataFrame(i, index=[0])
                    dfi['id'] = p.to_numeric(dfi['id'])
                    #print dfi.columns
                    #df = df.combine_first(dfi.set_index('id'))
                    df = df.combine_first(dfi.set_index('time'))
                except:
                    ''
        df['accountBalance'] = p.to_numeric(df['accountBalance'])
        df['accountBalance'] = df['accountBalance'].bfill().ffill()
        #print df.dtypes
        #print df#.sort_index()
        df = df.ix[:,'accountBalance']
        #print df 
        #%pylab inline
        #df.plot()
        df.to_csv('/mldev/bin/data/oanda/cache/transactions/transactions.%s.csv' % accountID)
        return df


def getc4(df, dfh, oanda2, instrument='USD_JPY', verbose=False, update=False):
    import hashlib as hl
    import talib
    if int(verbose) >= 5: qd.data('df.shape 1: %s' % str(df.shape))
    dfm = p.DataFrame()
    patterns = ['CDL2CROWS',
     'CDL3BLACKCROWS',
     'CDL3INSIDE',
     'CDL3LINESTRIKE',
     'CDL3OUTSIDE',
     'CDL3STARSINSOUTH',
     'CDL3WHITESOLDIERS',
     'CDLABANDONEDBABY',
     'CDLADVANCEBLOCK',
     'CDLBELTHOLD',
     'CDLBREAKAWAY',
     'CDLCLOSINGMARUBOZU',
     'CDLCONCEALBABYSWALL',
     'CDLCOUNTERATTACK',
     'CDLDARKCLOUDCOVER',
     'CDLENGULFING',
     'CDLEVENINGSTAR',
     'CDLGAPSIDESIDEWHITE',
     'CDLHAMMER',
     'CDLHANGINGMAN',
     'CDLHARAMI',
     'CDLHARAMICROSS',
     'CDLHIGHWAVE',
     'CDLHIKKAKE',
     'CDLHIKKAKEMOD',
     'CDLHOMINGPIGEON',
     'CDLIDENTICAL3CROWS',
     'CDLINNECK',
     'CDLINVERTEDHAMMER',
     'CDLKICKING',
     'CDLKICKINGBYLENGTH',
     'CDLLADDERBOTTOM',
     'CDLLONGLINE',
     'CDLMARUBOZU',
     'CDLMATCHINGLOW',
     'CDLMATHOLD',
     'CDLMORNINGSTAR',
     'CDLONNECK',
     'CDLPIERCING',
     'CDLRICKSHAWMAN',
     'CDLRISEFALL3METHODS',
     'CDLSEPARATINGLINES',
     'CDLSHOOTINGSTAR',
     'CDLSHORTLINE',
     'CDLSPINNINGTOP',
     'CDLSTALLEDPATTERN',
     'CDLSTICKSANDWICH',
     'CDLTAKURI',
     'CDLTASUKIGAP',
     'CDLTHRUSTING',
     'CDLTRISTAR',
     'CDLUNIQUE3RIVER',
     'CDLUPSIDEGAP2CROWS',
     'CDLXSIDEGAP3METHODS']
    """
    'CDLDOJI',
     'CDLDOJISTAR',
     'CDLDRAGONFLYDOJI',
     'CDLEVENINGDOJISTAR',
     'CDLGRAVESTONEDOJI',
     'CDLLONGLEGGEDDOJI',
     'CDLMORNINGDOJISTAR'
    """
    qd = QoreDebug()
    qd.on()
    #@profile
    #def goThruPatterns(df, dfm, dfh, oanda2, patterns, instrument='USD_JPY', update=False):
    df1 = df
    dif1  = df1.to_dict()
    verbose=False
    for i in patterns:
        if int(verbose) >= 5: qd.data('goThruPatterns(%s): %s' % (instrument, i))
        #dfm0 = getccc(df, dfh, oanda2, i, instrument=instrument, update=update)
        #@profile
        #def getccc(df, dfh, oanda2, mode, instrument='USD_JPY', update=False):    
        ##def getcc(df, dfh, oanda2, mode, instrument='USD_JPY', update=False):
        mode=i
        for j in 'M1 M5 M15 M30 H1 H4 D W M'.split(' '):
            #qd.data('goThruPatterns(%s): %s' % (instrument, j))
            #qd.data('df1.shape 2: %s' % str(df1.shape))
            #df1 = getc(df1, dfh, oanda2, instrument=instrument, granularity=j, mode=mode, update=update, verbose=verbose)
            
            #@profile
            #def getc(df1, dfh, oanda2, instrument='USD_JPY', granularity='M1', mode='CDLBELTHOLD', verbose=False, update=False):
            granularity=j
        
            if update:
                try: dfh[instrument][granularity] = None
                except: ''
            
            try:
                if int(verbose) >= 5: qd.data('caching history %s.. ' % granularity)
                res = dfh[instrument][granularity]
            except Exception as e:
                if int(verbose) >= 5: qd.data(e)
                if int(verbose) >= 5: qd.data('getting history %s.. ' % granularity)
                res = oanda2.get_history(instrument=instrument, granularity=granularity, count=15)
                try:
                    dfh[instrument][granularity] = p.DataFrame(res['candles']).set_index('time')
                except:
                    dfh[instrument] = {}
                    dfh[instrument][granularity] = p.DataFrame(res['candles']).set_index('time')
            csvIndex = ','.join(list(dfh[instrument][granularity].index))
            #qd.data(csvIndex)
            if int(verbose) >= 5: 
                qd.data(hl.md5(csvIndex).hexdigest())
                print
                qd.data('instrument/granularity: %s/%s' % (instrument, granularity))
            
        
    for i in patterns:
        if int(verbose) >= 5: qd.data('goThruPatterns(%s): %s' % (instrument, i))
        #dfm0 = getccc(df, dfh, oanda2, i, instrument=instrument, update=update)
        #@profile
        #def getccc(df, dfh, oanda2, mode, instrument='USD_JPY', update=False):    
        ##def getcc(df, dfh, oanda2, mode, instrument='USD_JPY', update=False):
        mode=i
        for j in 'M1 M5 M15 M30 H1 H4 D W M'.split(' '):
            granularity=j
            exec("pnda = talib.%s(dfh[instrument][granularity]['openBid'].get_values(), dfh[instrument][granularity]['highBid'].get_values(), dfh[instrument][granularity]['lowBid'].get_values(), dfh[instrument][granularity]['closeBid'].get_values())" % mode)
            #qd.data('%s: %s' % (len(dfh[instrument][granularity]), len(pnda)))
            #df1[granularity] = pnda
            #dfh[instrument][granularity][granularity] = pnda
            #qd.data(dfh[instrument][granularity].ix[:,granularity])
            #df1 = normalizeme(df1)
            #df1 = sigmoidme(df1)
            #df1 = tanhme(df1)
            # original
            #df1 = df1.combine_first(dfh[instrument][granularity].ix[dfh[instrument][granularity].ix[:,'complete'],[granularity]])
            # cythonized
            # df1 = p.concat([df1, df2], axis=1)
            #qd.data(dfh)
            #nsrch = dfh[instrument][granularity].ix[:,'complete']
            nsrch = dfh[instrument][granularity]['complete']
            #dfh0 = dfh[instrument][granularity].ix[nsrch,[granularity]]

            #dfh0_0 = dfh[instrument][granularity][granularity].ix[nsrch]
            #qd.data('type dfh[instrument][granularity][granularity]: %s' % type(dfh[instrument][granularity][granularity]))
            pnda = p.Series(pnda, index=nsrch.index)
            #qd.data('type pnda: %s' % type(pnda))
            #qd.data('shape pnda: %s' % pnda.shape)
            #qd.data('shape nsrch: %s' % nsrch.shape)
            #qd.data(pnda)
            #qd.data(nsrch)
            dfh0_0 = pnda.ix[nsrch]
            
            #dfh0 = p.DataFrame(dfh0_0, columns=[granularity])
            #dfh0 = dfh0.combine_first(dfh0_0)
            
            #dfh0 = p.DataFrame([], index=dfh0_0.index)
            #dfh0[granularity] = dfh0_0

            #******
            #dfh0 = p.DataFrame(dfh0_0, index=dfh0_0.index)
            #dict(zip(df.index, df.get_values().tolist()))
            difh0 = {granularity: dict(zip(dfh0_0.index, dfh0_0.get_values().tolist()))}
	

            #difh0 = dfh0.to_dict()
            #qd.data(difh0)
            #sys.exit()

            #df1 = combineDF(dif1, difh0)
            #df1 = combineDF2(dif1, difh0)
            
            dif1 = combineDF3(dif1, difh0)
            
            #df1 = combineDF(df1, dfh0)
            #df1 = p.concat([df1, dfh0], axis=1)
            
            #qd.data('%s %s' % (instrument, granularity))
            #qd.data(dfh[instrument][granularity].ix[dfh[instrument][granularity].ix[:,'complete'], [granularity]])
            #if int(verbose) >= 5: qd.data(df1.columns)
            #qd.data(df1.ix[:,'openBid highBid lowBid closeBid'.split(' ')])
            #return df1
            #return dfh[instrument][granularity].ix[dfh[instrument][granularity].ix[:,'complete'],[granularity]]


            #qd.data('df1.shape 3: %s' % str(df1.shape))
        #return df1#.set_index('mode')
        try:    df1 = p.DataFrame(dif1)
        except: df1 = p.DataFrame(dif1, index=[granularity])
        #df1['mode'] = mode
        #df1 = getcc(df1, dfh, oanda2, mode, instrument=instrument, update=update)
        dfm1 = df1
        #qd.data(dfm1.tail(3))
        dfm1 = dfm1.ffill()
        #qd.data(dfm1.tail(3))
        dfm1 = dfm1.bfill()
        if int(verbose) >= 5: qd.data(dfm1.tail(3))
        dfm1 = dfm1.tail(1)
        if int(verbose) >= 5: qd.data(dfm1)
        dfm1 = dfm1.ix[:, 'M1 M5 M15 M30 H1 H4 D W M'.split(' ')]
        if int(verbose) >= 5: qd.data(dfm1)
        dfm1 = dfm1.transpose()
        if int(verbose) >= 5: qd.data(dfm1)
        #dfm1 = df1.ffill().bfill().tail(1).ix[:, 'M1 M5 M15 M30 H1 H4 D W M'.split(' ')].transpose()
        if int(verbose) >= 5: qd.data('len df1: %s' % len(df1))
        sed = df1.index[len(df1)-1]
        #qd.data(sed)
        dfm1[mode] = dfm1.ix[:, sed]
        #return dfm1.ix[:, [mode]]
        dfm0 = dfm1.ix[:, [mode]]
        if int(verbose) >= 5: qd.data(dfm0)
        #dfm  = dfm.combine_first(dfm0)
        dfm = p.concat([dfm, dfm0], axis=1)
        if verbose:
            qd.data('dfm1.shape: %s' % str(dfm1.shape))
            qd.data('dfm.shape: %s' % str(dfm.shape))
            qd.data('dfm0.shape: %s' % str(dfm0.shape))
            qd.data('df.shape: %s' % str(df.shape))
            qd.data('dfh.shape: %s' % len(dfh))

    #from numba import double
    #from numba.decorators import jit, autojit
    #goThruPatterns_numba = autojit(goThruPatterns)
    #dfm = goThruPatterns_numba(df, dfm, dfh, oanda2, patterns, instrument=instrument, update=update)
    #dfm = goThruPatterns(df, dfm, dfh, oanda2, patterns, instrument=instrument, update=update)
    with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
        dfm = dfm.transpose()
        dfmg = dfm > 0
        dfml = dfm < 0
        dfm['buy']  = n.sum(n.array(dfmg.get_values(), dtype=int), 1)
        dfm['sell'] = n.sum(n.array(dfml.get_values(), dtype=int), 1)
        dfm = dfm.transpose()
        dfm.ix[:, instrument] = n.sum(dfm.get_values(), 1)
        #qd.data(n.sum(n.array(dfmk.transpose().get_values(), dtype=int), 0))
        #if int(verbose) >= 5: qd.data(dfm.transpose())
        res = dfm.transpose().ix[[instrument],:]
        #qd.data(res)
        #qd.data(instrument)
        return res

def differentPolarity(a, b):
    return n.logical_or(n.logical_and(a < 0, b > 0), n.logical_and(a > 0, b < 0))

def getSideBool(ser):
    return map(lambda x: 1 if x == 'buy' else -1, ser)

#@profile
def calcPl(bid, ask, price, sideBool, pairedCurrencyBid, pairedCurrencyAsk, units):
    #pl00001 = ( ((bid+ask)/2) )
    #pl00002 = ( price )
    #pl00003 = ((pairedCurrencyBid+pairedCurrencyAsk)/2)
    #pl00004 = (1 / ((pairedCurrencyBid+pairedCurrencyAsk)/2))
    #pl00005 = ( ((bid+ask)/2) - price ) * (1 / ((pairedCurrencyBid+pairedCurrencyAsk)/2))
    #qd.data('sideBool:%s' % sideBool)
    lsb = len(sideBool)
    close = n.zeros(lsb)
    pairedCurrencyClose = n.zeros(lsb)
    #close = map(lambda x: , sideBool)
    for i in range(lsb):
        #if sideBool[i] == 1: 
        #    close[i] = ask[i]
        #    pairedCurrencyClose[i] = pairedCurrencyAsk[i]
        #else:                
        #    close[i] = bid[i]
        #    pairedCurrencyClose[i] = pairedCurrencyBid[i]
        try:    close[i]               = ask[i]               if sideBool[i] == 1 else bid[i]
        except: ''
        try:    pairedCurrencyClose[i] = pairedCurrencyAsk[i] if sideBool[i] == 1 else pairedCurrencyBid[i]
        except: ''
    #if sideBool == 1:
    #    close               = bid
    #    pairedCurrencyClose = pairedCurrencyBid
    #if sideBool == -1:
    #    close               = ask
    #    pairedCurrencyClose = pairedCurrencyAsk
    #return ( ( (bid + ask) / 2) - price ) * sideBool * (1 / ((pairedCurrencyBid + pairedCurrencyAsk) / 2)) * units
    return ( close - price ) * sideBool * (1 / pairedCurrencyClose) * units

def getCurrentTrades(oanda2, oq, accid, currentPositions, loginIndex=None):
    qd = QoreDebug()
    qd.on()
    #qd.off()
    from numpy import zeros as n_zeros
    
    import oandapyV20
    import oandapyV20.endpoints.trades as trades
    import oandapyV20.endpoints.accounts as accounts
    co, loginIndex, env0, access_token0, oanda0 = getConfig(loginIndex=loginIndex)
    client = oandapyV20.API(access_token=access_token0)

    try:
        r = trades.TradesList(accid)
        rv = client.request(r)
        currentTradesV20                 = p.DataFrame(rv['trades'])
        currentTradesV20['price']        = p.to_numeric(currentTradesV20['price'])
        currentTradesV20['initialUnits'] = p.to_numeric(currentTradesV20['initialUnits'])
        currentTradesV20['units']        = n.absolute(currentTradesV20['initialUnits'])
        currentTradesV20['side']         = map(lambda x: 'buy' if x > 0 else 'sell', currentTradesV20['initialUnits'])
        qd.data('accid 00101: %s' % accid)
        qd.data('access_token0 00101: %s' % access_token0)
        qd.data(currentTradesV20, name='currentTradesV20 0010')
    except Exception as e:
        qd.data('err: %s' % e)
        currentTradesV20 = p.DataFrame([])
    """
    with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
        try:
            #qd.data(currentTradesV20.dtypes)
            #currentTradesV20 = currentTradesV20.convert_objects(convert_numeric=True)
            currentTradesV20['unrealizedPL'] = p.to_numeric(currentTradesV20['unrealizedPL'])
            mdf = currentTradesV20.sort_values(by='unrealizedPL', ascending=False)
            #qd.data(mdf[mdf['unrealizedPL'] > 0])
            qd.data(mdf)
        except: ''
    """
    try:
        currentTrades = oanda2.get_trades(accid, count=500)['trades']    
        currentTrades = p.DataFrame(currentTrades)
    except:
        currentTrades = p.DataFrame([])

    with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
        qd.data(currentTrades, name='currentTrades:: 00101')
        currentTrades = currentTrades.combine_first(currentTradesV20)
        qd.data(currentTrades, name='currentTrades:: 00102')
    
    try:
        r = accounts.AccountInstruments(accid)
        rv = client.request(r)
        instrumentsV20 = p.DataFrame(rv['instruments']).set_index('name')
        instrumentsV20['pip'] = n.power(10.0, instrumentsV20['pipLocation']) # convert legacy pip to v20
        with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
            qd.data(instrumentsV20, name='instruments 00103a')
    except Exception as e:
        qd.data('err: %s' % e)
        instrumentsV20 = p.DataFrame([])

    # source: http://stackoverflow.com/questions/33126477/pandas-convert-objectsconvert-numeric-true-deprecated
    try:
        #instruments = p.DataFrame(oanda2.get_instruments(accid)['instruments']).set_index('instrument').convert_objects(convert_numeric=True)
        instruments = p.DataFrame(oanda2.get_instruments(accid)['instruments']).set_index('instrument')
    except:
        instruments = p.DataFrame([])
    instruments = instruments.combine_first(instrumentsV20)
    qd.data(instruments, name='instruments 00103b')
    qd.data(currentPositions, name='currentPositions 00104')
    instruments['pip'] = p.to_numeric(instruments['pip'])
    currentPrices = oanda2.get_prices(instruments=','.join(list(currentPositions.index)))['prices']
    currentPrices = p.DataFrame(currentPrices).set_index('instrument')
    currentTrades = currentTrades.sort_values(by=['instrument', 'id'], ascending=[True, True]).set_index('instrument')
    currentTrades = currentTrades.combine_first(currentPrices)
    #currentTrades = currentTrades.combine_first(instruments)
    #currentTrades = p.concat([currentTrades, instruments], axis=0, join='outer')
    currentTrades = currentTrades.join(instruments, how='inner')
    currentTrades['instrument'] = currentTrades.index
    currentTrades['sideBool'] = getSideBool(currentTrades['side'])
    currentTrades['sideS'] = n_zeros(len(currentTrades))
    for i in xrange(len(currentTrades)):
        currentTrades.ix[i, 'sideS'] = currentTrades.ix[i, 'bid'] if currentTrades.ix[i, 'sideBool']  > 0 else currentTrades.ix[i, 'ask']
    currentTrades['plpips'] = (currentTrades['sideS'] - currentTrades['price']) / currentTrades['pip'] * currentTrades['sideBool']
    #currentTrades['pl'] = (currentTrades['sideS'] - currentTrades['price']) * currentTrades['units'] * currentTrades['sideBool'] #*  currentTrades['pip']

    #    ctsdf = getSyntheticCurrencyTable(oanda2, oq, ct['instrument'])
    #    
    #    ct['indx'] = ct.index
    #    ct['rg'] = range(0, len(ct.index))
    #    ct = ct.set_index('rg')
    #    ct = ct.combine_first(ctsdf)
    #    ct = ct.set_index('indx')
    ctsdf = getSyntheticCurrencyTable(oanda2, oq, currentTrades['instrument'])    
    currentTrades['indx'] = currentTrades.index
    currentTrades['rg'] = range(0, len(currentTrades.index))
    currentTrades = currentTrades.set_index('rg')
    currentTrades = currentTrades.combine_first(ctsdf)
    currentTrades = currentTrades.set_index('indx')

    currentTrades['pairedCurrencyAsk'] = currentTrades['pairedCurrencyAsk'].fillna(1)
    currentTrades['pairedCurrencyBid'] = currentTrades['pairedCurrencyBid'].fillna(1)

    currentTrades['tradeValue'] = currentTrades['units'] * currentTrades['quotedCurrencyAsk']
    currentTrades['tradeValue2'] = currentTrades['units'] * currentTrades['pairedCurrencyAsk']
    currentTrades['tradeValue3'] = 1.0 / currentTrades['pairedCurrencyAsk']
    currentTrades['tradeValue4'] = currentTrades['sideS'] - currentTrades['price']
    currentTrades['tradeValue5'] = currentTrades['units'] * currentTrades['tradeValue3'] * currentTrades['tradeValue4']
    currentTrades['pl'] = calcPl(currentTrades['bid'], currentTrades['ask'], currentTrades['price'], currentTrades['sideBool'], currentTrades['pairedCurrencyBid'], currentTrades['pairedCurrencyAsk'], currentTrades['units'])

    #with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
    #    qd.data(currentTrades.sort_values(by='pl'), name='currentTrades')
    for i in xrange(len(currentTrades)):
        currentTrades.ix[i, 'pl'] = currentTrades.ix[i, 'pl'] / 100 if currentTrades.ix[i, 'pip'] == 0.01 else currentTrades.ix[i, 'pl']
    return currentTrades

def interactiveMode(defaultMsg='Sure you want to create order? (y/N/q): '):
    qd.data('interactiveMode()')
    ans = raw_input(defaultMsg)
    if ans.strip() == 'q':
        sys.exit()
        return
    if ans.strip() != 'y':
        raise(Exception('User intervened: order not created'))


def oandaCloseTrade(oanda2, accid, ticket, method=None, data=None):
    qd = QoreDebug()
    qd.on()
    #qd.off()
    import pymongo as mong
    try:
        oanda2.close_trade(accid, ticket)
        # collect trade data
        di = {'method':'oandaCloseTrade::%s' % method, 'account':accid, 'ticket':ticket, 'type':'close-trade', 'data':data}
        mongo = mong.MongoClient()
        mongo.ql.broker_oanda_trades.insert(di)
        mongo.close()
    except Exception as e:
        qd.exception(e)

def oandaCreateOrder(oanda2, accid, instrument, side, units, method=None, data=None):
    qd = QoreDebug()
    qd.on()
    #qd.off()
    import pymongo as mong
    try:
        oanda2.create_order(accid, type='market', instrument=instrument, side=side, units=units)
        # collect trade data
        di = {'method':'oandaCreateOrder::%s' % method, 'account':accid, 'type':'market', 'instrument':instrument, 'side':side, 'units':units, 'data':data}
        mongo = mong.MongoClient()
        mongo.ql.broker_oanda_trades.insert(di)
        mongo.close()
    except Exception as e:
        qd.exception(e)
    
#@profile
def fleetingProfitsCloseTrade(oanda2, dryrun, accid, i, plp, noInteractiveFleetingProfits, noInteractiveLeverage, noInteractiveDeleverage, verbose=False):
    qd = QoreDebug()
    qd.on()
    #qd.off()
    import ujson as json
    if dryrun == False:
        try:
            if int(verbose) > 7: plp.ix[i,:]
            if int(verbose) >= 2: qd.data("oanda2.close_trade(%s, %s, %s, %s) %s" % (plp.ix[i, 'instrument'], plp.ix[i, 'units'], accid, i, plp.ix[i, 'pl']))
            if not noInteractiveFleetingProfits:
                if noInteractiveLeverage: raise(Exception('nil --> nif conflict'))
                if noInteractiveDeleverage: raise(Exception('nid --> nif conflict'))
                interactiveMode()
            oandaCloseTrade(oanda2, accid, i, method='fleetingProfitsCloseTrade', data=json.dumps(plp.ix[ticket, :].fillna(0).to_dict()))
        except Exception as e:
            qd.exception(e)

#@profile
def leverageTrades(dryrun, oanda2, dfu3, accid, i, side, units, noInteractiveLeverage, noInteractiveDeleverage, noInteractiveFleetingProfits, verbose, noInteractive, currentTrades, loginIndex=None):
    qd = QoreDebug()
    qd.on()
    #qd.off()
    #import pymongo as mong
    import ujson as json
    if dryrun == False:
        try:
            if noInteractiveLeverage == True or noInteractiveDeleverage == True:
                #noInteractive = True
                ''
            if int(verbose) >= 5:
                qd.data('deleverageBool:          %s' % dfu3.ix[i, 'deleverageBool'])
                qd.data('noInteractive:           %s' % noInteractive)
                qd.data('noInteractiveLeverage:   %s' % noInteractiveLeverage)
                qd.data('noInteractiveDeleverage: %s' % noInteractiveDeleverage)
                qd.data('noInteractiveFleetingProfits: %s' % noInteractiveFleetingProfits)
            if dfu3.ix[i, 'deleverageBool'] == True and (not noInteractive and not noInteractiveDeleverage):
                if int(verbose) >= 5: qd.data('nid---')
                if noInteractiveLeverage: raise(Exception('nil --> nid conflict'))
                if noInteractiveFleetingProfits: raise(Exception('nif --> nid conflict'))
                #qd.data(ct.sort_values(by=['pl'], ascending=[False]))
                dfu = currentTrades[currentTrades['instrument'] == i]
                dfu['plPerUnit'] = dfu['pl'] / dfu['units']
                dfu = dfu.sort_values(by=['plPerUnit', 'units'], ascending=[False, True])
                with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
                    if int(verbose) >= 7:
                        qd.data(dfu)
                if int(verbose) >= 5: 
                    qd.data('pl: %s' % currentTrades[currentTrades['instrument'] == i].ix[:,'pl'].sum())
                    print
                    qd.data('# selective deleverage')
                unitsLeft = units
                for j in dfu.index:
                    
                    prevUnitsLeft = unitsLeft
                    unitsLeft -= dfu.ix[j, 'units']
                    closeBool = True if unitsLeft >= 0 else False
                    if int(verbose) >= 8:
                        qd.data('ticket:%s units:%s units:%s unitsLeft:%s closeBool:%s' % (j, dfu.ix[j, 'units'], units, unitsLeft, closeBool))
                    
                    try:
                        partialDeleverageLoss = dfu3.ix[i, 'deleverageLoss'] * dfu.ix[j, 'units'] / dfu3.ix[i, 'units']
                        dloss = 'loss[partialDeleverageLoss/deleverageLoss/unitsj/unitsi]:%.3f/%.3f/%.3f/%.3f' % (partialDeleverageLoss, dfu3.ix[i, 'deleverageLoss'], dfu.ix[j, 'units'], dfu3.ix[i, 'units'] )
                        if closeBool:
                            interactiveMode(defaultMsg='Sure you want to partialClose[%s] ticket %s %s %s? unitsLeft:%s prevUnitsLeft:%s %s  (y/N/q): ' % (i, j, dfu.ix[j, 'side'], dfu.ix[j, 'units'], unitsLeft, prevUnitsLeft, dloss))
                            logApplicationUsage('d', description='deleverage[partialClose]', data=dfu.ix[j, :].to_dict())
                            if int(verbose) >= 5: qd.data('oanda2.close_trade(%s, %s)' % (accid, j))
                            
                            #oanda2.close_trade(accid, j)
                            ## collect trade data
                            #di = {'method':'leverageTrades[deleverage:partial-close]', 'account':accid, 'ticket':j, 'type':'close-trade', 'data':json.dumps(dfu.ix[j, :].fillna(0).to_dict())}
                            #mongo = mong.MongoClient()
                            #mongo.ql.broker_oanda_trades.insert(di)
                            #mongo.close()
                            oandaCloseTrade(oanda2, accid, j, method='leverageTrades[deleverage:partial-close]', data=json.dumps(dfu.ix[j, :].fillna(0).to_dict()))
                        else:
                            if prevUnitsLeft > 0:
                                interactiveMode(defaultMsg='Sure you want to deleverage %s[%s]? side=%s, units=%s %s (y/N/q): ' % (i, j, side, prevUnitsLeft, dloss))
                                logApplicationUsage('d', description='deleverage[standardClose]', data=dfu.ix[j, :].to_dict())
                                if int(verbose) >= 5: qd.data('oanda2.create_order(%s, type=%s, instrument=%s, side=%s, units=%s)' % (accid, 'market', i, side, prevUnitsLeft))
                                    
                                #oanda2.create_order(accid, type='market', instrument=i, side=side, units=prevUnitsLeft)
                                ## collect trade data
                                #di = {'method':'leverageTrades[deleverage:complete]', 'account':accid, 'type':'market', 'instrument':i, 'side':side, 'units':prevUnitsLeft, 'data':json.dumps(dfu.ix[j, :].fillna(0).to_dict())}
                                #mongo = mong.MongoClient()
                                #mongo.ql.broker_oanda_trades.insert(di)
                                #mongo.close()
                                oandaCreateOrder(oanda2, accid, i, side, prevUnitsLeft, method='leverageTrades[deleverage:complete]', data=json.dumps(dfu.ix[j, :].fillna(0).to_dict()))
                    except Exception as e:
                        qd.exception(e)
                raise(Exception(''))
                            
                interactiveMode()
            if dfu3.ix[i, 'deleverageBool'] == False and (not noInteractive and not noInteractiveLeverage):
                if int(verbose) >= 5: qd.data('nil---')
                if noInteractiveDeleverage: raise(Exception('nid --> nil conflict'))
                if noInteractiveFleetingProfits: raise(Exception('nif --> nil conflict'))
                interactiveMode()
            #if noInteractive == False and (noInteractiveDeleverage == False and noInteractiveLeverage == False):
            #    qd.data('ni---')
            #    interactiveMode()
            stopLossOn = False
            try:
                # oanda legacy
                try:
                    if stopLossOn == False: raise('stopLoss disabled')
                    mmstop = round(dfu3.ix[i, 'stop'], 5)
                    oanda2.create_order(accid, type='market', instrument=i, side=side, units=units, stopLoss=mmstop)
                except Exception as e:
                    qd.exception(e)
                    oanda2.create_order(accid, type='market', instrument=i, side=side, units=units)
            except:
                # oanda (v20) api
                from oandapyV20 import API # the client
                from oandapyV20.exceptions import V20Error
                import oandapyV20.endpoints.orders as orders
                co, loginIndex, env0, access_token0, oanda0 = getConfig(loginIndex=loginIndex)
                client = API(access_token=access_token0)
                vunits = str(units if side == 'buy' else -units)
                orderData = {
                    "order": {
                        "type": "MARKET",
                        "positionFill": "DEFAULT",
                        "instrument": i,
                        "timeInForce": "FOK",
                        "units": vunits
                    }
                }
                try:
                    if stopLossOn == False: raise('stopLoss disabled v20')
                    mmstop = round(dfu3.ix[i, 'stop'], 5)
                    orderData['order'].update({"stopLossOnFill": {
                        "timeInForce": "GTC",
                        "price": str(mmstop)
                    }})
                except Exception as e:
                    qd.exception(e)
                r = orders.OrderCreate(accid, data=orderData)
                client.request(r)
                qd.data(r.response, name='leverageTrades() v20:: OrderCreate response')
                #p.DataFrame(r.response['orderCreateTransaction'])
                #p.DataFrame(r.response['orderFillTransaction'])
                
            # collect trade data

            try:
                di = {'method':'leverageTrades[leverage:create-order]', 'account':accid, 'type':'market', 'instrument':i, 'side':side, 'units':units, 'data':json.dumps(dfu.ix[j, :].fillna(0).to_dict())}
                mongo = mong.MongoClient()
                mongo.ql.broker_oanda_trades.insert(di)
                mongo.close()
            except Exception as e:
                #qd.exception(e)
                ''
            #oandaCreateOrder(oanda2, accid, i, side, units, method='leverageTrades[leverage:create-order]', data=json.dumps(dfu.ix[j, :].fillna(0).to_dict()))
        except Exception as e:
            qd.exception(e)

def logApplicationUsage(mode, description=None, data=None):
    import pymongo as mong
    import datetime, calendar
    ds = datetime.datetime.utcnow()
    ts = calendar.timegm(ds.utctimetuple())
    ts = ts + float(ds.microsecond) / 1000000
    di = {}
    di.update({'utctime':ts})
    di.update({'mode':mode})
    if description: di.update({'description':description})
    if data:        di.update({'data':data})
    mongo = mong.MongoClient()
    mongo.ql.application_usage_patterns.insert(di)
    mongo.close()

def getSyntheticCurrencyTable(oanda2, oq, instruments):
    ctsdfli = list(instruments)
    #qd.data(p_read_csv('/mldev/bin/data/oanda/cache/instruments.csv'))
    ctsdf = p.DataFrame(oq.syntheticCurrencyTable(ctsdfli, homeCurrency='USD'))
    qres  = oanda2.get_prices(instruments=','.join(oq.wew(ctsdf['quotedCurrency'])))
    qres  = p.DataFrame(qres['prices']).set_index('instrument')
    pres  = oanda2.get_prices(instruments=','.join(oq.wew(ctsdf['pairedCurrency'])))
    pres  = p.DataFrame(pres['prices']).set_index('instrument')
    res = p.DataFrame([])
    res = res.combine_first(qres)
    res = res.combine_first(pres)
    
    #qd.data(qres)
    #qd.data(pres)
    #qd.data(res)
    for x in range(len(ctsdf.index)):
        try:    ctsdf.ix[x, 'quotedCurrencyAsk'] = res.ix[ctsdf.ix[x, 'quotedCurrency'], 'ask']
        except: ''
        try:    ctsdf.ix[x, 'quotedCurrencyBid'] = res.ix[ctsdf.ix[x, 'quotedCurrency'], 'bid']
        except: ''
        try:    ctsdf.ix[x, 'pairedCurrencyAsk'] = res.ix[ctsdf.ix[x, 'pairedCurrency'], 'ask']
        except: ''
        try:    ctsdf.ix[x, 'pairedCurrencyBid'] = res.ix[ctsdf.ix[x, 'pairedCurrency'], 'bid']
        except: ''
    #qd.data(ctsdf)
    #res = oanda2.get_prices(instruments=','.join(oq.wew(ctsdf['quotedCurrency'])))
    ctsdf.ix[:,'pairedCurrencyAsk pairedCurrencyBid'.split(' ')] = ctsdf.ix[:,'pairedCurrencyAsk pairedCurrencyBid'.split(' ')].fillna(1)
    return ctsdf

def getCurrentTradesAndPositions(oanda2, accid, oq, loginIndex=None):
    qd = QoreDebug()
    qd.on()

    import oandapyV20
    import oandapyV20.endpoints.positions as positions
    co, loginIndex, env0, access_token0, oanda0 = getConfig(loginIndex=loginIndex)
    client = oandapyV20.API(access_token=access_token0)

    try:
        r = positions.PositionList(accid)
        rv = client.request(r)
        currentPositionsV20 = p.DataFrame(rv['positions']).set_index('instrument')
        currentPositionsV20['unrealizedPL'] = p.to_numeric(currentPositionsV20['unrealizedPL'])
        currentPositionsV20 = currentPositionsV20[currentPositionsV20['unrealizedPL'] <> 0]

        # convert v20 units [long/short] to single 'units' field for legacy versopm
        csd = p.DataFrame()
        cddf = p.DataFrame(p.DataFrame(currentPositionsV20['long'].to_dict()).transpose()['units'])
        cddf['unitsLong'] = cddf['units']
        csd = csd.combine_first(cddf)
        cddf = p.DataFrame(p.DataFrame(currentPositionsV20['short'].to_dict()).transpose()['units'])
        cddf['unitsShort'] = cddf['units']
        csd = csd.combine_first(cddf)
        csd['unitsLong'] = p.to_numeric(csd['unitsLong'])
        csd['unitsShort'] = p.to_numeric(csd['unitsShort'])
        csd['units'] = csd['unitsLong'] + csd['unitsShort']
        #qd.data(csd.dtypes)
        #qd.data(csd.ix[:, 'units'.split()])
        currentPositionsV20['units'] = csd['units']
        #qd.data(currentPositionsV20)
    except Exception as e:
        qd.exception(e)
        currentPositionsV20 = p.DataFrame([])

    try:
        cp = oanda2.get_positions(accid)['positions']
        currentPositions = p.DataFrame(cp)
        try:    currentPositions = currentPositions.set_index('instrument')#.ix[:,'side units'.split(' ')]
        except Exception as e:
            qd.exception(e)
        qd.data(currentPositions)
    except:
        currentPositions = p.DataFrame([])
        
    currentPositions = currentPositions.combine_first(currentPositionsV20)
    
    qd.data(currentPositions, name='currentPositions 0015::')
    
    qd.data('tesst-------2')
    
    try:
        currentTrades = getCurrentTrades(oanda2, oq, accid, currentPositions, loginIndex=loginIndex)
    except Exception as e:
        qd.exception(e)
        currentTrades = p.DataFrame([])
    try:
        ct = currentTrades.set_index('id').ix[:,'instrument price side sideBool units ask bid plpips pl sideS status time displayName maxTradeUnits pip'.split(' ')]
    except Exception as e:
        ct = p.DataFrame([])
    qd.data(ct, name='ct')
    gct = p.DataFrame([])
    try:
        gct = ct.groupby('instrument') #.sort_values(by='pl', ascending=False)[ct['pl'] > 0]
        gct = gct.aggregate(n.mean).ix[:, 'units pl pip'.split(' ')].sort_values(by='pl', ascending=False)#[ct['pl'] > 0]
        currentPositions['pip'] = gct['pip']
    except Exception as e:
        ''
    qd.data('tesst-------')
    qd.data(gct, name='gct')
    
    return [currentPositions, currentTrades, ct, gct]

#@profile

def getAccounts(oanda0, access_token0):
    
    qd = QoreDebug()
    qd.on()
    #qd.off()

    # oanda (v20) api
    from oandapyV20 import API # the client
    from oandapyV20.exceptions import V20Error
    from oandapyV20.endpoints.accounts import AccountList
    from oandapyV20.endpoints.accounts import AccountSummary
    try:
        #accountID = "..."
        client = API(access_token=access_token0)
        accountsV20 = p.DataFrame(client.request(AccountList())['accounts'])
        accountsV20['accountId'] = accountsV20['id']
        accountsV20 = accountsV20.set_index('accountId')
        for i in accountsV20.index:
            try:
                #qd.data('inddsd:%s' % i)
                r = AccountSummary(accountID=i)
                rv = client.request(r)
                dfa = p.DataFrame(rv)
                dfa[i] = dfa['account']
                with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
                    idf = dfa.transpose()
                    #idf = p.DataFrame(idf.ix[i, :], axis=[0])
                    #qd.data(idf)
                    accountsV20 = accountsV20.combine_first(idf)
                    #accountsV20 = idf.combine_first(accountsV20)
            except V20Error as ve:
                qd.data(ve)
        accountsV20 = accountsV20.drop('account')
        accountsV20 = accountsV20.drop('lastTransactionID')
        with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
            qd.data(accountsV20, name='accountsV20:::')
    except Exception as e:
        qd.logTraceBack(e)
        qd.exception(e)
        ''
    
    # oanda api
    try:
        res = oanda0.get_accounts()['accounts']
        qd.data(res, name='res1234:')
        accounts0 = p.DataFrame(res)
        for i in list(accounts0.index):
            accounts0 = accounts0.combine_first(p.DataFrame(oanda0.get_account(accounts0.ix[i, 'accountId']), index=[i]))
        accounts0 = accounts0.set_index('accountId')
        with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
            qd.data(accounts0, name='accounts0::')
    except Exception as e:
        qd.logTraceBack(e)
        qd.exception(e)
    
    accounts = p.DataFrame([])
    try:
        accounts = accounts.combine_first(accounts0)
    except Exception as e:
        qd.logTraceBack(e)
        qd.exception(e)
    try:
        accounts = accounts.combine_first(accountsV20)
    except Exception as e:
        qd.logTraceBack(e)
        qd.exception(e)
    #qd.data(accounts)
    accounts['accountId'] = accounts.index
    # convert all rows in accountId column to strings (make it searchable)
    accounts['accountId'] = n.array(accounts['accountId'], dtype=n.str)
    accounts['id'] = range(len(accounts.index))
    accounts = accounts.set_index('id')
    qd.data(accounts, name='accounts::')
    return accounts

def getConfig(loginIndex=None, args=None):

    qd = QoreDebug()
    qd.on()
    #qd.off()

    co = p.read_csv('/mldev/bin/datafeeds/config.csv', header=None)
    
    qd.data('loginIndex::%s' % loginIndex)
    qd.data('args::%s' % args)
    
    try:    loginIndex = int(args.loginIndex)
    except:
        if loginIndex == None:
            loginIndex = 0    
    loginIndex =  int(loginIndex)
    with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
        qd.data('co::%s' % co)
        qd.data('co:type:%s' % type(co))
        qd.data('loginIndex::%s' % loginIndex)
        qd.data('loginIndex type::%s' % type(loginIndex))
    env0=co.ix[loginIndex,1]
    access_token0=co.ix[int(loginIndex),2]
    oanda0 = oandapy.API(environment=env0, access_token=access_token0)
    qd.data('access_token0::%s' % access_token0)
    return [co, loginIndex, env0, access_token0, oanda0]

def rebalanceTrades(oq, dfu3, oanda2, accid, dryrun=True, leverage=50, verbose=False, noInteractive=False, noInteractiveLeverage=False, noInteractiveDeleverage=False, noInteractiveFleetingProfits=False, threading=True, sortRebalanceList=None, loginIndex=None):
    
    qd = QoreDebug()
    qd.on()
    #qd.off()

    import pymongo as mong
    import calendar

    co, loginIndex, env0, access_token0, oanda0 = getConfig(loginIndex=loginIndex)

    if threading:
        from multiprocessing.pool import ThreadPool

    if int(verbose) >= 5: qd.data('----------')
    
    # recalculate percentages [diffp]
    dfu3['diffp'] = (dfu3['diff'].get_values())/n.sum(dfu3['diff'].get_values())

    qd.data('accid:%s' % accid)
    qd.data('access_token0:%s' % access_token0)
    #maccount = oanda2.get_account(accid)
    maccount = getAccounts(oanda2, access_token0)
    with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
        qd.data('accid 2:%s %s' % (accid, type(accid)))
        qd.data('access_token0 2:%s' % access_token0)
        qd.data('maccount::', maccount)
        #qd.data(p.DataFrame(maccount.columns))
        qd.data('maccount', maccount.to_dict())
        qd.data('maccount', maccount.dtypes)
        qd.data('maccount::2')
        maccount = maccount[maccount['accountId'] == str(accid)]
        qd.data('maccount', maccount)
        maccount = maccount.ix[maccount.index[0],:].to_dict()
        qd.data('maccount::3', maccount)
    #marginAvail = maccount['marginAvail']
    unrealizedPl = float(maccount['unrealizedPl'])
    netAssetValue = float(maccount['balance']) + unrealizedPl
    balance       = float(maccount['balance'])
    #oinsts = ','.join(list(dfu3.index))
    qd.data(dfu3.index, name='dfu3index')
    prdf = p.DataFrame(oanda2.get_prices(instruments=','.join(list(dfu3.index)))['prices']).set_index('instrument')
    #prdf.ix[:,['instrument','bid']]
    #prdf.ix['EUR_USD','bid']
    dfu3['amount'] = n.ceil(dfu3['diffp'] * netAssetValue * leverage / prdf.ix[:,'bid'])

    try:
        [currentPositions, currentTrades, ct, gct] = getCurrentTradesAndPositions(oanda2, accid, oq, loginIndex=loginIndex)
    except Exception as e:
        qd.exception(e)
        
    try:
        ffsds = 'instrument side units plpips pl time'.split(' ')
        plp = ct.sort_values(by='pl', ascending=False)
        plp = plp[plp['pl'] > 0]
        pln = ct.sort_values(by='pl', ascending=False)
        pln = pln[pln['pl'] < 0]

        pll = p.DataFrame([plp.ix[:, 'pl'].sum(), pln.ix[:, 'pl'].sum()], index=['plp', 'pln'], columns=['pls'])
        if threading:
            pool = ThreadPool(processes=270)
            fleetingProfitsPL = (netAssetValue * (1.0/len(ct))/100)
            qd.data('fleetingProfitsPL:%s' % fleetingProfitsPL)
            for i in list(plp.index):
                if plp.ix[i, 'pl'] >= fleetingProfitsPL:
                    async_result = pool.apply_async(fleetingProfitsCloseTrade, [oanda2, dryrun, accid, i, plp, noInteractiveFleetingProfits, noInteractiveLeverage, noInteractiveDeleverage, verbose])
                    return_val   = async_result.get()
                    #qd.data(return_val)
            pool.close()
        else:
            fleetingProfitsCloseTrade(oanda2, dryrun, accid, i, plp, noInteractiveFleetingProfits, noInteractiveLeverage, noInteractiveDeleverage, verbose)
            
        if int(verbose) >= 5: 
            with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
                #qd.data(instruments, name='instruments:')
                #qd.data(currentPrices)
                qd.data(len(currentTrades), name='currentTrades:')
                qd.data(currentTrades.sort_values(by=['instrument', 'id'], ascending=[True, True]).set_index('id'))#.ix[:,'instrument price side time units'.split(' ')]
                #qd.data(gct)
                #ffsds = 'instrument side units plpips pl time'.split(' ')
                #plp = ct.sort_values(by='pl', ascending=False)
                #plp = plp[plp['pl'] > 0]
                #pln = ct.sort_values(by='pl', ascending=False)
                #pln = pln[pln['pl'] < 0]
                pll = p.DataFrame([plp.ix[:, 'pl'].sum(), pln.ix[:, 'pl'].sum()], index=['plp', 'pln'], columns=['pls'])
                qd.data(pll)
                for i in list(plp.index):
                    if dryrun == False:
                        qd.data("oanda2.close_trade(%s, %s) %s" % (accid, i, plp.ix[i, 'pl']))
                        #oanda2.close_trade(accid, i)
                    
                qd.data(plp.ix[:, ffsds])
                qd.data(pln.ix[:, ffsds])

                qd.data(currentPositions.sort_values(by='units', ascending=False), name='currentPositions:')

        # get rebalance amount
        #qd.data(currentPositions)
        #qd.data(dfu3.ix[currentPositions.index, :])
        #cu = currentPositions.ix[dfu3.index, :]
        cu = currentPositions.combine_first(dfu3)
        cu['bool'] = getSideBool(cu['side'])
        cu = cu.fillna(0)
        if int(verbose) >= 5: 
            with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
                qd.data(cu.sort_values(by='diffp', ascending=False).ix[:, 'amount bool buy diff diffp sell side sidePolarity unit units amountSidePolarity positions rebalance'.split(' ')])
        #print
        dfu3 = dfu3.combine_first(cu)
        dfu3 = dfu3.combine_first(gct)
    except Exception as e:
        qd.exception(e)
    try:
        dfu3['amountSidePolarity'] = dfu3['sidePolarity'] * dfu3['amount']
        dfu3['positions'] = cu.ix[:, 'units'] * cu.ix[:, 'bool']
    except Exception as e:
        qd.exception(e)
        #dfu3['positions'] = 0
        ''
    dfu3 = cw(dfu3, oanda2, oq, accid, maccount, leverage=leverage, verbose=verbose)

    #dfu3['rebalance'] = dfu3.ix[:, 'amountSidePolarity'] - dfu3.ix[:, 'positions']
    try:    positions = dfu3.ix[:, 'positions']
    except: positions = n.array([0]*len(dfu3.index))
    dfu3['rebalance'] = (dfu3.ix[:, 'sidePolarity'] * dfu3.ix[:, 'amount2']) - positions
    dfu3['rebalancep'] = n.abs(dfu3.ix[:, 'rebalance'].get_values()) / n.abs(positions)
    dfu3['rebalanceBool'] = n.int16(dfu3.ix[:, 'rebalance'] <> 0)
    dfu3['deleverageBool'] = n.logical_and(differentPolarity(positions, dfu3.ix[:, 'rebalance']), positions <> 0)
    dfu3['diffpRebalancep'] = dfu3.ix[:, 'diffp'].get_values() * dfu3.ix[:, 'rebalancep'].get_values() * dfu3.ix[:, 'deleverageBool'].get_values()
    #dfu3['diffpRebalancepBalance'] = dfu3.ix[:, 'diffpRebalancep'].get_values() * balance
    #dfu3['diffpRebalancepBalance'] = dfu3.ix[:, 'diffpRebalancep'] * dfu3.ix[:, 'pl']
    try: dfu3['diffpRebalancep2'] = abs((dfu3.ix[:, 'rebalance']) / dfu3.ix[:, 'positions'])
    except: ''
    try:
        dfu3['diffpRebalancepBalance'] = map(lambda x: 1 if x > 1 else x, abs((dfu3.ix[:, 'rebalance']) / dfu3.ix[:, 'positions'])) * dfu3.ix[:, 'pl']
        #dfu3['diffpRebalancepBalance'] = map(lambda x: 1 if x > 1 else x, abs((dfu3.ix[:, 'rebalance']) / dfu3.ix[:, 'positions']))
        dfu3['diffpRebalancep'] = dfu3.ix[:, 'diffpRebalancepBalance'] / balance
        #dfu3['diffpRebalancepBalance'] = netAssetValue
    except Exception as e: 
        qd.exception(e)

    # margin used
    dfu3['bc_hc']       = map(lambda x: dfu3.ix[x, 'quotedCurrencyPriceBid'] if dfu3.ix[x, 'powQuoted'] > 0 else (1 / dfu3.ix[x, 'quotedCurrencyPriceBid']), dfu3.index)
    dfu3['marginRatio'] = 50
    try: dfu3['marginUsed']  = (dfu3.ix[:, 'bc_hc'] * dfu3.ix[:, 'units']) / dfu3['marginRatio']
    except: ''
    dfu3['rebalanceMarginUsed'] = (dfu3.ix[:, 'bc_hc'] * n.abs(dfu3.ix[:, 'rebalance'])) / dfu3['marginRatio']
    
    # indicates if this is:
    #   a deleverage
    #     - (+ve.) 
    #   a leverage
    #     - (-e.) 
    #     - if rebalance consumes the marginUsed and changes the sidePolarity
    try: dfu3['diffRebalanceMarginUsed']     = dfu3['marginUsed'] - dfu3['rebalanceMarginUsed']
    except: ''
    try: dfu3['diffRebalanceMarginUsedBool'] = dfu3['diffRebalanceMarginUsed'] > 0
    except: ''
    
    # the rebalance units as percentage of all units
    try: dfu3['rebalanceOverUnits']  = (n.abs(dfu3.ix[:, 'rebalance']) / dfu3.ix[:, 'units'])  # deprecated
    except: ''
    try: dfu3['marginUsedP']  = dfu3['rebalanceOverUnits'] * dfu3['marginUsed']                # deprecated
    except: ''
    
    if sortRebalanceList == 'reverse'    or sortRebalanceList == 'r' or sortRebalanceList == None:
        sortby                    = ['deleverageBool', 'diffRebalanceMarginUsedBool', 'rebalanceMarginUsed', 'diffpRebalancep']
        sortAscending             = [False,            True,                          False,                 True]
    if sortRebalanceList == 'reversepl'    or sortRebalanceList == 'p':
        sortby                    = ['deleverageBool', 'pl', 'diffpRebalancep']
        sortAscending             = [False,            True,                          False,                 True]
    if sortRebalanceList == 'reversepl'    or sortRebalanceList == 'rp':
        sortby                    = ['deleverageBool', 'diffRebalanceMarginUsedBool', 'pl', 'diffpRebalancep']
        sortAscending             = [False,            True,                          False,                 True]
    
    if sortRebalanceList == 'deleverage' or sortRebalanceList == 'd':
        sortby                    = ['deleverageBool', 'diffRebalanceMarginUsedBool', 'rebalanceMarginUsed', 'diffpRebalancep']
        sortAscending             = [False,            False,                         False,                 True]
    if sortRebalanceList == 'deleveragepl' or sortRebalanceList == 'dp':
        sortby                    = ['deleverageBool', 'diffRebalanceMarginUsedBool', 'pl', 'diffpRebalancep']
        sortAscending             = [False,            False,                         False,                 True]
        
    if sortRebalanceList == 'leverage'   or sortRebalanceList == 'l':
        sortby                    = ['deleverageBool', 'diffRebalanceMarginUsedBool', 'rebalanceMarginUsed', 'diffpRebalancep']
        sortAscending             = [True,             True,                          False,                 True]
        
    if noInteractiveLeverage: 
        sortAscending[0]      = True
    
    #for i in dfu3.sort_values(by=sortby, ascending=sortAscending).index:
    #    dfu3.ix[i, 'pl098'] = ct[ct['instrument'] == i].ix[:,'pl'].sum()
    try: dfu3['deleverageLoss'] = dfu3['pl'] * dfu3['rebalance'] / dfu3['units'] 
    except: ''

    with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
        f1Base         = 'amount bool buy diff diffp sell side sidePolarity amountSidePolarity bid ask spread pip spreadPip pairedCurrencyPriceBid pairedCurrencyPriceAsk quotedCurrencyPriceBid quotedCurrencyPriceAsk diffRebalanceMarginUsed rebalanceMarginUsed marginUsed marginUsedP unitsAvailable units exposure exposureSum allMargin amount2 amount2Sum amount4 amount4Sum diffamount4amount2 positions rebalance rebalancep diffp diffpRebalancep diffpRebalancepBalance pl pl098 pl00001 deleverageLoss diffpRebalancep2 bc_hc powQuoted pow2 rebalanceOverUnits'
        if int(verbose) >= 5: f1 = '%s rebalanceBool deleverageBool diffRebalanceMarginUsedBool' % f1Base
        else:       f1 = f1Base
        if int(verbose) >= 5: 
            qd.data('-=-=-=-=-')
            qd.data('-=-=-=-=-')
            try: qd.data('sumMarginUsed: %s' % n.sum(dfu3['marginUsed']))
            except: ''
            qd.data('sortRebalanceList:%s' % sortRebalanceList)
            qd.data('sortby:%s' % sortby)
            qd.data('sortAscending:%s' % sortAscending)
            #qd.data(dfu3.sort_values(by='diffp', ascending=False).ix[:, f1.split(' ')])
            try: qd.data(dfu3.sort_values(by=sortby, ascending=sortAscending).ix[:, f1.split(' ')])
            except: ''
            print
            
            #qd.data(ct.sort_values(by=['pl'], ascending=[False]))
            #print

    if threading:
        poolFleetingProfits = ThreadPool(processes=270)
        poolLeverage        = ThreadPool(processes=270)
    if int(verbose) >= 5:
        qd.data('                                                                 MU=MarginUsed')
        qd.data('                                                                  R=Rebalance')
        qd.data('                                                                  r=rebalanceMarginUsed')
        qd.data('                                                                dMU=diffRebalanceMarginUsed')
        qd.data('                                                                drb=diffpRpBalance')
        qd.data('                                                               drbp=diffpRebalancep')
    qd.data('===1==1==1=1=1=1====')
    with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
        try:
            gct = ct.groupby('instrument')
            gct = gct.aggregate(n.mean)#.ix[:, 'units pl'.split(' ')].sort_values(by='pl', ascending=False)#[ct['pl'] > 0]
            if int(verbose) >= 8:
                qd.data(ct) #.sort_values(by='', ascending=False)
                qd.data(gct)
        except: ''
        #qd.data(ct.sort_values(by='plpips', ascending=False))
    qd.data('===1==1==1=1=1=1====')
    try:    dfu3s = dfu3.sort_values(by=sortby, ascending=sortAscending).index
    except: dfu3s = dfu3.index
    for i in dfu3s:
        #qd.data(dfu3.ix[[i], :].transpose())
        try: units = int(abs(dfu3.ix[i, 'rebalance']))#-1
        except: units = 0
        side  = 'buy' if int(dfu3.ix[i, 'rebalance']) > 0 else 'sell'
        #dfu3.ix[i, 'side']
        #dfu3.ix[i, 'side']
        if units > 0:
            status = '[LIVE]' if dryrun == False else '[dryrun]'
            try:
                reverseEntryStatus  = 'reverseEntry' if dfu3.ix[i, 'diffRebalanceMarginUsedBool'] == False else 'deleverage'
                deleverageStatus = '[v %s pl/drb/dLoss(drbp):%.3f/%.3f/%.3f(%.3f%s)]' % (reverseEntryStatus.rjust(12), dfu3.ix[i, 'pl'], dfu3.ix[i, 'diffpRebalancepBalance'], dfu3.ix[i, 'deleverageLoss'], dfu3.ix[i, 'diffpRebalancep']*100, '%')  if dfu3.ix[i, 'deleverageBool'] == 1 else '[^   leverage]'
            except:
               deleverageStatus = ''
            closePositionStatus = '[closePosition]' if dfu3.ix[i, 'amount2'] == 0 else ''
            try:
                if int(verbose) >= 8:
                    qd.data("<broker>.create_order(%s, type='market', instrument='%s', side='%s', units=%s[%s]) %s %s %s rebalanceMU/MU/diffRebalanceMU:(%.3f/%.3f/%.3f)" % (accid, i, side.rjust(4), str(units).rjust(4), str(dfu3.ix[i, 'units']).rjust(10), status, deleverageStatus, closePositionStatus, dfu3.ix[i, 'rebalanceMarginUsed'], dfu3.ix[i, 'marginUsed'], dfu3.ix[i, 'diffRebalanceMarginUsed']))
                else:
                    qd.data("<broker>.create_order(instrument='%s', side='%s', units=%s[%s]) %s %s %s r/MU/dMU:(%.3f/%.3f/%.3f)" % (i, side.rjust(4), str(units).rjust(4), str(dfu3.ix[i, 'units']).rjust(10), status, deleverageStatus, closePositionStatus, dfu3.ix[i, 'rebalanceMarginUsed'], dfu3.ix[i, 'marginUsed'], dfu3.ix[i, 'diffRebalanceMarginUsed']))
            except: ''

            #for i in list(plp.index):
            if threading:
                try:
                    async_result = poolFleetingProfits.apply_async(fleetingProfitsCloseTrade, [oanda2, dryrun, accid, i, plp, noInteractiveFleetingProfits, noInteractiveLeverage, noInteractiveDeleverage, verbose])
                    return_val   = async_result.get()
                    #qd.data(return_val)
                except: ''
    
                async_result = poolLeverage.apply_async(leverageTrades, [dryrun, oanda2, dfu3, accid, i, side, units, noInteractiveLeverage, noInteractiveDeleverage, noInteractiveFleetingProfits, verbose, noInteractive, ct, loginIndex])
                return_val   = async_result.get()
                return_val
            else:
                try:
                    fleetingProfitsCloseTrade(oanda2, dryrun, accid, i, plp, noInteractiveFleetingProfits, noInteractiveLeverage, noInteractiveDeleverage, verbose)
                except: ''
                leverageTrades(dryrun, oanda2, dfu3, accid, i, side, units, noInteractiveLeverage, noInteractiveDeleverage, noInteractiveFleetingProfits, verbose, noInteractive, ct, loginIndex=loginIndex)
                
            #qd.data(return_val)
            #leverageTrades(dryrun, oanda2, dfu3, accid, i, side, units, noInteractiveLeverage, noInteractiveDeleverage, noInteractiveFleetingProfits, verbose, noInteractive)
    
    if threading:
        poolFleetingProfits.close()
        poolLeverage.close()
        
    print 'maccount:::'
    #qd.data(p.DataFrame(maccount))
    #qd.data(maccount)
    try: pll[0] = pll['pls']
    except: ''
    #maccount = oanda2.get_account(accid)
    qd.data(type(maccount), name='maccount type')
    qd.data(maccount, name='maccount 010')
    #qd.data(maccount.shape, name='maccount shape')
    dfa = p.DataFrame(maccount, index=[0])
    try: dfa = dfa.combine_first(pll.ix[:,[0]].transpose())
    except: ''
    dfa['netAssetValue'] = dfa['balance'] + dfa['unrealizedPl']
    dfa['unrealizedPlPcnt'] = dfa['unrealizedPl'] / dfa['balance'] * 100
    try: dfa['plpcnt'] = dfa['plp'] / dfa['balance'] * 100
    except: ''
    try: dfa['plncnt'] = dfa['pln'] / dfa['balance'] * 100
    except: ''
    
    # aliases
    dfa['nav'] = dfa['netAssetValue']
    dfa['uPl'] = dfa['unrealizedPl']
    dfa['uPlPcnt'] = dfa['unrealizedPlPcnt']

    ds = dd.datetime.utcnow()
    ts = calendar.timegm(ds.utctimetuple())
    ts = ts + float(ds.microsecond)/1000000
    dfa.ix[0, 'utctime'] = ts

    qd = QoreDebug()
    qd.log('testme')

    try:    sumDiffpRebalancepBalance = dfu3['diffpRebalancepBalance'].sum()
    except: sumDiffpRebalancepBalance = 0

    try: dfaPlp = dfa.ix[0, 'plp']
    except: dfaPlp = 0
    
    balanceDeleveraged    = dfa.ix[0, 'balance'] + sumDiffpRebalancepBalance
    balanceDeleveragedPlp = dfa.ix[0, 'balance'] + dfaPlp + sumDiffpRebalancepBalance

    #li = list(dfa.ix[:, 'plp plpcnt'.split(' ')].get_values()[0])
    #li = li.append('%')

    dfa = dfa.transpose()
    qd.data(dfa, name='dfa 545')
    accountId = str(dfa.ix['accountId', 0])
    dfa[accountId] = dfa[0]
    
    dfa = dfa.transpose()
    di = dfa.ix[accountId, :].transpose().to_dict()
    mongo = mong.MongoClient()
    mongo.ql.broker_oanda_account.insert(di)

    if int(verbose) >= 1:
        with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):

            #qd.data(dfu3[:, ['diffpRebalancepBalance', 'diffpRebalancep']].sum())
            qd.data('%s %s' % (dfu3['diffpRebalancepBalance'].sum(), dfu3['diffpRebalancep'].sum()))
            qd.data('DeleveragedBalance: %s' % (balanceDeleveraged))
            qd.data('DeleveragedBalance+plp: %s' % (balanceDeleveragedPlp))
            qd.data('diffDeleveragedBalance+plp2Balance: %s' % (balanceDeleveragedPlp - dfa.ix[0, 'balance']))
            print
            qd.data(plp.ix[:, ffsds])
            #qd.data('%s %s%s' % li)
            #qd.data('%s %s' % list(dfa.ix[:, 'plp plpcnt'.split(' ')].get_values()[0]))
            qd.data(list(dfa.ix[:, 'plp plpcnt'.split(' ')].get_values()[0]))
            #qd.data(pln.ix[:, ffsds])
            print
            
            qd.data(dfa.ix[:, 'accountCurrency accountId accountName balance uPl uPlPcnt nav realizedPl plp plpcnt pln plncnt openTrades marginUsed marginAvail'.split(' ')])
            print
    
    return dfu3

#@profile
def cw(dfu33, oanda2, oq, accid, maccount, leverage=50, verbose=False):

    qd = QoreDebug()
    qd.on()
    #qd.off()

    dfu33 = dfu33.fillna(0)
    if int(verbose) >= 5: qd.data('#--- cw(start)')
    li = list(dfu33.sort_values(by='diffp', ascending=False).index)
    if int(verbose) >= 5: 
        qd.data(li, name='li')

    df  = oq.syntheticCurrencyTable(li, homeCurrency='USD')
    sdf = p.DataFrame(df)
    df = p.DataFrame(df).set_index('instrument').ix[:,['pairedCurrency','pow']]
    pcdf = df.ix[:,'pairedCurrency'].get_values()
    if int(verbose) >= 5:  qd.data(pcdf)
    pcdf = oq.wew(pcdf)
    if int(verbose) >= 5: 
        qd.data(pcdf)
        print
    #li = n.c_[li,pcdf]#[0]
    pdf = list(li)+list(pcdf)
    if int(verbose) >= 5:  qd.data(pdf)
    #fdf = fdf.combine_first(df)
    pairs = ','.join(list(pdf))
    if int(verbose) >= 5:  qd.data(pairs)

    res = oanda2.get_prices(instruments=','.join(oq.wew(sdf['instrument'])))
    res = p.DataFrame(res['prices'])
    if int(verbose) >= 5: 
        with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
            qd.data(list(sdf['quotedCurrency']))
            qd.data(sdf, name='sdf')
            qd.data(res, name='res')
    res = res.set_index('instrument')
    #qd.data(res.ix[oq.wew(list(sdf['quotedCurrency'])), :])
    #ldf = p.DataFrame(li)
    #sdf['pc'] = ma 
    sdf = sdf.set_index('instrument')
    if int(verbose) >= 5: 
        with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
            qd.data(dfu33, name='dfu33')
            qd.data(sdf, name='sdf')
    instrumentCurrency = sdf.ix[dfu33.index, ['instrument','pow']]
    instrumentCurrency['instrument'] = dfu33.index
    if int(verbose) >= 5: 
        qd.data(instrumentCurrency, name='instrumentCurrency')
        qd.data('====')
    quotedCurrency = sdf.ix[dfu33.index, ['quotedCurrency','pow']]
    if int(verbose) >= 5: 
        qd.data(quotedCurrency, name='quotedCurrency')
        qd.data('====')
    pairedCurrency = sdf.ix[dfu33.index, ['pairedCurrency','pow']]
    if int(verbose) >= 5: 
        qd.data(pairedCurrency, name='pairedCurrency')
        qd.data('====')
    #---
    quotedCurrencyPrice = res.ix[quotedCurrency['quotedCurrency'],['bid']].fillna(1)
    #quotedCurrencyPrice['pow'] = 
    quotedCurrencyPrice['ask'] = res.ix[quotedCurrency['quotedCurrency'],['ask']].fillna(1)
    quotedCurrencyPrice['instrument'] = quotedCurrency.index
    quotedCurrencyPrice['quotedCurrency'] = quotedCurrencyPrice.index
    quotedCurrencyPrice = quotedCurrencyPrice.set_index('instrument')
    quotedCurrencyPrice['diffp'] = dfu33['diffp']

    pairedCurrencyPrice = res.ix[pairedCurrency['pairedCurrency'],['bid']].fillna(1)
    pairedCurrencyPrice['ask'] = res.ix[pairedCurrency['pairedCurrency'],['ask']].fillna(1)
    pairedCurrencyPrice['instrument'] = pairedCurrency.index
    pairedCurrencyPrice['pairedCurrency'] = pairedCurrencyPrice.index
    pairedCurrencyPrice = pairedCurrencyPrice.set_index('instrument')

    instrumentCurrencyPrice = res.ix[instrumentCurrency['instrument'],['bid']].fillna(1)
    instrumentCurrencyPrice['ask'] = res.ix[instrumentCurrency['instrument'],['ask']].fillna(1)
    instrumentCurrencyPrice['instrument'] = instrumentCurrency.index
    instrumentCurrencyPrice['instrumentCurrency'] = instrumentCurrencyPrice.index
    instrumentCurrencyPrice = instrumentCurrencyPrice.set_index('instrument')

    #---
    #.sort_values(by='diffp', ascending=False)
    if int(verbose) >= 5: 
        qd.data(quotedCurrencyPrice, name='quotedCurrencyPrice')#.sort_values(by='diffp', ascending=False)
    if int(verbose) >= 5: 
        qd.data(pairedCurrencyPrice, name='pairedCurrencyPrice')#.sort_values(by='diffp', ascending=False)
    if int(verbose) >= 5: 
        qd.data(instrumentCurrencyPrice, name='instrumentCurrencyPrice')
        qd.data('====')
    #qd.data(res)
    #qd.data(sdf['quotedCurrency'])
    #qd.data(sdf.ix[quotedCurrencyPrice.index,:])
    if int(verbose) >= 5: qd.data('====')

    balance       = float(maccount['balance'])
    #marginAvail   = maccount['marginAvail']
    netAssetValue = float(maccount['balance']) - float(maccount['unrealizedPl'])
    dfu33['pow2'] = sdf.ix[quotedCurrencyPrice.index,'pow'].get_values()
    dfu33['powPaired'] = sdf.ix[quotedCurrencyPrice.index,'powPaired'].get_values()
    dfu33['powQuoted'] = sdf.ix[quotedCurrencyPrice.index,'powQuoted'].get_values()
    dfu33['quotedCurrencyPriceBid'] = quotedCurrencyPrice['bid'].get_values()
    dfu33['quotedCurrencyPriceAsk'] = quotedCurrencyPrice['ask'].get_values()
    dfu33['pairedCurrencyPriceBid'] = pairedCurrencyPrice['bid'].get_values()
    dfu33['pairedCurrencyPriceAsk'] = pairedCurrencyPrice['ask'].get_values()
    dfu33['bid'] = instrumentCurrencyPrice['bid'].get_values()
    dfu33['ask'] = instrumentCurrencyPrice['ask'].get_values()
    dfu33['priceAvg'] = (dfu33['bid'] + dfu33['ask']) / 2
    dfu33['spread'] = n.abs(dfu33['bid'] - dfu33['ask'])
    try: dfu33['spreadPip'] = dfu33['spread'] / dfu33['pip']
    except: ''
    dfu33['unitsAvailable'] = netAssetValue * leverage / n.power(dfu33['quotedCurrencyPriceBid'], dfu33['pow2'])
    try: 
        dfu33['exposure'] = dfu33['units'] * dfu33['quotedCurrencyPriceAsk']
        dfu33['exposureSum'] = n.sum(dfu33['exposure'])
    except: ''
    dfu33['allMargin'] = balance * leverage
    dfu33['pl00001'] = ( ((dfu33['bid']+dfu33['ask'])/2) ) * (1 / (dfu33['pairedCurrencyPriceBid']+dfu33['pairedCurrencyPriceAsk'])/2)   #* dfu33['pow2']

    dfu33['amount4'] = dfu33['unitsAvailable'] * dfu33['diffp']
    dfu33['amount4Sum'] = n.sum(dfu33['amount4'])

    dfu33['amount2'] = dfu33['allMargin'] * dfu33['diffp']
    dfu33['amount2Sum'] = n.sum(dfu33['amount2'])
    dfu33['diffamount4amount2'] = dfu33['amount2'] - dfu33['amount4']

    # close = pl/units+open
    dfu33['riskAmount']          = (balance * 10.0 / 100)
    dfu33['riskAmountDiffp']     = (dfu33['riskAmount'] * dfu33['diffp'])
    dfu33['sidePolarityInverse'] = map(lambda x: 1 if x == -1 else -1, dfu33['sidePolarity'])
    dfu33['stopPrice'] = dfu33['riskAmountDiffp'] / dfu33['amount2'] + dfu33['priceAvg']
    dfu33['stop']                = (dfu33['sidePolarityInverse'] * dfu33['stopPrice'])
    #dfu33['stop']     = ((balance * 1.0/100 * dfu33['diffp']) / (dfu33['allMargin'] * dfu33['diffp']))
    #dfu33['stop']   = (balance * 1.0/100 * dfu33['diffp'])    # balance * dfu33['diffp'] * leverage
    #qd.data(quotedCurrencyPrice['bid'])
    #qd.data(p.DataFrame(netAssetValue * 50 * quotedCurrencyPrice['bid'].get_values()))
    qd.data('============================================')
    qd.data('============================================')
    qd.data('============================================')
    qd.data('============================================')
    qtime = time.time()
    with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
        # portfolio oanda
        sorted_dfu33 = dfu33.sort_values(by='diffp', ascending=False)
        qd.data(sorted_dfu33, name='dfu33::')
        fname = '/ml.dev/bin/data/oanda/cache/patterns/patterns.dfu33.%s.csv' % qtime
        sorted_dfu33.to_csv(fname)
        print 'Saved to pattern file: %s' % fname

        pa = Patterns()
        dfu33m = pa.computePortfolioMetatrader(dfu33)
        sorted_dfu33m = dfu33m.sort_values(by='diffp', ascending=False)
        
        # portfolio metatrader
        #qd.data(sorted_dfu33m.ix[:,'allMarginMetatrader amount2Metatrader side lots diffp'.split(' ')], name='dfu33 metatrader::')
        portfolioMetatrader = sorted_dfu33m.ix[:,'balanceMetatrader leverageMetatrader allMarginMetatrader amount2Metatrader side diffp lots'.split(' ')]
        portfolioMetatrader = portfolioMetatrader[portfolioMetatrader['diffp'] > 0]
        qd.data(portfolioMetatrader, name='portfolioMetatrader::')
        fname = '/ml.dev/bin/data/oanda/cache/patterns/patterns.portfolioMetatrader.%s.csv' % qtime
        portfolioMetatrader.to_csv(fname)
        print 'Saved to metatrader pattern file: %s' % fname
       
    qd.data('============================================')
    qd.data('============================================')
    qd.data('============================================')
    if int(verbose) >= 5: 
        with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
            qd.data(dfu33.ix[:, 'quotedCurrencyPriceBid quotedCurrencyPriceAsk unitsAvailable diffp pow2 units exposure exposureSum allMargin amount2 amount4 amount rebalance'.split(' ')], name='dfu33')
    if int(verbose) >= 5:  qd.data('#--- cw(end)')
    
    return dfu33

class CryptoCoinBaseClass:
    
    def __init__(self):
        ''
        
class CoinMarketCap:
    
    def __init__(self):
        ''

    def updateData(self):
        # source: http://coinmarketcap-nexuist.rhcloud.com/
        t = fetchURL('http://coinmarketcap-nexuist.rhcloud.com/api/all', cachemode='a', fromCache=False, mode='json')
        t

class btce(CryptoCoinBaseClass):
    def getTicker(self, code):
        # eg. code = btc_usd
        url = 'https://btc-e.com/api/3/ticker/'+code
        r = fetchURL(url, mode='json')
        #print r
        ky = r[code].keys()
        #print ky
        #print r[code].values()
        r = p.DataFrame(r[code].values(), index=ky, columns=[code]).transpose()
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
        tis = p.read_csv(sio.StringIO(t), delimiter='\t', index_col=0).ix[:,[0,1,2]]
        tis = tis.sort('Transaction Speed (in seconds)', ascending=True)
        #print tis.ix[0:3,[0,2]]
        #print tis
        tis = list(tis.ix[:,[0]].transpose().get_values()[0])
        """
        for i in list(n.array(self.pk, dtype=string0)):
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
            #print p.DataFrame(list(r['pairs']['ltc_gbp']))
            pk = r['pairs'].keys()
            pv = r['pairs'].values()
            #print pk
            li = []
            for i in pv:
                li.append(i.values())
            li = p.DataFrame(li, index=pk, columns=pv[0].keys())
            self.pk = pk
            return li
            #pk = p.DataFrame(pk, index=pk, columns=['pair'])
            #print pk
            #print pk.combine_first(li)
            #print r
        except TypeError, e:
            debug(e)
    
    def getRatesOnExchange(self):
        self.check()
        pc = p.DataFrame()
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
            #ky = r[code].keys()    
            #print ky
            rb = p.DataFrame(r[code]['bids'], columns=['bp','ba'])
            ra = p.DataFrame(r[code]['asks'], columns=['ap','aa'])
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
            ro = p.DataFrame(li, columns=ky)
            r = ro.ix[:,['price','amount']]
            #print r
            """
            rb = p.DataFrame(r[code]['bids'], columns=['bp','ba'])
            ra = p.DataFrame(r[code]['asks'], columns=['ap','aa'])
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
        arbtable1 = n.random.randn(len(pk)*len(self.exchanges)).reshape(len(pk),len(self.exchanges));
        return arbtable1

    def getArbRates(self, doPlot=False):
        #print pk
        arbtable1 = self.getArbTable(self.pk)
        rarb = p.DataFrame(arbtable1, index=self.pk, columns=self.exchanges);
        #print rarb; print;
        
        ms = []
        arbHdr = ['sell','buy','arbitrageRate']
        arbRates = p.DataFrame([])
        for i in range(0,len(self.pk)):
        #for i in range(0,2):
            ind = i
            debug(self.pk[ind])
            m = rarb.ix[self.pk[ind]]
            debug(m)
            m = p.DataFrame(n.array(m).reshape(len(m),1) / n.array(m) * 100 - 100, index=self.exchanges, columns=self.exchanges); 
            debug(m); debug('');
            m1 = n.max(m,0); #print m1;
            exhds = list(m1.index)
            #print (n.nonzero(m == m1))
            #print (n.nonzero(m1 == n.max(m1)))
            #maxIndx = n.max(n.nonzero(m1 == n.max(m1)))
            maxNum = n.max(m1,0); #print maxNum;
            indx = (n.nonzero(n.array(m == maxNum, dtype=int)))
            arbRate = p.DataFrame([exhds[indx[0][0]], exhds[indx[1][0]], maxNum], index=arbHdr, columns=[self.pk[ind]])
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
        print p.DataFrame(arrSortedAR.ix[list(arrSortedAR.ix[:,'p1']).index(self.p1), :]).transpose(); print
        print p.DataFrame(arrSortedAR.ix[list(arrSortedAR.ix[:,'p2']).index(self.p2), :]).transpose()
    
    def getMostProfitablePair(self):
        fastestCoins = self.getFastestCryptoCoins()
        #fcs = []
        try:
            arbRates
        except Exception as e:
            print e
            arbRates = self.getArbRates()
        arr = arbRates.transpose()
        po1 = []; po2 = []
        for row in (n.array(arr.index, dtype=string0)):
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
        #rin = p.DataFrame(n.int0(n.abs(n.random.randn(26)*10)))
        abc = list(it.permutations(abc, 3))
        abc = n.array(abc).tolist()
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
        li = n.array(li).tolist()
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
#from selenium import webdriver
#from selenium.selenium import selenium
#from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
#from selenium.webdriver.common.action_chains import ActionChains

class Bloomberg():
    def __init__(self):
        self.driver = None
        self.billionaires = p.DataFrame()

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

    def mclean(s):
        try:
            s = s.replace('$','')
            try:
                if s.index('B') > 0:
                    s = s.replace('B', '')
                    s = float(s)*1e9
            except:
                ''
            try:
                if s.index('M') > 0:
                    s = s.replace('M', '')
                    s = float(s)*1e6
            except:
                ''
        except:
            ''
        try:
            return float(s)
        except:
            return 0
    
    def getProfile(self, rank):
        print 'Fetching BBGB profile for rank:{0}'.format(rank)
        
        self.driver.find_elements_by_xpath('//*[@id="menu"]/ul/li[1]')[0].click() # click explore
        self.driver.find_elements_by_xpath('//*[@id="views"]/div[1]/div['+str(rank)+']/div[3]')[0].click()
        
        li = {}
        li['rank'] = self.driver.find_elements_by_xpath('//*[@id="profile"]/div/div[1]/ul/li[1]')[0].text.replace('#','')
        li['name'] = self.driver.find_elements_by_xpath('//*[@id="profile"]/div/div[1]/ul/li[2]')[0].text
        li['networth'] = self.driver.find_elements_by_xpath('//*[@id="profile"]/div/div[1]/ul/li[3]/span')[0].text
        li['age'] = self.driver.find_elements_by_xpath('//*[@id="profile"]/div/div[1]/div[2]/ul/li[1]/span[2]')[0].text
        li['biggestasset'] = self.driver.find_elements_by_xpath('//*[@id="profile"]/div/div[1]/div[2]/ul/li[2]/span[2]')[0].text
        li['source'] = self.driver.find_elements_by_xpath('//*[@id="profile"]/div/div[1]/div[2]/ul/li[3]/span[2]')[0].text
        li['lastchange'] = self.driver.find_elements_by_xpath('//*[@id="profile"]/div/div[1]/div[2]/ul/li[4]/span[2]/span[1]')[0].text
        li['YTD change'] = self.driver.find_elements_by_xpath('//*[@id="profile"]/div/div[1]/div[2]/ul/li[5]/span[2]/span[1]')[0].text
        li['funfact'] = self.driver.find_elements_by_xpath('//*[@id="profile"]/div/div[1]/div[3]')[0].text
        li['country'] = self.driver.find_elements_by_xpath('//*[@id="profile"]/div/div[1]/div[4]/span[1]')[0].text
        li['industry'] = self.driver.find_elements_by_xpath('//*[@id="profile"]/div/div[1]/div[4]/span[2]')[0].text
        li['overview'] = self.driver.find_elements_by_xpath('//*[@id="profile"]/div/div[2]/div[1]/span/p')[0].text
        li['intel'] = self.driver.find_elements_by_xpath('//*[@id="profile"]/div/div[2]/div[3]/ul')[0].text
        li['dob'] = self.driver.find_elements_by_xpath('//*[@id="profile"]/div/div[2]/div[5]/div[1]/ul/li[1]/span')[0].text
        li['education'] = self.driver.find_elements_by_xpath('//*[@id="profile"]/div/div[2]/div[5]/div[1]/ul/li[2]/span')[0].text
        li['family'] = self.driver.find_elements_by_xpath('//*[@id="profile"]/div/div[2]/div[5]/div[1]/ul/li[3]/span')[0].text
        li['story'] = self.driver.find_elements_by_xpath('//*[@id="profile"]/div/div[2]/div[5]/div[1]/span')[0].text
        li['milestones'] = self.driver.find_elements_by_xpath('//*[@id="profile"]/div/div[2]/div[5]/div[2]/ul')[0].text
        li['networth-story'] = self.driver.find_elements_by_xpath('//*[@id="profile"]/div/div[2]/div[6]/div[2]')[0].text
        
        #li['portfolio'] = self.driver.find_elements_by_xpath('//*[@id="profile"]/div/div[2]/div[6]/div[1]/div[1]/div[1]/@style')[0].text    
        #print self.driver.find_element_by_xpath('//*[@id="profile"]/div/div[2]/div[6]/div[1]/div[1]/div[1]')
        
        #li['portfolio-public'] = self.driver.find_elements_by_xpath('//*[@id="profile"]/div/div[2]/div[6]/div[1]/div[1]/div[1]')[0].html
        li['portfolio-private'] = self.driver.find_elements_by_xpath('//*[@id="profile"]/div/div[2]/div[6]/div[1]/div[1]/div[2]')[0].text
        li['portfolio-liabilities'] = self.driver.find_elements_by_xpath('//*[@id="profile"]/div/div[2]/div[6]/div[1]/div[2]')[0].text
        #li[''] = self.driver.find_elements_by_xpath('')[0].text
        #li[''] = self.driver.find_elements_by_xpath('')[0].text
        
        df = p.DataFrame(li, index=[0])#.transpose()
        df['indx'] = n.array(df.ix[:,'rank'], dtype=int16)
        df = df.set_index('indx')
        hdir = '/mldev/bin/data/bloomberg/billionaires/'
        mkdir_p(hdir)
        #df.to_csv('{0}rank.{1}.csv'.format(hdir, rank))
        #import ujson as j
        #jdf = ujson.dumps(df)
        #print jdf
        return df

    def getAllBillionaires(self, fromn=1):
        num = 200+2
        dfs = list(xrange(1, num))
        #self.billionaires = p.DataFrame()
        for i in xrange(fromn, num):
            try:
                dfs[i] = self.getProfile(i)
                self.billionaires = self.billionaires.combine_first(dfs[i])
                indx = xrange(0,4)
                hdir = '/mldev/bin/data/bloomberg/billionaires/'
                self.billionaires.ix[:,indx].to_csv('{0}/bloomberg-billionaires-index.csv'.format(hdir))
            except IndexError, e:
                print e
        
        for i in xrange(len(self.billionaires.ix[:,0])):
            self.billionaires.ix[i,'YTD change'] = mclean(self.billionaires.ix[i,'YTD change'])
            self.billionaires.ix[i,'networth'] = mclean(self.billionaires.ix[i,'networth'])
            self.billionaires.ix[i,'age'] = mclean(self.billionaires.ix[i,'age'])
        return self.billionaires
    
    def apad(self, a, num):
        a = n.array(a, dtype=int16)
        #print a
        az = n.zeros(num)
        #print az
        az[0:len(a)] = a
        return list(az)
    #apad([45,56,76], 5)
    
    def getPortfolio(self):
        ps = {}
        dfs = {}
        
        xp = '//*[@id="profile"]/div/div[2]/div[6]/div[1]/div[1]/div'
        res = self.driver.find_elements_by_xpath(xp)
        for i in res:
            nclass = i.get_attribute('class')
            print nclass
        
            xp = '//*[@id="profile"]/div/div[2]/div[6]/div[1]/div[1]/div[@class="'+nclass+'"]/div[@class="item"]'
            psn = []
            for i in self.driver.find_elements_by_xpath(xp): 
                psn.append(int(i.value_of_css_property('width').replace('px', '')))
            ps[nclass] = psn
        
            xp = '//div[@class="'+nclass+'"]/div[@class="item"]'
            els = self.driver.find_elements_by_xpath(xp)
            df = p.DataFrame()
            li = {}
            for i in xrange(len(els)):
                #print i
                #print els[i]
                ActionChains(self.driver).move_to_element(els[i]).perform()
                xp = '//*[@id="billionaires"]//div[@class="bubble"]/ul/li'
                res = self.driver.find_elements_by_xpath(xp)
                reso = res[0].text.split(' ')
                try:
                    li[i] = [res[0].text, res[1].text, reso[0], reso[1], reso[2]]
                except:
                    li[i] = [res[0].text, res[1].text, '', '', '']
                df = df.combine_first(p.DataFrame(li).transpose())
            df['px'] = psn
            print df
            dfs[nclass] = df
            print
        #print dfs
        
        #print p.DataFrame(ps)
        #a = n.array(ps['cash'])
        li = []
        for i in ps:
            li.append(len(ps[i]))
        for i in ps:
            ps[i] = self.apad(ps[i], n.max(li))
        print p.DataFrame(ps)

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
        co = p.read_csv('config.csv', header=None)
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
            except IndexError:
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
            return p.DataFrame(els, columns=[column])
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
        df = p.DataFrame(range(len(lss[0])))
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
                df = p.DataFrame(range(len(lss[0])))
                for i in lss:
                    df[i.columns[0]] = i
            except TypeError, e:
                print e
            """
            # combine all lists into a dataframe
            #print lss
            df = p.DataFrame(range(len(lss[0])))
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
                allPositions2 = p.read_json(self.fname_trader_positions)
                #print allPositions2
            except ValueError, e:
                allPositions2 = p.DataFrame()
                allPositions2.to_json(self.fname_trader_positions)
                #print allPositions2
                #print e
                
            fp = open(self.fname_trader_positions, 'r')
            allPositions2 = ujson.loads(fp.read())
            fp.close()
            
            #print allPositions2
            #print
            
            positions = df            
            #print positions
            #print positions.to_dict()
            allPositions2[username] = positions.to_dict()
            #allPositions2.to_json(self.fname_trader_positions)
            allPositions2 = convertDictKeysToString(allPositions2)
            #print ujson.dumps(allPositions2)
            
            fp = open(self.fname_trader_positions, 'w')
            fp.write(ujson.dumps(allPositions2))
            fp.close()
            
        return df
        
    # get target portfolio from etoro user
    def getTargetPortfolio(self, username=None):
        fname = self.fname_trader_positions
        fp = open(fname, 'r')
        em = fp.read()
        em = ujson.loads(em)
        #for i in em:
        #    print p.DataFrame(em[i])
        target = p.DataFrame([])
        if username == None:
            for i in em:
                emi = p.DataFrame(em[i])
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
            emi = p.DataFrame(em[username])
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
        idx = p.DataFrame(idx)
        p0 = p.DataFrame()
        if mode == 1:
            print idx.transpose().get_values()
            print n.diff(idx)
            print idx[0]
            for [i, j] in enumerate(res):
                print "{0} {1}".format(i,j)
        for i in idx:
            p0 = p0.combine_first(p.DataFrame(res).ix[idx[i][0]:idx[i][1],:])
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
            except AttributeError:
                if mode == 1:
                    print i[0]
                #print e
                ''
        ms = p.DataFrame(ms, columns=['Fecha', 'Concepto/Empresa', 'Debito/Credito', 'Saldo'])
        for i in range(len(ms.ix[:,2])):
            ms.ix[i,0] = self.cleanBancorDate(ms.ix[i,0], self.getBancorYear(fname))
            ms.ix[i,2] = self.cleanBancorNumber(ms.ix[i,2])
            ms.ix[i,3] = self.cleanBancorNumber(ms.ix[i,3])
        #print ms
        #pres = p.DataFrame(res).ix[:,:]
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
