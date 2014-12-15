%% Index tracking using genetic algorithms
% This script will use the genetic algorithm to select stocks to track a
% fictitous index. The function |CreateIndex| will create the weights for
% an index using random selections. This index will drop stocks at dates
% throughout the year we are interested in.
fpos = InitialiseSession;

%% Create an Index to track

load DemoData;
load Potential
rand('twister',s);

StartDate = datenum('01/01/2007','dd/mm/yyyy');
StartIdx = find(Dates > StartDate); StartIdx = StartIdx(1);
InitDate = datenum('01/01/2006','dd/mm/yyyy');
InitIdx = find(Dates > InitDate); InitIdx = InitIdx(1);
EndIdx = numel(Dates);

NumStocks = size(Companies,1); % Number of stocks in our universe

NumDays = numel(Dates(InitIdx:EndIdx));
Wts = CreateIndex(NumDays,100,NumStocks);

%% Genetic Algorithm step
% Extract the data we need for the genetic algorithm step and then run the
% simulation

[cv,wts,NumStocks,Idx] = GetGAData(Wts,Stocks,Dates,StartDate);
[W,X] = gaStockSelect(cv,wts,10,70,true);

%% How have we done?
% Reconstruct our portfolio
PF = zeros(NumStocks,1); PF(Idx) = W;
[Indx,Tracker] = ReconstructPF(PF,Wts,Stocks,StartIdx);

figure('position',fpos); 
plot(Dates(StartIdx:end),[Indx,Tracker],'linewidth',2);

title('Comparison of Index and Tracker','fontsize',24);
legend('Index','Tracker','location','nw','fontsize',18);
xlabel('Date','fontsize',24);
grid on;
datetick('x');

%% Results
% Depending on the choices made by the random number generator the
% resulting index and tracker normally start quite closely but as time 
% they will diverge as the weights in the index shift but the weights in
% the tracker remain constant. As a result the tracker should respond to
% this deviation.
