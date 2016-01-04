
import pandas as p
import numpy as n
import threading
#@profile
def test1():
    
    lenn = 1000
    ds = n.random.randn(lenn,5)
    df = p.DataFrame(ds)
    #df = df.convert_objects(convert_numeric=False)
    #print df
    print len(df)
    
    step = lenn/100
    
    @profile
    def thr1(df, i, step):
        print i
        dfn = df.ix[(i*step):(i+1)*step-1,:]
        #print dfn
        dfnp = dfn.pivot(0,1,2)    
        #dfnp = dfnp.ffill().bfill()
        print dfnp
        #dfm = dfm.combine_first(dfnp)

    dfm = p.DataFrame()
    
    # map
    ts = []
    for i in xrange(lenn/step):
#        thr1(df, i, step)
        ts.append(threading.Thread(target=thr1, args=[df, i, step]))
        ts[i].daemon = False
        ts[i].start()

    #print dfm.ffill().bfill()
    
    #print
    #print df

test1()
