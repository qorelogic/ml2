
import urllib2 as u
import json as j
import os, errno

def debug(str, verbosity):
    if verbosity == 9:
        print str
        return str

def fetchURL(url, mode='json'):
    response = u.urlopen(url)
    html = response.read()
    ret = j.loads(html)
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
