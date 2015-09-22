#!/usr/bin/env python

import sys

def defp(pt):
    try:    sys.path.index(pt)
    except: sys.path.append(pt)

defp('/ml.dev/bin')
defp('/ml.dev/lib/oanda/oandapy')
    
from qore import *
from qoreliquid import *
from oandaq import OandaQ
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
import zmq, time
import ujson as j
import pymongo as mong

qd = QoreDebug()
qd.off()
qd.stackTraceOff()

# import celery message-queue tasks
from mqtasks import *

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
    
oq = OandaQ()

modes = 'demo,feed,plotly,csv,babysit,zmq'.split(',')

def usage():
    qd._getMethod()
    return "usage: demo | feed | plotly | csv | babysit | zmq"

#------------------------------
# tick streamer (data feed)
class MyStreamer(oandapy.Streamer):
    def __init__(self, *args, **kwargs):
        qd._getMethod()
        
        oandapy.Streamer.__init__(self, *args, **kwargs)
        self.ticks = 0
        self.hdir = '/ml.dev/bin/data/oanda/datafeed'
        mkdir_p(self.hdir)
        
    def init(self, mode):
        qd._getMethod()
        
        self.mode = mode        

        while switch(self.mode):
            if case('demo'):
                break
            if case('feed'):
                self.mongo = mong.MongoClient()
                break
            if case('csv'):
                break
            if case('plotly'):
                self.rtc = RealtimeChart()
                #self.rtc.qd.on()
                #self.rtc.qd.stackTraceOn()
                return self.rtc
                break
            if case('babysit'):
                self.trades = oq.oandaConnection().get_trades(oq.aid)['trades']
                self.account = oq.oandaConnection().get_account(oq.aid)
#		oq.gotoMarket()
                break
            if case('zmq'):
                self.trades = oq.oandaConnection().get_trades(oq.aid)['trades']
                self.account = oq.oandaConnection().get_account(oq.aid)
                #oq.gotoMarket()

                ctx = zmq.Context()
                #socket = ctx.socket(zmq.REP)
                #socket = ctx.socket(zmq.PUSH)
                self.socket = ctx.socket(zmq.PUB);
                self.socket.bind('tcp://*:5555')
                
                self.mongo = mong.MongoClient()
                
                break

            print usage()
            break

    def on_success(self, data):
        qd._getMethod()
        
        #self.ticks += 1
        #if self.ticks == 2: self.disconnect()
        try:
            tick = p.DataFrame(data['tick'], index=[0])
            tick['timestamp'] = oq.oandaToTimestamp(tick['time'].ix[0])
            csvc = n.array(tick.ix[:,[2,0,1,3,4]].get_values()[0], dtype=str)
            while switch(self.mode):
                if case('demo'):
                    print data
                    break
                if case('feed'):
                    # insert to ql mongodb
                    self.mongo.ql.ticks.insert(data['tick'])
                    break
                if case('csv'):
                    csv = ",".join(csvc)            
	              #appendCsv.delay(csv, '{0}/{1}.csv'.format(self.hdir, pair))
                    #print p.DataFrame(data['tick'], index=[0]).to_string(index=False).split('\n')[1]
                    #pair = data['tick']['instrument']
                    #fp = open('{0}/{1}.csv'.format(self.hdir, pair), 'a')
                    #fp.write(csv+'\n')
                    #fp.close()
                    print csv
                    break
                if case('plotly'):
                    self.rtc.update(csvc)
                    break
                if case('babysit'):
                    res = oq.babysitTrades(self.trades, data['tick'])
                    #if res == False:
                    #    print data
                    break
                if case('zmq'):
                    res = oq.babysitTrades(self.trades, data['tick'], verbose=True)
                    #print j.dumps(res.get_values())
                    #print (res.to_dict())
                    csv = ",".join(csvc)
                    #if res == False:
                    #    print data
                    
                    #self.socket.recv(0) # only for REP
                    #stri = 'world {0}'.format(int(n.random.rand()*10))
                    stri = '{0}'.format(csv)
                    #print stri
                    topic = 'tester'
                    self.socket.send("%s %s" % (topic, stri)) # only for PUB
                    #self.socket.send(stri)
                    
                    # insert to ql mongodb
                    self.mongo.ql.ticks.insert(data['tick'])
                    
                    break
                print usage()
                break
            
        except IndexError, e:
            #print 'usage: python oanda.py'
            ''
            print '4:'
            print e
            qd.printTraceBack()
        except requests.ConnectionError, e:
            qd.printTraceBack()
            ''
            #print e
        except KeyError, e:
            qd.printTraceBack()
            ''
            #print e
            
    def on_error(self, data):
        qd._getMethod()
        
        self.disconnect()

