import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

coins = ['BTC-USD', 'EHT-USD', 'ADA-USD']
interval = ['15m', '30m', '1h', '1d', '1w']
ticker, interval = coins[0], interval[3]

def EMA_cross(ticker, period, interval, slow=50, fast=20):
    data = yf.download(tickers = ticker, period = period , interval = interval)

    ema_slow = data['Close'].ewm(span=slow, adjust=False).mean()
    ema_fast = data['Close'].ewm(span=fast, adjust=False).mean()
    signal = np.zeros(len(data))
    signal[fast:] = np.where(ema_fast[fast:] > ema_slow[fast:], 1.0, 0.0)
    signal_diff = np.diff(signal)
    
    buy_signals = np.where(signal_diff == 1)[0]
    sell_signals = np.where(signal_diff == -1)[0]
    
    buy_dates = data.iloc[buy_signals].index
    sell_dates = data.iloc[sell_signals].index
    
    output = {
        'Close' : data['Close'], #for plot
        'Data': data,
        'Sell Dates': sell_dates,
        'Buy Dates': buy_dates,
#         'Success Rate': success_rate #missing
    }
    return output

btc = EMA_cross(ticker, '3y', interval, 50, 20)
print(btc)