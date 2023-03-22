# Moving Average

import yfinance as yf
import math

coins = ['BTC-USD', 'ETH-USD', 'ADA-USD']
interval = ['15m', '30m', '1h', '1d', '1w']
ticker, interval = coins[2], interval[3]
day1, day2 = 5,150 # user input

def calculate_moving_average(ticker, interval, day1, day2):
    
    # Download historical data for any Crypto Coin (ticker)
    data = yf.download(ticker, period = "1y", interval = interval)

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

    if len(results) > 0:
         success_rate = results.count('Success') / len(results)
    else:
         success_rate = 0


    # Return the moving average values, buy and sell dates, results, and success rate
    # return data['Close'],ma1, ma2, buy_dates, sell_dates, results, success_rate

    output = {
        'Coin_Close': list(data['Close']), # plot
        'MA1': list(
            map(lambda e:  None if math.isnan(e) else e, ma1)
        ), # plot
        'MA2': list(
            map(lambda e: None if math.isnan(e) else e, ma2)
        ), # plot
        'Sell Dates': list(sell_dates), # plot
        'Buy Dates': list(buy_dates), # plot
        'Results': list(results), # shit
        'Success Rate': success_rate # the most important (changes depend on user input, maybe we can give some default value maybe at first, idk)
    }
    
    return output

    # For Plotting : data['Close'], ma1, ma2, + in a triangle form(buy_dates, sell_dates)
    # Note for the website : day2 must be bigger than day1
