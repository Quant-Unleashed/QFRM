import pandas as  pd
from HistoricalData import histData
from matplotlib import pyplot as plt

constituents = pd.read_csv("ind_nifty100list.csv") 
constituents = [constituents.iloc[i,2] for i in range(0, len(constituents))]


ticker = [i + ".NS" for i in constituents]

interval = "1d"
df_histData = []
for i in ticker:
    print(i)
    x = histData(i, "", "", interval)
    df_histData.append(x)


#Skew period analysis
index = histData("^NSEI", "", "", interval)

idx_px = index['Adj Close']
idx_ret = idx_px.pct_change()
idx_ret = idx_ret.dropna()

idx_ret.skew

for k in [20,60]:
    skew = [0 for i in range(k)]
    for i in range(len(idx_ret) - k):
        skew.append(idx_ret[i:i+k].skew())
    plt.plot(skew, label = str(k))

plt.legend(loc='upper center')
plt.show()