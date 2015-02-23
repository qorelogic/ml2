
import urllib2 as u
import json as j
import os, errno
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )

def debug(str, verbosity=8):
    #if verbosity == 9:
    if verbosity == 8:
        #print str
        logging.debug(str)

        return str

def fetchURL(url, mode='json', cachemode='w'):
    # mode = json | html
    response = u.urlopen(url)
    ret = response.read()
    
    # cache to file
    hdir = '/ml.live/bin/data/cache'
    mkdir_p(hdir)
    fp = open(hdir+'/'+u.quote(url,''), cachemode)
    fp.write(ret+'\n')
    fp.close()
    
    if mode == 'json':
        ret = j.loads(ret)
    return ret

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
