import yfinance as yf
import pandas as pd
import numpy as np
import math
import datetime as dt

coins = ['BTC-USD', 'ETH-USD', 'ADA-USD', 'DNB-USD', 'KRP-USD', 'OKB-USD', 'MATIC-USD', 'DOT-USD','SOL-USD',
         'LINK-USD', 'TRX-USD', 'LTC-USD', 'UNI-USD', 'AVAX-USD']
interval = ['15m', '30m', '1h', '1d', '1w']

end_date = dt.datetime.strptime("2023-01-01", "%Y-%m-%d").date()
start_date = end_date - dt.timedelta(days=365) # for 1 year
ticker, interval = coins[0], interval[3]

def get_bollinger_dates(ticker, interval, start_date = 0, end_date = 0, window = 20) :
    if start_date == 0 and end_date == 0:
        data = yf.download(ticker, period = 'max', interval=interval)
    elif start_date == 0:
        data = yf.download(ticker, period = 'max', interval=interval, end = end_date)
    elif end_date == 0:
        data = yf.download(ticker, period = 'max', interval=interval, start = start_date)
    else:
        data = yf.download(ticker, start = start_date, end = end_date, interval=interval)

    data['20MA'] = data['Close'].rolling(window=window).mean()
    data['20SD'] = data['Close'].rolling(window=window).std()

    # Calculate the upper and lower Bollinger Bands
    data['Upper'] = data['20MA'] + (data['20SD'] * 2)
    data['Lower'] = data['20MA'] - (data['20SD'] * 2)
    
    buy_points = []
    sell_points = []
    
    buy_dates = []
    sell_dates = []
    for i in range(len(data['Close'])):
        if data['Close'][i] > data['Upper'][i]:
            sell_points.append(data['Close'][i])
            sell_dates.append(data.index[i])
        elif data['Close'][i] < data['Lower'][i]:
            buy_points.append(data['Close'][i])
            buy_dates.append(data.index[i])
            
    sell_df = pd.DataFrame({'Date': sell_dates, 'Close' : sell_points, 'status' : 0})
    buy_df = pd.DataFrame({'Date': buy_dates, 'Close' : buy_points, 'status' : 1})

    df = pd.concat([sell_df, buy_df])
    df = df.sort_values(by = ['Date'])
    df = df.reset_index(drop = True)

    status = 1
    success = 0
    count = 0
    for i in range(len(df)-1):
        if(status and df.iloc[i].status ==  1):
            status = 0
            index = i
        if(status == 0):
            self = df.iloc[i]
            nex = df.iloc[i+1]
            if(self.status == 1):
                if(nex.status == 0):
                    count += 1   
                    if (self.Close < nex.Close):
                        
                        success += 1

    success_rate: float
    success_rate = success/count * 100 if count > 0 else 0

    na_20ma = data['20MA'].isna().sum()

    return {
        'dates' : list(data.index)[na_20ma:], #for plot(x axis)
        'close': list(data['Close'][na_20ma:].values), #for plot(y axis)
        'upper': list(data['Upper'][na_20ma:].values),     #for plot(y axis)
        'lower': list(data['Lower'][na_20ma:].values),     #for plot(y axis)
        '20MA': list(data['20MA'][na_20ma:].values),  #for plot(y axis) 
        # 'Data': data,
        'sell_dates': list(sell_dates), #for plot(x axis)
        'buy_dates': list(buy_dates), #for plot(x axis)
        'buy_points' : list(buy_points), #for plot(y axis)
        'sell_points' : list(sell_points), #for plot(y axis)
        'success_rate': success_rate   
    }
