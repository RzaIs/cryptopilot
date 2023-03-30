import yfinance as yf
import datetime as dt
import math
import pandas as pd

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
    
    # Calculate the success rate of the recommendations
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
                        
    success_rate = success/count if count > 0 else 0
    
    
    return {
        'dates' : list(data.index), # plot points on (1)(2) x axis
        'k_percent': list( # both to plot together independently (2) y axis
            map(lambda e: None if math.isnan(e) else e, k_percent)
        ),
        'd_percent': list( # both to plot together independently (2) y axis
            map(lambda e: None if math.isnan(e) else e, d_percent)
        ),
        'close': list(data['Close'].values),     # plot (1) y axis
        'buy_dates': list(buy_dates), # plot points on (1)(2) x axis
        'buy_points' : list(buy_points), # plot points on (1)(2) y axis
        'sell_dates':list(sell_dates), # plot points on (1)(2) x axis
        'sell_points' : list(sell_points), # plot points on (1)(2) y axis
        'success_rate': success_rate # the most fudjking important 
    }
