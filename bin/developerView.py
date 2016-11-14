# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

import flask
from flask import Flask, render_template, url_for
import json as j
import os

app = flask.Flask(__name__)
#app = flask.Flask(__name__, static_folder='/mldev/screenshots/developerLogs/screen/qore2/')

@app.route('/')
def test():
    #cmd = 'ls /mldev/screenshots/developerLogs/screen/qore2/*png | perl -pe "s/.+\///g" 2> /dev/null'
    #res = os.popen(cmd).read().strip().split('\n')#[0]
    res = timestamps02()
    print res
    bu = ''
    meta = {}
    for i in res:
        meta.update({'title':i})
        meta.update({'title2':i})        
        #liquid-screenshot-qore2-1478885822.png
        #bu += '<img src="file://%s" /><br />\n' % i
        bu += '<img src="liquid-screenshot-qore2-1478885822.png" /><br />\n' #% i
        break
    #return '\n'.join(res)
    #return bu
    return render_template('developerView.html', mess=res[0:200], meta=meta)
    #return 'everything is running\n'

@app.route('/rome2rio')
def rome2rio():
	import urllib2
	#url = 'http://<server>/api/1.2/xml/Autocomplete?key=<key>&query=cinque'
	url = 'http://free.rome2rio.com/api/1.2/json/Search?key=7L3e3oOO&oName=London&dName=Paris'
	#url = 'http://google.com'
	response = urllib2.urlopen(url)
	html = response.read()
	ret = j.loads(html)
	#print ret
	return html

def timestamps01():
    import re
    import pandas as p
    import numpy as n
    #import matplotlib.pylab as plt
    cmd = 'ls /mldev/screenshots/developerLogs/screen/qore2/*png | perl -pe "s/.+\///g" 2> /dev/null'
    res = os.popen(cmd).read().strip().split('\n')#[0]
    df = p.DataFrame(res)
    #for i in xrange(len(res)):
    #	gr = re.match(re.compile(r'(.+-)([\d]+)(.*)'), res[i]).groups()
    #	#print gr
    #	print gr[1]
    df[1] = map(lambda x: re.match(re.compile(r'(.+-)([\d]+)(.*)'), x).groups()[1], res)
    df = df.convert_objects(convert_numeric=True)
    #df[1].plot()
    #plt.show()
    df = df.sort(1)
    #gdf = df.groupby(1)
    #print gdf.describe()
    
    print df[1]
    
    df = p.DataFrame([n.min(df[1]), n.max(df[1])], index=['min', 'max']).transpose()
    df['diff'] = df['max']-df['min']    
    print df
    

def timestamps02(verbose=False):
    import re, os
    import pandas as p
    import numpy as n
    import datetime as dd
    
    # 01
    #import matplotlib.pylab as plt
    cmd = 'ls /mldev/screenshots/developerLogs/screen/qore2/*png | perl -pe "s/.+\///g" 2> /dev/null'
    res = os.popen(cmd).read().strip().split('\n')#[0]
    df = p.DataFrame(res)
    #for i in xrange(len(res)):
    #	gr = re.match(re.compile(r'(.+-)([\d]+)(.*)'), res[i]).groups()
    #	#print gr
    #	print gr[1]
    df[1] = map(lambda x: re.match(re.compile(r'(.+-)([\d]+)(.*)'), x).groups()[1], res)
    df[1] = p.to_numeric(df[1])
    #df[1].plot()
    #plt.show()
    df = df.sort_values(by=1)
    #df[2] = map(lambda x: dd.datetime.fromtimestamp(x), df[1])
    #df[3] = map(lambda x: dd.datetime.fromtimestamp(x).second, df[1])
    df[4] = map(lambda x: dd.datetime.fromtimestamp(x).minute, df[1])
    df['m5'] = df[4] % 5
    df['m10'] = df[4] % 10
    df['m60'] = df[4] % 60
    
    #gdf = df.groupby(1)
    #print gdf.describe()
    
    dfs = p.DataFrame([n.min(df[1]), n.max(df[1])], index=['min', 'max']).transpose()
    dfs['diff'] = dfs['max']-dfs['min']    
    #print dfs#.set_index(0)
    
    df = df.set_index(1)
    #print df.tail(10)
    
    # 02
    ld = range(dfs.ix[0,'min'], dfs.ix[0,'max'])
    dfr = p.DataFrame([n.nan]*len(ld), index=ld)#.set_index(0)
    dfr['minute'] = map(lambda x: dd.datetime.fromtimestamp(x).minute, dfr.index)
    dfr['m5']   = dfr['minute'] % 5
    dfr['m10']  = dfr['minute'] % 10
    dfr['m60']  = dfr['minute'] % 60
    #for i in [10, 10, 60]:
    #    dfr['m%s'%i] = dfr['minute'] % i
    #print dfr[dfr['m10'] == 0].tail(10)
    
    # 03
    dfr1 = df.combine_first(dfr).sort_index().ffill().bfill()
    with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
        if verbose: print dfr1.tail(30)
    res = dfr1[dfr1['m10'] == 0]#.tail(20)
    return list(res.ix[:,0].get_values())
    	
    #print '\n'.join(res)

if __name__ == "__main__":
	app.config['DEBUG'] = True
	app.run()
	#timestamps01()
      #print timestamps02()

