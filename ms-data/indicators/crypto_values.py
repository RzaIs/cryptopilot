import datetime as dt
import yfinance as yf


coins = ['BTC-USD', 'ETH-USD', 'ADA-USD', 'DNB-USD', 'KRP-USD', 'OKB-USD', 'MATIC-USD', 'DOT-USD','SOL-USD',
         'LINK-USD', 'TRX-USD', 'LTC-USD', 'UNI-USD', 'AVAX-USD']
interval = ['15m', '30m', '1h', '1d', '1w']

end_date = dt.datetime.strptime("2023-01-01", "%Y-%m-%d").date()
start_date = end_date - dt.timedelta(days=365) # for 1 year
ticker, interval = coins[2], interval[3]

coins = ['BTC-USD', 'ETH-USD', 'ADA-USD', 'DNB-USD', 'KRP-USD', 'OKB-USD', 'MATIC-USD', 'DOT-USD','SOL-USD',
         'LINK-USD', 'TRX-USD', 'LTC-USD', 'UNI-USD', 'AVAX-USD']
interval = ['15m', '30m', '1h', '1d', '1w']

end_date = dt.datetime.strptime("2023-01-01", "%Y-%m-%d").date()
start_date = end_date - dt.timedelta(days=365) # for 1 year
ticker, interval = coins[2], interval[3]

def value(ticker, interval, start_date = 0, end_date = 0):
    if start_date == 0 and end_date == 0:
        data = yf.download(ticker, period = 'max', interval=interval)
    elif start_date == 0:
        data = yf.download(ticker, period = 'max', interval=interval, end = end_date)
    elif end_date == 0:
        data = yf.download(ticker, period = 'max', interval=interval, start = start_date)
    else:
        data = yf.download(ticker, start = start_date, end = end_date, interval=interval)

    output = {
        'index': list(data.index),
        'open': data['Open'],
        'high': data['High'], 
        'low': data['Low'],
        'close': data['Close'], 
        'adj_close': data['Adj Close'], 
        'volume': list(data['Volume'])
        }

    return output