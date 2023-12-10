from datetime import date
import nsepy as nse
from HistoricalData import histData
import pandas as pd
from pandas.tseries.offsets import MonthEnd
from datetime import datetime as dt

#stocks = pd.read_csv("EQUITY_L.csv")
#stocks = stocks.iloc[:,0]

#ticker = "TCS"
year = 2021
month = 1
CallPut = "CE"
stock= 'BANKNIFTY'
start = pd.to_datetime('1/2/2021')
end = pd.to_datetime('2/10/2021')
interval = '1d'


#expiry = list(nse.derivatives.get_expiry_date(year=year, month=month))
#expDate = [i for i in expiry if i.day == max([i.day for i in expiry])][0]


'''stock_opt = nse.get_history(symbol=ticker,
                        start=date(year,month,1),
                        end=date(year,month,24),
                        option_type=CallPut,
                        strike_price=2600,
                        expiry_date=expDate)
'''

# Strike Prices

#deltas = [1,2.5,5,10,20,50,100,500]

#price = histData("SBIN.NS", date(year,month,1), date(year,month,5), '1d')
#price = int(price.Close[0])
    
def getStrike1(price, v):
    if (price%v) < (v/2):
        x = price - price%v
    else:
        x = price - price%v + v
    return x

def getATM(price):
    if price < 1000:
        x = getStrike1(price, 20)
    elif price >= 1000 and price < 5000:
        x = getStrike1(price, 100)
    else:
        x = getStrike1(price, 500)
    return x

#atm = getATM(price)

def getStrikeDiff(ticker, x, year, month, expDate):
    deltas = [1,2.5,5,10,20,50,100,500]
    stock_K1 = nse.get_history(symbol=ticker,
                               start=date(year,month,1),
                               end=date(year,month,8),
                               index = True,
                               option_type="CE",
                               strike_price= x,
                               expiry_date=expDate)
     
    for i in deltas:
        stock_K2 = nse.get_history(symbol=ticker,
                               start=date(year,month,1),
                               end=date(year,month,8),
                               index = True,
                               option_type="CE",
                               strike_price= x + i,
                               expiry_date=expDate)
        if ((len(stock_K1) == len(stock_K2)) and len(stock_K1) != 0):
            strike_delta = i
            break
        elif len(stock_K1) == 0:
            print(x, "is not a valid strike price")
            strike_delta = 1000000
            break
        else:
            print(x, "is not a valid strike delta")
    return strike_delta

#y = getStrikeDiff(x)

#strikes = [(x - 10*y) + (i * y) for i in range(20)]

def getStrikes(ticker, year, month, k):
    if month == 1:
        oldexp = list(nse.derivatives.get_expiry_date(year=year-1, month=12))        
    else:
        oldexp = list(nse.derivatives.get_expiry_date(year=year, month=month-1))

    oldExpDate = [i for i in oldexp if i.day == max([i.day for i in oldexp])][0]
    
    expiry = list(nse.derivatives.get_expiry_date(year=year, month=month))
    expDate = [i for i in expiry if i.day == max([i.day for i in expiry])][0]
    price = histData("^NSEBANK", date(oldExpDate.year,oldExpDate.month,oldExpDate.day), date(year,month,8), '1d')
    price = int(price.Close[0])
    atm = getATM(price)
    y = getStrikeDiff(ticker, atm, year, month, expDate)
    strikes = [(atm - (k/2)*y) + (i * y) for i in range(k)]
    return strikes

#NumStrikes = 20

#sbiX = getStrikes("SBIN", 2021, 1, 30)



sbiS = histData("^NSEBANK", start, end, interval)
sbiS.index = [dt.date(i) for i in sbiS.index]


#Ranks = [1,2,1,2]
ce1=[]
ce2=[]
pe1=[]
pe2=[]
atm = []

ce1p=[]
ce2p=[]
pe1p=[]
pe2p=[]
atmp = []

lce1p=[]
lce2p=[]
lpe1p=[]
lpe2p=[]
latmp = []


ex= []


mend = sbiS.index[0] + MonthEnd(1)

sbiX = getStrikes("BANKNIFTY", mend.year, mend.month, 120)
expiry = list(nse.derivatives.get_expiry_date(year=mend.year, month=mend.month))
expDate = pd.to_datetime([i for i in expiry if i.day == max([i.day for i in expiry])][0])
oldexp = start

smax = max(sbiS[(sbiS.index >= oldexp) & (sbiS.index <= expDate)].Close.to_list()) + (3*(sbiX[1] - sbiX[0]))
smin = min(sbiS[(sbiS.index >= oldexp) & (sbiS.index <= expDate)].Close.to_list())  - (3*(sbiX[1] - sbiX[0]))

sbiX = [j if ((j <= smax) & (j >= smin)) else 1E10 for j in sbiX]

while 1E10 in sbiX: sbiX.remove(1E10)

StC = []
StP = []

for xt in sbiX:
    StC.append(nse.get_history(symbol='BANKNIFTY', start=oldexp, end=mend, index = True, option_type="CE", strike_price= xt, expiry_date=expDate).Close)
    StP.append(nse.get_history(symbol='BANKNIFTY', start=oldexp, end=mend, index = True, option_type="PE", strike_price= xt, expiry_date=expDate).Close)
StC = pd.DataFrame(StC).transpose()
StC.columns = sbiX
StP = pd.DataFrame(StP).transpose()
StP.columns = sbiX

STC = [StC]
STP = [StP]


