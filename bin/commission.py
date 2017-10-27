
#~ format bank
import numpy as n
import pandas as p

c = n.matrix('1e3 2e3 20e3 60e3 100e3').A
c = n.mean(c)
print c

#c = p.DataFrame(c)
#print df

#~ c           = [1e3 2e3 20e3 60e3 100e3]
#~ c           = mean(c);
#~ ret         = 100;
#~ comisCap    = 2;
#~ comisReturn = 20;
#~ com         = [(c * comisCap / 100) (c * ret / 100 * comisReturn / 100)]';
#~ num           = 10;

ret         = 100
comisCap    = 2
comisReturn = 20
com         = n.array([(c * comisCap / 100), (c * ret / 100 * comisReturn / 100)])
num         = 2030-2017

#~ df      = [0:num]';
#~ df(:,2) = c;
#~ df(:,3) = df(:,2) .* power(1 + ret / 100, df(:,1));

df = p.DataFrame()
df[1] = n.array(range(0, num))
df[2] = c;
df[3] = df[2] * n.power(1 + float(ret) / 100, df[1]);

#~ df(:,4)       = c;
#~ df([2:num+1],4) = df([1:num], 3);
#~ df(:,4)       = df(:,3) - df(:,4);

df[4]                = c;
df.loc[2:num + 1, 4] = df.loc[1:num-2, 3].tolist();
df[4]                = df.loc[:,3] - df.loc[:,4];

#~ df(:,5) = df(:,3) * comisCap    / 100;
#~ df(:,6) = df(:,4) * comisReturn / 100;

df[5] = df[3] * comisCap    / 100;
df[6] = df[4] * comisReturn / 100;

#~ df(:,7)  = df(:,5)  + df(:,6);
#~ df(:,8)  = df(:,7) ./ df(:,3) * 100;
#~ df(:,9)  = cumsum(df(:,7));
#~ df(:,10) = df(:,9) * 18.25;

df[7]  = df[5] + df[6];
df[8]  = df[7] / df[3] * 100;
df[9]  = n.cumsum(df[7]);
df[10] = df[9] * 18.25;

#~ totalComis = sum(df(:,7));
totalComis = sum(df[7]);

#~ disp(com);
#~ disp("\t1=index 2=capital    3=capital+return 4=return\t5=2%capital 6=20%[capReturn]")
df = df.rename_axis({1:'volume', 2:'capital', 3:'capital+return', 4:'return', 5:'2%capital', 6:'20%[capReturn]', 7:'totalRate', 8:'rateEquiv', 9:'rateCumsum', 10:'rateCumsumARS'}, axis='columns')
#~ disp(df);
#~ disp(totalComis)

with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
	print df
