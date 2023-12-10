#import pandas as pd
#from TechnicalAnalysisFunction import TaLib as ta
from datetime import date
#import nsepy as nse
from HistoricalData import histData
import talib as ta
from matplotlib import pyplot as plt


ticker = 'TCS'
month = 9
year = 2020
CallPut = "CE"
interval = "1d" 
major = "Momentum"
indicator = "RSI"
endDate = date(2021,9,30)
startDate = date(year,month-1,1)

def getValue(stock, interval, major, indicator, periods = "max"):
    stock = histData(stock, startDate, endDate,interval)
    Open = stock.iloc[:,0]
    close = stock.iloc[:,3]
    high = stock.iloc[:,1]
    low = stock.iloc[:,2]
    volume = stock.iloc[:,5]
    data = ta(major, indicator, Open, close, high, low, volume,  periods)
    return data



'''
expiry = list(nse.derivatives.get_expiry_date(year=year, month=month))
expDate = [i for i in expiry if i.day == max([i.day for i in expiry])][0]
'''

price = histData(ticker + '.NS', startDate, endDate, '1d')

'''
stock_opt = nse.get_history(symbol=ticker,
                        start=startDate,
                        end=endDate,
                        option_type=CallPut,
                        strike_price=2300,
                        expiry_date=expDate)

Opt_close = stock_opt.Close
'''
#RSI = getValue(ticker,interval,major,"RSI",'max')
#MA = getValue(ticker,interval,major,"MA",'max')

RSI = ta.RSI(price.Close, timeperiod=14)
MA = ta.MA(price.Close, timeperiod=14, matype=0)
price['RSI'] = RSI
price['MA'] = MA

plt.plot(range(len(RSI) -14), RSI.dropna())
plt.plot(range(len(RSI) -14), [50 for i in range(len(RSI) -14)])
plt.plot(range(len(RSI) -14), [70 for i in range(len(RSI) -14)])
plt.plot(range(len(RSI) -14), [30 for i in range(len(RSI) -14)])
#plt.plot(range(len(MA) -13), MA.dropna())
#plt.plot(range(len(MA) -13), MA.dropna())
