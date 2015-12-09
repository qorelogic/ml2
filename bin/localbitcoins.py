#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 17:18:27 2015

@author: qore2
"""

from qore import *
import numpy as n

def defp(pt):
    try:    sys.path.index(pt)
    except: sys.path.append(pt)

defp('../lib/bitcoin/localbitcoins/digithink_py-localbitcoins.github.py.git')

from api import LocalbitcoinsAPI

class LocalBitcoins:

    def __init__(self):
        self.USD_in_ARS = 14.81
        #self.USD_in_ARS = 14.66

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

    def localbitcoinsPublicAds(self, currency='USD', adtype='buy', payment_method=None):
        #from qore import *

        if payment_method != None:
            payment_method_txt = payment_method+'/' # follows: /buy-bitcoins-online/{currency:3}/{payment_method}/.json
        else:
            payment_method_txt = ''
            
        res = fetchURL('https://localbitcoins.com/{1}-bitcoins-online/{0}/{2}.json'.format(currency, adtype, payment_method_txt))
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

        #print df.columns
        #print df

        #dfi = df.ix[:,['temp_price', 'temp_price_usd','p', 'p1', 'p2','profile', 'payment_method', 'trade_type']].sort('temp_price')
        #dfi = df.ix[:,['temp_price', 'temp_price_usd','p', 'p2','profile', 'payment_method', 'trade_type', 'online_provider', 'payment_window_minutes', 'max_amount', 'max_amount_available', 'max_amount_diff', 'max_amount_pcnt', 'min_amount', 'url']].sort('temp_price')
        dfi = df.ix[:,['url', 'sms_verification_required', 'online_provider', 'currency', 'temp_price', 'temp_price_usd', 'temp_price_usdblue', 'max_amount', 'max_amount_available', 'min_amount', 'max_amount_diff', 'max_amount_pcnt', 'trade_type', 'bank_name', 'city', 'countrycode', 'created_at', 'first_time_limit_btc', 'location_string', 'msg', 'payment_window_minutes', 'reference_type', 'require_feedback_score', 'require_identification', 'require_trade_volume', 'trusted_required', 'visible', 'volume_coefficient_btc']].sort('temp_price')

        #dfi.plot()
        #print dfi.sort('max_amount_pcnt')
        p.set_option('display.max_columns', None)
        p.set_option('display.max_rows', None)
        #p.set_option('display.max_columns', 500)
        p.set_option('display.width', 1000)

        #sortby = 'max_amount_pcnt'
        sortby = 'temp_price_usdblue'
        print dfi.sort(sortby)
        #print '================================================================================'
        #print dfi.sort(sortby).transpose()
        print n.max(dfi.ix[:,'temp_price'])
        print n.min(dfi.ix[:,'temp_price'])
        print n.mean(dfi.ix[:,'temp_price'])
        
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
    
    def renderAdMessage(self, lang):
        
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
            data['msg']                             = """Term of Trade :
    PLEASE READ THIS BEFORE YOU START A TRADE! 
    MUST MEET ALL THE REQUIREMENTS!!!
    I acсept trades with buyers who has:
    -100+ trades (DEALS) 
    -localbitcoins account older than 6 months
    -Paypal VERIFIED account
    -Paypal account matching localbitcoins verified name or I.D.
    You are required to send pp only after my confirmation.
    I accept payment from EACH PayPal account only ONCE A DAY.
    If your localbitcoins account is less than 1 year old I will consider trading only once a week. 
    I leave the right to refuse trading with you without explanations.
    Please send as to family or friends or cover PP fee!
    Thanks!
    """        
        if lang == 'es':
            data['msg']                             = """Transferencia bancaria Cualquier consulta o duda o referencias, por chat de localbitcoin . Envie sus , CBU , CUIT , tipo de cuenta. y hacemos la transferencia inmediata.
    Recibes tus pesos en el momento, las 24 hs inclusive los fines de semana. 
    
    Si es a altas horas de la madrugada, ni bien me levanto transfiero inmediato.
    
    Es necesario enviarnos los siguientes datos:
    
    - Titular de la cuenta
    - CUIT o DNI
    - Nombre del banco 
    - CBU y Nro de cuenta
    
    We speak english, change your BTC and get pesos with a better rate.
    
    Gracias
    
    NOTA : Algunas transferencias bancarias pueden tardar 24/48 horas , dependiendo del sistema bancario y sus horarios o regulacione.s
    
    """
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
                data['max_amount']     = int(float((12000.0-500-6000)*risk/100))
                data['min_amount']     = 100
                print data
                data['price_equation'] = self.renderPriceEquation(data['trade_type'], data['currency'])
                data['msg']            = self.renderAdMessage('es')
                
            if data['currency'].upper() == 'USD':
                
                #data['max_amount']     = 1
                #data['min_amount']     = 1
                data['price_equation'] = self.renderPriceEquation(data['trade_type'], data['currency'])
                data['msg']            = self.renderAdMessage('en')        
    
            data['require_trusted_by_advertiser'] = False
            
            print p.DataFrame(data, index=[0]).transpose()
            #data = {'address': 'test address', 'amount': 0.0001}
            method = '/api/ad/{0}/'.format(ad_id)
            print method
            print 
            #try:
            response = api.make_request('POST', method, params=data)
            #except:
            #    print ''
            #    print dir(response)
            #    print response.headers
    
            
    def createAd(self, amount, trade_type, lang, currency, online_provider=None):
        
        os.environ['DREST_DEBUG'] = '1'
    
        from api import LocalbitcoinsAPI
        api = LocalbitcoinsAPI()
    
        data['amount']                          = str(amount)
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
    
            data['max_amount'] = (12000.0-500)*10/100
            data['min_amount'] = 1000
            
            data['price_equation'] = self.renderPriceEquation(data['trade_type'], currency)
            
            if online_provider != None:
                data['online_provider']                 = online_provider.upper()
            else:
                data['online_provider']                 = 'NATIONAL_BANK'
            
            data['msg'] = renderAdMessage('es')
    
        if currency.upper() == 'USD':
            data['city']                            = 'New York'
            data['location_string']                 = 'New York, New York'
            data['countrycode']                     = 'US'
    
            data['max_amount'] = int(floor(amount))
            data['min_amount'] = 1
            
            data['price_equation'] = self.renderPriceEquation(data['trade_type'], currency)
    
            if online_provider != None:
                data['online_provider']                 = online_provider.upper()
            if online_provider == None:
                data['online_provider']                 = 'PAYPAL'
    
            data['msg'] = renderAdMessage('en')
    
        data['account_info']                    = 'test'
        data['bank_name']                       = ''
        data['sms_verification_required']       = False
        data['track_max_amount']                = True
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

    country_code='US'
    currency='ARS'
    payment_method=None
    lb = LocalBitcoins()
    lb.localbitcoinsPublicAds(currency=currency, adtype='buy', payment_method=payment_method)
    print '================================================================================'
    lb.localbitcoinsPublicAds(currency=currency, adtype='sell', payment_method=payment_method)
    print '================================================================================'

    country_code='US'
    currency='USD'
    payment_method='paypal'
    lb = LocalBitcoins()
    lb.localbitcoinsPublicAds(currency=currency, adtype='buy', payment_method=payment_method)
    print '================================================================================'
    lb.localbitcoinsPublicAds(currency=currency, adtype='sell', payment_method=payment_method)
    print '================================================================================'

    #lb.localbitcoinsPaymentMethods(country_code=country_code)
    #lb.localbitcoinsCountryCodes()
    #lb.localbitcoinsCurrencies()
    
