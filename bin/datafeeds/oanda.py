
import sys

def defp(pt):
    try:    sys.path.index(pt)
    except: sys.path.append(pt)

defp('/ml.dev/bin')
defp('/ml.dev/lib/oanda/oandapy')
    
from qore import *
from qoreliquid import *
import oandapy
import pandas as p
import numpy as n
import requests
import datetime as dd
import time
# error classes
import requests
import socket

#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

co = ''
try:
    co = p.read_csv('config.csv', header=None)
except IOError, e:
    print e
    sys.exit()
    

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


import time
import numpy as np
import matplotlib.pyplot as plt

#------------------------------
# tick streamer (data feed)
class MyStreamer(oandapy.Streamer):
    def __init__(self, *args, **kwargs):
        oandapy.Streamer.__init__(self, *args, **kwargs)
        self.ticks = 0
        self.hdir = '/ml.dev/bin/data/oanda/datafeed'
        mkdir_p(self.hdir)
        
        self.df = p.DataFrame()
        self.sw = StatWing()
        
        # real time plot
        plt.axis([0, 2000, -0.41, -0.38])
        plt.ion()
        plt.show()
        self.i = 0
 
    def on_success(self, data):
        #self.ticks += 1
        #if self.ticks == 2: self.disconnect()
        try:
            pair = data['tick']['instrument']
            #print p.DataFrame(data['tick'], index=[0]).to_string(index=False).split('\n')[1]
            tick = p.DataFrame(data['tick'], index=[0])
            tick['timestamp'] = oandaToTimestamp(tick['time'].ix[0])
            csvc = n.array(tick.ix[:,[2,0,1,3,4]].get_values()[0], dtype=str)
            
            #csv = ",".join(csvc)            
            #fp = open('{0}/{1}.csv'.format(self.hdir, pair), 'a')
            #fp.write(csv+'\n')
            #fp.close()
            #print csv
            
            self.df[csvc[0]] = [float(csvc[1])]
            print self.df.transpose()
            nX = self.df.transpose()
            print nX 
            y = self.sw.predictFromTheta(nX=nX)
            
            #for i in range(1000):
            #y = np.random.random()
            pcn = 0.5
            try:
                imax = n.max(self.sw.nxps)
                #imax = imax + (imax * pcn/100)
                imax = imax + n.std(self.sw.nxps)
            except:
                ''
            try:
                imin = n.min(self.sw.nxps)
                #imin = imin - (imin * pcn/100)
                imin = imin - n.std(self.sw.nxps)
            except:
                ''
            #plt.axis([0, 2000, -0.41, -0.38])
                
            try:
                plt.axis([0, len(self.sw.nxps)+10, imin, imax])
            except:
                ''
            plt.scatter(self.i, y)
            plt.draw()
            #time.sleedf
            
            self.i += 1
            
        except requests.ConnectionError, e:
            ''
            #print e
        except KeyError, e:
            ''
            #print e

    def on_error(self, data):
        self.disconnect()

# source: http://www.digi.com/wiki/developer/index.php/Handling_Socket_Error_and_Keepalive
def do_work( forever = True):
    while True:
        print 'receiving feed..'
        try:
            stream = MyStreamer(environment=env2, access_token=access_token2)
            #pairs = ",".join(list(n.array(p.DataFrame(oanda2.get_instruments(accid)['instruments']).ix[:,'instrument'].get_values(), dtype=str))) #"EUR_USD,USD_CAD"
            #res = getPricesLatest(df, oanda2, sw).index
            #pairs = ",".join(list(res))
            pairs = 'EUR_USD,EUR_JPY,EUR_GBP,EUR_CHF,EUR_CAD,EUR_AUD,EUR_NZD,EUR_SEK,EUR_NOK,EUR_TRY,EUR_DKK'
            stream.start(accountId=accid, instruments=pairs)
        except socket.error, e:
            print '1:'
            print e
        except TypeError, e:
            ''
            print '2:'
            print e
        except NameError, e:
            ''
            print '3:'
            print e
        except IndexError, e:
            #print 'usage: python oanda.py'
            ''
            print '4:'
            print e
        except requests.exceptions.ChunkedEncodingError, e:
            print '5:'
            print e
        except requests.ConnectionError, e:
            print '6:'
            print e
            stream.disconnect()
        except KeyboardInterrupt, e:
            'disconnecting'
            stream.disconnect()
        #except:
        #    print 'unhandled error'
        #------------------------------
        
        try:
            #time.sleep(1)
            print 'connection error'
            print 'attempting disconnect before reconnecting'
            stream.disconnect()
        except:
            pass
         
if __name__ == '__main__':
    do_work( True)
