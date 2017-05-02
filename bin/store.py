#!/usr/bin/env python

import argparse
# source: https://docs.python.org/2/howto/argparse.html
parser = argparse.ArgumentParser()
parser.add_argument("-ca",   '--canonicalAsins',                  help="web scrapes trending asin data from amazon. prints asin data along with relevant metrics, urls and descriptions", action="store_true")
parser.add_argument("-cad",  '--canonicalAsinsDetail',            help="prints a list of trending asins along with relevant metrics", action="store_true")
parser.add_argument("-all",  '--bestSellersAll',                  help="converts best sellers mjson list to expanded csv file", action="store_true")
parser.add_argument("-cadm", '--canonicalAsinsDetailMetrics',     help="web scrapes relevant metrics for asins", action="store_true")
parser.add_argument("-l",    '--limit',                           help="tail limit")
parser.add_argument("-s",    '--sort',                            help="sort")
parser.add_argument("-d",    '--descending',                      help="descending", action="store_true")
parser.add_argument("-ci",   '--createInventory',                 help="createInventory", action="store_true")
args = parser.parse_args()

"""
In [69]: li = 'amz'
In [70]: li = list(li)
In [71]: li.append('o')
In [72]: li.append('n')
In [73]: li
Out[73]: ['a', 'm', 'z', 'o', 'n']
In [74]: li.insert(2, 'a')

In [69]: li = 'amz'
In [70]: li = list(li)
In [71]: li.append('o')
In [72]: li.append('n')
In [73]: li
Out[73]: ['a', 'm', 'z', 'o', 'n']
In [74]: li.insert(2, 'a')
"""

#//*[@id="zg_left_col1"]/div[1]/div[2]/div/div[2]
#//*[@id="zg_centerListWrapper"]/div[2]/div[2]/div/a/div[1]/img
#//*[@id="zg_left_col1"]/div[1]/div[2]/div/div[2]

from qore import QoreDebug
qd = QoreDebug()
qd.on()

import re
import requests as req
import time     as tt
import pandas   as p
from lxml       import html
import ujson    as uj

