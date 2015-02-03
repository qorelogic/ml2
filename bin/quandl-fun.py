# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import numpy as n
import pandas as p
import Quandl as q
import datetime as dd
from qoreliquid import *
from matplotlib import pyplot as plt
from pylab import rcParams
rcParams['figure.figsize'] = 20, 5

# <codecell>

#Wall Street Warriors Season 1 Episode 1
#https://www.youtube.com/watch?v=nyRiuv4EDB4

# <codecell>

pa = ''
# 2
pa += 'USDRUB USDARS USDJPY USDCHF EURUSD GBPUSD'

dr = getDataFromQuandl(pa, 'RUB')
dr = dr.ix[3000:len(dr)-1,:]
dr = normalizeme(dr)
dr = sigmoidme(dr)
#print n.corrcoef(dr.get_values())
#print dr
plot(dr)
legend(dr.columns,3)
show()

# <codecell>

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

de = getDataFromQuandl(pa, 'EUR')

# <codecell>

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

du = getDataFromQuandl(pa, 'USD')

# <codecell>

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

da = getDataFromQuandl(pa, 'AUD')

# <codecell>

res = n.diff(n.array(de.tail(30)).transpose())
#print res
plot(res)
title('Diff')

# <codecell>

pa = []
# 16
pa += ' /BITCOIN/MTGOXUSD /BITCOIN/BITSTAMPUSD /OFDP/GOLD_2 /OFDP/SILVER_5'

db = getDataFromQuandl(pa, 'BTC')

# <codecell>

#ran = n.random.randn(3,3)
print ran
grid = n.corrcoef(ran)
print grid
#scatter(ran)
#import matplotlib.pyplot as plt
#imshow()

#grid = np.random.random((10,10))
#print grid

#imshow(grid, extent=[0,9,0,1], aspect=3)
#title('Manually Set Aspect')
#tight_layout()
#show()

#ax = scaledimage(grid)

# <codecell>

"""
Simple matrix intensity plot, similar to MATLAB imagesc()

David Andrzejewski (david.andrzej@gmail.com)
"""
import numpy as NP
import matplotlib.pyplot as P
import matplotlib.ticker as MT
import matplotlib.cm as CM
 
def scaledimage(W, pixwidth=1, ax=None, grayscale=True):
    """
    Do intensity plot, similar to MATLAB imagesc()

    W = intensity matrix to visualize
    pixwidth = size of each W element
    ax = matplotlib Axes to draw on 
    grayscale = use grayscale color map

    Rely on caller to .show()
    """
    # N = rows, M = column
    (N, M) = W.shape 
    # Need to create a new Axes?
    if(ax == None):
        ax = P.figure().gca()
    # extents = Left Right Bottom Top
    exts = (0, pixwidth * M, 0, pixwidth * N)
    if(grayscale):
        ax.imshow(W,
                  interpolation='nearest',
                  cmap=CM.gray,
                  extent=exts)
    else:
        ax.imshow(W,
                  interpolation='nearest',
                  extent=exts)
 
    ax.xaxis.set_major_locator(MT.NullLocator())
    ax.yaxis.set_major_locator(MT.NullLocator())
    return ax
 
# Define a synthetic test dataset
testweights = NP.array([[0.25, 0.50, 0.25, 0.00],
                        [0.00, 0.50, 0.00, 0.00],
                        [0.00, 0.10, 0.10, 0.00],
                        [0.00, 0.00, 0.25, 0.75]])
testweights = NP.random.randn(100,100)
# Display it
#ax = scaledimage(testweights)
#ax = scaledimage(ran)
P.show()

# <codecell>

print de.ix[:,]

# <codecell>

#cc1 = de.get_values()
cc1 = de.ix[:].transpose() #.get_values()
cc1 = n.corrcoef(cc1)
grid = p.DataFrame(cc1)
#print cc1
#grid = grid.sort(1, ascending=False)
grid = grid.sort(0, ascending=False)
print grid

#ax = scaledimage(grid)

sys.exit()

from pylab import rcParams
rcParams['figure.figsize'] = 20, 5
imshow(grid, extent=[0,100,0,10], aspect=10)
title('Manually Set Aspect')
tight_layout()

show()

# <codecell>

#print len(de.columns)
#print de.ix[:,[0,1]]
def getCorrelations(d, primary):
    corrs = []
    for i in range(0, len(d.columns)):
        corrs.append(n.corrcoef(d.ix[:,primary], d.ix[:,i])[0][1])
    corrs = p.DataFrame(corrs, index=d.columns, columns=[primary])
    #print n.correlate(r1, r2)
    #corrs = corrs.sort(columns=primary, ascending=False)
    print corrs
    return corrs
    #plot(corrs,'.')
c0 = getCorrelations(de, de.columns[0])
c1 = getCorrelations(de, de.columns[1])
c2 = getCorrelations(de, de.columns[2])
c = c0.combine_first(c1)
c = c.combine_first(c2)
#c = c.sort(columns=de.columns[0], ascending=True)

c = n.array(c)
#print c
#ax = scaledimage(c)
#plot(c)
#print c1
#print c2

