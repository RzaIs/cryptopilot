import yfinance as yf
import datetime as dt


coins = ['BTC-USD', 'ETH-USD', 'ADA-USD']
interval = ['15m', '30m', '1h', '1d', '1w']

end_date = dt.datetime.strptime("2023-01-01", "%Y-%m-%d").date()
start_date = end_date - dt.timedelta(days=365) # for 1 year
ticker, interval = coins[2], interval[3]


def calculate_macd(ticker, start_date, end_date, interval):
    
    # Download historical data for any Crypto Coin (ticker)
    data = yf.download(ticker, start = start_date, end = end_date, interval=interval)

    # Calculate the MACD values
    exp1 = data['Close'].ewm(span=12, adjust=False).mean()
    exp2 = data['Close'].ewm(span=26, adjust=False).mean()
    macd = exp1 - exp2
    signal = macd.ewm(span=9, adjust=False).mean()
    histogram = macd - signal

    # Find the buy and sell dates based on the MACD and signal line crossovers
    buy_dates, sell_dates = [], []
    for i in range(1, len(macd)):
        if macd[i] > signal[i] and macd[i-1] <= signal[i-1]:
            buy_dates.append(macd.index[i])
        elif macd[i] < signal[i] and macd[i-1] >= signal[i-1]:
            sell_dates.append(macd.index[i])

    # Evaluate the success rate of the MACD indicator
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
         
    # Return the MACD values, buy and sell dates, results, and success rate
    output = {
        'MACD': macd,
        'Signal': signal,
        'Histogram': histogram,
        'Buy Dates': buy_dates,
        'Sell Dates': sell_dates,
        'Results': results,
        'Success Rate': success_rate
    }

    return output
