
import argparse
# source: https://docs.python.org/2/howto/argparse.html
parser = argparse.ArgumentParser()
parser.add_argument("-v", '--verbose', help="turn on verbosity")
parser.add_argument("-l", '--live', help="go live and turn off dryrun", action="store_true")
parser.add_argument("-mm", '--monitorMargin', help="list logins", action="store_true")
parser.add_argument("-mt", '--monitorTrades', help="list logins", action="store_true")
parser.add_argument("-mtv", '--monitorAccountsProfitableTradesVerbose', help="list logins", action="store_true")
parser.add_argument("-cpt", '--closeProfitableTrades', help="closeProfitable trades with monitorTrades", action="store_true")
parser.add_argument("-ll", '--listLogins', help="list logins", action="store_true")
parser.add_argument("-la", '--listAccounts', help="list logins", action="store_true")
parser.add_argument("-li", '--loginIndex', help="set the account index given by -ll")
parser.add_argument("-ai", '--accountIndex', help="set the account index given by -la")
parser.add_argument("-hh", '--history', help="history", action="store_true")
parser.add_argument("-hf", '--historyFilename', help="history file name")
parser.add_argument("-hi", '--historyIndex', help="history index")
parser.add_argument("-a", '--analyze', help="go live and turn off dryrun", action="store_true")
parser.add_argument("-w", '--web', help="data dump", action="store_true")
parser.add_argument("-acc", '--account', help="account number")
parser.add_argument('-g', "-gearing", '--leverage', help="gearing or leverage, default=50")
parser.add_argument('-n', '--num', help="number of trades default=None")
parser.add_argument('-dp', '--diffpThreshold', help="trade only signals above a given threshold default=0")
parser.add_argument('-lim', '--limitMaxTrades', help="trade only a maximum limit number of trades limitMaxTrades")
#parser.add_argument("-c", '--connect', help="connect, v=Vultr", action="store_true")
parser.add_argument("-i", '--interactive', help="Interactive Loop", action="store_true")
parser.add_argument("-ni", '--noInteractive', help="No interactive Q&A", action="store_true")
parser.add_argument("-nid", '--noInteractiveDeleverage', help="No interactive Q&A for the deleverage option", action="store_true")
parser.add_argument("-nil", '--noInteractiveLeverage', help="No interactive Q&A for the deleverage option", action="store_true")
parser.add_argument("-nif", '--noInteractiveFleetingProfits', help="No interactive Q&A for the fleeting profits routine", action="store_true")

parser.add_argument("-s", '--sortRebalanceList', help="reverse[r[p=pl]] | deleverage[d[p=pl]] | leverage[l]")

parser.add_argument('-not', '-noth', '-nothreads', '--nothreading', help="No threading", action="store_true")
args = parser.parse_args()

import sys
try: sys.path.index('/ml.dev/bin/datafeeds')
except: sys.path.append('/ml.dev/bin/datafeeds')

import numpy as n
import sys
try: sys.path.index('/ml.dev/bin/datafeeds')
except: sys.path.append('/ml.dev/bin/datafeeds')

import numpy as n
import pandas as p
#mport Quandl as q
#from Quandl import Quandl as q
import datetime as dd
from qoreliquid import *
import talib as talib
#from matplotlib import pyplot as plt
#from pylab import rcParams
#get_ipython().magic(u'pylab inline')
#rcParams['figure.figsize'] = 20, 5

# oanda api
import oandapy
#import oandapyV20.endpoints.trades as trades
import oandapyV20.endpoints.accounts as accounts

qd = QoreDebug()
qd.on()

co, loginIndex, env0, access_token0, oanda0 = getConfig(args=args)

#env1=co.ix[1,1]
#access_token1=co.ix[1,2]
#oanda1 = oandapy.API(environment=env1, access_token=access_token1)

