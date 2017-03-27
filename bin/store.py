#!/usr/bin/env python

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
        xres = []
        try:
            xres.append(tree.xpath(xpath))
        except:
            for i in xpath:
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
            print '    -- end:i: --'
            print '    =================================================='

        print '=================================================='

        if len(df.index) > 0:
            with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
                print 'df'
                print df
                df.to_csv('/opt/data/amz-best-sellers.csv')

    def updatecsv(self, fname, df):
        try:
            canonicalAsinsDF = p.read_csv(fname, index_col=0)
        except:
            canonicalAsinsDF = p.DataFrame([])
        canonicalAsinsDF = canonicalAsinsDF.combine_first(df)
        canonicalAsinsDF.to_csv(fname, encoding='utf-8')
        return canonicalAsinsDF

if __name__ == "__main__":
    a = AMZ()

    domain = 'amazon.com'
    ilevel = 5
    df     = p.read_csv('/opt/data/amz-best-sellers.all.csv', index_col=0)
    
    for i in range(len(df['0'][0:ilevel])): #for i in df[0][0:level]:
        url = 'https://www.%s/Best-Sellers-%s' % (domain, df['0'][i])
        print url
        res = req.get(url) #, proxies=proxies) #res = req.get(i) #, proxies=proxies)
        xps = [
            '//*[@id="zg_centerListWrapper"]/div/div[2]/div/a/div[2]/text()',
            '//div/div[2]/div/div[1]/a[1]/i/span/text()',
            '//div/div[2]/div/div[2]/span[1]/span[1]/text()',
            '//*[@id="zg_centerListWrapper"]/div/div[2]/div/div[1]/a[2]/text()',
            '//*[@id="zg_centerListWrapper"]/div/div[2]/div/div[1]/a[2]/@href',
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
        dfi = a.xpath2dataframe(xps, res.text, columns=cols, replace=['\n',''])
        dfi2 = a.xpath2dataframe([
            '//link[@rel="canonical"]/@href',
        ], res.text, replace=['\n',''])
        canonical = list(dfi2[0])[0]
        with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
            print dfi
        print '----------------------------------------------------------------'
        dfi['canonical'] = (map(lambda x: x.replace('https://www.amazon.com/',''), [canonical] * len(dfi.index)))
        dfi['stars']     = p.to_numeric(map(lambda x: x.replace(' out of 5 stars',''), dfi['stars']))
        dfi['cost']      = p.to_numeric(map(lambda x: x.replace('$',''), dfi['cost']))
        dfi['reviews']   = p.to_numeric(map(lambda x: x.replace(',',''), dfi['reviews']))
        dfi['asin']      = (map(lambda x: x.replace('/product-reviews/',''), dfi['asin']))
        dfi['asinUrl']   = (map(lambda x: 'https://www.amazon.com%s'%(x), dfi['asin']))
        dfi['url']       = (map(lambda x: 'https://www.amazon.com%s'%(x), dfi['url']))
        for i in range(len(dfi.index)):
            dfi.ix[i, 'canonicalAsin'] = '%s-%s' % (dfi.ix[i, 'canonical'], dfi.ix[i, 'asin'])
        dfi = dfi.set_index('canonicalAsin')
        dfi = a.updatecsv('/opt/data/amz-canonicalasins-detail.csv', dfi)

        canonicalAsinsDF = a.updatecsv('/opt/data/amz-canonicalasins.csv', p.DataFrame({canonical: [list(dfi['asin'])]}, index=['asin']).transpose())
        print canonicalAsinsDF

        print dfi.dtypes
        with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
            print dfi
        print '=================================================='
