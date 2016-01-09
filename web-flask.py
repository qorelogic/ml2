#!/usr/bin/python

import sys
def defp(pt):
    try:    sys.path.index(pt)
    except: sys.path.append(pt)
defp('bin')
#defp('/mldev/bin')
#defp('/mldev/lib/oanda/oandapy')

from flask import Flask
from flask import render_template

#from datafeeds.analyzer import Feeder
#from qore import *
#from qoreliquid import *
#import threading

import pandas as p
#import gmaps
import ujson as j

#hdir = '/mldev/lib/crawlers/transport/jpatokal_openflights.github.py.git/data'
hdir = 'lib/crawlers/transport/jpatokal_openflights.github.py.git/data'

app = Flask(__name__)

def getRoutes():
    
    dfa = p.read_csv(hdir+'/airports.dat', header=None)
    dfaa = dfa.ix[:,4]
    ldfaa = list(dfaa)
    
    dfr = p.read_csv(hdir+'/routes.dat', header=None)
    airportCodesFrom = list(dfr.ix[:, 2])
    airportCodesTo   = list(dfr.ix[:, 4])
    data = []
    #for i in xrange(len(dfr.index)):
    for i in dfr.index:
        try:
            airportCodeFrom = ldfaa.index(airportCodesFrom[i])
            airportCodeTo   = ldfaa.index(airportCodesTo[i])
            #print '{0} {1}'.format(dfa.ix[airportCodeFrom, 6], dfa.ix[airportCodeFrom, 7])
            #print '{0} {1}'.format(dfa.ix[airportCodeTo, 6], dfa.ix[airportCodeTo, 7])
            data.append([[dfa.ix[airportCodeFrom, 6], dfa.ix[airportCodeFrom, 7]], [dfa.ix[airportCodeTo, 6], dfa.ix[airportCodeTo, 7]]])
        except Exception as e:
            #print e
            ''
    #print p.DataFrame(data)
    return data
  
@app.route("/")
@app.route("/hello")
@app.route('/hello/<name>')
def hello(name=None):
    #an = Feeder()
    #an.fireupThreads()  
    
    dfa = p.read_csv(hdir+'/airports.dat', header=None)
    dfr = p.read_csv(hdir+'/routes.dat', header=None)
    #print dfa.ix[0, :].get_values()
    airports = dfa.ix[:,[6,7]].get_values()
    #print airports 
    #print dfa
    #gmaps.heatmap?
    #gmaps.heatmap(airports, height='400px', width='980px', max_intensity=2, point_radius=8)
    airports = j.dumps(airports.tolist())
    routes   = getRoutes()
    
    #data = gmaps.datasets.load_dataset('taxi_rides')
    #maps = gmaps.heatmap(data)
    #gmaps.display(maps)

    return render_template('hello.html', name=name, airports=airports, routes=routes)    

if __name__ == "__main__":
    app.debug = True
    app.run(debug=False, host='0.0.0.0', port=80)