# <codecell>

from pylab import rcParams
rcParams['figure.figsize'] = 20, 5*3
fig = plt.figure()

ax1 = fig.add_subplot(211)
ax1.plot(sigmoidme(normalizeme(du)),'.')
#ax1.title('USD pairs')
#legend(d.columns)
ax2 = fig.add_subplot(212)
ax2.plot(sigmoidme(normalizeme(de)),'.')
#ax2.title('EUR pairs')
#ax3 = fig.add_subplot(213)
#ax3.plot(sigmoidme(normalizeme(da)))
#ax3.title('AUD pairs')
plt.show()

# <codecell>

drbrte = q.get("DOE/RBRTE", authtoken="WVsyCxwHeYZZyhf5RHs2")

# <codecell>

import numpy as n

def plotB(d):
    r = range(0,len(d))
    #plot(r)
    res = n.power(2,r)
    ic = 10
    #res
    
    hds = []
    hds.append('Value')
    
    d['ex1'] = ic * n.power(1 + 0.37 / 100, r)
    #res1 = n.power(1 + 0.6 / 100, r)
    hds.append('ex1')
    
    d['ex2'] = ic * n.power(1 + 0.29 / 100, r)
    #res2 = n.power(1 + 0.48 / 100, r)
    hds.append('ex2')
    
    d['ex3'] = ic * n.power(1 + 0.19 / 100, r)
    hds.append('ex3')
    
    res = d.ix[0:700,hds]
    #print d
    #print res
    plot(res)
    legend(['value','ex1','ex2','ex3'])

#print drbrte
#plot(drbrte.ix[:,['Value']])
plotB(drbrte)

# <codecell>

res
y = res.ix[:,'Close']
y

# <codecell>

import Quandl as q
d = q.get("BCHARTS/BTCEUSD", authtoken="WVsyCxwHeYZZyhf5RHs2")
print d
plot(d.ix[:,['Close']])

# <codecell>

#print d.ix[:,['Close']]
#print len(d)
a = n.array(d.ix[0:len(d),['Close']]).transpose().tolist()[0]
b = n.array(d.ix[1:len(d),['Close']]).transpose().tolist()[0]
b.insert(len(de),0)
#print len(a)
#print len(b)
#print a[0]
de = p.DataFrame(index=d.index)
#print len(de)

de['a'] = a
de['b'] = b
# tomorrow opens higher
de['c'] = n.array((de.ix[:,'a'] - de.ix[:,'b']) < 0)
#print 
print de.tail(10)

# <codecell>

import Quandl as q
def quandlget(t):
    return q.get(t, authtoken="WVsyCxwHeYZZyhf5RHs2")

BCHAIN_NTRAN = quandlget("BCHAIN/NTRAN")
BCHAIN_MKTCP = quandlget("BCHAIN/MKTCP")
BCHAIN_TOTBC = quandlget("BCHAIN/TOTBC")
BCHAIN_NTRAT = quandlget("BCHAIN/NTRAT")
BCHAIN_HRATE = quandlget("BCHAIN/HRATE")
BCHAIN_ETRVU = quandlget("BCHAIN/ETRVU")
BCHAIN_NADDU = quandlget("BCHAIN/NADDU")
BCHAIN_AVBLS = quandlget("BCHAIN/AVBLS")
BCHAIN_MIREV = quandlget("BCHAIN/MIREV")

# <codecell>

"""
plot(BCHAIN_HRATE)
plot(BCHAIN_NTRAN)
plot(BCHAIN_MKTCP)
plot(BCHAIN_TOTBC)
plot(BCHAIN_NTRAT)
plot(BCHAIN_HRATE)
plot(BCHAIN_ETRVU)
plot(BCHAIN_NADDU)
plot(BCHAIN_AVBLS)
plot(BCHAIN_MIREV)
"""

# <codecell>

import pandas as p
dd = p.DataFrame()
dd['BCHAIN_NTRAN'] = BCHAIN_NTRAN.ix[:,'Value']
dd['BCHAIN_MKTCP'] = BCHAIN_MKTCP.ix[:,'Value']
dd['BCHAIN_TOTBC'] = BCHAIN_TOTBC.ix[:,'Value']
dd['BCHAIN_NTRAT'] = BCHAIN_NTRAT.ix[:,'Value']
dd['BCHAIN_HRATE'] = BCHAIN_HRATE.ix[:,'Value']
dd['BCHAIN_ETRVU'] = BCHAIN_ETRVU.ix[:,'Value']
dd['BCHAIN_NADDU'] = BCHAIN_NADDU.ix[:,'Value']
dd['BCHAIN_AVBLS'] = BCHAIN_AVBLS.ix[:,'Value']
dd['BCHAIN_MIREV'] = BCHAIN_MIREV.ix[:,'Value']
dd['btceusd'] = d.ix[:,['Close']]
dd['tomorrowHiger'] = de['c']

