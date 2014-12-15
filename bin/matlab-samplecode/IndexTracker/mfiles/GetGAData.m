function [cv,wts,NumStocks,Idx] = GetGAData(Wts,Stocks,Dates,StartDate)

StartIdx = find(Dates > StartDate); StartIdx = StartIdx(1);
NumStocks = size(Wts,2);
Idx = find(Wts(StartIdx,:) ~= 0);
wts = Wts(StartIdx,Idx);

% Now use a years worth of previous data to estimate the covariance matrix
InitIdx = find(Dates > StartDate-365); InitIdx = InitIdx(1);
Data = tick2ret(Stocks(InitIdx:StartIdx,Idx));

% Strip out NaN columns
[r,c] = find(isnan(Data));

Data(:,c) = [];
wts(c) = []; % Not investing in these stocks;
Idx(c) = [];

% Calculate covariance matrix
cv = cov(Data);

end