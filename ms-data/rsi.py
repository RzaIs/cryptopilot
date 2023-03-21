import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

coins = ['BTC-USD', 'EHT-USD', 'ADA-USD']
interval = ['15m', '30m', '1h', '1d', '1w']
ticker, interval = coins[2], interval[3]

def calculate_RSI(ticker, interval):
    # Get data from Yahoo Finance for 1 year period with 1-day intervals for given ticker
    data = yf.download(ticker, period='1y', interval=interval)

    # Calculate the differences between the closing prices of each day
    price_diff = data['Close'].diff()

    # Drop the first row, which is null
    price_diff = price_diff.dropna()

    # Calculate the changes in price for up and down movements
    pos_price = price_diff.clip(lower=0)
    neg_price = price_diff.clip(upper=0).abs()

    # Calculate the rolling average of the up and down price movements
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
            results.append('Negative')
        else:
            results.append('Positive')

    for date in buy_dates:
        if data.loc[date, 'Close'] > data.loc[date-pd.Timedelta(days=1), 'Close']:
            results.append('Positive')
        else:
            results.append('Negative')

    # Calculate the success rate of the recommendations
    success_rate = results.count('Positive') / len(results) * 100

#     # Print the results
#     print('RSI Values:', rsi)
#     print('Sell Dates:', sell_dates)
#     print('Buy Dates:', buy_dates)
#     print('Results:', results)
#     print('Success Rate: %.2f%%' % success_rate)

    output = {
        'RSI': rsi,
        'Sell Dates': sell_dates,
        'Buy Dates': buy_dates,
        'Results': results,
        'Success Rate': success_rate
    }
    
    return output

#     return rsi, sell_dates, buy_dates, results, success_rate


def plot_RSI(ticker, interval):
    # Calculate RSI values and buy/sell dates using calculate_RSI function
    rsi = calculate_RSI(ticker, interval)['RSI']
    sell_dates = calculate_RSI(ticker, interval)['Sell Dates']
    buy_dates = calculate_RSI(ticker, interval)['Buy Dates']

    rsi_df = rsi.to_frame().reset_index()
    sell_indexes = rsi_df[rsi_df['Date'].apply(lambda x: x in sell_dates)].index
    buy_indexes = rsi_df[rsi_df['Date'].apply(lambda x: x in buy_dates)].index
    
    
    # Get data from Yahoo Finance for 1 year period with 1-day intervals for given ticker
    data = yf.download(ticker, period='1y', interval=interval)

    # Set the theme of our chart
    plt.style.use('fivethirtyeight')

    # Make our resulting figure much bigger
    plt.rcParams['figure.figsize'] = (20, 20)

    # Create two charts on the same figure.
    ax1 = plt.subplot2grid((10,1), (0,0), rowspan = 4, colspan = 1)
    ax2 = plt.subplot2grid((10,1), (5,0), rowspan = 4, colspan = 1)

    # First chart:
    # Plot the closing price on the first chart
    ax1.plot(data['Close'], linewidth=2)
    ax1.set_title('Bitcoin Close Price')

    # Second chart
    # Plot the RSI
    ax2.set_title('Relative Strength Index')
    ax2.plot(rsi, color='orange', linewidth=1)
    # Add two horizontal lines, signalling the buy and sell ranges.
    # Oversold
    ax2.axhline(30, linestyle='--', linewidth=1.5, color='green')
    # Overbought
    ax2.axhline(70, linestyle='--', linewidth=1.5, color='red')

    # Add markers for the buy and sell signals
    ax1.plot(sell_dates, data.iloc[sell_indexes - 1]['Close'], 'r^', markersize=8)
    ax1.plot(buy_dates, data.iloc[buy_indexes - 1]['Close'], 'g^', markersize=8)
    ax2.plot(sell_dates, rsi.iloc[sell_indexes - 1], 'r^', markersize=8)
    ax2.plot(buy_dates, rsi.iloc[buy_indexes - 1], 'g^', markersize=8)

    # Display the charts
    plt.show()


# Calling the functions

# calculate_RSI(ticker, interval)
plot_RSI(ticker, interval)