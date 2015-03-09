
import oandapy
import pandas as p
import sys

co = p.read_csv('config.csv', header=None)

env1=co.ix[0,1]
access_token1=co.ix[0,2]
oanda1 = oandapy.API(environment=env1, access_token=access_token1)

env2=co.ix[1,1]
access_token2=co.ix[1,2]
oanda2 = oandapy.API(environment=env2, access_token=access_token2)

acc = oanda2.get_accounts()['accounts']
accid = acc[0]['accountId']

# tick streamer (data feed)
class MyStreamer(oandapy.Streamer):
    def __init__(self, *args, **kwargs):
        oandapy.Streamer.__init__(self, *args, **kwargs)
        self.ticks = 0

    def on_success(self, data):
        self.ticks += 1
        #print p.DataFrame(data['tick'], index=[0])
        try:
            print p.DataFrame(data['tick'], index=[0]).to_string(index=False).split('\n')[1]
        except KeyError, e:
            ''
            #print e
        
        #if self.ticks == 2:
        #    self.disconnect()

    def on_error(self, data):
        self.disconnect()
        
stream = MyStreamer(environment=env2, access_token=access_token2)
try:
    pair = sys.argv[1]
    stream.start(accountId=accid, instruments=pair)
    #stream.start(accountId=<accoundid>, instruments="EUR_USD,USD_CAD")
except ConnectionError, e:
    print e
except KeyboardInterrupt, e:
    'disconnecting'
    stream.disconnect()

