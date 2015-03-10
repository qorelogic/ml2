
import sys

try:
    sys.path.index('/ml.dev/bin')
except:
    sys.path.append('/ml.dev/bin')
    
from qore import *
import oandapy
import pandas as p
import numpy as n
import requests
import datetime as dd

#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

co = p.read_csv('config.csv', header=None)

env1=co.ix[0,1]
access_token1=co.ix[0,2]
oanda1 = oandapy.API(environment=env1, access_token=access_token1)

env2=co.ix[1,1]
access_token2=co.ix[1,2]
oanda2 = oandapy.API(environment=env2, access_token=access_token2)

acc = oanda2.get_accounts()['accounts']
accid = acc[0]['accountId']

def oandaToTimestamp(ptime):
    dt = dd.datetime.strptime(ptime, '%Y-%m-%dT%H:%M:%S.%fZ')
    return (dt - dd.datetime(1970, 1, 1)).total_seconds() / dd.timedelta(seconds=1).total_seconds()

# tick streamer (data feed)
class MyStreamer(oandapy.Streamer):
    def __init__(self, *args, **kwargs):
        oandapy.Streamer.__init__(self, *args, **kwargs)
        self.ticks = 0
        self.hdir = '/ml.dev/bin/data/oanda/datafeed'
        mkdir_p(self.hdir)
        
    def on_success(self, data):
        #self.ticks += 1
        #if self.ticks == 2: self.disconnect()
        try:
            pair = data['tick']['instrument']
            #print p.DataFrame(data['tick'], index=[0]).to_string(index=False).split('\n')[1]
            tick = p.DataFrame(data['tick'], index=[0])
            tick['timestamp'] = oandaToTimestamp(tick['time'].ix[0])
            csv = ",".join(n.array(tick.ix[:,[2,0,1,3,4]].get_values()[0], dtype=str))
            fp = open('{0}/{1}.csv'.format(self.hdir, pair), 'a')
            fp.write(csv+'\n')
            fp.close()
        except KeyError, e:
            ''
            #print e

    def on_error(self, data):
        self.disconnect()
        
stream = MyStreamer(environment=env2, access_token=access_token2)
try:
    pairs = ",".join(list(n.array(p.DataFrame(oanda2.get_instruments(accid)['instruments']).ix[:,'instrument'].get_values(), dtype=str))) #"EUR_USD,USD_CAD"
    stream.start(accountId=accid, instruments=pairs)
except TypeError, e:
    ''
    #print e
except NameError, e:
    ''
    #print e
except IndexError, e:
    #print 'usage: python oanda.py'
    ''
    #print e
except requests.ConnectionError, e:
    print e
except KeyboardInterrupt, e:
    'disconnecting'
    stream.disconnect()