dd = (dd- n.mean(dd))/n.std(dd)
dd = 1 / (1 + n.power(n.e, -dd))
#print dd.tail(10)
dd.to_csv('test-2131211212.csv')
print len(dd)
plot(dd,'.')
legend(['BCHAIN_NTRAN','BCHAIN_MKTCP','BCHAIN_TOTBC','BCHAIN_NTRAT','BCHAIN_HRATE','BCHAIN_ETRVU','BCHAIN_NADDU','BCHAIN_AVBLS','BCHAIN_MIREV','btceusd','tomorrowHigher'],2)

# <codecell>

def computeCost(X, y, theta):
    X = n.array(X)
    #print X
    m = len(y)
    J = 0
    J = 1.0/(2*m) * n.sum(n.power(n.dot(X,theta)-y,2))
    return J

print computeCost( n.array([1, 2, 1, 3, 1, 4, 1, 5]).reshape(4,2), n.array([7, 6, 5, 4]).reshape(4,1), n.array([0.1,0.2]).reshape(2,1) )
# 11.945
print computeCost( n.array([1,2,3,1,3,4,1,4,5,1,5,6]).reshape(4,3), n.array([7, 6, 5, 4]).reshape(4,1), n.array([0.1,0.2,0.3]).reshape(3,1))
# 7.0175

# <codecell>

import pandas as p
import numpy as n
res = p.DataFrame(n.array([1, 2, 1, 3, 1, 4, 1, 5]).reshape(4,2))

#print n.array([1,5,1,2,1,4,1,5]).reshape(4,2)
y=500
x=4
res = n.array(n.random.randn(y*x)).reshape(y,x)
#print n.array([1,6,4,2]).reshape(4,1)
plot(res)

# <codecell>

def gradientDescent(X, y, theta, alpha, num_iters):
    m = len(y)
    J_history = n.zeros(num_iters)
    for iter in range(0,num_iters):
        theta = theta - (float(alpha)/m) * n.dot((n.dot(X,theta)-y).transpose(),X).transpose()
        J_history[iter] = computeCost(X, y, theta)
    
    return [theta, J_history]
    
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

# <codecell>

# gradient descent
data = p.read_csv('/coursera/ml-007/programming-exercises/mlclass-ex1/ex1data1.txt', header=None)
#print data
X = data.ix[:,0]
y = data.ix[:,1]
m = len(y)

#plot(X,y,'.')

X = p.DataFrame()
X[0] = ones(m)
X[1] = data.ix[:,0]

theta = n.zeros(2)

#% Some gradient descent settings
iterations = 1500;
alpha = 0.01;
    
#% compute and display initial cost
computeCost(X, y, theta)

#% run gradient descent
[theta, J_hist] = gradientDescent(X, y, theta, alpha, iterations);

#% print theta to screen
print 'Theta found by gradient descent: '
#print '%f %f \n', theta(1), theta(2)
print theta

# <codecell>

#print n.dot(X,theta)
#plot(X.ix[:,1],y,'.')
#plot(,y,'-')
print n.dot(n.array([1, 3.5]), theta) * 1e4
print n.dot(n.array([1, 7]), theta) * 1e4

# <codecell>

theta0_vals = linspace(-10, 10, 100)
theta1_vals = linspace(-1, 4, 100)
thetas = []
lowCC = 1e9
thetas = []
J_vals = n.zeros(len(theta0_vals)*len(theta1_vals)).reshape(len(theta0_vals),len(theta1_vals))
for i in range(0,len(theta0_vals)):
    for j in range(0,len(theta1_vals)):
        t = n.array([theta0_vals[i], theta1_vals[j]])
        #print theta0_vals[i]
        #print theta1_vals[j]
        #print t
        cc = computeCost(X, y, t)
        J_vals[i][j] = cc
        if cc < lowCC:
            lowCC = cc
            lowT = t
            thetas.append(list(t))
        #print t
print lowCC
print lowT
print thetas
#print cc
#print J_vals
contour(theta0_vals, theta1_vals, J_vals, logspace(-2, 3, 20))
#print thetas
#plot(t[0], t[1], 'xr')
plot(lowT[0], lowT[1], 'xr')
#plot(J_vals)

# <codecell>

th = n.array(thetas)
#print th
contour(theta0_vals, theta1_vals, J_vals, logspace(-2, 3, 80))
plot(th[:,0], th[:,1])

# <codecell>

lgs = logspace(-2, 3, 20)
contour(theta0_vals, theta1_vals, J_vals, lgs)
#plot(J_vals) 
#plot(theta0_vals, theta1_vals, '.')
#print J_vals

# <codecell>

#lgs = logspace(-2, 3, 20)
lgs = logspace(0, 1, 20)
#print lgs
#plot(lgs.transpose())
#c = n.array([1,2.2,3.1,4.8,5.1,6.1]).reshape(3,2)
y2 = 10
x = 2
#c = n.random.randn(y2*x).reshape(y2,x)
#print c
#contour(c)
#plot(c,'.')
#plot(c)
#print J_vals.transpose()
#print plot(J_vals)
#plot(t[0], t[1], 'xr')
cc = computeCost(X, y, t)

# <codecell>

len(J_vals)
#print J_vals
plot(J_vals,'.')

