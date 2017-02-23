
import argparse
parser = argparse.ArgumentParser()
#parser.add_argument("-v", '--verbose', help="turn on verbosity")
parser.add_argument("-p", '--populate', help="Populate CSV file", action="store_true")
parser.add_argument("-f", '--fname', help="Read Keyword Planner CSV export file")

args = parser.parse_args()

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

if __name__ == "__main__":
    
    try:
        fname = args.fname
    except:
        print usage
        sys.exit()
    
    seo = SEO()
    try:
        if args.populate:
            seo.populateAllintitle(fname)
        if args.fname:
            seo.visualizeRank()
    except KeyboardInterrupt as e:
        ''
