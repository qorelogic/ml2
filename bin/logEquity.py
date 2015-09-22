
import sys
try: sys.path.index('/mldev/bin')
except: sys.path.append('/mldev/bin')

#from oandaq import OandaQ
from qorequant import QoreQuant
from pandas import read_csv as p_read_csv
from qore import mkdir_p

df = p_read_csv('/mldev/bin/datafeeds/config.csv', header=None)
# get the active oanda account indeces
ain = list(df.ix[list(df[3] == 1),0].index)
for i in ain:
    #qq.oq = OandaQ(verbose=True, selectOandaAccount=i)    
    qq = QoreQuant(verbose=True, selectOandaAccount=i)
    qq.oq.logEquity(daemon=False, csvSave=False)
