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

def get_bollinger_dates(ticker, interval, start_date, end_date, window = 20) :
    if start_date is None and end_date is None:
        data = yf.download(ticker, period = 'max', interval=interval)
    elif start_date is None:
        data = yf.download(ticker, period = 'max', interval=interval, end = end_date)
    elif end_date is None:
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
            
    success_rate: float

    success_rate = successRate(buy_dates, buy_points, sell_dates, sell_points)

    count_na = data['20MA'].isna().sum()

    return {
        'dates' : list(data.index)[count_na:], #for plot(x axis)
        'close': list(data['Close'][count_na:].values), #for plot(y axis)
        'upper': list(map(
            lambda e: None if math.isnan(e) else e, 
            data['Upper'][count_na:].values
        )),     #for plot(y axis)
        'lower': list(map(
            lambda e: None if math.isnan(e) else e,
            data['Lower'][count_na:].values
        )),     #for plot(y axis)
        '20MA': list(data['20MA'][count_na:].values),  #for plot(y axis) 
        # 'Data': data,
        'sell_dates': list(sell_dates), #for plot(x axis)
        'buy_dates': list(buy_dates), #for plot(x axis)
        'buy_points' : list(buy_points), #for plot(y axis)
        'sell_points' : list(sell_points), #for plot(y axis)
        'success_rate': success_rate   
    }
