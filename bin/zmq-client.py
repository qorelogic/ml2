#!/usr/bin/env python

import zmq, time, sys
from pandas import DataFrame as p_DataFrame
from numpy import array as n_array
import numpy as n
from collections import deque
import os
import curses
import threading

def normalizeme(dfr, pinv=False):
    
    nmean = n.mean(dfr, axis=0)
    nstd = n.std(dfr, axis=0)
    #nmean = n.mean(dfr)
    #nstd = n.std(dfr)
    dfr = (dfr - nmean) / nstd
    #dfr = n.divide((dfr - nmean), nstd)
    if pinv == False:
        return dfr
    else:
        return [dfr, nmean, nstd]
        
def sigmoidme(dfr):
    return 1.0 / (1 + pow(n.e,-dfr))


class ZMQClient:

    def __init__(self):
        # option to change the port number from default 5555
        try:
            hostport = sys.argv[1]
        except:
            hostport = 5555    
        
        res      = hostport.split(':')
        host     = res[len(res)-2]
        if host == '': host = 'localhost'
        port     = res[len(res)-1]
        hostport = '{0}:{1}'.format(host, port)
        connect  = 'tcp://{0}'.format(hostport)

        ctx = zmq.Context()
        #self.socket = ctx.socket(zmq.REQ)
        self.socket = ctx.socket(zmq.SUB)
        self.socket.connect(connect)
        
        # Subscribe to tester
        topicfilter = 'tester'
        #socket.subscribe(topicfilter) # only for SUB
        self.socket.setsockopt(zmq.SUBSCRIBE, topicfilter)
        
        #df = p_DataFrame()
        
        self.hdr = ['EUR','USD','GBP','AUD','NZD','CAD','MXN']
        self.indr = []
        
        #self.hdr0 = [[21,31], [34, 45], [50, 59], [65, 73]]
        #self.dmaps = dict(zip(self.hdr, self.hdr0))

        t0 = threading.Thread(target=self.getMouse)
        t0.daemon = False
        t0.start()
        
        from oandaq import OandaQ   
        self.oq = OandaQ(selectOandaAccount=1)
        
        self.activated = 0
        
    #@profile
    def renderArray(self, a, index=None, columns=None):
        lsnlen = []
        for i in a:
            lsnlen.append(len(i))
        lsnlenmax = n.max(lsnlen)
        
        self.indr = index
        
        # index
        for j in xrange(len(index)):
            stdscr.addstr(j+3, 0+10, '{:^8}'.format(index[j]), curses.color_pair(1))

        # header
        for j in xrange(len(columns)):
            stdscr.addstr(1, (j*lsnlenmax)+(j*8)+20, '{:^25}'.format(columns[j]), curses.color_pair(1))
            
        # body
        for i in xrange(len(a)):
            for j in xrange(len(a[0])):
                #curses.A_REVERSE
                #stdscr.addstr(i+3, (j*lsnlenmax)+(j*8)+20, '{:>25}'.format('%1.6f' % a[i][j]), curses.color_pair(2))
                vals = a[i][j].split(' ')
                if float(vals[1]) > 0:
                    color_pair = 2
                elif float(vals[1]) < 0:
                    color_pair = 3
                else:
                    color_pair = 4
                
                #if float(vals[1]) > 0 or float(vals[1]) < 0:
                stdscr.addstr(i+3, (j*lsnlenmax)+(j*8)+20, '{:>25}'.format(a[i][j]), curses.color_pair(color_pair))
        stdscr.refresh()
        #time.sleep(0.01)
    """
    for i in xrange(100):
        cn = 8
        a = n.random.randn(40,cn)
        zc.renderArray(a)
    """
    
    def getCurrencyCodes(self, ps):
        return list(p_DataFrame(ps).drop_duplicates().transpose().get_values()[0])
    
    def currencyPairs2CurrencyCodes(self, pairs):
        ps = []
        for i in pairs:#.split(','):
            pr = i.split('_')
            ps.append(pr[0])
            ps.append(pr[1])
        return ps

    def pivotTicksToCurrencyCode(self, pairs, df):
        ps    = self.currencyPairs2CurrencyCodes(pairs)
        currs = self.getCurrencyCodes(ps)
        #print currs
        lcurrs = len(currs)
        lc = n.zeros(lcurrs*lcurrs).reshape(lcurrs, lcurrs)
        di = df.to_dict()
        kdi = di.keys()
        vdi = di.values()
        for i in kdi:
            isp = i.split('_')
            #print vdi
            #print '{0} {1} {2}'.format(di[i], i, isp)
            lcurrs = dict(zip(currs, xrange(len(currs))))
            lc[lcurrs[isp[1]]][lcurrs[isp[0]]] = di[i]
        dfm = p_DataFrame(lc, index=currs, columns=currs)
        return dfm
    
    def getLast(self, df, depth, num=None, instruments=None):
        if num != None:
            df=df.ix[len(df.index)-1-num, :]
        else:
            try:
                df=df.ix[depth-1, :]
            except:
                df=df.ix[depth-2, :]
                
        if type(instruments) != type(None):
            instruments['p'] = n.zeros(len(instruments.index))
            df = df.combine_first(instruments['p'])
        
        #print df
        return df
    
    #@profile
    def processDfm(self, dfm):
        #try: dfm.ix['total', 'AUD CAD NZD CHF EUR GBP USD'.split(' ')] = n.sum(dfm.ix[:, 'AUD CAD NZD CHF EUR GBP USD'.split(' ')])
        #except: ''
        try:
            dfm = dfm.convert_objects(convert_numeric=True)
            dfu = dfm.ix[:, self.hdr]
            #print dfu[(dfu.values) > 0]
            dfu = dfu.sort()#.get_values()
            
            #absolutely_unused_variable = os.system('clear')  # on linux / os x
            #rows, columns = os.popen('stty size', 'r').read().split()
            #for i in xrange(int(rows)+len(dfu.index)): print ''
            #print dfu
            
            #print dfm.ix[:, 'AUD CAD NZD CHF EUR GBP USD'.split(' ')]
            #print dfm[(dfm.values < 5)] #.any(1)
            #print dfm[(dfm.values < 1.5).any(1)].ix[:, 'AUD CAD NZD CHF EUR GBP USD'.split(' ')]
            #print dfm.ix[:,(dfm.ix[:, 'AUD CAD NZD CHF EUR GBP USD'.split(' ')] < 10)]
        except:
            ''
        #print n.sum(dfm.ix[:, 'AUD CAD NZD CHF EUR GBP USD'.split(' ')])
        #print dfm.ix[:, ['USD']]
        #dfu = dfm.ix[['USD'], :].transpose()
        #dfu = dfu.convert_objects(convert_numeric=True)
        
        #print dfu
        #print (dfu['USD'] != int(0))
        return dfu
    
    #@profile
    def currencyMatrix(self, df=None, mode=None, mong=None, depth=None, verbose=False, instruments=None):
        #from oandaq import OandaQ
        #oq = OandaQ()
        #pairs = ",".join(list(n.array(p_DataFrame(oq.oandaConnection().get_instruments(oq.aid)['instruments']).ix[:,'instrument'].get_values(), dtype=str)))
        
        if verbose == True:
            stdscr.addstr(1, 120, '{:^12}'.format('mode:{0}'.format(mode)), curses.color_pair(1))
            stdscr.addstr(2, 120, '{:^12}'.format('depth:{0}'.format(depth)), curses.color_pair(1))
            stdscr.addstr(3, 120, '{:^12}'.format('mong:{0}'.format(len(mong[mode+'s']))), curses.color_pair(1))
            #self.renderArray(dfu.sort().get_values(), index=dfu.index, columns=dfu.columns)
                
        ######
        
        if mode == 'avg':
            #print mong['avgs'].keys()
            #for i in mong['avgs'].keys():
            #    print len(mong['avgs'][i])
            #    print mong['avgs'][i]
            df = p_DataFrame(mong['avgs'])
            #print df
            for i in df.columns:
                #print df[i]
                #a = list(n.array(df[i], dtype=float))
                #a = filter(lambda x: x != 0, a)
                #print a
                #a = normalizeme(a)
                #a = sigmoidme(a)
                #a = n.divide(1, a) # only for USD as base currency
                #print a
                #b = a#[1,2,3]
                #df.ix[len(df)-len(b):len(df)-1, i] = b
                #df[i] = normalizeme(n.array(df[i], dtype=float))
                #df[i] = sigmoidme(n.array(df[i], dtype=float))
                ''
            """
            df = p_DataFrame()
            for i in avgs:
                #print i
                #print avgs[i]
                df[i] = [avgs[i]]
                print df[i]
                #df[i] = normalizeme(n.array(df[i], dtype=float))
                #df[i] = sigmoidme(n.array(df[i], dtype=float))
            """
        
        df = p_DataFrame(mong[mode+'s'])

        #print df  
        #print depth
        df0 = self.getLast(df, depth, instruments=instruments)
        df1 = self.getLast(df, depth, num=1, instruments=instruments)

        #from oandaq import OandaQ
        #oq = OandaQ()
        #pairs = ",".join(list(n.array(p_DataFrame(oq.oandaConnection().get_instruments(oq.aid)['instruments']).ix[:,'instrument'].get_values(), dtype=str)))
        #pairs = list(df0.ix[depth-1, :].index)
        dfm0 = self.pivotTicksToCurrencyCode(list(df0.index), df0)
        dfm1 = self.pivotTicksToCurrencyCode(list(df1.index), df1)
        #print dfm0#.get_values()
        
        dfu0 = self.processDfm(dfm0)
        dfu1 = self.processDfm(dfm1)
        #print dfu0.get_values()

        a0 = dfu0.get_values()
        a1 = dfu1.get_values()
        #print a0.shape
        #print a1.shape
        dfmd = n.array([a0, a1])
        #print dfmd
        s = n.core.defchararray.add(n.array(dfmd[0], dtype=n.string0), ' ')
        s = n.core.defchararray.add(s , n.array(n.around(dfmd[0]-dfmd[1], decimals=6), dtype=n.string0))
        s = n.core.defchararray.add(s, ' ')
        s = n.core.defchararray.add(s , n.array(n.around((dfmd[0]-dfmd[1])/dfmd[0]*1000, decimals=1), dtype=n.string0))
        dfum = p_DataFrame(s, index=dfu0.index, columns=dfu0.columns)

        #self.renderArray(dfu0.get_values(), index=dfu0.index, columns=dfu0.columns)
        dfum = dfum.sort()
        self.renderArray(dfum.get_values(), index=dfum.index, columns=dfum.columns)
    
    #@profile
    def client(self, mode='avg'):
        de = deque()
        #bids = deque()
        pairs = {}
        bids = {}
        asks = {}
        avgs = {}
        spreads = {}
        from pandas import read_csv as p_read_csv
	
        from oandaq import OandaQ
        oq = OandaQ()
        oq.generateInstruments()
        instruments = p_read_csv('data/oanda/cache/instruments.csv').set_index('instrument')
    
        depth = 20
        c = 0
        while True:
            #self.socket.send('test client') # only for REQ
            data = self.socket.recv(0)
            data = data.split(' ')
            data = ' '.join(data[1:]) # fixes the previous space split
            data = data.split(',')
            ts = str(data[4][0:10])+str(data[3][19:26])
            #de.append(ts)
            
            pair = data[0]
            # append data into pairs
            def _uwe(name, ddd, pair, data):
                try:
                    ddd[pair]['bids'].append(data[1])
                except:
                    try:
                        ddd[pair]['bids'] = deque()
                        ddd[pair]['bids'].append(data[1])
                    except:
                        ddd[pair] = {}
                        ddd[pair]['bids'] = deque()
                        ddd[pair]['bids'].append(data[1])
                return ddd

            def _uwe2(ddd, pair, data):
                try:
                    ddd[pair].append(data)
                except:
                    #ddd[pair] = deque()
                    ddd[pair] = deque([0]*depth)
                    ddd[pair].append(data)
                return ddd
                
            pairs = _uwe('bids', pairs, pair, data)
            pairs = _uwe('asks', pairs, pair, data)
            pairs = _uwe('avgs', pairs, pair, data)
            pairs = _uwe('spreads', pairs, pair, data)
            
            mong = {'bids':bids, 'asks':asks, 'avgs':avgs, 'spreads':spreads}
            ########
            # bids
            bids = _uwe2(bids, pair, data[1])
            
            if len(pairs[pair]['bids']) >= depth: pairs[pair]['bids'].popleft()
            #df = normalizeme(n.array(pairs[pair]['bids'], dtype=float))
            #df = sigmoidme(n.array(bids, dtype=float))
    
            if len(bids[pair]) >= depth: bids[pair].popleft()
            #df = normalizeme(n.array(bids[pair], dtype=float))
            #df = sigmoidme(n.array(bids, dtype=float))
            
            #print pair
            #print list(df)
            #print pairs.keys()
            df = p_DataFrame(bids)
            for i in df.columns:
                df[i] = normalizeme(n.array(df[i], dtype=float))
                df[i] = sigmoidme(n.array(df[i], dtype=float))
            #df = normalizeme(n.array(df, dtype=float))
            #df[]
            #print df.ix[depth-1, :]#.bfill().ffill()#.transpose()
            #print 'plot'
            
            #print list(df.ix[depth-1, :].index)
            #self.currencyMatrix(df=df, instruments=instruments)
            ########
            # asks
            asks = _uwe2(asks, pair, data[1])
            
            if len(asks[pair]) >= depth: asks[pair].popleft()
            df = p_DataFrame(asks)
            #for i in df.columns:
            #    df[i] = normalizeme(n.array(df[i], dtype=float))
            #    df[i] = sigmoidme(n.array(df[i], dtype=float))
            #self.currencyMatrix(df=df, instruments=instruments)
            ########
            # avgs
            try: # catch exceptions from commodity instruments
                avg = abs( (float(data[1]) + float(data[2]))/2 )
            except:
                continue
            avgs = _uwe2(avgs, pair, avg)
            
            if len(avgs[pair]) >= depth:
                #print 'len avg pair:{0} depth:{1}'.format(len(avgs[pair]), depth)
                avgs[pair].popleft()
                #print len(avgs[pair])
            df = p_DataFrame(avgs)
    
            if mode == 'avg':
                self.currencyMatrix(df=df, mode=mode, mong=mong, depth=depth, instruments=instruments)
            ########
            # spreads
            try: # catch exceptions from commodity instruments
                spread = abs(float(data[1]) - float(data[2])) / instruments.ix[pair, 'pip']
            except:
                continue
            spreads = _uwe2(spreads, pair, spread)
            
            if len(spreads[pair]) >= depth: spreads[pair].popleft()
            df = p_DataFrame(spreads)
            #for i in df.columns:
            #    df[i] = normalizeme(n.array(df[i], dtype=float))
            #    df[i] = sigmoidme(n.array(df[i], dtype=float))
            if mode == 'spread':
                self.currencyMatrix(df=df, mode=mode, mong=mong, depth=depth, instruments=instruments)
            ########
            #print de
            #print list(de)
            de.append(data)
            if len(de) >= depth: de.popleft()
    
            """
            #df = n_array(list(de))
            #print pivot(df, )
            df = p_DataFrame(list(de))
            
            #df = df.pivot(4, 3, 2)#.bfill().ffill()
            #df = df.convert_objects(convert_numeric=True)
            #df = df.drop_duplicates()
            try:
                #df = df.pivot(3, 0, 1)#.bfill().ffill()
                #df = df.describe().transpose().sort('count', ascending=False)
                print df.ix[:, [3]]
            except:
                ''
            #print prevData
            #print data
            print
            #dfd = p_DataFrame([prevData, data])
            #print dfd#.pivot(4, 3, 2)
            #print dfd.ix[[0,2,3,4], :].transpose()
            #print df.combine_first()
            
            
            c += 1
            """
            #time.sleep(0.1)

    def getMouse(self):
        #stdscr.addstr("This is a Sample Curses Script\n\n") 
        marginDebug = 135
        self.risk   = 1
        stop        = 20
        while True: 
           event = stdscr.getch() 
           if event == ord("q"): 
               import sys
               sys.exit()
               break 
           if event == ord('1'):
                   self.risk = 1
                   stdscr.addstr(7,marginDebug,'risk: {0}'.format(self.risk))
           if event == ord('2'):
                   self.risk = 2
                   stdscr.addstr(7,marginDebug,'risk: {0}'.format(self.risk))
           if event == ord('3'):
                   self.risk = 3
                   stdscr.addstr(7,marginDebug,'risk: {0}'.format(self.risk))
           if event == ord('4'):
                   self.risk = 4
                   stdscr.addstr(7,marginDebug,'risk: {0}'.format(self.risk))
           if event == ord('5'):
                   self.risk = 5
                   stdscr.addstr(7,marginDebug,'risk: {0}'.format(self.risk))
           if event == ord('6'):
                   self.risk = 6
                   stdscr.addstr(7,marginDebug,'risk: {0}'.format(self.risk))
           if event == ord('7'):
                   self.risk = 7
                   stdscr.addstr(7,marginDebug,'risk: {0}'.format(self.risk))
           if event == ord('8'):
                   self.risk = 8
                   stdscr.addstr(7,marginDebug,'risk: {0}'.format(self.risk))
           if event == ord('9'): 
                   self.risk = 9
                   stdscr.addstr(7,marginDebug,'risk: {0}'.format(self.risk))
           if event == ord("b") or event == ord("w"):  # w alias for buy
                   self.activated = 1
                   self.side = 'b'
                   stdscr.addstr(4,marginDebug,'activated: {0}'.format(self.activated)) # for debugging
                   stdscr.addstr(5,marginDebug,'side: {0}'.format(self.side))
           if event == ord("s"): 
                   self.activated = 1
                   self.side = 's'
                   stdscr.addstr(4,marginDebug,'activated: {0}'.format(self.activated))
                   stdscr.addstr(5,marginDebug,'side: {0}'.format(self.side))
                   stdscr.refresh()
           if event == curses.KEY_MOUSE:
               mm = curses.getmouse()               
               mip = self.getp(mm[1], mm[2])
               try:
                   pair = '{0}_{1}'.format(mip[0], mip[1])
                   #self.oq.buy(risk, stop, instrument='EUR_USD', tp=None, nostoploss=False)
                   if self.activated == 1 and self.side == 'b':
                       self.oq.buy(self.risk, stop, instrument=pair, verbose=False)
                       stdscr.addstr(6,marginDebug,'message: buy {0} {1} {2}'.format(self.risk, stop, pair))
                   if self.activated == 1 and self.side == 's':
                       self.oq.sell(self.risk, stop, instrument=pair, verbose=False)
                       stdscr.addstr(6,marginDebug,'message: sell {0} {1} {2}'.format(self.risk, stop, pair))
                   #stdscr.getstr()
                   #stdscr.addstr(mm[2],mm[1],'{2}_{3}'.format(mm[1], mm[2], mip[0], mip[1]))
                   stdscr.addstr(mm[2],mm[1],'{0}_{1}'.format(mm[1], mm[2])) # for debugging
                   stdscr.addstr(3,marginDebug,'buy or sell {2}? (b/s): '.format(mm[1], mm[2], pair)) # for debugging
                   #stdscr.addstr(6,marginDebug,'message: {0}'.format(msg)) # for debugging
               except Exception as e:
                   print e
                   ''
               stdscr.refresh()

    """
    octave
    a = [21 31; 34 45; 50 59; 65 72]
    ar = reshape(a', 1, 8)
    x = 57
    [max(ar(ar < x)) min(ar(x < ar))]
    """
    def getp(self, x, y):
        #x = 57
        #a   = n.matrix('21 31; 34 45; 50 59; 65 73; 80 90; 95 105').A
        a   = n.matrix('20 35; 37 50; 51 67; 71 79; 82 96; 97 109; 114 129').A
        ar  = a.reshape(1,a.shape[0]*a.shape[1])[0]
        
        try:
            res = [max(ar[ar < x]), min(ar[x < ar])]
            df = p_DataFrame(a, index=self.hdr)
            df['in'] = df.index
            df0 = df.set_index(0)
            return [df0.ix[res[0], 'in'], self.indr[y-3]]
        except:
            return ''
            
stdscr = curses.initscr()

curses.start_color()
curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)

curses.noecho()
curses.cbreak()
stdscr.keypad(1)
# source: http://stackoverflow.com/questions/18837836/how-can-i-hide-the-cursor-in-ncurses
curses.curs_set(0)
curses.mousemask(1)

mode = sys.argv[2]
zc = ZMQClient()

try:
    zc.client(mode=mode)
except KeyboardInterrupt as e:
    print ''
except Exception as e:
    curses.nocbreak(); stdscr.keypad(0); curses.echo()
    curses.endwin()

curses.nocbreak(); 
stdscr.keypad(0); 
curses.echo()
curses.endwin()

#from pandas import read_csv as p_read_csv
#instruments = p_read_csv('data/oanda/cache/instruments.csv').set_index('instrument')
#instruments

#from pandas import read_csv as p_read_csv
#df = p_read_csv('data/oanda/cache/instruments.csv')
#pairs = list(df.ix[:, 'instrument'])
#currencyMatrix(pairs)
