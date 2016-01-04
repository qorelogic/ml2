
import pandas as p
import numpy as n

@profile
def test1():
    
    lenn = 1000
    ds = n.random.randn(lenn,5)
    df = p.DataFrame(ds)
    #df = df.convert_objects(convert_numeric=False)
    #print df
    print len(df)
    
    step = lenn/100
    
    dfm = p.DataFrame()
    for i in xrange(lenn/step):
        print i
        dfn = df.ix[(i*step):(i+1)*step-1,:]
        #print dfn
        dfnp = dfn.pivot(0,1,2)    
        #dfnp = dfnp.ffill().bfill()
        print dfnp
        #dfm = dfm.combine_first(dfnp)

    #print dfm.ffill().bfill()
    
    #print
    #print df

test1()
