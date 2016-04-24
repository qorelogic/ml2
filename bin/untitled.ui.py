# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created: Tue Mar 22 00:23:21 2016
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

import pandas as p
import numpy as n
import ujson as u
import zmq
import sys

try:
    from PyQt4 import QtCore, QtGui
    
    # http://www.qtcentre.org/threads/53341-Qt4-designer-on-RPi-no-module-named-qwt_plot
    import PyQt4.Qwt5 as Qwt
    #from qwt_plot import QwtPlot
except Exception as e:
    ''
    
numPoints = 1000
xs = n.arange(numPoints)
ys = n.sin(3.14159*xs*10/numPoints) #this is our data

#@profile
def plotSomething(res):
    global ys
    index = list(res.index)
    res = res.transpose()
    res = n.array(res.get_values()[0], dtype=n.float)
    res = list(res)
    #print p.DataFrame(dict(zip(xs, ys)), index=[0]).transpose().tail(41)
    df = p.DataFrame(res, index=index)#.transpose()#.tail(41)
    df['ar'] = range(0, len(df.index))
    #print df
    #print len(res)
    xs = n.arange(len(res))
    #print len(xs)
    #print len(ys)
    #print dict(zip(xs, ys))

    #ys = n.roll(ys,-1)
    #c.setData(xs, ys)
    c.setData(xs, res)
    #print '%s: %s' % (xs, ys)

    uiplot.qwtPlot.replot()

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s
except Exception as e:
    print e
    

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)
except Exception as e:
    print e

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(640, 480)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 10, 511, 291))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.qwtPlot = Qwt.QwtPlot(self.horizontalLayoutWidget)
        self.qwtPlot.setObjectName(_fromUtf8("qwtPlot"))
        self.horizontalLayout.addWidget(self.qwtPlot)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 20))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))


def reccInit(widget=None, args=None, hostport='127.0.0.1:5555', topic = 'tester', verbose=True):

    #hostport = '104.207.135.67:5555'
    #hostport = '127.0.0.1:5557'
    print hostport
    
    try:
        res      = hostport.split(':')
    except:
        res = hostport
    host     = res[len(res)-2]
    if host == '': host = 'localhost'
    port     = res[len(res)-1]
    
    hostport = '{0}:{1}'.format(host, port)
    connect  = 'tcp://{0}'.format(hostport)

    ctx = zmq.Context()
    #self.socket = ctx.socket(zmq.REQ)
    socket = ctx.socket(zmq.SUB)
    socket.connect(connect)
    
    # Subscribe to tester
    topicfilter = topic
    #socket.subscribe(topicfilter) # only for SUB
    socket.setsockopt(zmq.SUBSCRIBE, topicfilter)
    
    if verbose == True:
        print 'subscribing to: %s, topic:%s' % (hostport, topicfilter)
    
    return socket
    
    
def recc(widget=None, args=None):
    
    socket = reccInit(widget=widget, args=args, hostport='127.0.0.1:5557', topic = 'tester')

    while True:
        data = socket.recv(0)
        data = data[7:]
        #print data
        data = u.loads(data)
        #print data
        res = p.DataFrame(data).transpose().set_index(1)
        #res = data[7:].split(',')
        try:
            if args.verbose:
                print 'test'
        except Exception as e:
            #print e
            ''
        if widget:
            widget.emit(QtCore.SIGNAL('test123'), res)