with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):

    if args.monitorMargin:
        from qoreliquid import Patterns
        pa = Patterns(loginIndex=loginIndex)
        pa.monitorAccountsMarginCloseout()
        sys.exit()
        
    if args.monitorTrades:
        from qoreliquid import Patterns
        pa = Patterns(loginIndex=loginIndex)
        if args.closeProfitableTrades:
              closeProfitableTrades = True
        else: closeProfitableTrades = False
        if args.monitorAccountsProfitableTradesVerbose:
              monitorAccountsProfitableTradesVerbose = True
        else: monitorAccountsProfitableTradesVerbose = False
        if args.account:
              account = args.account
        else: account= None
        pa.monitorAccountsProfitableTrades(verbose=monitorAccountsProfitableTradesVerbose, closeProfitableTrades=closeProfitableTrades, account=account)
        sys.exit()        

    if args.listLogins:
            print co
            sys.exit()
    
    if args.listAccounts:
            
            adf = getAccounts(oanda0, access_token0)
            print adf.ix[:,'accountId accountCurrency accountName marginRate mt4AccountID tags'.split(' ')]
            #accid = acc[loginIndex]['accountId']
            #print 'using account: {0}'.format(accid)
            sys.exit()

try:
    if args.accountIndex == None:
        raise('accountIndex is none')
    accountIndex = int(args.accountIndex)
except:        
    accountIndex = 0

try:
    acc = getAccounts(oanda0, access_token0)
    if int(args.verbose) >= 5:
        qd.data(args.account, name='args account:')
        with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
            qd.data(p.DataFrame(acc), name='acc::')
    try:
        if args.account == None:
            raise('account is none')
        accid = str(args.account)
    except:        
        try:
            #with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
            #    print acc
            accid = acc.ix[accountIndex, 'accountId']
        except Exception as e:
            qd.exception(e)
            sys.exit()
    qd.data(accountIndex, name='accountIndex:')
    qd.data(accid, name='using account:')
except Exception as e:
    qd.exception(e)

