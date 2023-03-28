import pandas as pd
import numpy as np
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
    
    buy_points = data.iloc[buy_signals].Close.values
    sell_points = data.iloc[sell_signals].Close.values

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
                count += 1   
                if(nex.status == 0 and self.Close < nex.Close):
                    success += 1
    
    success_rate = (success/count)*100

    return {
        'close' : data['Close'], #for plot
        'sell_dates': list(sell_dates),
        'buy_dates': list(buy_dates),
        'success_rate': success_rate
    }
