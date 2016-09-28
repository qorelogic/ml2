#!/usr/bin/env python
import pandas as p
import pymongo as mong
import datetime, calendar
import ujson
import oandapy

def logAccounts(selAcc=0):
    ###
    co = p.read_csv('/mldev/bin/datafeeds/config.csv', header=None)
    co.ix[selAcc,4] = 'oanda2'
    env2=co.ix[selAcc,1]
    access_token2=co.ix[selAcc,2]
    oanda2 = oandapy.API(environment=env2, access_token=access_token2)
    ###
    
    dfm2 = p.DataFrame()
    acc = oanda2.get_accounts()['accounts']
    for i in acc:
        accid = i['accountId']
        res = oanda2.get_account(accid)
        df = p.DataFrame(res, index=[accid])
        dfm2 = dfm2.combine_first(df)
    ds = datetime.datetime.utcnow()
    ts = calendar.timegm(ds.utctimetuple())
    ts = ts + float(ds.microsecond) / 1000000
    di = {}
    di.update({'user':co.ix[selAcc,0]})
    di.update({'utctime':ts})
    #if dfm2.get_values():
    data = dfm2.to_dict()
    di.update({'data':ujson.dumps(data)})
    #print p.DataFrame(di['data'])
    print di
    
    mongo = mong.MongoClient()
    try:
        mongo.ql.broker_oanda_accounts.insert(di)
    except Exception as e:
        print e
    mongo.close()

logAccounts(selAcc=0)
logAccounts(selAcc=1)
