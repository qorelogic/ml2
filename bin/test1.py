
import pandas as p
import numpy as n
import threading
#@profile
def pivot_dataframe(ds, order):
    
    df = p.DataFrame(ds)
    #df = df.convert_objects(convert_numeric=False)
    #print df
    print 'len(df):\t{0}'.format(len(df))
    
    step = lenn/10
    print 'step:\t{0}'.format(step)
    
    # source: http://stackoverflow.com/questions/6893968/how-to-get-the-return-value-from-a-thread-in-python
    #@profile
    def prePivotSplit(df, i, step, results, order):
        #print i
        print 'dfn = df.ix[{0}:{1},:]'.format((i*step), (i+1)*step-1)
        dfn = df.ix[(i*step):(i+1)*step-1,:]
        print 'dfn:\t{0}'.format(dfn.shape)
        #print dfn
        dfnp = dfn.pivot(order[0],order[1],order[2])
        #dfnp = dfnp.ffill().bfill()
        #print dfnp
        #print results
        #results[i] = i
        results[i] = dfnp
        print 'dfnp:\t{0}'.format(dfnp.shape)
        #dfm = dfm.combine_first(dfnp)        

    dfm = p.DataFrame()
    
    # map
    lent = lenn/step
    print 'lent:\t{0}'.format(lent)
    threads = [None] * lent
    results = [None] * lent
    for i in xrange(lent):
        #prePivotSplit(df, i, step)
        #threads.append(threading.Thread(target=prePivotSplit, args=[df, i, step, results]))
        threads[i] = threading.Thread(target=prePivotSplit, args=[df, i, step, results, order])
        threads[i].daemon = False
        threads[i].start()

    for i in xrange(lent):
        threads[i].join()
        
    #dfo = p.DataFrame(n.array([None] * (lenn*lenn)).reshape(lenn, lenn))
    dfo = p.DataFrame()
    for i in xrange(lent):
        print 'step: {0}\ti: {1}\tu1: {2}\tu2: {3}'.format(step, i, i*step, (i+1)*step-1)
        #print results[i]
        #dfo.ix[i*step:(i+1)*step-1] = results[i]
        dfo = dfo.combine_first(results[i])
    
    #print " ".join(results)
    return dfo
    

    #print dfm.ffill().bfill()
    
    #print
    #print df

lenn = 100
ds = n.random.randn(lenn,3)
df = pivot_dataframe(ds, order=(0,1,2))
print df
