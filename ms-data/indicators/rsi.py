#Relative Strength Index

import yfinance as yf
import pandas as pd
import datetime as dt


coins = ['BTC-USD', 'ETH-USD', 'ADA-USD', 'DNB-USD', 'KRP-USD', 'OKB-USD', 'MATIC-USD', 'DOT-USD','SOL-USD',
         'LINK-USD', 'TRX-USD', 'LTC-USD', 'UNI-USD', 'AVAX-USD']
interval = ['15m', '30m', '1h', '1d', '1w']

end_date = dt.datetime.strptime("2023-01-01", "%Y-%m-%d").date()
start_date = end_date - dt.timedelta(days=365) # for 1 year
ticker, interval = coins[2], interval[3]

def calculate_RSI(ticker, start_date, end_date, interval):
    # Get data from Yahoo Finance for 1 year period with 1-day intervals for given ticker
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

    # Calculate the relative strength index
    rsi = 100 - (100 / (1 + (roll_pos_avg / roll_neg_avg)))

    # Find the dates where RSI hit 70 or 30
    sell_dates = rsi[(rsi.shift(1) >= 70) & (rsi < 70)].index
    buy_dates = rsi[(rsi.shift(1) <= 30) & (rsi > 30)].index

    # Check if each recommendation was positive or negative
    results = []
    for date in sell_dates:
        if data.loc[date, 'Close'] < data.loc[date-pd.Timedelta(days=1), 'Close']:
            results.append('Failure')
        else:
            results.append('Success')

    for date in buy_dates:
        if data.loc[date, 'Close'] > data.loc[date-pd.Timedelta(days=1), 'Close']:
            results.append('Success')
        else:
            results.append('Failure')

    # Calculate the success rate of the recommendations
    if len(results) > 0:
         success_rate = results.count('Success') / len(results)
    else:
         success_rate = 0

    output = {
        'Coin_Close':data['Close'], # plot
        'RSI': rsi, # plot
        'Sell Dates': sell_dates, # plot triangle
        'Buy Dates': buy_dates, # plot triangle
        'Results': results, # shit
        'Success Rate': success_rate # the most important
    }
    
    return output