import curses
import numpy as n
#@profile
def renderNcurses():
    
    fp = open('/tmp/123.txt', 'a')
    
    #"""
    stdc = curses.initscr()
    
    if not curses.has_colors():
        curses.endwin()
        print "no colors"
        sys.exit()
    else:
        curses.start_color()
    
    #cw = curses.newwin()
    curses.noecho()    # don't echo the keys on the screen
    curses.cbreak()    # don't wait enter for input
    curses.curs_set(0) # don't show cursor.
    
    RED_TEXT = 1
    curses.init_pair(RED_TEXT, curses.COLOR_RED, curses.COLOR_BLACK)
    BLUE_TEXT = 2
    curses.init_pair(BLUE_TEXT, curses.COLOR_BLUE, curses.COLOR_BLACK)
    GREEN_TEXT = 3
    curses.init_pair(GREEN_TEXT, curses.COLOR_GREEN, curses.COLOR_BLACK)
    
    y, x = stdc.getmaxyx()
    wh = y
    window = curses.newwin(wh, 170, 0, 0)
    window.box()
    
    import ujson as j
    
    q1 = 7
    cn = 22
    stw = [0] * cn
    
    def fill(window, ch):
        y, x = window.getmaxyx()
        s = ch * (x - 1)
        for line in xrange(y):
            window.addstr(line, 0, s)
    #"""
    
    cur_x = 10
    cur_y = 10
    
    socket = reccInit(args=args, hostport='127.0.0.1:5558', topic = 'tester')

    #@profile
    def selectBars(currencies, pairs, delimiter=','):

        li = []
        for i in pairs.split(delimiter):
            li.append(i.split('_')[0])
            li.append(i.split('_')[1])
        li = li

        #print '-- currencies ---'
        #print currencies
        df = p.DataFrame(currencies, index=currencies)
        #print '-- li ---'
        #print li
        li0 = list(df.ix[li, :].transpose().get_values()[0])
        li0 = p.Series(li0).unique()
        df = p.DataFrame(currencies)
        df[1] = df.index
        df = df.set_index(0)
        df[0] = df.index
        #print '-- li0 ---'
        #print li0
        #print df
        #print '-- df.ix[li0, :] ---'
        df = df.convert_objects(convert_numeric=True)
        return df.ix[li0, :].sort(1)

    #data0 = u.loads(socket.recv(0)[7:])
    #print selectBars(data0[1], 'EUR_USD,AUD_USD,GBP_USD')#.ix[:, 1].get_values()
    #return

    while True:
        try:
            data = socket.recv(0)
        except zmq.error.ZMQError as e:
            continue
        data = data[7:]
        #print data
        data = u.loads(data)
        #print data
        ##res = p.DataFrame(data).transpose().set_index(1)
        
        try:
            window.addch(cur_y, cur_x, '@')
        except Exception as e:
            #fp.write("1 %s \n" % e)
            ''
        #fill(window, ' ')
        dii = dict(zip(data[1], data[0]))
        #window.addstr(1, 1, "%s" % (dii), curses.color_pair(RED_TEXT))
        window.refresh()
        #window.getch()
        #window.touchwin()
        #window.refresh()
        #for i in range(len(data[0])):
        
        #selectBars(data0[1], 'EUR_USD,AUD_USD,GBP_USD')

        # Check if screen was re-sized (True or False)
        resize = curses.is_term_resized(y, x)
        # Action in loop if resize is True:
        if resize is True:
            y, x = stdc.getmaxyx()
            wh = y
            #window.resize(wh, 170, 0, 0)
            window.resize(wh, x)
            stdc.clear()
            curses.resizeterm(y, x)
            stdc.refresh()
        window.addstr(1, 1, "y:%s" % (y), curses.color_pair(GREEN_TEXT))
        window.addstr(2, 1, "x:%s" % (x), curses.color_pair(GREEN_TEXT))
        window.addstr(3, 1, "resize:%s" % (resize), curses.color_pair(GREEN_TEXT))
        
        #for i in range(cn):
        sBars = selectBars(data[1], args.nc).ix[:, 1].get_values()
        for i in sBars:

            am = n.array(data[0], dtype=n.float)
            am = float(am[i]) / n.max(am) * 100
            #am = 10
            
            h  = int(float(wh-3) * abs(am) / 100 - 2)
            #fp.write("h:%s am:%s\n" % (h, am))
            #h = 5
            t = wh-(h+1)
            
            try:
                #del stw[i]
                #stw[i] = None
                #window.refresh()
                ''
            except Exception as e:
                #fp.write("11 %s \n" % e)
                ''
            
            try:
                fill(stw[i], ' ')
                stw[i].refresh()
            except Exception as e:
                #fp.write("2 %s \n" % e)
                ''
            try:
                stw[i] = curses.newwin(h, q1, t, i*(q1-1)+1)
                #stw[i] = curses.newwin(h, q1, t, sBars.index(i)*(q1-1)+1)
                stw[i].box()
                try:
                    if am > 0:
                        col = GREEN_TEXT
                    else:
                        col = RED_TEXT
                    am = abs(float(am))
                    stw[i].addstr(1, 1, "%s" % (data[1][i]), curses.color_pair(col))
                    stw[i].addstr(2, 1, "%s:%.0f" % (i, am), curses.color_pair(col))
                    stw[i].addstr(3, 1, "h:%s" % (h), curses.color_pair(col))
                    stw[i].addstr(4, 1, "t:%s" % (t), curses.color_pair(col))
                except Exception as e:
                    #fp.write("3 %s \n" % e)
                    ''
                stw[i].refresh()
                #del stw[i]
                #window.refresh()
            except Exception as e:
                #fp.write("2 %s \n" % e)
                ''
        #staticwin2 = curses.newwin(5, 10, 1, 12)
        #staticwin2.box()
        #staticwin2.box()
        #staticwin2.refresh()
    
        #window.touchwin()
        #window.refresh()
        
        """
        for i in range(len(stw)):
            try: del stw[i]
            except Exception as e:
                fp.write("5 %s \n" % e)
        """
        """
        inchar = window.getch()
        try: window.addch(cur_y, cur_x, ' ')
        except Exception as e:
            #fp.write("4 %s \n" % e)
            ''
        # W,A,S,D used to move around the @
        if inchar == ord('w'):
            cur_y -= 1
        elif inchar == ord('a'):
            cur_x -= 1
        elif inchar == ord('d'):
            cur_x += 1
        elif inchar == ord('s'):
            cur_y += 1
        elif inchar == ord('q'):
            break
        """
    
    #import time
    #time.sleep(1)
    
    curses.nocbreak(); 
    #stdscr.keypad(0); 
    curses.echo()
    #curses.endwin()
    
    curses.endwin()
    
    #fp.close()


