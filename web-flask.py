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

@app.route("/")
@app.route("/hello")
@app.route('/hello/<name>')
def hello(name=None):
    #an = Feeder()
    #an.fireupThreads()  
    
    df = p.read_csv(hdir+'/airports.dat', header=None)
    #print df.ix[0, :].get_values()
    data = df.ix[:,[6,7]].get_values()
    #print data 
    #print df
    #gmaps.heatmap?
    #gmaps.heatmap(data, height='400px', width='980px', max_intensity=2, point_radius=8)
    jdata = j.dumps(data.tolist())
    
    #data = gmaps.datasets.load_dataset('taxi_rides')
    #maps = gmaps.heatmap(data)
    #gmaps.display(maps)

    return render_template('hello.html', name=name, data=jdata)    

if __name__ == "__main__":
    app.debug = True
    app.run(debug=True, host='0.0.0.0', port=80)
