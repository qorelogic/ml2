
import urllib2 as u
#import json as j
import ujson as j
import os, errno
import logging
import re
import numpy as n

#logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s')
logging.basicConfig(filename='/tmp/qore.dev.log', level=logging.DEBUG)

hdir = '/ml.live/bin/data/cache'

def debug(str, verbosity=8):
    #if verbosity == 9:
    if verbosity == 8:
        #print str
        logging.debug(str)

        return str

def cleanJsonContent(t):
    return re.sub(re.compile(r'[\s]+'), ' ', ''.join(t.split('\n')))

def fetchFromCache(url):
    # from cache file
    #mkdir_p(hdir)
    fp = open(hdir+'/'+u.quote(url,''), 'r')
    r = fp.read()
    fp.close()
    return r

def fetchURL(url, mode='json', cachemode='w', fromCache=False):
    # mode = json | html
    try:
        if fromCache == True:
            debug('fetchURL(): '+url)
            ret = fetchFromCache(url)
        else:
            debug('fetchURL(fetchedFromCache): '+url)
            response = u.urlopen(url)
            ret = response.read()
            
            # cache to file
            mkdir_p(hdir)
            fname = hdir+'/'+u.quote(url,'')
            debug('fetchURL(): caching to file: '+fname)
            fp = open(fname, cachemode)
            if mode == 'json':
                ret = cleanJsonContent(ret)
            fp.write(ret+'\n')
            fp.close()
        
        if mode == 'json':
            debug('fetchURL(): json format: '+url)
            ret = j.loads(ret)
        return ret
    except u.URLError, e:
        debug(e)        
    except NameError, e:
        debug(e)

def saveJson(jsoncontent, fname):
    print 'saving json to {0}'.format(fname)
    fp = open(fname, 'a')
    fp.write(jsoncontent)
    fp.close()

# getWebContentToText
def lynxDump2(url):
    response = u.urlopen(url)
    html = response.read()
    html = html.decode('utf-8')
    return html2text.html2text(html)

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

def isRange(a, rangeHasMissingIntegers=False):
    """
    Is the given array a valid integer range between its min and max
    """
    a = n.array(a, dtype=int)
    ar = n.array(range(n.min(a), n.max(a)+1))
    au = n.unique(a)
    #print ar
    #print au

    if rangeHasMissingIntegers:
        """
        If the given array of integers has missing integers
        ie. not a valid integer range, output zero for every missing integer in the range
        a = [1,4,7]
        outpus [1,0,0,4,0,0,7]
        """
        ar = ar.reshape(len(ar),1)
        elm = ar * n.array(n.equal(ar, n.unique(a)), dtype=int)
        return list(n.array(n.dot(elm, n.ones(len(au)).reshape(len(au),1)).transpose()[0], dtype=int))
    
    if n.sum(ar) == n.sum(au):
        return True
    else:
        return False