if __name__ == "__main__":

    import argparse
    # source: https://docs.python.org/2/howto/argparse.html
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-qt", help="PyQt Version", action="store_true")
    parser.add_argument("-nc", help="ncurses ui arg eg. EUR_USD,AUD_USD,GBP_USD")
    parser.add_argument("-mtc", help="mongo ticks count", action="store_true")
    parser.add_argument("-v", '--verbose', help="ncurses Version", action="store_true")
    #parser.add_argument("-c", '--connect', help="connect, v=Vultr", action="store_true")
    #parser.add_argument("-n", "-num", "--num", help="c.getNodes()")

    args = parser.parse_args()

    if args.mtc:
        
        from collections import deque as d
        from matplotlib.pylab import *
        import time
        
        @profile
        def mtc():
            
            de = d()
            te = d()
            
            #topicfilter = 'avgs'
            socket = reccInit(args=args, hostport='127.0.0.1:5555', topic = 'count')
            while True:
                data = socket.recv(0)
                data = int(data[7:])
                ts = (time.time())
                #ts = str(ts)
                de.append(data)
                te.append(ts)
                depth = 100
                if len(de) > depth:
                    te.popleft()
                    de.popleft()
                #print n.array(te)
                #print n.array(de)
                df = n.array([te, de], n.float96).T
                #df[:, 2] = df[:,0]
                df = p.DataFrame(df)
                #try:
                #    ndiff = list(df.ix[1:(depth-1),0].get_values() - df.ix[0:(depth-2),0].get_values())
                #    df[3] = [0]*len(df.index)
                #    df.ix[1:depth-1, 3] = ndiff
                #except Exception as e:
                #    print e
                lni = len(df.index)
                #print lni
                if int(data) % depth == 0 and lni >= depth:
                    ndiff = df.diff()
                    #print ndiff.get_values()
                    df[2] = ndiff.get_values()[:,0]
                    df[3] = ndiff.get_values()[:,0].round(3)
                    df[4] = ndiff.get_values()[:,0].round(2)
                    dfg = df.groupby(4)
                    print dfg.describe()
                    with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
                        print df#.ix[:,:]
                    #n.set_printoptions(precision=4)
                    n.set_printoptions(formatter={'all':lambda x: str(x)})
                    #print n.array(df, dtype=n.float96)#.ix[:,:]
                    #plot(ndiff)
                    #show()
                    #break
                    
                
                #print p.DataFrame([n.array(de), n.array(te)], index=[n.array(te)])
        mtc()
        
        
    if args.nc:


        import curses
        try:
            renderNcurses()
        except zmq.error.ZMQError as e:
            curses.nocbreak(); 
            #stdscr.keypad(0); 
            curses.echo()
            #curses.endwin()
            curses.endwin()
            #print e
            from qore import QoreDebug
            qd = QoreDebug()
            qd.on()
            qd.printTraceBack()
        except KeyboardInterrupt as e:            
            curses.nocbreak(); 
            #stdscr.keypad(0); 
            curses.echo()
            #curses.endwin()
            curses.endwin()
            ''
            
            


    if args.qt:

        app = QtGui.QApplication(sys.argv)
        MainWindow = QtGui.QMainWindow()
        #ui = Ui_MainWindow()
        #ui.setupUi(MainWindow)
        uiplot = Ui_MainWindow()
        uiplot.setupUi(MainWindow)
        
        # set up the QwtPlot (pay attention!)
        # source: http://www.swharden.com/blog/
        c=Qwt.QwtPlotCurve()  #make a curve
        c.attach(uiplot.qwtPlot) #attach it to the qwtPlot object
        uiplot.timer = QtCore.QTimer() #start a timer (to call replot events)
        uiplot.timer.start(10.0) # emmitter #set the interval (in ms)
        #MainWindow.connect(uiplot.timer, QtCore.SIGNAL('timeout()'), plotSomething)
    
        MainWindow.connect(MainWindow, QtCore.SIGNAL('test123'), plotSomething)
        
        import threading
        t0 = threading.Thread(target=recc, args=[MainWindow])
        t0.daemon = False
        t0.start()
        
        MainWindow.show()
        sys.exit(app.exec_())

    sys.exit()
