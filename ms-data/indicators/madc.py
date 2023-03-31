import yfinance as yf
import datetime as dt
import numpy as np
import pandas as pd
from .success_rate import *


coins = ['BTC-USD', 'ETH-USD', 'ADA-USD', 'DNB-USD', 'KRP-USD', 'OKB-USD', 'MATIC-USD', 'DOT-USD','SOL-USD',
         'LINK-USD', 'TRX-USD', 'LTC-USD', 'UNI-USD', 'AVAX-USD']
interval = ['15m', '30m', '1h', '1d', '1w']

end_date = dt.datetime.strptime("2023-01-01", "%Y-%m-%d").date()
start_date = end_date - dt.timedelta(days=365) # for 1 year
ticker, interval = coins[5], interval[3]

def calculate_macd(ticker, interval, start_date, end_date):
    
    # Download historical data for any Crypto Coin (ticker)
    if start_date is None and end_date is None:
        data = yf.download(ticker, interval=interval)
    elif start_date is None:
        data = yf.download(ticker, interval=interval, end = end_date)
    elif end_date is None:
        data = yf.download(ticker, interval=interval, start = start_date)
    else:
        data = yf.download(ticker, start = start_date, end = end_date, interval=interval)

    # Calculate the MACD values
    exp1 = data['Close'].ewm(span=12, adjust=False).mean()
    exp2 = data['Close'].ewm(span=26, adjust=False).mean()
    macd = exp1 - exp2
    signal = macd.ewm(span=9, adjust=False).mean()
    histogram = macd - signal

    data['Signal'] = np.where(histogram > 0, 1, -1)
    data['Position'] = data['Signal'].diff()


    buy_dates = data[data['Position'] < 0].index
    sell_dates = data[data['Position'] > 0].index
    
    buy_points_g1 = data.loc[buy_dates].Close.values
    sell_points_g1 = data.loc[sell_dates].Close.values
    
    buy_points_g2 = macd.loc[buy_dates].values
    sell_points_g2 = macd.loc[sell_dates].values
    
    
    # Find the buy and sell dates based on the MACD and signal line crossovers

    success_rate = successRate(buy_dates, buy_points_g1, sell_dates, sell_points_g1)

    # Return the MACD values, buy and sell dates, results, and success rate
    return {
        'dates' : list(data.index),  # plot (1)(2) x axis
        'close' : list(data.Close.values),  # plot (1) y axis
        'macd': list(macd.values),  # plot (2) y axis
        'signal': list(signal.values),  # plot (2) y axis
        'histogram': list(histogram.values),  # histogram (2) y axis
        'buy_dates': list(buy_dates),  # plot (1)(2) x axis
        'sell_dates': list(sell_dates), # plot (1)(2) x axis
        'sell_points_g2' : list(sell_points_g2), # plot (2) x axis
        'buy_points_g2' : list(buy_points_g2), # plot (2) x axis
        'buy_points_g1' : list(buy_points_g1), # plot (1) x axis
        'sell_points_g1' : list(sell_points_g1), # plot (1) x axis
        'success_rate': success_rate
    }