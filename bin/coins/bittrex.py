
import sys
try: sys.path.index('/ml.dev/bin')
except: sys.path.append('/ml.dev/bin')

from qore import ZZZ

class Bittrex(ZZZ):

    def receiveJson(self, mtype='fills', view=None, currency=None):
        import pandas as p
        import ujson as uj
        di = {
            'buys':'Buys',
            'sells':'Sells',
            'fills':'Fills',
        }
        #if mtype == 'fills':
        #    mtype = di[mtype]
        print mtype
        print di[mtype]
        dfm = p.DataFrame([])
        if di[mtype] == 'Fills':
            ascending = False
        if di[mtype] == 'Buys':
            ascending = True
        if di[mtype] == 'Sells':
            ascending = False
        stat = {}
        while True:
            res = self.socketClient.recv(0)
            res = uj.loads(res)
            #print res.keys()
            mn = res['MarketName']
            try: stat[mn] += 1
            except: stat[mn] = 0
            if mn == currency:
                #pass
                ''
            print mn
            if view == 'stats':
                print p.DataFrame(stat, index=['num']).transpose().sort_values(by='num', ascending=False).head(5) #.sort_index()
            else:
                #print res
                df = p.DataFrame(res[di[mtype]])
                try:    df = df.set_index('Rate')
                except: ''
                #dfm = dfm.combine_first(df)
                dfm = df.combine_first(dfm)
                cnt = len(df.index)
                if cnt > 0:
                    print '==='
                    #print dfm.sort_values(by='Rate', ascending=ascending).head(10)
                    print dfm[dfm['Quantity'] > 0].sort_index(ascending=ascending).tail(20)
            #print di[mtype]
            #print p.DataFrame(res['Buys'])
            #print '---'
            #print p.DataFrame(res['Sells'])
            #print '---'
            #print p.DataFrame(res['Fills'])
    

if __name__ == "__main__":
    
    
    import argparse
    # source: https://docs.python.org/2/howto/argparse.html
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", '--verbose', help="turn on verbosity")
    parser.add_argument("-c", '--client', help="parseCoinMrketCap skipTo", action="store_true")
    parser.add_argument("-m", '--markets', help="parseCoinMrketCap skipTo", action="store_true")
    parser.add_argument("-t", '--type', help="parseCoinMrketCap skipTo")
    parser.add_argument("-s", '--stats', help="parseCoinMrketCap skipTo", action="store_true")
    parser.add_argument("-cu", '--currency', help="parseCoinMrketCap skipTo")
    
    args = parser.parse_args()

    if args.type:
        mtype = args.type

    if args.currency:
        currency = args.currency

    if args.client:
        z = Bittrex()
        z.initClient(port=3000, subject='')
        view = None
        if args.stats:
            view = 'stats'
        try:    z.receiveJson(mtype=mtype, view=view, currency=currency)
        except: z.receiveJson(mtype=mtype, view=view)
    
    if args.markets:
        from bitmex import apiRequest
        import pandas as p
        res = apiRequest('https://bittrex.com/api/v1.1', '/public/getmarkets')
        res = p.DataFrame(res['result'])#.set_index('MarketName')
        print ','.join(list(res['MarketName']))
        #print res