class AMZ:

    def xpath2dataframe(self, xpath, txt, columns=None, replace=[]):
        tree = html.fromstring(txt)
        #xres = tree.xpath(xpath)
        print xpath
        xres = []
        try:
            xres.append(tree.xpath(xpath))
        except:
            for i in xpath:
                print i
                try:
                    gr = re.match(re.compile(r'.*?(([\d]+):([\d]+)).*'), i).groups()
                    #print gr
                    vals = []
                    dvals = {}
                    for j in range(int(gr[1]), int(gr[2])+1):
                        xpi = re.sub(re.compile(r'(.*?)([\d]+):([\d]+)(.*)'), '\\1%s\\4', i)
                        #print xpi
                        res = tree.xpath(xpi % j)
                        #print res
                        try:    val = res[0]
                        except: val = ''
                        xp = xpi % j
                        #print '%s : %s' % (xp, val)
                        vals.append(val)
                        dvals.update({j-int(gr[1]): val})
                        #xres.append(tree.xpath(xpi % j))
                    #print vals
                    #print dvals
                    xres.append(vals)
                except Exception as e:
                    #print e
                    #qd.printTraceBack()
                    #print i
                    xres.append(tree.xpath(i))
        #print xres
        #df = p.DataFrame(xres, columns=[0])
        #print len(xres)
        #print xres
        #print columns
        df = p.DataFrame(xres, index=columns).transpose()
        #df = p.DataFrame(xres, index=list(range(0,len(xres)))).transpose()
        #df = p.DataFrame({0:xres,1:xres}, index=[0,1]).transpose()
        if len(replace) == 2:
            try:
                for i in df.columns:
                    df[i] = map(lambda x: x.replace(replace[0], replace[1]).strip(), df[i])
            except Exception as e:
                print e
        return df

    def __init__(self):
        ''
        
    def init(self):
        level = 0
        msleep = 3
        domain = 'amazon.com'
        initUrl = 'https://www.%s/Best-Sellers/zgbs' % domain
        print
        print '-- initUrl:%s --' % initUrl
        #print '%s' % initUrl
        res = req.get(initUrl)
        df    = self.xpath2dataframe('//*[@id="zg_browseRoot"]/ul/li/a/@href', res.text)
        df[0] = map(lambda x: re.sub(re.compile(r'http.*?Sellers-(.*)', re.I), '\\1', x), df[0])
        if len(df.index) > 0:
            with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
                print 'df'
                print df
        
        ilevel = len(df[0]) if level == 0 else level
        for i in range(len(df[0][0:ilevel])): #for i in df[0][0:level]:
            tt.sleep(msleep)
            print
            print '    -- i:%s --' % df[0][i] #print '    -- i:%s --' % i
            #print '    %s' % df[0][i] #print '    %s' % i
            res = req.get('https://www.%s/Best-Sellers-%s' % (domain, df[0][i])) #, proxies=proxies) #res = req.get(i) #, proxies=proxies)
            dfi = self.xpath2dataframe('//*[@id="zg_browseRoot"]/ul/ul/li/a/@href', res.text)
            dfi[0] = map(lambda x: re.sub(re.compile(r'http.*?Sellers-(.*)'), '\\1', x), dfi[0])
            if len(dfi.index) > 0:
                with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
                    print 'dfi = df[%s]' % i
                    print dfi
                df.ix[i,1] = uj.dumps(list(dfi[0]))
            
            jlevel = len(dfi[0]) if level == 0 else level
            for j in range(len(dfi[0][0:jlevel])): #for j in dfi[0][0:level]:
                tt.sleep(msleep)
                print
                print '        -- j:%s --' % dfi[0][j] #print '        -- j:%s --' % j
                #print '        %s' % dfi[0][j] #print '        %s' % j
                res = req.get('https://www.%s/Best-Sellers-%s' % (domain, dfi[0][j])) #, proxies=proxies) #res = req.get(j) #, proxies=proxies)
                dfj = self.xpath2dataframe('//*[@id="zg_browseRoot"]/ul/ul/ul/li/a/@href', res.text)
                dfj[0] = map(lambda x: re.sub(re.compile(r'http.*?Sellers-(.*)'), '\\1', x), dfj[0])
                if len(dfj.index) > 0:
                    with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
                        print 'dfj = dfi[%s]' % j
                        print dfj
                    dfi.ix[j,1] = uj.dumps(list(dfj[0]))
                
                try:
                    klevel = len(dfj[0]) if level == 0 else level
                    """
                    for k in range(len(dfj[0][0:klevel])): #for k in dfj[0][0:level]:
                        #tt.sleep(msleep)
                        print
                        print '            -- k:%s --' % dfj[0][k] #print '            -- k:%s --' % k
                        #print '            %s' % dfj[0][k] #print '            %s' % k
                        res = req.get('https://www.%s/Best-Sellers-%s' % (domain, dfj[0][k])) #, proxies=proxies) #res = req.get(k) #, proxies=proxies)
                        dfk = self.xpath2dataframe('//*[@id="zg_browseRoot"]/ul/ul/ul/li/a/@href', res.text)
                        dfk[0] = map(lambda x: re.sub(re.compile(r'http.*?Sellers-(.*)'), '\\1', x), dfk[0])
                        if len(dfk.index) > 0:
                            with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
                                print 'dfk = dfj[%s]' % k
                                print dfk
                            dfj.ix[k,1] = uj.dumps(list(dfk[0]))
                        print '            -- end:k: --'
                        print '            =================================================='
                    """
                except Exception as e:
                    print e

                if len(dfj.index) > 0:
                    with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
                        print 'dfj = dfi[%s]' % j
                        print dfj
                    dfi.ix[j,1] = uj.dumps(dfj.fillna(0).to_dict())
                print '        -- end:j: --'
                print '        =================================================='
            
            if len(dfi.index) > 0:
                with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
                    print 'dfi = df[%s]' % i
                    print dfi
                df.ix[i,1] = uj.dumps(dfi.fillna(0).to_dict())
                df.to_csv('/opt/data/amz-best-sellers.csv')
                df.to_json('/opt/data/amz-best-sellers.json')
            print '    -- end:i: --'
            print '    =================================================='

        print '=================================================='

        if len(df.index) > 0:
            with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
                print 'df'
                print df
                df.to_csv('/opt/data/amz-best-sellers.csv')
                df.to_json('/opt/data/amz-best-sellers.json')

    def updatecsv(self, fname, df):
        try:
            canonicalAsinsDF = p.read_csv(fname, index_col=0)
        except:
            canonicalAsinsDF = p.DataFrame([])
        canonicalAsinsDF = canonicalAsinsDF.combine_first(df)
        canonicalAsinsDF.to_csv(fname, encoding='utf-8')
        return canonicalAsinsDF

    def we23(self, dfi, field, replace):
        for i in dfi.index:
            try: 
                for j in replace:
                    dfi.ix[i,field] = dfi.ix[i,field].replace(j[0],j[1])
                #dfi.ix[i,field] = dfi.ix[i,field].replace('$','')
                #dfi.ix[i,field] = dfi.ix[i,field].replace(',','')
            except Exception as e:
                #print e
                dfi.ix[i,field] = 0
        dfi[field]      = p.to_numeric(dfi[field])
        return dfi[field]

    def bestSellersAll(self):
        qd = QoreDebug()
        qd.on()
        qd.stackTraceOn()
        fname = '/opt/data/amz-best-sellers.all.csv'
        df = p.read_csv('/opt/data/amz-best-sellers.csv', index_col=0)
        #with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
        #    print df.sort_index()
            
        li = []
            
        #print
        for i in range(len(df['1'])):
            #print '---------'
            #print df['0'][i]
            li.append(df['0'][i])
            try:
                dfi = uj.loads(df['1'][i])
                dfi = p.DataFrame(dfi)
                dfi['index'] = p.to_numeric(dfi.index)
                dfi = dfi.set_index('index')
                #with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
                #    print dfi.sort_index()
                for j in range(len(dfi['1'])):
                    #print '   ------'
                    #print '   %s' % dfi['0'][j]
                    li.append(dfi['0'][j])
                    jtxt = dfi['1'][j]
                    try:
                        dfj = uj.loads(jtxt)
                        dfj = p.DataFrame(dfj)
                        dfj['index'] = p.to_numeric(dfj.index)
                        dfj = dfj.set_index('index')
                        #with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
                        #    print dfj.sort_index()
                        for k in range(len(dfj['1'])):
                            #print '      ---'
                            #print '      %s' % dfj['0'][k]
                            li.append(dfj['0'][k])
                            dfk = uj.loads(dfj['1'][k])
                            dfk = p.DataFrame(dfk)
                            dfk['index'] = p.to_numeric(dfk.index)
                            dfk = dfk.set_index('index')
                            #with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
                            #    print dfk.sort_index()
                    except Exception as e:
                        #print e
                        ''
                    #print
                #print
            except Exception as e:
                #qd.printTraceBack()
                ''
            #print
        
        dfli = p.DataFrame(li)
        print dfli
        #for i in dfli.index:
        #    print dfli.ix[i, :][0]
        dfli.to_csv(fname, encoding='utf-8')
        print 'Saved to: %s' % fname


    def canonicalAsins(self):
        domain = 'amazon.com'
        df     = p.read_csv('/opt/data/amz-best-sellers.all.csv', index_col=0)
        level = 0
        crawlTime = tt.time()
        #ilevel = len(df)
    
        ilevel = len(df['0']) if level == 0 else level
        for i in range(len(df['0'][0:ilevel])): #for i in df[0][0:level]:
            url = 'https://www.%s/Best-Sellers-%s' % (domain, df['0'][i])
            print url
            res = req.get(url) #, proxies=proxies) #res = req.get(i) #, proxies=proxies)
            xps = [
                '//*[@id="zg_centerListWrapper"]/div/div[2]/div/a/div[2]/text()',
                '//div[2:21]/div[2]/div/div[1]/a[1]/i/span/text()',
                #'//div[2:21]/div[2]/div/div[2]/span[1]/span/text()', # 1
                '//div[2:21]/div[2]/div/div[2]/span/text()', # 2
                '//*[@id="zg_centerListWrapper"]/div[2:21]/div[2]/div/div[1]/a[2]/text()',
                '//*[@id="zg_centerListWrapper"]/div[2:21]/div[2]/div/div[1]/a[2]/@href',
                '//*[@id="zg_centerListWrapper"]/div/div[2]/div/a/div[1]/img/@src',
                '//*[@id="zg_centerListWrapper"]/div/div[2]/div/a/@href',
            ]
            cols = [
                'name',
                'stars',
                'cost',
                'reviews',
                'asin',
                'img',
                'url',
            ]
            dfi = self.xpath2dataframe(xps, res.text, columns=cols, replace=['\n',''])
            dfi2 = self.xpath2dataframe([
                '//link[@rel="canonical"]/@href',
            ], res.text, replace=['\n',''])
            try:
                canonical = list(dfi2[0])[0]
                # xpath debug
                #print res.text
                #with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
                #    print dfi
                dfi['canonical'] = (map(lambda x: x.replace('https://www.amazon.com/',''), [canonical] * len(dfi.index)))
        
                """
                for i in dfi.index:
                    try: dfi.ix[i,'stars'] = dfi.ix[i,'stars'].replace(' out of 5 stars','')
                    except Exception as e:
                        print e
                        dfi.ix[i,'stars'] = 0
                dfi['stars']      = p.to_numeric(dfi['stars'])
                """
                dfi['stars']     = p.to_numeric(map(lambda x: x.replace(' out of 5 stars',''), dfi['stars']))
        
                """
                for i in dfi.index:
                    try: 
                        dfi.ix[i,'cost'] = dfi.ix[i,'cost'].replace('$','')
                        dfi.ix[i,'cost'] = dfi.ix[i,'cost'].replace(',','')
                    except Exception as e:
                        print e
                        dfi.ix[i,'cost'] = 0
                dfi['cost']      = p.to_numeric(dfi['cost'])
                """
                try:
                    dfi['cost']      = self.we23(dfi, 'cost', [['$',''],[',','']])
                except:
                    ''
                #dfi['cost']      = p.to_numeric(map(lambda x: x.replace('$',''), dfi['cost']))
        
                """
                for i in dfi.index:
                    try:
                        dfi.ix[i,'reviews'] = dfi.ix[i,'reviews'].replace(',','')
                    except Exception as e:
                        print e
                        dfi.ix[i,'reviews'] = 0
                dfi['reviews']      = p.to_numeric(dfi['reviews'])
                """
                dfi['reviews']   = p.to_numeric(map(lambda x: x.replace(',',''), dfi['reviews']))
        
                dfi['productReviews'] = dfi['asin']
                dfi['asin']      = (map(lambda x: x.replace('/product-reviews/',''), dfi['asin']))
                dfi['asinUrl']   = (map(lambda x: 'https://www.amazon.com/dp/%s'%(x), dfi['asin']))
                dfi['url']       = (map(lambda x: 'https://www.amazon.com/%s'%(x), dfi['url']))
                dfi['crawlTime'] = crawlTime
                for i in range(len(dfi.index)):
                    dfi.ix[i, 'canonicalAsin'] = '%s-%s' % (dfi.ix[i, 'canonical'], dfi.ix[i, 'asin'])
        
                with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
                    #print dfi
                    print dfi.ix[:, 'name cost stars reviews asin asinUrl'.split(' ')]
                print '----------------------------------------------------------------'
                dfi = dfi.set_index('canonicalAsin')
                dfi = self.updatecsv('/opt/data/amz-canonicalasins-detail.csv', dfi)
                #print list(dfi.index)
                #print list(dfi.columns)
                dfij = dfi.ix[p.unique(dfi.index), :]
                dfij = dfij.reset_index()
                #print dfij
                dfij.to_json('/opt/data/amz-canonicalasins-detail.json')
                
        
                canonicalAsinsDF = self.updatecsv('/opt/data/amz-canonicalasins.csv', p.DataFrame({canonical: [list(dfi['asin'])]}, index=['asin']).transpose())
                canonicalAsinsDF.to_json('/opt/data/amz-canonicalasins.json')
                #print canonicalAsinsDF
        
                #with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
                #    print dfi
                print '=================================================='
            except Exception as e:
                ''

    def setArgs(self, args):

        self.args = args

        try:    self.limit = int(args.limit)
        except: self.limit = 10
    
        try:
            self.sort = (args.sort)
            if self.sort == None:
                raise
        except: self.sort = 'reviews'
        
        print args
        
    def canonicalAsinsDetail(self, limit=None, sort=None):
        import numpy as n
        import re
        if limit != None:
            self.limit = limit
        if sort != None:
            self.sort = sort
        dfli = p.read_csv('/opt/data/amz-canonicalasins-detail.csv', index_col=0)
        dfli['dp'] = map(lambda x: 'https://www.amazon.com/dp/%s' % x, dfli['asin'])
        dfli['timeNow'] = tt.time()
        dfli['timeDiff'] = dfli['timeNow'] - dfli['crawlTime']
        #dfli['cost'] = p.to_numeric(dfli['cost'])
        #dfli['cost'] = map(lambda x: max(x.replace('-', '').split(' ')), dfli['cost'])
        dfli = dfli.sort_values(by=self.sort, ascending=not self.args.descending)
        dfli = dfli.tail(self.limit)

        dfliCost = n.array(dfli['cost'])
        for i in xrange(len(dfliCost)):
            try:
                #dfli['cost'][i]
                #li = dfli.loc[i, 'cost']
                #li = dfli.ix[i, 'cost']
                #li = dfli['cost'][i]
                li = dfliCost[i]
                
                li = li.replace('-', '')
                li = re.sub(re.compile(r'[\s]+'), ' ', li)
                #print 'preli: %s' % li
                li = li.split(' ')
                #print 'lipossplit: %s' % li
                li = n.array(li, dtype=n.float)
                #print 'liposnaaray: %s' % li
                #print 'maxli: %s' % n.max(li)
                dfliCost[i] = n.max(li)
            except Exception as e:
                #print e
                ''
            #print 'i: %s' % i
        dfli['cost'] = dfliCost
        dfli['cost'] = dfli['cost'].fillna(0)
        
        with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 10000000):
            df = dfli.ix[:,'asin productReviews stars cost reviews dp crawlTime timeDiff'.split(' ')].sort_values(by=self.sort, ascending=not self.args.descending)
            print 'limit: %s' % self.limit
            print 'len: %s' % len(df.index)
            print df
            #print df.head(50)
            #print df['cost']
            print dfli.dtypes

    def canonicalAsinsDetailMetrics(self):

        from seo import SEO

        dfli = p.read_csv('/opt/data/amz-canonicalasins-detail.csv', index_col=0)
        dfli['dp'] = map(lambda x: 'https://www.amazon.com/dp/%s' % x, dfli['asin'])
        #with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
        #    print dfli.ix[:,'asin productReviews stars cost reviews dp'.split(' ')].sort_values(by='reviews')
        #for i in dfli['0']:
            #print 'https://www.amazon.com/Best-Sellers-%s' % i
        
        seo = SEO()
        di = {}
        mdf = p.DataFrame()
        for i in dfli.index:
            print dfli.ix[i, 'dp']
            px = seo.proxyServers(True, 10)
            proxy = '%s://%s:%s'%(px['schema'], px['host'], px['port'])
            print 'proxy:%s' % proxy
            proxies = {
                #'http': 'http://217.76.204.197:8080',
                #'http': 'http://128.199.169.17:80',
                # http://stackoverflow.com/questions/30286293/make-requests-using-python-over-tor        
                'http': proxy,
                #'http': 'http://127.0.0.1:8118',
                #'http': 'socks5://localhost:9050',
                #'https': 'socks5://localhost:9050',
            }
            res = req.get(dfli.ix[i, 'dp'], proxies=proxies)
            tree = html.fromstring(res.text)
            #xres = tree.xpath('//tr[3]/td/span/span[1]/text()')
            xres = tree.xpath('//li[@id="SalesRank"]/text()')
            xres = map(lambda x: x.replace('\n', '').strip(), xres)
            try:
                #print xres[1]
                #print xres
                reg = re.match(re.compile(r'#([\d]+) in (.*?) \(.*'), xres[1]).groups()
                #print reg
                #print reg[0]
                di.update({'asin': dfli.ix[i, 'dp']})
                di.update({'abr': reg[0]})
                di.update({'in': reg[1]})
                mdf = mdf.combine_first(p.DataFrame(di, index=[dfli.ix[i, 'asin']]))
            except Exception as e:
                print e
                print res.text
            break
        #print di
        print mdf
        mdf = self.updatecsv('/opt/data/amz-canonicalasins-detail-metrics.csv', mdf)
        return mdf
    
    # TODO: write implementation
    def createInventory(self):
        self.canonicalAsinsDetail(20, 'stars')
        ''

if __name__ == "__main__":

    a = AMZ()
    a.setArgs(args)

    # web scrapes trending asin data from amazon
    # prints asin data along with relevant metrics, urls and descriptions
    if args.canonicalAsins:
        a.canonicalAsins()
        
    # prints a list of trending asins along with relevant metrics
    if args.canonicalAsinsDetail:
        a.canonicalAsinsDetail()

    # Extract more asin relevant metrics
    if args.canonicalAsinsDetailMetrics:
        a.canonicalAsinsDetailMetrics()

    # create inventory
    if args.createInventory:
        a.createInventory()

    if args.bestSellersAll:
        a.bestSellersAll()
