# -*- coding: utf-8 -*-

import pandas as p

class SEO:
    
    fnameProxies = '/mldev/lib/DataPipeline/data/proxies_numbeo.csv'
    
    def __init__(self):
        ''

    def allInTitle(self, srch):
        import requests as req
        import re
        # http://docs.python-guide.org/en/latest/scenarios/scrape/
        from lxml import html
        # https://www.youtube.com/watch?v=yguaBk1JLsU

        srch = srch.replace(' ', '+')
        #srch = 'cheap+flights'
        yrl = 'http://www.google.com/search?q=allintitle%3A%22{0}%22&oq=allintitle%3A%22{1}%22'.format(srch, srch)
        #yrl = 'http://www.google.com'
        #print yrl
        
        # google proxies
        # http://proxies4google.com/packages-pricing/

        while True:
            px = self.proxyServers(True, 1)
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
            try:
                res = req.get(yrl, proxies=proxies)
                #print res.text
                tree = html.fromstring(res.text)
                xres = tree.xpath('//*[@id="resultStats"]/text()')
            except Exception as e:
                print e
                self.flagServer(px['host'], px['port'], method='cannot_connect_to_proxy')
                return {'proxies':proxies, 'error':e}
            break
        msg = ''
        if res.text.strip() == 'Authentication required':
            msg = res.text.strip()
            px = self.setAuthorizationRequired(host=px['host'], port=px['port'])
        try:
            xres = float(re.match(r'.*?([\d\.\,]+).*', xres[0]).groups()[0].replace('.', '').replace(',', ''))
            #print self.testGoogle(res.text)
        except Exception as e:
            #return res.text
            print '==============================='
            if res.text.strip() != 'Authentication required':
                res = self.testGoogle(res.text)
                print res
                self.setBlockedServers(px['host'], px['port'])
            print '==============================='
        #return {'allintitleResults':xres, 'proxies':proxies}
        res = {'allintitleResults':xres, 'msg':msg}
        res.update(px)
        return res
    
    def testGoogle(self, res):
        from lxml import html
        import re
        tree = html.fromstring(res)
        #print res.text
        #print tree.xpath('//div/text()')
        #print
        xp = tree.xpath('//div/text()')
        try:
            print xp[5]
        except Exception as e:
            #print e
            ''
        try:
            print xp[6]
        except Exception as e:
            #print e
            ''
        try:
            print xp[7]
        except Exception as e:
            #print e
            ''
        try:
            print xp[8]
        except Exception as e:
            #print e
            ''
        try:
            print xp[9]
        except Exception as e:
            #print e
            ''
        try:
            #import re
            ip = xp[11].replace('IP address: ', '').strip()
            #print ip
            #print re.match(re.compile(r'.+?([\d\.]+).+?'), xp[11]).group()
    
            if 'block' == re.match(re.compile(r'.*?(block).*', re.S), xp[8]).groups()[0]:
                return {'isBlocked': True, 'ip': ip}
            else:
                return {'isBlocked': False, 'ip': ip}
        except Exception as e:
            #print e
            return {'error':e}
            

    def flagServer(self, host, port, method=None, boolean=True):

        print 'flagging server: %s:%s %s[%s]' % (host, port, method, boolean)
        px = p.read_csv(self.fnameProxies, index_col=0)
        if not px.index.is_monotonic_increasing:
            px = p.read_csv(self.fnameProxies)
        #print px

        rpx = px[px['host']   == host]
        rpx = rpx[rpx['port'] == port]
        bid = rpx.index[0]
        px.ix[bid, method] = boolean
        px[method] = px[method].fillna(False)
        px.to_csv(self.fnameProxies)
        """
        if method == 'blocked_google.com':
            # set the blocked server
            rpx = px[px['host']   == host]
            rpx = rpx[rpx['port'] == port]
            bid = rpx.index[0]
            px.ix[bid, method] = boolean
            px[method] = px[method].fillna(False)
            px.to_csv(self.fnameProxies)

        if method == 'authorizationRequired':
            # authorization required
            rpx = px[px['host'] == host]
            rpx = rpx[rpx['port'] == port]
            bid = rpx.index[0]
            px.ix[bid, method] = boolean
            px[method] = px[method].fillna(False)
            px.to_csv(self.fnameProxies)
        """

        return px

    def setBlockedServers(self, host, port, blocked=True, method='blocked_google.com'):

        px = self.flagServer(host, port, method=method)

        return px

    def setAuthorizationRequired(self, host, port, method='authorizationRequired'):
        
        px = self.flagServer(host, port, method=method)

        return px

    def proxyServers(self, random=True, num=10):
        import random as rr
        px = p.read_csv(self.fnameProxies, index_col=0)
        if not px.index.is_monotonic_increasing:
            px = p.read_csv(self.fnameProxies)
        #print px
        
        try: px = px[px['blocked_google.com']      == False]
        except: ''
        try: px = px[px['authorizationRequired']   == False]
        except: ''
        try: px = px[px['cannot_connect_to_proxy'] == False]
        except: ''
        px = px[px['ssl']                     == False]

        px = px.sort_values(by=['reliability', 'latency'], ascending=[False, True]).head(num).ix[:, 'host port'.split(' ')]
        px['hostPort'] = map(lambda x: '%s:%s'%(px.ix[x, 'host'], px.ix[x, 'port']), px.index)
        px['schema'] = 'http'
        px = px.ix[:, 'hostPort host port schema'.split(' ')]
        #print px
        if random:
            #rint = rr.randint(0,10-1)
            rint = rr.choice(px.index)
            #print px
            #print dict(px.transpose()[rint])
            #return {'url':'http://'+rr.choice(px)}
            #return {'url':'http://'+px.ix[rint, 'hostPort']}
            px = dict(px.transpose()[rint])
            return px
        else:
            return px    

    def populateAllintitle(self, fname):
        import pandas as p
        #fname = '/opt/data/seo/cheap-flights_Keyword Planner 2017-02-18 at 22-27-36.csv'
        #fname = '/opt/data/seo/cheap-flights_Keyword Planner 2017-02-18 at 22-31-30.3.csv'
        #fname = '/opt/data/seo/cheap-flights_Keyword Planner 2017-02-19 at 00-25-52.csv'
    
        csv = p.read_csv(fname, index_col=0)
        if not csv.index.is_monotonic_increasing:
            csv = p.read_csv(fname)
    
        allintitles = {}
    
        try:
            csv['allintitle'] = csv['allintitle'].fillna(0)
            pcsv = csv[csv['allintitle'] == 0]
        except:
            pcsv = csv
    
        lcsv = list(pcsv.ix[:, 'Keyword'])
        print len(lcsv)
        #from multiprocessing.pool import ThreadPool
        #try:
        """
            pool = ThreadPool(processes=270)
            for i in lcsv[0:50]:
                async_result = pool.apply_async(allInTitle, [i])
                allintitle   = async_result.get()['allintitleResults']
                #allintitle = allInTitle(i)['allintitleResults']
                print '%s: %s' % (i, allintitle)
                allintitles.update({i: allintitle})
            pool.close()
        """
        #except:
        for i in lcsv[0:50]:
            allintitle = self.allInTitle(i)
            #print 
            #print allintitle
            try:
                allintitle = allintitle['allintitleResults']
                print '%s: %s' % (i, allintitle)
                allintitles.update({i: allintitle})
                #print i
                #print csv[csv['Keyword'] == i].index
                #csv.ix[indx,'allintitle'] = allintitle
                #print csv
        
                bid = csv[csv['Keyword'] == i].index[0]
                csv.ix[bid, 'allintitle'] = allintitle
                #print csv.ix[bid, :]
                print len(csv.index)
                #print csv.columns
                csv.to_csv(fname)
            except:
                ''
            print '========='
    
        print '11111=============================='
        print allintitles
        df = p.DataFrame(allintitles, index=[0]).transpose()
        #df[0] = p.to_numeric(df[0])
        print df.dtypes
        #print df
    
