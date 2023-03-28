import yfinance as yf
import pandas as pd
import numpy as np
import math

coins = ['BTC-USD', 'EHT-USD', 'ADA-USD']
interval = ['15m', '30m', '1h', '1d', '1w']
crypto, interval = coins[0], interval[3]

def get_bollinger_dates(crypto, period, interval, window) :
    data = yf.download(tickers=crypto, period = period, interval = interval)

    data['20MA'] = data['Close'].rolling(window=window).mean()
    data['20SD'] = data['Close'].rolling(window=window).std()

    # Calculate the upper and lower Bollinger Bands
    data['Upper'] = data['20MA'] + (data['20SD'] * 2)
    data['Lower'] = data['20MA'] - (data['20SD'] * 2)
    
    buy_signals = []
    sell_signals = []
    for i in range(len(data['Close'])):
        if data['Close'][i] > data['Upper'][i]:
            buy_signals.append(np.nan)
            sell_signals.append(data['Close'][i])
        elif data['Close'][i] < data['Lower'][i]:
            buy_signals.append(data['Close'][i])
            sell_signals.append(np.nan)
        else:
            buy_signals.append(np.nan)
            sell_signals.append(np.nan)

    buy_signals = pd.Series(buy_signals, index = data.index)
    sell_signals = pd.Series(sell_signals, index = data.index)
    
    buy_dates = buy_signals[buy_signals.values != np.nan].index
    sell_dates = sell_signals[sell_signals.values != np.nan].index
    
    num_trades = 0
    num_wins = 0

    for i in range(window, len(data)):
            # Buy when the price crosses below the lower band
        if data['Close'][i-1] > data['Lower'][i-1] and data['Close'][i] <= data['Lower'][i]:
            num_trades += 1
            num_wins += 1

            # Sell when the price crosses above the upper band
        elif data['Close'][i-1] < data['Upper'][i-1] and data['Close'][i] >= data['Upper'][i]:
            num_trades += 1
    if(num_trades != 0):
        success_rate = (num_wins / num_trades)*100
    else:
        success_rate = num_wins
    
    print(sell_dates)

    return {
        'Close': list(data['Close'].values), #for plot
        'Upper': list( #for plot
            map(lambda e: None if math.isnan(e) else e, data['Upper'].values)    
        ),
        'Lower': list(  #for plot
            map(lambda e: None if math.isnan(e) else e, data['Lower'].values)    
        ),
        '20MA': list( #for plot
            map(lambda e: None if math.isnan(e) else e, data['20MA'].values)
        ), 
        # 'Data': data,
        'Sell Dates': list(sell_dates),
        'Buy Dates': list(buy_dates),
        'Success Rate': success_rate
    }
