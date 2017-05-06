
import pandas as p
from qoreliquid import pf

# bitmex
import drest
#api = drest.API('http://socket.coincap.io/')
api = drest.API('https://www.bitmex.com/api/v1')
#response = api.make_request('GET', '/trade?count=100&reverse=false')
#response = api.make_request('GET', '/instrument')
response = api.make_request('GET', '/instrument/indices')
#print response.data

df = p.DataFrame(response.data)#.transpose()
pf(df)