#@profile
def main(loginIndex, args, leverage=10, dryrun=True, verbose=False):

    pa = Patterns(loginIndex=loginIndex)

    # In[ ]:

    threading = not args.nothreading
    
    """
    #oanda0.get_accounts()
    targetSalaryPerSecond = (40e3 / (60*60*24*260))
    asddf = p.DataFrame(oanda0.get_trades(558788)['trades'])#.set_index('instrument')#.ix[:,'side units'.split(' ')]
    asddf['timeu'] = oq.oandaToTimestamp(asddf['time'])
    asddf['timeage'] = time.time() - n.array(oq.oandaToTimestamp(asddf['time']))
    asddf['targetSalaryPerSecond'] = targetSalaryPerSecond * asddf['timeage']
    asddf.ix[:, 'time timeu timeage targetSalaryPerSecond'.split(' ')]
    """
    
    # In[ ]:
    
    
    
    
    import os
    cmd = 'ls -t /ml.dev/bin/data/oanda/cache/patterns/patterns.dfu.* 2> /dev/null'
    fname = os.popen(cmd).read().strip().split('\n')[0]
    dfh = {}
    df = p.DataFrame()
    if args.analyze:
        logApplicationUsage('analyze', description='analyze')
        dfu = p.DataFrame()
        if threading:
            from multiprocessing.pool import ThreadPool
            pool = ThreadPool(processes=270)
        #instruments = p.DataFrame(oanda0.get_instruments(accid)['instruments']).set_index('instrument')
        #symbols = instruments.index
        #symbols  = 'AUD_CAD,AUD_CHF,AUD_HKD,AUD_JPY,AUD_NZD,AUD_SGD,AUD_USD,CAD_CHF,CAD_HKD,CAD_JPY,CAD_SGD,CHF_HKD,CHF_JPY,CHF_ZAR,EUR_AUD,EUR_CAD,EUR_CHF,        EUR_DKK,EUR_GBP,EUR_HKD,EUR_HUF,EUR_JPY,EUR_NOK,EUR_NZD,EUR_PLN,EUR_SEK,EUR_SGD,EUR_TRY,EUR_USD,EUR_ZAR,GBP_AUD,GBP_CAD,GBP_CHF,GBP_HKD,GBP_JPY,GBP_NZD,GBP_PLN,GBP_SGD,GBP_USD,GBP_ZAR,HKD_JPY,NZD_CAD,NZD_CHF,NZD_HKD,NZD_JPY,NZD_SGD,NZD_USD,SGD_CHF,SGD_HKD,SGD_JPY,TRY_JPY,USD_CAD,USD_CHF,USD_CNH,USD_CZK,USD_DKK,USD_HKD,USD_HUF,USD_JPY,USD_MXN,USD_NOK,USD_PLN,        USD_SEK,USD_SGD,USD_THB,USD_TRY,USD_ZAR,ZAR_JPY'.split(',') # 20170223
        #symbols = 'AUD_CAD,AUD_CHF,AUD_HKD,AUD_JPY,AUD_NZD,AUD_SGD,AUD_USD,CAD_CHF,CAD_HKD,CAD_JPY,CAD_SGD,CHF_HKD,CHF_JPY,CHF_ZAR,EUR_AUD,EUR_CAD,EUR_CHF,EUR_CZK,EUR_DKK,EUR_GBP,EUR_HKD,EUR_HUF,EUR_JPY,EUR_NOK,EUR_NZD,EUR_PLN,EUR_SEK,EUR_SGD,EUR_TRY,EUR_USD,EUR_ZAR,GBP_AUD,GBP_CAD,GBP_CHF,GBP_HKD,GBP_JPY,GBP_NZD,GBP_PLN,GBP_SGD,GBP_USD,GBP_ZAR,HKD_JPY,NZD_CAD,NZD_CHF,NZD_HKD,NZD_JPY,NZD_SGD,NZD_USD,SGD_CHF,SGD_HKD,SGD_JPY,TRY_JPY,USD_CAD,USD_CHF,USD_CNH,USD_CZK,USD_DKK,USD_HKD,USD_HUF,USD_JPY,USD_MXN,USD_NOK,USD_PLN,USD_SAR,USD_SEK,USD_SGD,USD_THB,USD_TRY,USD_ZAR,ZAR_JPY'.split(',')        
        #symbols = 'EUR_USD,GBP_USD,GBP_JPY,USD_CAD'.split(',')
        # etoro symbols
        #symbols = "AUDCAD AUDCHF AUDJPY AUDNZD AUDUSD CADCHF CADJPY CHFHUF CHFJPY EURAUD EURCAD EURCHF EURGBP EURHUF EURJPY EURNOK EURNZD EURPLN EURSEK EURUSD GBPAUD GBPCAD GBPCHF GBPHUF GBPJPY GBPNZD GBPUSD NOKSEK NZDCAD NZDCHF NZDJPY NZDUSD USDCAD USDCHF USDCNH USDHKD USDHUF USDJPY USDMXN USDNOK USDPLN USDRUB USDSEK USDSGD USDTRY USDZAR ZARJPY".split(' ')
        #symbols = "AUD_CAD AUD_CHF AUD_JPY AUD_NZD AUD_USD CAD_CHF CAD_JPY CHF_HUF CHF_JPY EUR_AUD EUR_CAD EUR_CHF EUR_GBP EUR_HUF EUR_JPY EUR_NOK EUR_NZD EUR_PLN EUR_SEK EUR_USD GBP_AUD GBP_CAD GBP_CHF GBP_HUF GBP_JPY GBP_NZD GBP_USD NOK_SEK NZD_CAD NZD_CHF NZD_JPY NZD_USD USD_CAD USD_CHF USD_CNH USD_HKD USD_HUF USD_JPY USD_MXN USD_NOK USD_PLN USD_RUB USD_SEK USD_SGD USD_TRY USD_ZAR ZAR_JPY".split(' ')
        symbols = "AUD_CAD AUD_CHF AUD_JPY AUD_NZD AUD_USD CAD_CHF CAD_JPY CHF_JPY EUR_AUD EUR_CAD EUR_CHF EUR_GBP EUR_HUF EUR_JPY EUR_NOK EUR_NZD EUR_PLN EUR_SEK EUR_USD GBP_AUD GBP_CAD GBP_CHF GBP_JPY GBP_NZD GBP_USD NZD_CAD NZD_CHF NZD_JPY NZD_USD USD_CAD USD_CHF USD_CNH USD_HKD USD_HUF USD_JPY USD_MXN USD_NOK USD_PLN USD_SEK USD_SGD USD_TRY USD_ZAR ZAR_JPY".split(' ')
        qd.data(','.join(symbols), name='symbols: ')
        dmcnt = 0                                                        # display matrix: counter
        for i in symbols:
            i = i.strip()
            if threading:
                async_result = pool.apply_async(getc4, [df, dfh, oanda0, i])
                dfu0   = async_result.get()
            else:
                dfu0 = getc4(df, dfh, oanda0, instrument=i)
            if dmcnt == 0:                                               # display matrix:
                print '%s %s' % ('       ', n.array(list(dfu0.columns))) # display matrix: header
            print '%s %s' % (list(dfu0.index)[0], dfu0.get_values()[0])  # display matrix: body
            dmcnt += 1                                                   # display matrix
            dfu  = dfu.combine_first(dfu0)
            if int(verbose) >= 8:
                print dfu
        if threading:
            pool.close()
	    #break
        fname = '/ml.dev/bin/data/oanda/cache/patterns/patterns.dfu.%s.csv' % time.time()
        dfu.to_csv(fname)
    else:
        dfu = p.read_csv(fname, index_col=0)
    dfu['diff'] = n.abs(dfu['buy'] - dfu['sell'])
    if int(verbose) > 5:
        print dfu.sort('diff', ascending=False)
    
    # In[ calculate period weights ]:
    #@profile
    def periodWeightsTable():
        p0 = [1, 5, 15, 30, 60, 240, 1440, 1440*5, 1440*20]
        p1 = n.array(range(1, len(p0)+1))
        pp = p.DataFrame(p1, columns=[0])
        #pp(:,3) = pp(:,2)./power(pp(:,1), 3)
        pp['period'] = p0
        pp['weight'] = pp.ix[:,1] / n.power(pp.ix[:,0], 3)
        pp['percent'] = pp['weight'] / n.sum(pp['weight'])
        #pp.ix[:,[0,'weight']].plot()
        #pp
        return pp.set_index(0)
    pw = periodWeightsTable()
    if int(verbose) > 5: print pw
    
    with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
        cli = [0,1,2,3,4,5,6,7,8]
        mdfu = p.DataFrame(dfu.ix[:,cli].get_values() * pw['percent'].get_values(), index=dfu.index, columns=dfu.columns[cli])
        dfu  = mdfu.combine_first(dfu)
        posdf = dfu.ix[:,cli][dfu.ix[:,cli] > 0].fillna(0)
        negdf = dfu.ix[:,cli][dfu.ix[:,cli] < 0].fillna(0)
        dfu['buy'] = n.sum(posdf.get_values(), 1)
        dfu['sell'] = n.abs(n.sum(negdf.get_values(), 1))
        dfu['diff'] = n.abs(dfu['buy'] - dfu['sell'])
        if int(verbose) > 5:
            print
            print 'pw'
            print pw#['weight']
            print
            print 'element-wise *'
            print posdf
            print negdf
            print 
            print dfu.sort('diff', ascending=False)
    
    #sys.exit()
    
    if args.diffpThreshold: diffpThreshold=int(args.diffpThreshold)
    else:                   diffpThreshold=0

    if args.limitMaxTrades: limitMaxTrades=int(args.limitMaxTrades)
    else:                   limitMaxTrades=0

    dfu['diff'] = n.abs(dfu['buy'].get_values() - dfu['sell'].get_values())
    dfu['diffp'] = (dfu['diff'].get_values())/n.sum(dfu['diff'].get_values())
    dfu['side'] = map(lambda x: 'buy' if x == 1 else 'sell', (n.array((dfu['buy'].get_values() - dfu['sell'].get_values()) > 0, dtype=int)))
    dfu['sidePolarity'] = map(lambda x: 1 if x == 1 else -1, (n.array((dfu['buy'].get_values() - dfu['sell'].get_values()) > 0, dtype=int)))
    
    if int(verbose) >= 8:
        with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
            print '=4=4=4=4=4=4=4'
            print dfu

    # etoro symbols
    #li = "AUDCAD AUDCHF AUDJPY AUDNZD AUDUSD CADCHF CADJPY CHFHUF CHFJPY EURAUD EURCAD EURCHF EURGBP EURHUF EURJPY EURNOK EURNZD EURPLN EURSEK EURUSD GBPAUD GBPCAD GBPCHF GBPHUF GBPJPY GBPNZD GBPUSD NOKSEK NZDCAD NZDCHF NZDJPY NZDUSD USDCAD USDCHF USDCNH USDHKD USDHUF USDJPY USDMXN USDNOK USDPLN USDRUB USDSEK USDSGD USDTRY USDZAR ZARJPY"
    #li = li.split(' ')
    #dfu = dfu.ix[li, :]
    
    # set the limit number of maximum trades (limitMaxTrades)
    if limitMaxTrades == 0: # if limitMaxTrades is default (0), remove the limit
        limitMaxTrades = len(dfu.index)
    dfu = dfu.sort_values(by='diffp', ascending=True).tail(limitMaxTrades)
    dfu = dfu.sort_index()

    if int(verbose) >= 8:
        with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
            print '=5=5=5=5=5=5=5'
            print dfu
            print '=4=4=4=4=4=4=4'
    
    # set the percentage threshold
    dfu2 = dfu[dfu['diffp'] > (float(diffpThreshold)/100)].sort_values(by='diff', ascending=False)
    
    # recalculate percentages [diffp]
    dfu2['diffp'] = (dfu2['diff'].get_values())/n.sum(dfu2['diff'].get_values())
    with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
        if verbose: print dfu2
    
    
    # In[ ]:
    
    orders = dfu2.ix[:, 'diff side diffp sidePolarity'.split(' ')]
    if int(verbose) > 5: 
        print 'Oanda orders:'
        print orders
        print
    
    ps = """AUD/NZD
    AUD/USD
    EUR/CHF
    EUR/GBP
    EUR/JPY
    EUR/NOK
    EUR/SEK
    EUR/USD
    GBP/USD
    NZD/USD
    USD/CAD
    USD/CHF
    USD/CNH
    USD/JPY
    USD/RUB""".replace('/', '_')
    #print ps
    
    psdf = p.DataFrame(ps.split('\n'))
    psdf['1'] = 1
    psdf = psdf.set_index(0)
    # list only 1broker pairs in the orderbook
    oneBrokerOrderbook = psdf.ix[list(orders.index), :]
    #print oneBrokerOrderbook[oneBrokerOrderbook['1'] == 1]
    #print oneBrokerOrderbook
    #print
    try:
        dfu3 = orders.ix[oneBrokerOrderbook[oneBrokerOrderbook['1'] == 1].index, :]
        
        # recalculate percentages [diffp]
        dfu3['diffp'] = (dfu3['diff'].get_values())/n.sum(dfu3['diff'].get_values())
        if int(verbose) > 5:
            print '1broker orders:'
            print dfu3
    except Exception as e:
        qd.exception(e)
        print 'No'
        print
        
    verbose                 = args.verbose
    noInteractive           = args.noInteractive
    noInteractiveLeverage   = args.noInteractiveLeverage
    noInteractiveDeleverage = args.noInteractiveDeleverage
    noInteractiveFleetingProfits = args.noInteractiveFleetingProfits
    sortRebalanceList            = args.sortRebalanceList
    loginIndex                   = args.loginIndex
    
    oq = OandaQ(verbose=False)

    if args.account:
        try:
            dfu33 = rebalanceTrades(oq, dfu2, oanda0, str(args.account), dryrun=dryrun, leverage=leverage, verbose=verbose, noInteractive=noInteractive, noInteractiveLeverage=noInteractiveLeverage, noInteractiveDeleverage=noInteractiveDeleverage, noInteractiveFleetingProfits=noInteractiveFleetingProfits, sortRebalanceList=sortRebalanceList, loginIndex=loginIndex)
        except oandapy.OandaError as e:
            qd.exception(e)
            print 'Try a different account number'
    else:
        print 'using account 002: {0}'.format(accid)
        try:
            dfu33 = rebalanceTrades(oq, dfu2, oanda0, accid, dryrun=dryrun, leverage=leverage, verbose=verbose, noInteractive=noInteractive, noInteractiveLeverage=noInteractiveLeverage, noInteractiveDeleverage=noInteractiveDeleverage, noInteractiveFleetingProfits=noInteractiveFleetingProfits, threading=threading, sortRebalanceList=sortRebalanceList, loginIndex=loginIndex)
        except oandapy.OandaError as e:
            qd.exception(e)
        except Exception as e:
            qd.exception(e)

