import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
from .success_rate import *

coins = ['BTC-USD', 'ETH-USD', 'ADA-USD', 'DNB-USD', 'KRP-USD', 'OKB-USD', 'MATIC-USD', 'DOT-USD','SOL-USD',
         'LINK-USD', 'TRX-USD', 'LTC-USD', 'UNI-USD', 'AVAX-USD']
interval = ['15m', '30m', '1h', '1d', '1w']

end_date = dt.datetime.strptime("2023-01-01", "%Y-%m-%d").date()
start_date = end_date - dt.timedelta(days=365) # for 1 year
ticker, interval = coins[0], interval[3]



def EMA_cross(ticker, interval, start_date, end_date, slow=50, fast=20):
    if start_date is None and end_date is None:
        data = yf.download(ticker, period = 'max', interval=interval)
    elif start_date is None:
        data = yf.download(ticker, period = 'max', interval=interval, end = end_date)
    elif end_date is None:
        data = yf.download(ticker, period = 'max', interval=interval, start = start_date)
    else:
        data = yf.download(ticker, start = start_date, end = end_date, interval=interval)

    ema_slow = data['Close'].ewm(span=slow, adjust=False).mean()
    ema_fast = data['Close'].ewm(span=fast, adjust=False).mean()
    signal = np.zeros(len(data))
    signal[fast:] = np.where(ema_fast[fast:] > ema_slow[fast:], 1.0, 0.0)
    signal_diff = np.diff(signal)
    
    buy_signals = np.where(signal_diff == 1)[0]
    sell_signals = np.where(signal_diff == -1)[0]
    
    buy_dates = data.iloc[buy_signals].index
    sell_dates = data.iloc[sell_signals].index
    
    buy_points = data.iloc[buy_signals].Close.values
    sell_points = data.iloc[sell_signals].Close.values

    success_rate = successRate(buy_dates, buy_points, sell_dates, sell_points)

    o =  {
        'ema_slow' : list(ema_slow.values),  #for plot(y axis)
        'ema_fast' : list(ema_fast.values), #for plot(y axis)
        'close' : list(data['Close']), #for plot(y axis)
        'dates': list(data.index),  #for plot(x axis)
        'sell_dates': list(sell_dates), #for plot(x axis)
        'buy_dates': list(buy_dates), #for plot(x axis)
        'buy_points' : list(buy_points), #for plot(y axis)
        'sell_points' : list(sell_points), #for plot(y axis)
        'success_rate': success_rate
    }
    return o
