# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created: Tue Mar 22 00:23:21 2016
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

import pandas as p
import numpy as n
import zmq

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
    res = list(res)
    #print p.DataFrame(dict(zip(xs, ys)), index=[0]).transpose().tail(41)
    print p.DataFrame(res)#.transpose()#.tail(41)
    print len(res)
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
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 10, 631, 431))
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

if __name__ == "__main__":
    import sys
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
    
    def recc(widget):
        # option to change the port number from default 5555
        #argv1 = '104.207.135.67:5555'
        argv1 = '127.0.0.1:5555'
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
    
        while True:
            data = socket.recv(0)
            res = data[7:].split(',')
            res = n.array(res, dtype=n.float)
            widget.emit(QtCore.SIGNAL('test123'), res)

    
    import threading
    t0 = threading.Thread(target=recc, args=[MainWindow])
    t0.daemon = False
    t0.start()
    
    MainWindow.show()
    sys.exit(app.exec_())
