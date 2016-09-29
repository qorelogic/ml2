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
    
oq = OandaQ(selectOandaAccount=0, selectOandaSubAccount=6)

modes = 'demo,feed,plotly,csv,babysit,zmq,accountdata'.split(',')

def usage():
    qd._getMethod()
    #return "usage: demo | feed | plotly | csv | babysit | zmq | "
    return "usage: %s" % ' | '.join(modes)

@profile
def getCsvc(data):
    #data['tick']['timestamp'] = str(OandaQ._oandaToTimestamp(data['tick']['time']))
    data['tick']['timestamp'] = str(oq.oandaToTimestamp(data['tick']['time']))
    csvc = [data['tick']['instrument'], str(data['tick']['bid']), str(data['tick']['ask']), data['tick']['time'], data['tick']['timestamp']]
    return csvc

def getCsvc0(data):
    tick = p.DataFrame(data['tick'], index=[0])
    tick['timestamp'] = oq.oandaToTimestamp(tick['time'].ix[0])
    csvc = n.array(tick.ix[:,[2,0,1,3,4]].get_values()[0], dtype=str)
    return csvc

#------------------------------
# tick streamer (data feed)
class MyStreamer(oandapy.Streamer):
    def __init__(self, *args, **kwargs):
        qd._getMethod()
        
        oandapy.Streamer.__init__(self, *args, **kwargs)
        self.ticks = 0
        self.hdir = '/ml.dev/bin/data/oanda/datafeed'
        mkdir_p(self.hdir)
        
#    @profile
    def init(self, mode):
        qd._getMethod()
        
        self.mode = mode        

        self.zmq = ZMQ()

        while switch(self.mode):
            if case('demo'):
                break
            if case('feed'):
                try:
                    self.mongo = mong.MongoClient()
                except Exception as e:
                    print '%s: connection to mongodb failed' % e
                    sys.exit()
                self.zmq.zmqInit()
                break
            if case('csv'):
                break
            if case('accountdata'):
                #print oq.oanda2.get_accounts()
                accid = <account no.>
                self.trades    = oq.oanda2.get_trades(accid, count=500)
                self.trades    = p.DataFrame(self.trades['trades']) #.set_index('instrument')
                self.trades    = self.trades.combine_first(getSyntheticCurrencyTable(oq.oanda2, oq, self.trades['instrument']))
                self.prices    = oq.oanda2.get_prices(instruments=','.join(self.trades['instrument']))
                self.prices    = p.DataFrame(self.prices['prices']) #.set_index('instrument')
                self.trades['bid'] = self.prices['bid']
                self.trades['ask'] = self.prices['ask']
                self.positions = oq.oanda2.get_positions(accid, count=500)
                self.positions = p.DataFrame(self.positions['positions']).set_index('instrument')
                self.account = oq.oanda2.get_account(accid)
                self.account = p.DataFrame(self.account, index=[0])#.transpose()
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
                self.zmq.zmqInit()
                break

            print usage()
            break

    @profile
    def on_success(self, data):
        #qd._getMethod()
        
        #self.ticks += 1
        #if self.ticks == 2: self.disconnect()
        try:
            while switch(self.mode):
                if case('demo'):
                    print data
                    break
                if case('feed'):
                    # insert to ql mongodb
                    self.mongo.ql.ticks.insert(data['tick'])
                    self.zmq.zmqSend(data)
                    break
                if case('csv'):
                    csv = ",".join(getCsvc(data))            
	              #appendCsv.delay(csv, '{0}/{1}.csv'.format(self.hdir, pair))
                    #print p.DataFrame(data['tick'], index=[0]).to_string(index=False).split('\n')[1]
                    #pair = data['tick']['instrument']
                    #fp = open('{0}/{1}.csv'.format(self.hdir, pair), 'a')
                    #fp.write(csv+'\n')
                    #fp.close()
                    print csv
                    break
                if case('accountdata'):
                    pcsv = getCsvc(data)
                    csv  = ",".join(pcsv)

                    #self.positions.ix[pcsv[0], 'bid'] = pcsv[1]
                    #self.positions.ix[pcsv[0], 'ask'] = pcsv[2]
                    #self.positions = self.positions.fillna(0)
                    #print self.positions

                    #self.trades.ix[pcsv[0], 'bid'] = pcsv[1]
                    #self.trades.ix[pcsv[0], 'ask'] = pcsv[2]
                    with p.option_context('display.max_rows', 15, 'display.max_columns', 4000, 'display.width', 1000000):
                        tdf = self.trades[self.trades['instrument'] == pcsv[0]]
                        self.trades.ix[tdf.index, 'bid'] = float(pcsv[1])
                        self.trades.ix[tdf.index, 'ask'] = float(pcsv[2])
                        self.trades = self.trades.fillna(0)
                        self.trades['pl'] = calcPl(self.trades['bid'], self.trades['ask'], self.trades['price'], getSideBool(self.trades['side']), self.trades['pairedCurrencyBid'], self.trades['pairedCurrencyAsk'], self.trades['units'])
                        #print self.trades[self.trades['instrument'] == pcsv[0]]
                        #print self.trades.shape
                        #print self.trades.columns
                        #print self.trades.index
                        #print self.trades.ix[:, 'id instrument price side stopLoss takeProfit time trailingAmount trailingStop units bid ask pl'.split(' ')]
                        #print self.trades.ix[:, 'id instrument price side stopLoss takeProfit trailingAmount trailingStop units bid ask pl pairedCurrencyBid pairedCurrencyAsk'.split(' ')]
                        #print self.trades.ix[:, 'id instrument price side units bid ask pl'.split(' ')]
                        #print self.trades.ix[:, 'id instrument pl'.split(' ')]
                        #print self.trades.ix[:, 'id instrument price side units bid ask pl'.split(' ')]
                        sumPl = n.sum(self.trades['pl'])
                        self.account.ix[0, 'unrealizedPl'] = sumPl
                        self.account['netAssetValue'] = self.account['balance'] + self.account['unrealizedPl']
                        self.ffds = 'balance netAssetValue unrealizedPl'.split(' ')
                        print self.account.ix[:, self.ffds]#.to_dict()
                        #print self.prices
                        #print csv
                        #print '---'
                        #print
                    break
                if case('plotly'):
                    self.rtc.update(getCsvc(data))
                    break
                if case('babysit'):
                    res = oq.babysitTrades(self.trades, data['tick'])
                    #if res == False:
                    #    print data
                    break
                if case('zmq'):
                    #res = oq.babysitTrades(self.trades, data['tick'], verbose=True)
                    #print j.dumps(res.get_values())
                    #print (res.to_dict())
                    self.zmq.zmqSend(data)
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

