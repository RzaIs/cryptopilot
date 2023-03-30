import math
import yfinance as yf
import pandas as pd
import datetime as dt


coins = ['BTC-USD', 'ETH-USD', 'ADA-USD', 'DNB-USD', 'KRP-USD', 'OKB-USD', 'MATIC-USD', 'DOT-USD','SOL-USD',
         'LINK-USD', 'TRX-USD', 'LTC-USD', 'UNI-USD', 'AVAX-USD']
interval = ['15m', '30m', '1h', '1d', '1w']

end_date = dt.datetime.strptime("2023-01-01", "%Y-%m-%d").date()
start_date = end_date - dt.timedelta(days=365) # for 1 year
ticker, interval = coins[2], interval[3]

def calculate_RSI(ticker, interval, start_date, end_date):
    # Get data from Yahoo Finance for 1 year period with 1-day intervals for given ticker
    if start_date is None and end_date is None:
        data = yf.download(ticker, period = 'max', interval=interval)
    elif start_date is None:
        data = yf.download(ticker, period = 'max', interval=interval, end = end_date)
    elif end_date is None:
        data = yf.download(ticker, period = 'max', interval=interval, start = start_date)
    else:
        data = yf.download(ticker, start = start_date, end = end_date, interval=interval)


    # Calculate the differences between the closing prices of each day
    price_diff = data['Close'].diff()

    # Drop the first row, which is null
    price_diff = price_diff.dropna() 

    # Calculate the changes in price for up and down movements
    pos_price = price_diff.clip(lower=0)
    neg_price = price_diff.clip(upper=0).abs() # since it is negative

    # Calculate the rolling average of the up and down price movements for the last 14 days 
    roll_pos_avg = pos_price.rolling(14).mean()
    roll_neg_avg = neg_price.rolling(14).mean()

    # Calculate the relative strength index using the formula
    rsi = 100 - (100 / (1 + (roll_pos_avg / roll_neg_avg)))

    # Find the dates where RSI hit 70 or 30
    sell_dates = rsi[(rsi.shift(1) >= 70) & (rsi < 70)].index
    buy_dates = rsi[(rsi.shift(1) <= 30) & (rsi > 30)].index
    
    sell_points = data.loc[sell_dates].Close.values
    buy_points = data.loc[buy_dates].Close.values

    sell_points_2 = rsi.loc[sell_dates].values
    buy_points_2 = rsi.loc[buy_dates].values


    # Check if each recommendation was failure or success
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
    
    count_na = rsi.isna().sum()

    return {
        'close': list(data['Close'])[count_na+1:], # plot (1) y axis
        'dates' : list(data.index)[count_na+1:], # for plot x axis
        'rsi': list(rsi)[count_na:], # plot (2) y axis
        'sell_dates': list(sell_dates), # plot triangle points (1) (2) x axis
        'buy_dates': list(buy_dates), # plot triangle points (1) (2) x axis
        'sell_points': list(sell_points), # for plot y axis - sell prices of close value
        'buy_points' : list(buy_points), # for plot y axis - buy prices of close value
        'sell_points_2': list(sell_points_2),  # sell points of rsi
        'buy_points_2': list(buy_points_2),     # buy points of rsi
        'success_rate': success_rate # the most important
    }