def getDryRun(args):
    
    if args.live:
        dryrun=False
    else:
        dryrun=True
    qd.data(dryrun, 'dryrun:')
    return dryrun


import flask
import ujson as json

app = flask.Flask(__name__)

@app.route('/')
def test():
    return 'everything is running\n'

@app.route('/live')
def live():
    """
    args.live = True
    args.noInteractiveDeleverage = False
    args.noInteractiveLeverage = False
    # ask how to sort the list
    # reverse[r[p=pl]] | deleverage[d[p=pl]] | leverage[l]
    #ans = raw_input('sortRebalanceList? r[p]/d[p]/l: ')
    #ans = ans.strip()
    ans = 'rp'
    if ans == 'r' or ans == 'rp' or ans == 'd' or ans == 'dp' or ans == 'l':
        args.sortRebalanceList = ans
    else:
        res = 'default to sorting by r'
    """
    #res = json.dumps(oanda0.get_accounts()['accounts'])
    #res2 = json.dumps(oanda0.get_positions(947325))
    trades = oanda0.get_trades(947325, count=500)['trades']
    #df = p.DataFrame(trades)
    #print df
    trades = json.dumps(trades)
    #return trades    
    resp = flask.Response(trades)
    #resp.headers['mode'] = 'no-cors'
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Content-Type'] = "application/json"
    resp.headers['Accept'] = "application/json"
    return resp
    #return '<pre>%s</pre>' % df.to_string()