class ZMQ:

    def log(st):
        print st        

#    @profile
    def zmqInit(self):
        #fname = '/tmp/zmq.log'
        #self.fp = open(fname, 'a')
        ctx = zmq.Context()
        #socket = ctx.socket(zmq.REP)
        #socket = ctx.socket(zmq.PUSH)
        self.socket = ctx.socket(zmq.PUB);
        
        # A+B feeds
        try:
            port = 5555
            url  = 'tcp://*:{0}'.format(port)
            self.socket.bind(url)
        except:
            port = 5556
            url  = 'tcp://*:{0}'.format(port)
            self.socket.bind(url)
        
        try:
            self.mongo = mong.MongoClient()
        except:
            ''
        #self.log('feeding on {0}[zmq]'.format(url))

#    @profile
    def zmqSend(self, data):
        csvc = getCsvc(data)
        csv = ",".join(csvc)
        #print csvc
        #if res == False:
        #    print data
        
        #self.socket.recv(0) # only for REP
        #stri = 'world {0}'.format(int(n.random.rand()*10))
        stri = '{0}'.format(csv)
        #print stri
        topic = 'tester'
        self.socket.send("%s %s" % (topic, stri)) # only for PUB
        #self.socket.send(stri)
        #self.fp.write(msg+'\n')

            
# source: http://www.digi.com/wiki/developer/index.php/Handling_Socket_Error_and_Keepalive
#@profile
def do_work(mode, forever = True):
    qd._getMethod()

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
                if case('accountdata'):
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
                    pairs = ",".join(list(n.array(p.DataFrame(oq.oandaConnection().get_instruments(oq.aid)['instruments']).ix[:,'instrument'].get_values(), dtype=str))) #"EUR_USD,USD_CAD"
                    #pairs = oq.getBabySitPairs()
                    break
                print usage()
                break
            
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
            #stream.disconnect()
            break
        except Exception as e:
            qd.printTraceBack()
            print '7:'
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
