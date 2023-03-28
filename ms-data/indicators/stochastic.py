# Stochastic Oscillator Strategy

import yfinance as yf
import datetime as dt
import math

coins = ['BTC-USD', 'ETH-USD', 'ADA-USD', 'DNB-USD', 'KRP-USD', 'OKB-USD', 'MATIC-USD', 'DOT-USD','SOL-USD',
         'LINK-USD', 'TRX-USD', 'LTC-USD', 'UNI-USD', 'AVAX-USD']
interval = ['15m', '30m', '1h', '1d', '1w']

end_date = dt.datetime.strptime("2023-01-01", "%Y-%m-%d").date()
start_date = end_date - dt.timedelta(days=365) # for 1 year
ticker, interval = coins[2], interval[3]

def calculate_stochastic_oscillator(ticker, start_date, end_date, interval):
    
    # Get data from Yahoo Finance for 1 year period with 1-day intervals for given ticker
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
    success_count = 0
    for i in range(1, len(data)):
        if k_percent.iloc[i] < 20 and d_percent.iloc[i] < 20:
            if k_percent.iloc[i-1] > d_percent.iloc[i-1] and k_percent.iloc[i] < d_percent.iloc[i]:
                buy_dates.append(data.index[i])
                if close.iloc[i+1] > close.iloc[i]:
                    success_count += 1
            elif k_percent.iloc[i-1] < d_percent.iloc[i-1] and k_percent.iloc[i] > d_percent.iloc[i]:
                sell_dates.append(data.index[i])
                if close.iloc[i+1] < close.iloc[i]:
                    success_count += 1
    
    # Calculate the success rate of the recommendations
    total_count = len(buy_dates) + len(sell_dates)
    success_rate = success_count / total_count if total_count > 0 else 0
    
    
    return {
        'k_percent': list( # both to plot together independently (2)
            map(lambda e: None if math.isnan(e) else e, k_percent)
        ),
        'd_percent': list( # both to plot together independently (2)
            map(lambda e: None if math.isnan(e) else e, d_percent)
        ),
        'close': close,     # plot (1)
        'buy_dates': buy_dates, # plot points on (1)
        'sell_dates':sell_dates, # plot points on (1)
        'success_rate': success_rate # the most fudjking important 
    }