# source: http://www.digi.com/wiki/developer/index.php/Handling_Socket_Error_and_Keepalive
def do_work(mode, forever = True):
    qd._getMethod()

    oq = OandaQ()
    
    while True:
        print 'receiving feed..'
        try:
            stream = MyStreamer(environment=oq.env2, access_token=oq.access_token2)
            rtc = stream.init(mode)
            #pairs = ",".join(list(res))
            #res = getPricesLatest(df, oq.oandaConnection(), sw).index

            while switch(stream.mode):
                if case('demo'):
                    pairs = ",".join(list(n.array(p.DataFrame(oq.oandaConnection().get_instruments(oq.aid)['instruments']).ix[:,'instrument'].get_values(), dtype=str))) #"EUR_USD,USD_CAD"
                    break
                if case('feed'):
                    pairs = ",".join(list(n.array(p.DataFrame(oq.oandaConnection().get_instruments(oq.aid)['instruments']).ix[:,'instrument'].get_values(), dtype=str))) #"EUR_USD,USD_CAD"
                    break
                if case('csv'):
                    pairs = 'EUR_USD,EUR_JPY,EUR_GBP,EUR_CHF,EUR_CAD,EUR_AUD,EUR_NZD,EUR_SEK,EUR_NOK,EUR_TRY,EUR_DKK'
                    break
                if case('plotly'):
                    #pairs = 'EUR_USD,EUR_JPY,EUR_GBP,EUR_CHF,EUR_CAD,EUR_AUD,EUR_NZD,EUR_SEK,EUR_NOK,EUR_TRY,EUR_DKK'
                    pairs = rtc.getInstruments()
                    break
                if case('babysit'):
                    pairs = oq.getBabySitPairs()
                    break
                if case('zmq'):
                    pairs = oq.getBabySitPairs()
                    break
                print usage()
                break
            
            print 'getbabysit:{0}'.format(pairs)
            if pairs != '':
                print '------pairs-----'
                print pairs
                print '----------'
                stream.start(accountId=oq.aid, instruments=pairs)
                #sys.exit(0)
            else:
                #oq.gotoMarket()
                #break
                ''
            
        except socket.error, e:
            print '1:'
            print e
            qd.printTraceBack()
        except TypeError, e:
            ''
            print '2:'
            print e
            qd.printTraceBack()
        except NameError, e:
            ''
            print '3:'
            print e
            qd.printTraceBack()
        except IndexError, e:
            #print 'usage: python oanda.py'
            ''
            print '4:'
            print e
            qd.printTraceBack()
        except requests.exceptions.ChunkedEncodingError, e:
            print '5:'
            print e
            qd.printTraceBack()
        except requests.ConnectionError, e:
            print '6:'
            print e
            qd.printTraceBack()
            stream.disconnect()
        except KeyboardInterrupt, e:
            'disconnecting'
            qd.printTraceBack()
            stream.disconnect()
        except Exception as e:
            qd.printTraceBack()
            print e
            print 'unhandled error'
        #------------------------------
        
        try:
            #time.sleep(1)
            print 'connection error'
            print 'attempting disconnect before reconnecting'
            stream.disconnect()
        except:
            qd.printTraceBack()
            pass
         
if __name__ == '__main__':
    qd._getMethod()
    
    try:
        if sys.argv[1] not in modes:
            raise
        do_work(sys.argv[1], True)
    except Exception as e:
        qd.printTraceBack()
        print e
        print usage()
        
