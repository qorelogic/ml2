
#%reload_ext autoreload
#%autoreload 2
import sys
def defp(pt):
    try:    sys.path.index(pt)
    except: sys.path.append(pt)
defp('/ml.dev/bin')
defp('/ml.dev/lib/oanda/oandapy')
#from qoreliquid import *
from seo import SEO
import pandas as p
import numpy as n

usage = '<keyword planner filename>'

try:
    fname = sys.argv[1]
except:
    print usage
    sys.exit()

seo = SEO()
try:
	seo.populateAllintitle(fname)
except KeyboardInterrupt as e:
	''

