# -*- coding: utf-8 -*-
"""
Created on Thu Nov 13 21:52:25 2014

@author: qore2
"""

import numpy as n
import pandas as p
from matplotlib.pylab import *

class FinancialModel:
    
    def getRateFromProjectedAccruedment(from_capital, to_capital, period):
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
        
    def compoundVestedCapital(self, rate, period):
        rate   = n.array(rate, dtype=float64)
        period = n.array(period)    
        #return 100 * pow(1 + rate / 100, period)
        #res =  100 * n.power(1 + rate / 100, period.reshape(size(period), 1))
        return 100 * n.power(1 + rate.reshape(size(rate), 1) / 100, period)
        
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

fm = FinancialModel()
#fm.test()
fm

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
