#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 17:18:27 2015

@author: qore2
"""

from qore import *
import numpy as n

class LocalBitcoins:

    def __init__(self):
        self.USD_in_ARS = 14.66

    def localbitcoinsOrderbook(self, currency='USD'):
        #from qore import *
        orderbook = fetchURL('https://localbitcoins.com/bitcoincharts/{0}/orderbook.json'.format(currency))
        #print orderbook
        asks = p.DataFrame(orderbook['asks'])
        bids = p.DataFrame(orderbook['bids'])

        #%pylab inline
        plot(bids.ix[:,0])
        plot(asks.ix[:,0])

        print bids#.sort(0, ascending=True)
        print asks#.sort(0, ascending=True)

    def localbitcoinsTrades(self, currency='USD'):
        trades = fetchURL('https://localbitcoins.com/bitcoincharts/{0}/trades.json'.format(currency))
        """
        asks = p.DataFrame(orderbook['asks'])
        bids = p.DataFrame(orderbook['bids'])

        #%pylab inline
        plot(bids.ix[:,0])
        plot(asks.ix[:,0])

        print bids#.sort(0, ascending=True)
        print asks#.sort(0, ascending=True)   
        """
        df = p.DataFrame(trades)
        df = df.convert_objects(convert_numeric=True)
        df['p'] = df.ix[:, 'amount'] * df.ix[:, 'price']
        print df.sort('p')

    def localbitcoinsPublicAds(self, currency='USD', adtype='buy'):
        #from qore import *

        res = fetchURL('https://localbitcoins.com/{1}-bitcoins-online/{0}/.json'.format(currency, adtype))
        df = p.DataFrame()
        for i in res['data']['ad_list']:
            data = i['data']
            #print i
            #df = p.DataFrame(i['data']).transpose()
            #print df.ix[['temp_price','temp_price_usd'], 'username']
            #print data
            df = df.combine_first(p.DataFrame(data, index=[data['ad_id']]))
            #.transpose()
        df = df.convert_objects(convert_numeric=True)
        df['p']  = df.ix[:,'temp_price'] / df.ix[:,'temp_price_usd']
        df['p1'] = df.ix[:,'temp_price_usd'] * self.USD_in_ARS
        df['temp_price_usdblue'] = df.ix[:,'temp_price'] / self.USD_in_ARS
        df['max_amount_diff'] = df.ix[:,'max_amount'] - df.ix[:,'max_amount_available']
        df['max_amount_pcnt'] = df.ix[:,'max_amount_available'] / df.ix[:,'max_amount'] * 100
        df['url'] = n.core.defchararray.add('https://localbitcoins.com/ad/', n.array(df.ix[:,'ad_id'], dtype=n.string_))

        print df.columns
        #print df

        #dfi = df.ix[:,['temp_price', 'temp_price_usd','p', 'p1', 'p2','profile', 'payment_method', 'trade_type']].sort('temp_price')
        #dfi = df.ix[:,['temp_price', 'temp_price_usd','p', 'p2','profile', 'payment_method', 'trade_type', 'online_provider', 'payment_window_minutes', 'max_amount', 'max_amount_available', 'max_amount_diff', 'max_amount_pcnt', 'min_amount', 'url']].sort('temp_price')
        dfi = df.ix[:,['temp_price', 'temp_price_usd', 'p1', 'temp_price_usdblue', 'max_amount', 'max_amount_available', 'min_amount', 'max_amount_diff', 'max_amount_pcnt', 'url', 'trade_type', 'online_provider', 'bank_name', 'city', 'countrycode', 'created_at', 'currency', 'first_time_limit_btc', 'location_string', 'msg', 'payment_window_minutes', 'reference_type', 'require_feedback_score', 'require_identification', 'require_trade_volume', 'sms_verification_required', 'trusted_required', 'visible', 'volume_coefficient_btc']].sort('temp_price')

        #dfi.plot()
        #print dfi.sort('max_amount_pcnt')
        p.set_option('display.max_columns', None)
        p.set_option('display.height', 1000)
        p.set_option('display.max_rows', None)
        #p.set_option('display.max_columns', 500)
        p.set_option('display.width', 1000)

        #sortby = 'max_amount_pcnt'
        sortby = 'temp_price_usdblue'
        print dfi.sort(sortby)
        print '================================================================================'
        print dfi.sort(sortby).transpose()
        print n.max(dfi.ix[:,'temp_price'])
        print n.min(dfi.ix[:,'temp_price'])
        print n.mean(dfi.ix[:,'temp_price'])


if __name__ == "__main__":

    currency='ARS'
    lb = LocalBitcoins()
    lb.localbitcoinsPublicAds(currency=currency, adtype='buy')
    print '================================================================================'
    print '================================================================================'
    lb.localbitcoinsPublicAds(currency=currency, adtype='sell')
