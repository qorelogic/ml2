#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 17:18:27 2015

@author: qore2
"""

import argparse
# source: https://docs.python.org/2/howto/argparse.html
parser = argparse.ArgumentParser()
parser.add_argument("-v", '--verbose', help="turn on verbosity")
parser.add_argument("-l", '--list', help="go live and turn off dryrun", action="store_true")
parser.add_argument("-pms", '--paymentMethods', help="go live and turn off dryrun", action="store_true")
parser.add_argument("-cc", '--localbitcoinsCountryCodes', help="go live and turn off dryrun", action="store_true")
parser.add_argument("-currs", '--localbitcoinsCurrencies', help="go live and turn off dryrun", action="store_true")
parser.add_argument("-ua", '--updateAds', help="go live and turn off dryrun", action="store_true")

parser.add_argument("-sms", '--sms_verification_required', help="sms verify required", action="store_true")
parser.add_argument("-nosms", '--sms_verification_not_required', help="sms verify not required", action="store_true")
parser.add_argument("-feedback", '--require_feedback_score', help="require a feedback score higher than ...")
parser.add_argument("-id", '--require_identification', help="require a feedback score higher than ...", action="store_true")
parser.add_argument("-noid", '--require_no_identification', help="require a feedback score higher than ...", action="store_true")
parser.add_argument("-tv", '-vol', '--require_trade_volume', help="require a feedback score higher than ...")
parser.add_argument("-pm", '--paymentMethod', help="paymentMethod = paypal")
parser.add_argument("-c2p", "-local", '--crypto2local', help="paymentMethod = paypal", action="store_true")
parser.add_argument("-ars", '--ars', help="paymentMethod = paypal")
parser.add_argument("-lbtcprice", '--lbtc_arsbtc', help="paymentMethod = paypal")
parser.add_argument("-btceth", '--btceth', help="paymentMethod = paypal")

parser.add_argument("-ca", '--createAd', help="go live and turn off dryrun", action="store_true")
group = parser.add_argument_group('createAd')
group.add_argument("-max", '--maxAmount', help="max amount = int")
group.add_argument("-tt", '--tradeType', help="trade type = buy bitcoin | sell bitcoin")
group.add_argument("-cu", '--currency', help="currency = ARS | USD")

args = parser.parse_args()

from qore import *
import numpy as n

def defp(pt):
    try:    sys.path.index(pt)
    except: sys.path.append(pt)

defp('../lib/bitcoin/localbitcoins/digithink_py-localbitcoins.github.py.git')

from api import LocalbitcoinsAPI

class LocalBitcoins:

    def __init__(self):

        self.USD_in_ARS = self.getAmbitoUSDARSBlue()
        #self.USD_in_ARS = 14.81
        #self.USD_in_ARS = 14.66

    def getAmbitoUSDARSBlue(self):
        blue = p.read_csv('/ml.dev/lib/DataPipeline/ambitoUSDARSblue_numbeo.csv')
        #print blue
        return blue.ix[0,'venta']

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


    def localbitcoinsCountryCodes(self):
        
        url = 'https://localbitcoins.com/api/countrycodes/'

        res = fetchURL(url)
        df = p.DataFrame(res['data']['cc_list'])
        p.set_option('display.max_columns', None)
        p.set_option('display.max_rows', None)
        p.set_option('display.width', 1000)
        print df

    def localbitcoinsCurrencies(self):
        
        url = 'https://localbitcoins.com/api/currencies/'

        res = fetchURL(url)
        df = p.DataFrame(res['data']['currencies'])
        p.set_option('display.max_columns', None)
        p.set_option('display.max_rows', None)
        p.set_option('display.width', 1000)
        print df.transpose()

    def localbitcoinsPaymentMethods(self, country_code=None):
        
        if country_code != None:
            url = 'https://localbitcoins.com/api/payment_methods/{0}/'.format(country_code)
        else:
            url = 'https://localbitcoins.com/api/payment_methods/'

        res = fetchURL(url)
        print res
        df = p.DataFrame(res['data']['methods'])
        p.set_option('display.max_columns', None)
        p.set_option('display.max_rows', None)
        p.set_option('display.width', 1000)
        print df.transpose()

    def getPage(self, url, df=None):
        print 'url:%s' % url
        try:
            res = fetchURL(url)
        except TypeError as e:
            print 'no url to fetch'
            return [df, None]
            
        with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
            print 'df'
            #print df
            print 'count_df:%s' % len(df.index)
            print 'res'
            #print p.DataFrame(res)
        #print res
        try:
            print 'count_res:%s' % len(res['data']['ad_list'])
            for i in res['data']['ad_list']:
                data = i['data']
                #print i
                #df = p.DataFrame(i['data']).transpose()
                #print df.ix[['temp_price','temp_price_usd'], 'username']
                #print data
                df = df.combine_first(p.DataFrame(data, index=[data['ad_id']]))
                #.transpose()
        except:
            ''
        try: print 'count_df:%s' % len(df.index)
        except: ''
        nextP = None
        try:    nextP = res['pagination']['next']
        except: ''
        print 'nextP:%s' % nextP
        print '----------'
        try:
            df, nextP = self.getPage(url=nextP, df=df)
        except Exception as e:
            print e
        return [df, nextP]

    def localbitcoinsPublicAds(self, currency='USD', adtype='buy', payment_method=None):
        #from qore import *

        if payment_method != None:
            payment_method_txt = payment_method+'/' # follows: /buy-bitcoins-online/{currency:3}/{payment_method}/.json
        else:
            payment_method_txt = ''
        
        murl = 'https://localbitcoins.com/{1}-bitcoins-online/{0}/{2}.json'.format(currency, adtype, payment_method_txt)
        #murl = 'https://localbitcoins.com/{1}-bitcoins-online/{2}/.json'.format(currency, adtype, payment_method_txt)
        
        df, nextP = self.getPage(murl, df=p.DataFrame())
        try: print 'count_df 2:%s' % len(df.index)
        except: ''
        
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
        dfi = df.ix[:,['url', 'sms_verification_required', 'require_feedback_score', 'online_provider', 'currency', 'temp_price', 'temp_price_usd', 'temp_price_usdblue', 'max_amount', 'max_amount_available', 'min_amount', 'max_amount_diff', 'max_amount_pcnt', 'trade_type', 'bank_name', 'city', 'countrycode', 'created_at', 'first_time_limit_btc', 'location_string', 'msg', 'payment_window_minutes', 'reference_type', 'require_identification', 'require_trade_volume', 'trusted_required', 'visible', 'volume_coefficient_btc']].sort_values(by='temp_price')
        dfi = df.ix[:,['url', 'sms_verification_required', 'require_identification', 'require_trade_volume', 'trusted_required', 'require_feedback_score', 'online_provider', 'currency', 'temp_price', 'temp_price_usd', 'temp_price_usdblue', 'max_amount', 'max_amount_available', 'min_amount', 'max_amount_diff', 'max_amount_pcnt', 'trade_type', 'bank_name', 'city', 'countrycode', 'created_at', 'first_time_limit_btc', 'location_string', 'msg', 'payment_window_minutes', 'reference_type', 'visible', 'volume_coefficient_btc']].sort_values(by='temp_price')

        #dfi.plot()
        #print dfi.sort('max_amount_pcnt')
        p.set_option('display.max_columns', None)
        p.set_option('display.max_rows', None)
        #p.set_option('display.max_columns', 500)
        p.set_option('display.width', 1000)

        #sortby = 'max_amount_pcnt'
        sortby = 'temp_price_usdblue'
        
        if args.sms_verification_required:
            dfi = dfi[dfi['sms_verification_required'] == True]

        if args.sms_verification_not_required:
            dfi = dfi[dfi['sms_verification_required'] == False]
            
        if args.require_identification:
            dfi = dfi[dfi['sms_verification_required'] == True]
        if args.require_no_identification:
            dfi = dfi[dfi['sms_verification_required'] == False]

        if args.require_trade_volume:
            try:    require_trade_volume = int(args.require_trade_volume)
            except: require_trade_volume = 0
            dfi = dfi[dfi['require_trade_volume'] <= require_trade_volume]

        #print dfi.dtypes

        if args.require_feedback_score:
            try:    require_feedback_score = int(args.require_feedback_score)
            except: require_feedback_score = 100
            dfi = dfi[dfi['require_feedback_score'] <= require_feedback_score]

        dfi = dfi.sort_values(by=sortby)
        dfi['rank'] = range(1,len(dfi.index)+1)
        dfi['rankPcnt'] = map(lambda x: float(x)/n.max(dfi['rank'])*100, dfi['rank'])

        if adtype == 'buy':
            print dfi.sort_values(by='temp_price', ascending=False)
        if adtype == 'sell':
            print dfi.sort_values(by='temp_price', ascending=False)
        #print '================================================================================'
        #print dfi.sort(sortby).transpose()
        print n.max(dfi.ix[:,'temp_price'])
        print n.min(dfi.ix[:,'temp_price'])
        print n.mean(dfi.ix[:,'temp_price'])
        print 'count:%s' % len(dfi.index)
        
        
    #/api/contact_create/{ad_id}/


    
    def renderPriceEquation(self, trade_type, currency):
        
        comission_fee = 0.06
    
        if currency.upper() == 'USD':
            if trade_type.upper() == 'ONLINE_BUY':
                price_equation = 'bitfinexusd*(1-{0})'.format(comission_fee)
            if trade_type.upper() == 'ONLINE_SELL':
                price_equation = 'bitfinexusd*(1+{0})'.format(comission_fee)
            
        if currency.upper() == 'ARS':
            #price_equation = 'bitfinexusd*USD_in_ARS*1'
            if trade_type.upper() == 'ONLINE_BUY':
                price_equation = 'bitfinexusd*{0}*(1-{1})'.format(self.USD_in_ARS, comission_fee)
            if trade_type.upper() == 'ONLINE_SELL':
                price_equation = 'bitfinexusd*{0}*(1+{1})'.format(self.USD_in_ARS, comission_fee)
    
        return price_equation
    
    def renderAdMessage(self, lang, trade_type, online_provider):
        
        data = {}
        
        if lang == 'en':
            """
    1. You will send money from verified Personal / Premier PayPal account. If its unverified I will refund your money and trade will be cancelled.
    
    2. Business account is accepted only if its under your real name.
    
    3. I will send invoice to your PayPal address, so please write your PayPal email address in trade message after you open trade.
    
    4. I have to ask your ID, Driver License, proof of address, phone number and screenshot of PayPal balance for payment. So prepare it before open a trade.
    
    5. Your localbitcoins account must have more than 2 months age and have minimum 70+ succesfull trade with positive feedback.
    
    If you are not agree with my term please don't open a trade.
    
    Price is final, no hidden fee or tax, so you will pay exactly as trade amount.
    
    Please call / whatsapp me on +6285217939597 if I'm offline or you want to discuss something about term of trade.
            """

            """
    -100+ trades (DEALS) 
    -localbitcoins account older than 6 months
    -{0} Account matching localbitcoins verified name or I.D.
    I accept payment from EACH PayPal account only ONCE A DAY.
    If your localbitcoins account is less than 1 year old I will consider trading only once a week. 
    I leave the right to refuse trading with you without explanations.
            """
            data['msg']                             = """Term of Trade :
    PLEASE READ THIS BEFORE YOU START A TRADE! 
    MUST MEET ALL THE REQUIREMENTS!!!
    I acсept trades with buyers who have:
    -{0} VERIFIED account
    You are required to send {0} only after my confirmation.
    Please send as to family or friends or cover PP fee!
    Thanks!
    """.format(online_provider)
        
        if lang == 'es':
            bankDetails = []
            if trade_type == 'ONLINE_BUY':
                bankDetails.append("""Transferencia bancaria Cualquier consulta o duda o referencias, por chat de localbitcoin . Envie sus , CBU , CUIT , tipo de cuenta. y hacemos la transferencia inmediata.
    Recibes tus pesos en el momento, las 24 hs inclusive los fines de semana. 

    Es necesario enviarnos los siguientes datos:
    
    - Titular de la cuenta
    - CUIT o DNI
    - Nombre del banco 
    - CBU y Nro de cuenta
    
    NOTA : Algunas transferencias bancarias pueden tardar 24/48 horas , dependiendo del sistema bancario y sus horarios o regulacione.s

