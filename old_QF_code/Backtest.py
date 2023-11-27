import pandas as pd
import numpy as np
import math as m
from functools import reduce
from matplotlib import pyplot as plt
from TechnicalAnalysisFunction import TaLib as ta
from HistoricalData import histData


def getValue(stock, interval, major, indicator, periods = "max"):
    stock = histData(stock, pd.to_datetime('1/2/2019'), pd.to_datetime('9/30/2021'), interval)
    Open = stock.iloc[:,0]
    close = stock.iloc[:,3]
    high = stock.iloc[:,1]
    low = stock.iloc[:,2]
    volume = stock.iloc[:,5]
    data = ta(major, indicator, Open, close, high, low, volume,  periods)
    return data

def backtest1(tadata, buyValue, sellValue):
    inv = []
    buyqty = 0
    for i in range(len(tadata)):
        if i == 0:
            inv.append(buyqty)
        elif tadata[i] < buyValue and buyqty == 0:
            buyqty = 1
            inv.append(buyqty)
        elif tadata[i] > sellValue and buyqty == 1:
            buyqty = 0
            inv.append(buyqty)
        else:
            inv.append(buyqty)
    return inv

def performanceStats(returns, predictions):
    port_ret = np.cumprod(returns)
    annual_return = port_ret[len(port_ret)-1]**(252/(len(port_ret)-1)) - 1
    ann_std = np.std(port_ret)*m.sqrt(252)
    sharpe = annual_return / ann_std
    trade_hit_rate = len([x for x in port_ret if x > 1])/len(port_ret) 
    trade_win_loss = (np.mean([x for x in port_ret if x > 1]) - 1 )/(np.mean([x for x in port_ret if x <1]) - 1)
    max_drawdown = min([port_ret[i]/max(port_ret[0:i])-1 for i in range(1,len(port_ret))])
    TotalDays = len(predictions)
    TradingDays = len([abs(x) for x in predictions if x != 0])
    TradingDaysPerc = TradingDays/TotalDays
    HoldDays = len([abs(x) for x in predictions if x == 0])
    HoldDaysPerc = HoldDays/TotalDays
    PerformanceStats =  pd.DataFrame(np.column_stack((annual_return, ann_std, sharpe, trade_hit_rate, trade_win_loss, max_drawdown, TotalDays, TradingDays, TradingDaysPerc, HoldDays, HoldDaysPerc)), columns =['annual_return', 'ann_std', 'sharpe', 'trade_hit_rate', 'trade_win_loss', 'max_drawdown', 'TotalDays', 'TradingDays', 'TradingDaysPerc', 'HoldDays', 'HoldDaysPerc'])
    PerformanceStats = PerformanceStats.transpose()
    PerformanceStats.columns = ['Strategy']
    return(PerformanceStats)
    
    
def backtestmodel(stock, interval, major, indicator, periods, buyValue, sellValue, report):
    res = []
    tadata = getValue(stock, interval, major, indicator, periods)
    stock = histData(stock, pd.to_datetime('1/2/2019'), pd.to_datetime('9/30/2021'),interval)
    returns = stock.iloc[:,3].pct_change()
    predictions = backtest1(tadata, buyValue, sellValue)
    returns = 1 + (predictions * returns)
    returns = returns.dropna()
    perfStats = performanceStats(returns, predictions)
    res.append(returns)
    res.append(predictions)
    res.append(perfStats)
    if report == 'return':
        return returns
    elif report == 'prediction':
        return predictions
    elif report == 'performance':
        return perfStats
    elif report == 'all':
        return res
    else:
        return perfStats

def mapper(datain, colin, colout):
    data = pd.read_csv("EQUITY_L.csv")
    mapped = [data[data.iloc[:,colin] == i].iloc[:,colout] for i in datain]
    mapped = pd.concat(mapped)
    return mapped


stock = "SBIN.NS"#["Bajaj Finserv Limited","Bajaj Finance Limited"]
interval = "1d" 
major = "Momentum"
indicator = "RSI"
periods = []
buyValue = 20
sellValue = 80
report = "performance"


def runmodel1(stock, interval, major, indicator, periods, buyValue, sellValue, report):
    stock = mapper(stock, 1, 0)
    stock = [i +".NS" for i in stock]
    model = [backtestmodel(i, interval, major, indicator, periods, buyValue, sellValue, report) for i in stock]
    return model

model= runmodel1(stock, interval, major, indicator, periods, buyValue, sellValue, report)
    
sbin = backtestmodel("SBIN.NS", "1d", "Momentum", "RSI", "", 70, 30,"all")
            