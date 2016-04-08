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


def reccInit(widget=None, args=None):
    # option to change the port number from default 5555
    #argv1 = '104.207.135.67:5555'
    argv1 = '127.0.0.1:5557'
    #argv1 = sys.argv[1]
    try:
        hostport = argv1
    except:
        hostport = 5555
    
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
    topicfilter = 'tester'
    #socket.subscribe(topicfilter) # only for SUB
    socket.setsockopt(zmq.SUBSCRIBE, topicfilter)
    
    return socket
    
    
def recc(widget=None, args=None):
    
    socket = reccInit(widget=widget, args=args)

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

    wh = 30
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
    
    cur_x = 10
    cur_y = 10
    
    socket = reccInit(args=args)

    while True:
        data = socket.recv(0)
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
        li = n.random.randn(cn)*10
        li = n.abs(li)
        li = list(n.array(li, dtype=int))
        #fp.write("%s\n" % j.dumps(li))
        #fill(window, ' ')
        dii = dict(zip(data[1], data[0]))
        #window.addstr(1, 1, "%s" % (dii), curses.color_pair(RED_TEXT))
        window.refresh()
        #window.getch()
        #window.touchwin()
        #window.refresh()
        #for i in range(len(data[0])):
        for i in range(len(li)):
            #am = float(li[i]) / n.max(li) * 100
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
                stw[i].box()
                try:
                    if am > 0:
                        col = GREEN_TEXT
                    else:
                        col = RED_TEXT
                    am = abs(float(am))
                    stw[i].addstr(1, 1, "%s" % (data[1][i]), curses.color_pair(col))
                    stw[i].addstr(2, 1, "%s:%.0f" % (i, am), curses.color_pair(col))
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
    parser.add_argument("-nc", help="ncurses Version", action="store_true")
    parser.add_argument("-mtc", help="mongo ticks count", action="store_true")
    parser.add_argument("-v", '--verbose', help="ncurses Version", action="store_true")
    #parser.add_argument("-c", '--connect', help="connect, v=Vultr", action="store_true")
    #parser.add_argument("-n", "-num", "--num", help="c.getNodes()")

    args = parser.parse_args()

    if args.mtc:

        socket = reccInit(args=args)
    
        while True:
            data = socket.recv(0)
            data = data[7:]
            print data
        
        
    if args.nc:


        import curses
        try:
            renderNcurses()
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
