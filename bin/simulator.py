
class Simulator:
    
    def getTicks(self, num=2000, verbose=True):
        import pymongo
        #import pandas as p
        from pandas import DataFrame as p_DataFrame
    
        # Connection to Mongo DB
        host = '127.0.0.1'
        portA = 3310
        portB = 27017
        try:
            try:
                port = portA
                if verbose:
                    print ''
                    print 'Attempting connect:'
                    print "                     MongoDB[%s:%s]" % (host, port)
                conn = pymongo.MongoClient(host=host, port=port)
            except Exception as e:
                port = portB
                if verbose:
                    print "Could not connect to MongoDB[%s:%s]: %s" % (host, port, e)
                    print 'Attempting failover connect:'
                    print "                     MongoDB[%s:%s]" % (host, port)
                conn = pymongo.MongoClient(host=host, port=port)
            #print "Connected successfully!!!"
        except pymongo.errors.ConnectionFailure, e:
            if verbose:
                print "Could not connect to MongoDB[%s:%s]: %s" % (host, port, e)
                print 'Try starting mongodb:'
                print '$ mx w mongo'
                print ''
            import sys
            sys.exit()
        ##############
        
        #@profile
        def _pe(db, dfi, num=100):
            df = p_DataFrame()
            for i in db.ticks.find(dfi)[0:num]:
                try: df = df.combine_first(p_DataFrame(i, index=[i['_id']]))
                except KeyError as e: ''
            return df
        
        #@profile
        def _pe2(db, dfi, num=100):
            lis = []
            #for i in db.ticks.find(dfi)[0:num]:
            #ticks = db.ticks.find(dfi).limit(num)
            #db.ticks.createIndex( { 'time': 1 } )
            #ticks = db.ticks.find().sort({time:-1}).limit(num)
            # http://stackoverflow.com/questions/4421207/mongodb-how-to-get-the-last-n-records
            #ticks = db.ticks.find().sort([('time',-1)]).limit(num) # sorting is too costly
            ticks = db.ticks.find().limit(num) 
            #print dir(ticks)
            
            # https://docs.mongodb.org/v3.0/reference/method/cursor.count/
            if num == 0: num = ticks.count(True)
            for i in ticks[0:num]:
                k = i.keys()
                v = i.values()
                lis.append(v)
                #lis.insert(0, v)
            return p_DataFrame(lis, columns=k)
    
        # sparse ticks
        try:
            db = conn.ql
        except Exception as e:
            print e
            import sys
            sys.exit()
        dfi = {}
        
        #df = _pe(db, dfi, , num=num)
        df = _pe2(db, dfi, num=num)
        #print df
        return df
       
    #@profile
    def simulate(self, df=None, simulator=True, num=200, mode='csv', port=5555, verbose=False):
        #print 'simulator=%s, num=%s, mode=%s' % (simulator, num, mode)
        from pandas import DataFrame as p_DataFrame
        import time, zmq, sys
        import numpy as n
        from oandaq import OandaQ
        import ujson as j
        
        if type(df) == type(None):
            df = self.getTicks(num=num)
        dfn = df.get_values()
        if simulator == True:
            dff = p_DataFrame(dfn, index=df.index, columns=df.columns)
            #if dff.index.dtype == 'int64':
            #    dff = dff.set_index('time')
            #print dff.index.dtype
            #print type(dff.index.dtype)
    
            # message queue (zmq)
            ctx = zmq.Context()
            #socket = ctx.socket(zmq.REP)
            #socket = ctx.socket(zmq.PUSH)
            socket = ctx.socket(zmq.PUB);
            try:
                url = 'tcp://*:%s' % port
                socket.bind(url)
            except:
                # A+B feeds            
                try:
                    port = 5555
                    url = 'tcp://*:%s' % port
                    socket.bind(url)
                except:
                    port = 5556
                    url = 'tcp://*:%s' % port
                    socket.bind(url)

            print 'bound to port: %s, sending %s ticks..' % (url, num)
    
            try:
                dff['ts'] = OandaQ.oandaToTimestamp_S(dff.index)
            except:
                dff['ts'] = OandaQ.oandaToTimestamp_S(dff['time'])
            dff['dts'] = OandaQ.timestampToDatetime_S(dff['ts'])        
            ts = dff.ix[10,'ts']
            cts = time.time()
            #print ts
            #print cts
            ndiff = cts - ts
            #print ndiff
            dff['tsnowts'] = dff['ts'] + ndiff        
            dff['tsnow'] = OandaQ.timestampToDatetime_S(dff['ts'] + ndiff)
            cnt = 1
            
            time.sleep(2)
            
            for i in dff.get_values():
                #print 'i=%s' % (i)
                while i[len(i)-2] >= time.time():
                    time.sleep(0.001)
                v = n.array(list(i), dtype=str)
                #csv = ','.join(v)
                k = list(dff.columns)
                res = dict(zip(k, v))
                #print res
                dfp = p_DataFrame(res, index=[0])
                if dff.index.dtype == 'int64':
                    dfp = dfp.ix[:,['instrument', 'ask','bid', 'dts', 'time']]
                #print dfp.transpose()[0].to_dict()
                csv = list(dfp.get_values()[0])
                csv = ','.join(csv)
    
                # send to message queue
                topic = 'tester'
                
                if mode == 'csv':
                    stri = '{0}'.format(csv)
                    socket.send("%s %s" % (topic, stri)) # only for PUB
                    if verbose:
                        print '{0}: {1}'.format(cnt, stri)
                #self.socket.send(stri)
                
                if mode == 'dict':                    
                    ddict = dfp.transpose()[0].to_dict()
                    ddict = j.dumps(ddict)
                    socket.send("%s %s" % (topic, ddict)) # only for PUB                
                    if verbose:
                        print '{0}: {1}'.format(cnt, ddict)

                cnt +=1

if __name__ == "__main__":

    import argparse
    # source: https://docs.python.org/2/howto/argparse.html
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-n", '--num', help="number of ticks")
    parser.add_argument("-m", '--mode', help="mode: csv | dict")
    parser.add_argument("-p", '--port', help="port: 5555 | 5556 | 5557, etc.")
    parser.add_argument("-v", '--verbose', help="Verbose printing", action="store_true")

    args = parser.parse_args()

    if args.num:
        num = int(args.num)
    else:
        num = 400

    if args.mode:
        mode = args.mode
    else:
        mode = 'csv'

    if args.port:
        port = int(args.port)
    else:
        port = 5555

    s = Simulator()
    try:
        s.simulate(num=num, mode=mode, port=port, verbose=args.verbose)
    except KeyboardInterrupt as e:
        print ''
    #simulator(df=df, num=40)
