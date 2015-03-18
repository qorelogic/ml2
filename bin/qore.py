
import urllib2 as u
import json as j
import os, errno
import logging
import re

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

#for i in range(len(allPositions2['noasnoas'])):
#    try:
#        allPositions2['noasnoas'][str(i)] = allPositions2['noasnoas'].pop(i)
#    except:
#        ''
#print allPositions2
#print j.dumps(allPositions2)

# source: http://gotoanswer.stanford.edu/?q=Recursive+depth+of+python+dictionary
#Be sure to assign the result of the recursive call to depth. Also, as @amit says, 
# consider using max so that you can handle dicts with multiple key value pairs (a treelike structure).
#>>> myDict = {'leve1_key1': {'level2_key1': 
#               {'level3_key1': {'level4_key_1': 
#                  {'level5_key1':   'level5_value1'}}}}}
#>>> dict_depth(myDict)
#5
def dict_depth(d, depth=0):
    if not isinstance(d, dict) or not d:
        return depth
    return max(dict_depth(v, depth+1) for k, v in d.iteritems())

#You should store the value retured from the recursive call, 
# and return the max value found, otherwise - you are calling the recursive 
# function without doing anything with the returned value! [and returning 0 as expected, since it was never changed]
def dict_depth(d, depth=0):
    ret = depth 
    for i in d.keys():
        if type(d[i]) is dict:
            newDict = d[i]
            ret = max(dict_depth(newDict, depth+1),ret) #finding max and storing it
    return ret #returning the max found

def convertDictKeysToString(dt, depth=2):
    if dict_depth(dt) == 1:
        for i in dt.keys(): 
            dt[i] = ({str(k): v for k, v in dt[i].iteritems()})
    if dict_depth(dt) == 2:
        for i in dt.keys():
            for j in dt[i].keys():
                dt[i][j] = ({str(k): v for k, v in dt[i][j].iteritems()})
    return dt

#alp = convertDictKeysToString(allPositions2)
#alp = j.dumps(alp)
#print alp

#positions = et.getEtoroTraderPositions('noasnoas', )
