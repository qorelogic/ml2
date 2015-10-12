
class Simulator:
    
    def getTicks(self, num=2000):
        import pymongo
        #import pandas as p
        from pandas import DataFrame as p_DataFrame
    
        # Connection to Mongo DB
        try:
            conn = pymongo.MongoClient(port=27017)
            #print "Connected successfully!!!"
        except pymongo.errors.ConnectionFailure, e:
            print "Could not connect to MongoDB: %s" % e 
            ''
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
            ticks = db.ticks.find(dfi)
            #print dir(ticks)
            if num == 0: num = ticks.count()
            for i in ticks[0:num]:
                k = i.keys()
                v = i.values()
                lis.append(v)
            return p_DataFrame(lis, columns=k)
    
        # sparse ticks
        db = conn.ql
        dfi = {}    
        
        #df = _pe(db, dfi, , num=num)
        df = _pe2(db, dfi, num=num)
        #print df
        return df
       
    #@profile
    def simulate(self, df=None, simulator=True, num=200):
        from pandas import DataFrame as p_DataFrame
        import time, zmq
        import numpy as n
        from oandaq import OandaQ
        
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
            socket.bind('tcp://*:5555')
    
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
            for i in dff.get_values():
                while i[len(i)-2] >= time.time():
                    time.sleep(0.001)
                v = n.array(list(i), dtype=str)
                csv = ','.join(v)
                k = list(dff.columns)
                res = dict(zip(k, v))
                #print res
                dfp = p_DataFrame(res, index=[0])
                if dff.index.dtype == 'int64':
                    dfp = dfp.ix[:,['instrument', 'ask','bid', 'dts', 'time']]
                #print dfp.transpose()[0].to_dict()
    
                # send to message queue
                stri = '{0}'.format(csv)
                #print stri
                topic = 'tester'
                socket.send("%s %s" % (topic, stri)) # only for PUB
                #self.socket.send(stri)

if __name__ == "__main__":
    s = Simulator()
    s.simulate(num=400)
    #simulator(df=df, num=40)
