# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import flask

app = flask.Flask(__name__)

@app.route('/')
def test():
    return 'everything is running'

#@app.route('/high/poverty/stastes')
#def high_poverty_states():
#    donors_choose_url = 'http://'

if __name__ == "__main__":
    app.run()

# <codecell>

import json as j
j.

# <codecell>

import urllib2
#url = 'http://<server>/api/1.2/xml/Autocomplete?key=<key>&query=cinque'
url = 'http://free.rome2rio.com/api/1.2/json/Search?key=7L3e3oOO&oName=London&dName=Paris'
#url = 'http://google.com'
response = urllib2.urlopen(url)
html = response.read()
ret = j.loads(html)
print ret[]

# <codecell>


