
import flask, sys
import ujson as json
import urllib2
from flask import Flask, render_template, url_for

app = flask.Flask(__name__)

@app.route('/')
def test():
    #url = 'http://google.com'
    #html = url
    #response = urllib2.urlopen(url)
    #html = response.read()
    #ret = j.loads(html)
    #print ret
    #return html
#    return 'everything is running\n'

    #cmd = 'ls /mldev/screenshots/developerLogs/screen/qore2/*png | perl -pe "s/.+\///g" 2> /dev/null'
    #res = os.popen(cmd).read().strip().split('\n')#[0]
    """
    res = timestamps02()
    print res
    bu = ''
    meta = {}
    
    for i in res:
        meta.update({'title':i})
        meta.update({'title2':i})        
        #liquid-screenshot-qore2-1478885822.png
        #bu += '<img src="file://%s" /><br />\n' % i
        bu += '<img src="liquid-screenshot-qore2-1478885822.png" /><br />\n' #% i
        break
    #return '\n'.join(res)
    #return bu
    return render_template('developerView.html', mess=res[0:200], meta=meta)
    """
    return render_template('web.qoreliquid.html')
    #return app.root_path
    #return 'everything is running\n'

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

def serv(port=8080):
    host = '0.0.0.0'
    #print 'attempting on[host=%s, port=%s]' % (host, port)
    app.config['DEBUG'] = True
    app.run(host=host, port=port)
    print 'listening[host=%s, port=%s]' % (host, port)
    sys.exit()

if __name__ == '__main__':
    #if args.web:
    try:
        serv()
    except:
        serv(8081)
