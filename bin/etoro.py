# -*- coding: utf-8 -*-
"""
Created on Tue Nov 11 08:53:14 2014

@author: qore2
"""

import sys
import pandas as p
import numpy as n
import math as m
import matplotlib.pyplot as pp
import re
from subprocess import call

def etoro2pandasDataFrame():
    # beta people search
    # https://beta.etoro.com/discover/search

    #fname=sys.argv[1]
    #fname = "data/etoro/etoro.minimal-drawdown-4.txt"
    
    
    """
    fp = open(fname)
    t = fp.read()
    #print t
    """
    #t = sys.stdin.readlines()
    #t = call(["lynx", "-dump", 'data/etoro/etoro.minimal-drawdown-5.html'])
    import re
    from subprocess import Popen, PIPE    
    pop = Popen(["lynx", "-dump", 'data/etoro/etoro.minimal-drawdown-5.html'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = pop.communicate(b"input data that is passed to subprocess' stdin")
    rc = pop.returncode
    t = re.sub(re.compile("'"), '', output)
    t = t.split("\n")
    print t
    
    # find starting line number
    ns = []
    for num1, line in enumerate(t):
        if "ago" in line:
            ns.append(num1)
    sns = ns[0] - 2
    print sns
    #print t

    #import re
    #re.sub(re.compile())
    #rx=r".*(\[]).*"
    #print re.sub(re.compile(rx, re.M), "\1", t)
    #rxs = re.compile(rx, re.S).match(t).groups()[0]
    #print rxs
    #print t   
    
    #cstart = 1
    cend = sns-2
    
    """
    # columns
    cols = []
    for i in xrange(1,cend):
    #    print t[i]
        cols.append(t[i].strip())
    print cols
    """
    # index
    indx = []
    a5 = p.DataFrame()
    for i in xrange(cend+2,len(t)-1):
        print str(i)+ " " + str(t[i])
        #print 'i:'+str(i)
        mod = (int(i-sns) % 4)
        #print 'mod:'+str(mod)
        if mod == 2:
            a1 = t[i].split('ago')
            print a1
            if len(a1) == 1:
                a1.insert(0,'')
            a2 = a1[1].split('%')
            for j in xrange(0,len(a2)-1):
                a2[j] = re.sub(re.compile('<'),'', a2[j])
                a2[j] = float(a2[j])
            print a2
            a1 = p.DataFrame(a1)
            #print a2
            a2 = p.DataFrame(a2,[2,3,4,5,6])
            a3 = a1.combine_first(a2)
            a4 = p.DataFrame()
            a4[(i-(sns+2))/4] = a3.ix[:,0]
            a5 = a5.combine_first(a4.T)
            #print 
        
        indx.append(t[i])
        #if i % 4 == 0:
        #    print t[i]
        #if i % 4 == 1:
        #    print t[i]
    #print a4
    #print a5

    #print indx
    s = n.array(indx)
    num = float(len(s)+1) / 4
    #print num
    num = m.floor(num)
    #print num    
    s = s.reshape(num,4)
    df = p.DataFrame(s)
    df['a'] = a5.ix[:,0]
    df['b'] = a5.ix[:,2]
    df['c'] = a5.ix[:,3]
    df['d'] = a5.ix[:,4]
    df['e'] = a5.ix[:,5]

    df2 = p.DataFrame()
    df2['username'] = df.ix[:,0]
    df2['name'] = df.ix[:,1]
    df2['a'] = df.ix[:,'a']
    df2['b'] = df.ix[:,'b']
    df2['c'] = df.ix[:,'c']
    df2['d'] = df.ix[:,'d']
    df2['e'] = df.ix[:,'e']
    #print df2.ix[:,:]
    cols = ['b','d','e']
    top = df2.ix[:,cols]
    #top = 1 / (1+pow(n.e,-top))
    top = (top - n.mean(top)) / n.std(top)    
    print top
    pp.plot(top)
    pp.xlabel('traders')
    pp.legend(cols)
        
    #for i in xrange(14,len(t)-1):
    #    print t[i]

def test():
    s = n.random.randn(50)
    print s
    s = s.reshape(10,5)
    print s
    print p.DataFrame(s)
    
    s = n.array([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])
    print s
    s = s.reshape(3,5)
    print s
    a1 = p.DataFrame(s)
    print a1
    pp.plot(a1)
    

    s = n.array([1,2,3,4,'qwe'])
    print p.DataFrame(s)

etoro2pandasDataFrame()
#test()