for i in range(0, len(sbiS)):
    if sbiS.index[i] > expDate:
        oldexp = expDate
        mend = sbiS.index[i] + MonthEnd(2)
        sbiX = getStrikes("BANKNIFTY", mend.year, mend.month, 120)
        expiry = list(nse.derivatives.get_expiry_date(year=mend.year, month=mend.month))
        expDate = [i for i in expiry if i.day == max([i.day for i in expiry])][0]
        
        smax = max(sbiS[(sbiS.index >= oldexp) & (sbiS.index <= expDate)].Close.to_list()) + (3*(sbiX[1] - sbiX[0]))
        smin = min(sbiS[(sbiS.index >= oldexp) & (sbiS.index <= expDate)].Close.to_list())  - (3*(sbiX[1] - sbiX[0]))
        
        sbiX = [j if ((j <= smax) & (j >= smin)) else 1E10 for j in sbiX]
        
        while 1E10 in sbiX: sbiX.remove(1E10)
        
        StC = []
        StP = []
        
        for xt in sbiX:
            StC.append(nse.get_history(symbol='BANKNIFTY', start=oldexp, end=mend, index = True, option_type="CE", strike_price= xt, expiry_date=expDate).Close)
            StP.append(nse.get_history(symbol='BANKNIFTY', start=oldexp, end=mend, index = True, option_type="PE", strike_price= xt, expiry_date=expDate).Close)
        StC = pd.DataFrame(StC).transpose()
        StC.columns = sbiX
        StP = pd.DataFrame(StP).transpose()
        StP.columns = sbiX
        STC.append(StC)
        STP.append(StP)
            
    
    ce1.append(min([j if sbiS['Adj Close'].iloc[i] <= j else 1E10 for j in sbiX]))
    ce2.append(sorted(set([j if sbiS['Adj Close'].iloc[i] <= j else 1E10 for j in sbiX]))[1])
    pe1.append(max([j if sbiS['Adj Close'].iloc[i] >= j else 0 for j in sbiX]))
    pe2.append(sorted(set([j if sbiS['Adj Close'].iloc[i] >= j else 0 for j in sbiX]))[-2])
    atm.append([ce1[-1] if sbiS['Adj Close'].iloc[i] - pe1[-1] > ce1[-1] - sbiS['Adj Close'].iloc[i] else pe1[-1]][0])
    
    ce1p.append(StC[ce1[-1]][StC.index == sbiS.index[i]].iloc[0])
    ce2p.append(StC[ce2[-1]][StC.index == sbiS.index[i]].iloc[0])
    pe1p.append(StP[pe1[-1]][StP.index == sbiS.index[i]].iloc[0])
    pe2p.append(StP[pe2[-1]][StP.index == sbiS.index[i]].iloc[0])
    atmp.append(StP[atm[-1]][StP.index == sbiS.index[i]].iloc[0])
    ex.append(expDate)
    
    if i != 0:
        lce1p.append(StC[ce1[-2]][StC.index == sbiS.index[i]].iloc[0])
        lce2p.append(StC[ce2[-2]][StC.index == sbiS.index[i]].iloc[0])
        lpe1p.append(StP[pe1[-2]][StP.index == sbiS.index[i]].iloc[0])
        lpe2p.append(StP[pe2[-2]][StP.index == sbiS.index[i]].iloc[0])
        latmp.append(StP[atm[-2]][StP.index == sbiS.index[i]].iloc[0])
    else:
        lce1p.append(ce1p[-1])
        lce2p.append(ce2p[-1])
        lpe1p.append(pe1p[-1])
        lpe2p.append(pe2p[-1])
        latmp.append(atmp[-1])
        


    
sbiS['ce1'] = ce1
sbiS['ce2'] = ce2
sbiS['pe1'] = pe1
sbiS['pe2'] = pe2
sbiS['atm'] = atm
sbiS['ce1p'] = ce1p
sbiS['ce2p'] = ce2p
sbiS['pe1p'] = pe1p
sbiS['pe2p'] = pe2p
sbiS['atmp'] = atmp
sbiS['lce1p'] = lce1p
sbiS['lce2p'] = lce2p
sbiS['lpe1p'] = lpe1p
sbiS['lpe2p'] = lpe2p
sbiS['latmp'] = latmp
sbiS['Expiry'] = ex
    
    
STC = pd.concat(STC, ignore_index = False, sort = False)
STP = pd.concat(STP, ignore_index = False, sort = False)


#basic PnL - Buy 1st OTM Call every day.

pnl = [0]
ret = [0]

for i in range(1, len(sbiS)):
    if sbiS.index[i-1] == pd.to_datetime(sbiS['Expiry'].iloc[i-1]):
        x = 0
    else:
        x = sbiS['lce1p'].to_list()[i] - sbiS['ce1p'].to_list()[i-1]
    pnl.append(x)
    ret.append(ret[-1] + x)
    
sbiS['Strat_PNL'] = pnl
sbiS['Strat_return'] = ret

principal = ret[-1]/max(sbiS['ce1p'])







import pandas as pd

d1 = pd.read_csv("C:/Users/amank/Desktop/QF/Platform/NIFTY14800CE.csv")
d2 = pd.read_csv("C:/Users/amank/Desktop/QF/Platform/NIFTY14900CE.csv")
d3 = pd.read_csv("C:/Users/amank/Desktop/QF/Platform/NIFTY15000CE.csv")

d1 = d1.loc[::-1].reset_index(drop=True)
d2 = d2.loc[::-1].reset_index(drop=True)
d3 = d3.loc[::-1].reset_index(drop=True)

g1 = d2.iloc[:,6] - d1.iloc[:,6]
g2 = d3.iloc[:,6] - d2.iloc[:,6]


s1 = g1-g2
s2 = g2-g1


sf1 = s2[374:3000]

sf = []
x = 0
for i in sf1:
     
    if i < 0:
        x = x+1
        sf.append(x)
    else:
        x = 0
        sf.append(x)








