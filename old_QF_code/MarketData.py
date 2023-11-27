import pandas as pd
import os
#import numpy as np
#import math as m
#from functools import reduce
#from matplotlib import pyplot as plt
#from TechnicalAnalysisFunction import TaLib as ta
from HistoricalData import histData, histDataUpdate


data = pd.read_csv("EQUITY_L.csv")
data = [data.iloc[i,0] for i in range(0, len(data))]

stockNC  = []#pd.read_excel("StocksNotCovered.xlsx")

ticker = [i + ".NS" for i in data]

stocks_file = []

with os.scandir('histData/') as entries:
    for entry in entries:
        stocks_file.append(entry.name)

interval = ["1m", "2m", "5m", "15m", "30m", "1h", "1d", "5d", "1wk", "1mo", "3mo"]

for j in interval:
    for i in ticker:
        for k in stocks_file:
            if i and j in k:
                hist = histDataUpdate(i, j)
                break
            elif i + "_" + j in stockNC:
                break
            else:
                hist= histData(i, "", "", j)
                if len(hist > 1):
                    hist.index = hist.index.tz_localize(None)
                    hist.to_excel("histData/" + i + "_" + j + ".xlsx")
                else:
                    stockNC.append(i + "_" + j)

pd.DataFrame(stockNC).to_excel("StocksNotCovered.xlsx")
     