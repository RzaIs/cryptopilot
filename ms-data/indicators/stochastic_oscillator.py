import yfinance as yf
import datetime as dt
import math 
from .success_rate import *

coins = ['BTC-USD', 'ETH-USD', 'ADA-USD', 'DNB-USD', 'KRP-USD', 'OKB-USD', 'MATIC-USD', 'DOT-USD','SOL-USD',
         'LINK-USD', 'TRX-USD', 'LTC-USD', 'UNI-USD', 'AVAX-USD']
interval = ['15m', '30m', '1h', '1d', '1w']

end_date = dt.datetime.strptime("2023-01-01", "%Y-%m-%d").date()
start_date = end_date - dt.timedelta(days=365) # for 1 year
ticker, interval = coins[5], interval[3]

def calculate_stochastic_oscillator(ticker, interval, start_date, end_date):
    
    # Get data from Yahoo Finance for 1 year period with 1-day intervals for given ticker
    if start_date is None and end_date is None:
        data = yf.download(ticker, period = 'max', interval=interval)
    elif start_date is None:
        data = yf.download(ticker, period = 'max', interval=interval, end = end_date)
    elif end_date is None:
        data = yf.download(ticker, period = 'max', interval=interval, start = start_date)
    else:
        data = yf.download(ticker, start = start_date, end = end_date, interval=interval)
    
    # Calculate the Stochastic Oscillator values
    high = data['High'].rolling(window=14).max()
    low = data['Low'].rolling(window=14).min()
    close = data['Close']

    k_percent = (close - low) / (high - low) * 100
    d_percent = k_percent.rolling(window=3).mean()
    
    # Determine the buy and sell signals
    buy_dates = []
    sell_dates = []
    
    buy_points = []
    sell_points = []
    
    success_count = 0
    for i in range(1, len(data)):
        if k_percent.iloc[i] < 20 and d_percent.iloc[i] < 20:
            if k_percent.iloc[i-1] > d_percent.iloc[i-1] and k_percent.iloc[i] < d_percent.iloc[i]:
                buy_dates.append(data.index[i])
                buy_points.append(data.iloc[i].Close)
            elif k_percent.iloc[i-1] < d_percent.iloc[i-1] and k_percent.iloc[i] > d_percent.iloc[i]:
                sell_dates.append(data.index[i])
                sell_points.append(data.iloc[i].Close)
    
    success_rate:float
    success_rate = successRate(buy_dates, buy_points, sell_dates, sell_points)
    
    count_na = k_percent.isna().sum()
    
    return {
        'dates' : list(data.index)[count_na:], # plot points on (1)(2) x axis
        'k_percent': list(map(
            lambda e: None if math.isnan(e) else e,
            k_percent[count_na:]
        )), # both to plot together independently (2) y axis
        'd_percent': list(map(
            lambda e: None if math.isnan(e) else e,
            d_percent[count_na:]
        )), # both to plot together independently (2) y axis)
        'close': list(data['Close'].values)[count_na:],     # plot (1) y axis
        'buy_dates': list(buy_dates), # plot points on (1)(2) x axis
        'buy_points' : list(buy_points), # plot points on (1)(2) y axis
        'sell_dates':list(sell_dates), # plot points on (1)(2) x axis
        'sell_points' : list(sell_points), # plot points on (1)(2) y axis
        'success_rate': success_rate # the most fudjking important 
    }