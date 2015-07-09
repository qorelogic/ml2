#!/usr/bin/env python

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
import matplotlib.pyplot as plt

#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# todo: fix jbd2 io read write issue
# iotop -obtqqq | grep jbd2:
# https://bbs.archlinux.org/viewtopic.php?id=113516
# http://ubuntuforums.org/showthread.php?t=839998

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

oq = OandaQ()

#------------------------------
# tick streamer (data feed)
class MyStreamer(oandapy.Streamer):
    def __init__(self, *args, **kwargs):
        oandapy.Streamer.__init__(self, *args, **kwargs)
        self.ticks = 0
        self.hdir = '/ml.dev/bin/data/oanda/datafeed'
        mkdir_p(self.hdir)
        
        self.rtc = RealtimeChart()

    def on_success(self, data):
        #self.ticks += 1
        #if self.ticks == 2: self.disconnect()
        try:
            pair = data['tick']['instrument']
            #print p.DataFrame(data['tick'], index=[0]).to_string(index=False).split('\n')[1]
            tick = p.DataFrame(data['tick'], index=[0])
            tick['timestamp'] = oq.oandaToTimestamp(tick['time'].ix[0])
            csvc = n.array(tick.ix[:,[2,0,1,3,4]].get_values()[0], dtype=str)
            
            csv = ",".join(csvc)            
            #fp = open('{0}/{1}.csv'.format(self.hdir, pair), 'a')
            #fp.write(csv+'\n')
            #fp.close()
            #print csv
            
            self.rtc.update(csvc)
            
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
            #pairs = ",".join(list(res))
            #res = getPricesLatest(df, oanda2, sw).index
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
    ''
