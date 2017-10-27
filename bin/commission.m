
format bank

c           = mean([1e3 2e3 20e3 60e3 100e3]);
ret         = 100;
comisCap    = 2;
comisReturn = 20;
com         = [(c * comisCap / 100) (c * ret / 100 * comisReturn / 100)]';
num           = 10;

df      = [0:num]';
df(:,2) = c;
df(:,3) = df(:,2) .* power(1 + ret / 100, df(:,1));

df(:,4)       = c;
df([2:num+1],4) = df([1:num], 3);
df(:,4)       = df(:,3) - df(:,4);

df(:,5) = df(:,3) * comisCap    / 100;
df(:,6) = df(:,4) * comisReturn / 100;

df(:,7)  = df(:,5)  + df(:,6);
df(:,8)  = df(:,7) ./ df(:,3) * 100;
df(:,9)  = cumsum(df(:,7));
df(:,10) = df(:,9) * 18.25;

totalComis = sum(df(:,7));

disp(com);
disp("\t1=index 2=capital    3=capital+return 4=return\t5=2%capital 6=20%[capReturn]")
disp(df);
disp(totalComis)