""")
                bankDetails.append('transfiero')

            else:
                bankDetails.append('')
                bankDetails.append('libero')
            data['msg']                             = """{0}Si es a altas horas de la madrugada, ni bien me levanto {1} inmediato.
    
    We speak english, change your BTC and get pesos with a better rate.
    
    Gracias
""".format(bankDetails[0], bankDetails[1])

        return data['msg']
    
    def updateAds(self):
        os.environ['DREST_DEBUG'] = '0'
        # send a GET request for "/api/myself/"
        api = LocalbitcoinsAPI()
        res = api.make_request('GET', '/api/ads/')
        for i in res.data['data']['ad_list']:
            ad_id = i['data']['ad_id']
            print ad_id
            df = p.DataFrame(i).ix[['price_equation', 'lat', 'lon', 'city', 'location_string', 'countrycode', 'currency', 'account_info', 'bank_name', 'msg', 'sms_verification_required', 'track_max_amount', 'require_trusted_by_advertiser', 'require_identification', 'visible', 'max_amount','min_amount', 'trade_type', 'online_provider'], 'data']
            df = df.fillna(0)
            data = df.to_dict()
            #data = p.DataFrame(i).ix[:, 'data'].to_dict()
            data['account_info'] = ''
            data['bank_name'] = ''
            
            if data['currency'].upper() == 'ARS':
                
                risk = 25
                data['max_amount']     = int(float((12000.0)*risk/100))
                data['min_amount']     = 100
                #print data
                data['price_equation'] = self.renderPriceEquation(data['trade_type'], data['currency'])
                data['msg']            = self.renderAdMessage('es', trade_type=data['trade_type'], online_provider=data['online_provider'])
                
            if data['currency'].upper() == 'USD':
                
                #data['max_amount']     = 1
                #data['min_amount']     = 1
                data['price_equation'] = self.renderPriceEquation(data['trade_type'], data['currency'])
                data['msg']            = self.renderAdMessage('en', trade_type=data['trade_type'], online_provider=data['online_provider'])
    
            data['require_trusted_by_advertiser'] = False
            
            print p.DataFrame(data, index=[0]).transpose()
            #data = {'address': 'test address', 'amount': 0.0001}
            method = '/api/ad/{0}/'.format(ad_id)
            print method
            print 
            try:
                response = api.make_request('POST', method, params=data)
            except Exception as e:
                print e
            #    print dir(response)
            #    print response.headers
    
            
    def createAd(self, max_amount, trade_type, lang, currency, online_provider=None):
        
        os.environ['DREST_DEBUG'] = '1'
    
        from api import LocalbitcoinsAPI
        api = LocalbitcoinsAPI()
        data = {}
        data['max_amount']                          = str(max_amount)
        data['lat']                             = '0'
        data['lon']                             = '0'
        
        data['currency']                        = currency.upper() #'ARS' || 'USD'
    
        if trade_type == 'buy':
            data['trade_type']                      = 'ONLINE_BUY'
        if trade_type == 'sell':
            data['trade_type']                      = 'ONLINE_SELL'
    
        if currency.upper() == 'ARS':
            data['city']                            = 'Buenos Aires'
            data['location_string']                 = 'Buenos Aires, Autonomous City of Buenos Aires, Argentina'
            data['countrycode']                     = 'AR'
    
            data['max_amount'] = int((12000.0-500)*10/100)
            data['min_amount'] = 1000
            
            data['price_equation'] = self.renderPriceEquation(data['trade_type'], currency)
            
            if online_provider != None:
                data['online_provider']                 = online_provider.upper()
            else:
                data['online_provider']                 = 'NATIONAL_BANK'
            
            data['msg'] = self.renderAdMessage('es', trade_type=data['trade_type'], online_provider=data['online_provider'])
    
        if currency.upper() == 'USD':
            data['city']                            = 'New York'
            data['location_string']                 = 'New York, New York'
            data['countrycode']                     = 'US'
    
            try:
                if online_provider.upper() == 'OKPAY':
                    data['max_amount'] = 1
                    data['min_amount'] = 1
                else:
                    data['max_amount'] = int(n.floor(max_amount))
                    data['min_amount'] = 1
            except:
                ''
            
            try:    data['trade_type']
            except:
                parser.print_help()
                sys.exit()

            data['price_equation'] = self.renderPriceEquation(data['trade_type'], currency)
                
    
            if online_provider != None:
                data['online_provider']                 = online_provider.upper()
            if online_provider == None:
                data['online_provider']                 = 'PAYPAL'
    
            data['msg'] = self.renderAdMessage('en', trade_type=data['trade_type'], online_provider=data['online_provider'])
    
        data['account_info']                    = 'test'
        data['bank_name']                       = ''
        data['sms_verification_required']       = False
        try:
            if online_provider.upper() != 'OKPAY':
                data['track_max_amount']                = True
        except:
            ''
        data['require_trusted_by_advertiser']   = False
        data['require_identification']          = False
        
        print p.DataFrame(data, index=[0]).transpose()
        #data = {'address': 'test address', 'amount': 0.0001}
        method = '/api/ad-create/'
        print method
        print 
        print 
        #try:
        response = api.make_request('POST', method, params=data)
        #except:
        #    print ''
        #    print dir(response)
        #    print response.headers   


    
    
    def contactCreate(self, amount, ad_id, lang):
        os.environ['DREST_DEBUG'] = '1'
        # send a GET request for "/api/myself/"
        api = LocalbitcoinsAPI()
        data = {}
        data['amount'] = amount
        if lang == 'en':
            data['message'] = """Hi, send me your details. Thanks"""
        if lang == 'es':
            data['message'] = """Hola te compro a este precio, pasame tus detalles. Gracias"""
        print p.DataFrame(data, index=[0]).transpose()
        #data = {'address': 'test address', 'amount': 0.0001}
        method = '/api/contact_create/{0}/'.format(ad_id)
        print method
        print 
        #try:
        response = api.make_request('POST', method, params=data)
        #print response['error']['message']
        #except:
        #    print ''
        #    print dir(response)
        #    print response.headers
    
    def contactInfo(self, contact_id):
        os.environ['DREST_DEBUG'] = '1'
        # send a GET request for "/api/myself/"
        api = LocalbitcoinsAPI()
        response = api.make_request('GET', '/api/contact_info/{0}/'.format(contact_id))
        return p.DataFrame(response.data['data'])
    
    def contact_mark_as_paid(self, contact_id):
        os.environ['DREST_DEBUG'] = '1'
        # send a GET request for "/api/myself/"
        api = LocalbitcoinsAPI()
        response = api.make_request('GET', '/api/contact_mark_as_paid/{0}/'.format(contact_id))
        print p.DataFrame(response.data)
    
    #/api/contact_mark_as_paid/{contact_id}/
    
    def dashboard(self):
        os.environ['DREST_DEBUG'] = '0'
        # send a GET request for "/api/myself/"
        api = LocalbitcoinsAPI()
        response = api.make_request('GET', '/api/dashboard/')
        data = response.data['data']
        #print '==D=='
        #print p.DataFrame(data['contact_list'])
        for i in data['contact_list']:
            print '==='
            #print p.DataFrame(i)#.transpose()
            print 'contact_id: {0}'.format(i['data']['contact_id'])
            print 'created_at: {0}'.format(i['data']['created_at'])
            print 'advertisement: {0}'.format(i['data']['advertisement'])
            print 'seller: {0}'.format(i['data']['seller'])
            print 'reference_code: {0}'.format(i['data']['reference_code'])
            print 'amount: {0}'.format(i['data']['amount'])
            print 'amount_btc: {0}'.format(i['data']['amount_btc'])
            amount_local = float(i['data']['amount']) / float(i['data']['amount_btc'])
            print 'currency: {0}'.format(i['data']['currency'])
            print 'price: {0}'.format(amount_local)
            if i['data']['currency'] == 'ARS':
                print '{0} {1}'.format(amount_local / 14.81, amount_local / 14.66)
            if i['data']['currency'] == 'USD':
                print '{0} {1}'.format(amount_local, amount_local)
            print 'message_post_url: {0}'.format(i['actions']['message_post_url'])
            print 'messages_url: {0}'.format(i['actions']['messages_url'])
    
    def online_buy_contacts(self):
        os.environ['DREST_DEBUG'] = '1'
        # send a GET request for "/api/myself/"
        api = LocalbitcoinsAPI()
        response = api.make_request('GET', '/api/online_buy_contacts/')
        data = response.data['data']
        for i in data['contact_list']:
            print '==='
            print p.DataFrame(i)




if __name__ == "__main__":

    lb = LocalBitcoins()
    
    country_code='US'
    currency = args.currency
    payment_method = args.paymentMethod
    
    if currency == None:
        currency = 'usd'
        print 'currency:%s' % currency
        print 'currency type:%s' % type(currency)
    
    #if payment_method == None:
    #    payment_method = 'usd'
    
    if args.list:
        try:
            #if  currency.upper() == 'ARS':
            #    #currency='ARS'
            #    payment_method=None
            ''
        except: ''

        try:
            #if  currency.upper() == 'USD':
            #    #currency='USD'
            #    payment_method='paypal'
            ''
        except: ''

        lb.localbitcoinsPublicAds(currency=currency, adtype='buy', payment_method=payment_method)
        print '================================================================================'
        lb.localbitcoinsPublicAds(currency=currency, adtype='sell', payment_method=payment_method)
        print '================================================================================'

    if args.updateAds:
        lb.updateAds()

    if args.createAd:
        max_amount = args.maxAmount # int
        trade_type = args.tradeType # buy | sell
        currency   = args.currency # ARS | USD
        lang = 'en'
        
        lb.createAd(max_amount, trade_type, lang, currency, online_provider=None)

    if args.paymentMethods:
        lb.localbitcoinsPaymentMethods(country_code=country_code)

    if args.localbitcoinsCountryCodes:
        lb.localbitcoinsCountryCodes()

    if args.localbitcoinsCurrencies:
        lb.localbitcoinsCurrencies()

    def crypto2local(pesosRequired, lbtc_arsbtc, btceth):
        transactionFee                = 0.001
        lbtcIncomingBitcoinNetworkFee = 0
        #lbtcIncomingBitcoinNetworkFee = 0.00035225
        fees = transactionFee + lbtcIncomingBitcoinNetworkFee
        #comission = 1+(5.47/100*2)
        comission = 1#+(5.47/100*2)
        btc = (float(pesosRequired)/lbtc_arsbtc*comission)
        eth = btc/btceth
        baked = (btc + fees)/btc
        print
        print 'pesosRequired: %s' % (pesosRequired)
        print 'send btc: %s' % (btc)
        print 'send btc: %s %s' % (btc + fees, baked)
        print 'send eth: %s' % (eth)
        print 'send lbtc_arsbtc: %s' % (lbtc_arsbtc)
        print 'send lbtc_arsbtc: %s' % (lbtc_arsbtc*(baked))
        print btc * lbtc_arsbtc
        print (pesosRequired / lbtc_arsbtc + fees) * lbtc_arsbtc
        print (pesosRequired / lbtc_arsbtc + fees)
        
    if args.crypto2local:
        ars         = float(args.ars)
        try: lbtc_arsbtc = float(args.lbtc_arsbtc)
        except:
            print 'lbtc_arsbtc not set'
            sys.exit()
        try: btceth      = float(args.btceth)
        except:
            print 'btceth not set'
            sys.exit()
        crypto2local(ars, lbtc_arsbtc, btceth)
