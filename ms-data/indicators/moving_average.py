# Moving Average

import yfinance as yf
import datetime as dt
import math

coins = ['BTC-USD', 'ETH-USD', 'ADA-USD', 'DNB-USD', 'KRP-USD', 'OKB-USD', 'MATIC-USD', 'DOT-USD','SOL-USD',
         'LINK-USD', 'TRX-USD', 'LTC-USD', 'UNI-USD', 'AVAX-USD']
interval = ['15m', '30m', '1h', '1d', '1w']

end_date = dt.datetime.strptime("2023-01-01", "%Y-%m-%d").date()
start_date = end_date - dt.timedelta(days=365) # for 1 year
ticker, interval = coins[2], interval[3]
day1, day2 = 5,150 # user input

def calculate_moving_average(ticker, start_date, end_date, interval, day1, day2):
    
    # Get data from Yahoo Finance for 1 year period with 1-day intervals for given ticker
    data = yf.download(ticker, start = start_date, end = end_date, interval=interval)

    # Calculate the moving average values
    ma1 = data['Close'].rolling(window=day1).mean()
    ma2 = data['Close'].rolling(window=day2).mean()

    # Find the buy and sell dates based on the moving average values
    buy_dates = []
    sell_dates = []
    for i in range(day2, len(ma2)):  #considering day2 is bigger than day1
        if ma1[i] > ma2[i] and ma1[i-1] <= ma2[i-1]:
            buy_dates.append(ma2.index[i])
        elif ma1[i] < ma2[i] and ma1[i-1] >= ma2[i-1]:
            sell_dates.append(ma2.index[i])

    # Evaluate the success rate of the moving average indicator
    results = []
    for i in range(len(buy_dates)):
        if i < len(sell_dates):
            if sell_dates[i] > buy_dates[i]:
                results.append('Success')
            else:
                results.append('Failure')
        else:
            results.append('Open position')

    # Calculate the success rate of the recommendations
    success_rate = results.count('Success') / len(results) if len(results) > 0 else 0

    return {
        'coin_cloes': list(data['Close']), # plot
        'ma1': list(
            map(lambda e:  None if math.isnan(e) else e, ma1)
        ), # plot
        'ma2': list(
            map(lambda e: None if math.isnan(e) else e, ma2)
        ), # plot
        'sell_dates': list(sell_dates), # plot
        'buy_dates': list(buy_dates), # plot
        'results': list(results), # shit
        'success_rate': success_rate # the most important (changes depend on user input, maybe we can give some default value maybe at first, idk)
    }
    
    # For Plotting : data['Close'], ma1, ma2, + in a triangle form(buy_dates, sell_dates)
    # Note for the website : day2 must be bigger than day1
