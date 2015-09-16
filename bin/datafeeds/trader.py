
import sys

def defp(pt):
    try:    sys.path.index(pt)
    except: sys.path.append(pt)

defp('/ml.dev/bin')
defp('/ml.dev/lib/oanda/oandapy')

from qoreliquid import *

qq = QoreQuant()

def train():
    qq.main()
    #qq.updateDatasets()

def forecast():
    tp = qq.predict()
    qq.tradePrediction(tp)

if sys.argv[1] == 'forecast':
    try:
        forecast()
    except:
        train()
        forecast()
        
try:
    if sys.argv[1] == 'train':
        train()
except:
    print 'usage: trader.py <train|forecast>'