#from numpy import *
import numpy as n
    
def toCurrency(n):
    return '%2d' % n

def normalizeme(dfr):
    return ((dfr - n.mean(dfr))/n.std(dfr))

def sigmoidme(dfr):
    return 1.0 / (1 + pow(n.e,-dfr))

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
