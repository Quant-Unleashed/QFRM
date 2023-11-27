import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta




#stock = "^NSEBANK"
#interval = "1d"

intervals = ["1m", "2m", "5m", "15m", "30m", "1h", "1d", "5d", "1wk", "1mo", "3mo"]
maxPeriod = ["1d", "5d", "1wk", "1mo", "3mo"]

def histDataUpdate(stock, interval):
    data = pd.read_excel("histData/" + stock + "_" + interval +  ".xlsx")
    startdate = data.index[-1]
    newData = histData(stock, startdate, datetime.today(), interval)
    data1 = pd.concat(data,newData)
    data1 = data1.combine_first(newData)
    data1 = data1.loc[~data1.index.duplicated(keep='first')]
    data1.to_excel("histData/" + stock + "_" + interval +  ".xlsx")

def histData(stock, start, end, interval):
    if start == "":
        if interval in maxPeriod:
            data = yf.download(stock, period = "max", interval = interval)
            data = data[data.Close != 0]
            return data
        else:
            data = histDataIntraday(stock, interval)
            data = data[data.Close != 0]
            return data
    else:
        data = yf.download(stock, start=start, end=end, interval = interval)
        data = data[data.Close != 0]
        return data

#data = histData(stock, "1d")

#data1hour = histData("SBI", pd.to_datetime('01/31/2021'), pd.to_datetime('01/31/2022'),"1h")

def histDataIntraday(stock, interval):
    list_of_dfs = []
    print("Stock data is downloading for ", stock)
    if interval == '1m':
        for i in range(0,4):
            startdate = datetime.today() - timedelta(days= 7 + ((3-i)*7))
            enddate = datetime.today() - timedelta(days= 0 + ((3-i)*7))
            startdate = startdate.strftime('%Y-%m-%d')
            enddate = enddate.strftime('%Y-%m-%d')
            data = yf.download(stock, start=startdate, end=enddate, interval = "1m")
            list_of_dfs.append(data)
            print("Data from", startdate, "to", enddate, "is downloaded")    
        data = pd.concat(list_of_dfs)    
        print("Data downloaded for ", stock)
        return(data)
    else:
        if interval in ("2m", "5m", "15m", "30m"):
            startdate = datetime.today() - timedelta(days= 59)
        elif interval == '1h':
            startdate = datetime.today() - timedelta(days= 729)
        enddate = datetime.today()
        startdate = startdate.strftime('%Y-%m-%d')
        enddate = enddate.strftime('%Y-%m-%d')
        data = yf.download(stock, start=startdate, end=enddate, interval = interval)
        print("Data from", startdate, "to", enddate, "is downloaded")    
        print("Data downloaded for ", stock)
        return(data)
        
#sbi = histData("20MICRONS.NS","","", "1m")

    
#data1min = histData1min(stock)

def expirydays(data):
    days = []
    for i in range(len(data)):
        if data.index[i].weekday() == 3:
            days.append(data.iloc[i])
        elif data.index[i].weekday() == 4 and data.index[i-1].weekday() == 2:
            days.append(data.iloc[i-1])
    day = pd.DataFrame(days)
    return day



'''
thur = expirydays(data)

openhigh = [(thur.iloc[i,1] - thur.iloc[i,0]) for i in range(len(thur))]
openlow = [(thur.iloc[i,2] - thur.iloc[i,0]) for i in range(len(thur))]
openclose = [(thur.iloc[i,3] - thur.iloc[i,0])  for i in range(len(thur))]
highlow = [(thur.iloc[i,1] - thur.iloc[i,2])  for i in range(len(thur))]
highclose = [(thur.iloc[i,3] - thur.iloc[i,1]) for i in range(len(thur))]
lowclose = [(thur.iloc[i,3] - thur.iloc[i,2]) for i in range(len(thur))]

lim = 150

countoh = len([x for x in openhigh if x > lim])
countol = len([x for x in openlow if x < -1*lim])
countlc = len([x for x in lowclose if x > lim])
counthc = len([x for x in highclose if x < -1*lim])
countoc = len([x for x in openclose if abs(x) > lim])
counthl = len([x for x in highlow if x > lim])

'''