@app.route('/accounts')
def accounts():
    
    try:
        import pymongo as mong
        mongo = mong.MongoClient()
        res = mongo.ql.broker_oanda_accounts.find().limit(1)
        for i in res:
            print i
        mongo.close()
    except Exception as e:
        return e
        
    return 'test'

"""
@app.route('/')
def test():
	import urllib2
	url = 'http://'
	response = urllib2.urlopen(url)
	html = response.read()
	ret = j.loads(html)
	#print ret
	return html
"""

if __name__ == "__main__":    
	
    if args.web:        
        host = '0.0.0.0'
        port = 8080
        print 'listening[host=%s, port=%s]' % (host, port)
        app.run(host=host, port=port)        
        sys.exit()
    
    if args.leverage:
        leverage=int(args.leverage)
    else:
        leverage=50

    if args.account:
        account= str(args.account)
    else:
        account='558788'

    def plotTransactionHistory(acc, oaoa):
        th = oaoa.get_transaction_history(acc)
        df = p.DataFrame()
        for i in th['transactions']:
            df = df.combine_first(p.DataFrame(i, index=[i['id']]).transpose())           
        df = df.transpose()
        #print df
        plot(df.ix[:,'accountBalance'].ffill()); show()

    """
    try:
        main(loginIndex, args, leverage=leverage, dryrun=dryrun)
    except Exception as e:
        qd.exception(e)
    """
    
    def modeAnalyze(args, runMain=False, description=None):
        args.analyze = True
        args.live = False
        dryrun = getDryRun(args)
        logApplicationUsage('modeAnalyze', description=description)
        if runMain:
            main(loginIndex, args, leverage=leverage, dryrun=dryrun)
        return dryrun

    def modeLeverage(args, runMain=False, description=None):
        # fleetingProfits mode
        args.live = True
        args.noInteractiveLeverage = True
        dryrun = getDryRun(args)
        logApplicationUsage('modeLeverage', description=description)
        if runMain:
            main(loginIndex, args, leverage=leverage, dryrun=dryrun)
        return dryrun

    def modeFleetingProfits(args, runMain=False, description=None):
        # fleetingProfits mode
        args.live = True
        args.noInteractiveFleetingProfits = True
        dryrun = getDryRun(args)
        logApplicationUsage('modeFleetingProfits', description=description)
        if runMain:
            main(loginIndex, args, leverage=leverage, dryrun=dryrun)
        return dryrun

    while True:
        print 'account: {0}'.format(accid)
        if args.interactive:
            usageOptions = """
as   = account status,
ca   = change account,
ct   = change threshold,
tr   = trades,
po   = positions,
a    = analyze,
d    = deleverage,
dl   = deleverage list
l    = leverage,
f    = fleetingProfits,
fd   = fleetingProfits [deleverage],
fr   = fleetingProfits [reverse entry],
cpt  = closeProfitableTrades,
il   = infinite-loop,
li   = live [interactive mode],
?, h = help,
q  = quit
"""
            usage = 'usage: '+usageOptions
            args = parser.parse_args()
            mode = raw_input('mode >>> ')
            if mode == 'q': # quit
                sys.exit()
            if mode == 'ca': # 
                accountIndex = raw_input('accountIndex? : ')
                try:
                    #with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
                    #    print acc
                    accid = acc.ix[int(accountIndex), 'accountId']
                except Exception as e:
                    qd.exception(e)
            if mode == 'ct': #
                closeProfitableTradesThreshold = raw_input('closeProfitableTradesThreshold? : ')
                try:
                    closeProfitableTradesThreshold = float(closeProfitableTradesThreshold)
                except Exception as e:
                    qd.exception(e)
            if mode == 'as': # 
                args.live = False
                with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
                    print p.DataFrame(oanda0.get_accounts()['accounts'])
                    print p.DataFrame(oanda0.get_account(947325), index=[0])
                sys.exit()
            if mode == 'tr': # 
                args.live = False
                with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
                    print p.DataFrame(oanda0.get_accounts()['accounts'])
                    print p.DataFrame(oanda0.get_trades(947325)['trades'])
                sys.exit()
            if mode == 'po': # 
                args.live = False
                with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
                    print p.DataFrame(oanda0.get_accounts()['accounts'])
                    print p.DataFrame(oanda0.get_positions(947325)['positions'])
                sys.exit()
            if mode == 'li': # 
                args.live = True
                args.noInteractiveDeleverage = False
                args.noInteractiveLeverage = False
                # ask how to sort the list
                # reverse[r[p=pl]] | deleverage[d[p=pl]] | leverage[l]
                ans = raw_input('sortRebalanceList? r[p]/d[p]/l: ')
                ans = ans.strip()
                if ans == 'r' or ans == 'rp' or ans == 'd' or ans == 'dp' or ans == 'l':
                    args.sortRebalanceList = ans
                else:
                    print 'default to sorting by r'
            if mode == 'a': # analyze mode
                logApplicationUsage(mode, description='manual')
                #args.analyze = True
                #args.live = False
                dryrun = modeAnalyze(args, runMain=False)
            if mode == 'd': # deleverage mode (risk-off / remove from positions)
                logApplicationUsage(mode, description='manual')
                ans = raw_input('Sure you want to deleverage? y/N: ')
                if ans == 'y':
                    args.live = True
                    args.noInteractiveDeleverage = True
                
            if mode == 'l': # leverage mode (risk-on / add to positions)
                logApplicationUsage(mode, description='manual')
                #args.live = True
                #args.noInteractiveLeverage = True
                dryrun = modeLeverage(args, runMain=False)
            if mode == 'f': # fleetingProfits mode (tp / take profits)
                logApplicationUsage(mode, description='manual')
                #args.live = True
                #args.noInteractiveFleetingProfits = True
                dryrun = modeFleetingProfits(args, runMain=False)

            if mode == 'cpt': # close profitable trades
                from qoreliquid import Patterns
                pa = Patterns(loginIndex=loginIndex)
                closeProfitableTrades                  = True
                monitorAccountsProfitableTradesVerbose = False
                try:
                    closeProfitableTradesThreshold = closeProfitableTradesThreshold
                except:
                    closeProfitableTradesThreshold = 0.69
                #if args.account:
                #      account = args.account
                #else: account= None
                # bind accid variable to account connecting - ca with cpt options
                account = accid
                pa.monitorAccountsProfitableTrades(verbose=monitorAccountsProfitableTradesVerbose, closeProfitableTrades=closeProfitableTrades, account=account, closeProfitableTradesThreshold=closeProfitableTradesThreshold)

            if mode == 'il': # infinite-loop
                description='infinite-loop'
                logApplicationUsage(mode, description=description)
                ilWait = 30
                cnt = 1
                # initial analyze routine is called
                modeAnalyze(args, runMain=True, description=description)
                while True:
                    # close trades run modeFleetingProfits
                    dryrun = modeFleetingProfits(args, runMain=True, description=description)
                    # run analyzer every minute
                    if cnt % int(15 * 60.0 / ilWait) == 0:
                        dryrun = modeAnalyze(args, runMain=True, description=description)
                    # open trades run modeLeverage
                    dryrun = modeLeverage(args, runMain=True, description=description)
                    print 'infinite-loop[count]:%s' % cnt
                    cnt += 1
                    time.sleep(ilWait)

            if mode == '?' or mode == 'help' or mode == 'h': # help
                print usage
                continue
            qd.data(mode, name='mode:')
            qd.data(live, name='live:')
            qd.data(args.noInteractiveLeverage, name='noInteractiveLeverage:')
            qd.data(args.noInteractiveDeleverage, name='noInteractiveDeleverage:')
            qd.data(args.noInteractiveFleetingProfits, name='noInteractiveFleetingProfits:')

        #if args.live:
        #    dryrun=False
        #else:
        #    dryrun=True
        #if int(args.verbose) >= 5:
        #    print 'dryrun: %s' % dryrun
        dryrun = getDryRun(args)

        try:
            if args.history:
                #plotTransactionHistory(account, oanda0)
                try:
                    try:
                        historyFilename = args.historyFilename
                    except:
                        historyFilename = '/home/qore2/Desktop/f566016f51bde41a6c6fd2b4ec74cd82.csv'
                    df = p.read_csv(historyFilename)
                    dfi = df.sort_values(by='Transaction ID', ascending=True)
                except:
                    dfi = p.DataFrame([])
                with p.option_context('display.max_rows', 20000, 'display.max_columns', 4000, 'display.width', 1000000):
                    if args.historyIndex:
                        historyIndex = int(args.historyIndex)
                        dfi = dfi.ix[historyIndex:0,:]
                    print dfi#.columns
                    dfii = dfi.ix[:,'Transaction ID;Balance;Time (UTC)'.split(';')]#.tail(5)#.transpose()
                    #dfii['time'] = oq.oandaToTimestamp(dfii['Time (UTC)'])
                    dfp = dfii.ix[:,['Balance','Time (UTC)']].set_index('Time (UTC)')
                    dfp.plot()
                    show()
            else:
                main(loginIndex, args, leverage=leverage, dryrun=dryrun)
        except Exception as e:
            qd.exception(e)
        if not args.interactive:
            break
