import pandas as pd

def successRate(buy_dates, buy_points, sell_dates, sell_points):
    sell_df = pd.DataFrame({'Date': sell_dates, 'Close' : sell_points, 'status' : 0})
    buy_df = pd.DataFrame({'Date': buy_dates, 'Close' : buy_points, 'status' : 1})

    df = pd.concat([sell_df, buy_df])
    df = df.sort_values(by = ['Date'])
    df = df.reset_index(drop = True)
    
    status = 1
    i = 0
    count = 0
    success = 0
    while(i<len(df)):
        if(status and df.iloc[i].status ==  1):
            status = 0
        if(status == 0):
            buy, sell = [], []
            if(df.iloc[i].status ==  1):
                while(i < len(df) and df.iloc[i].status ==  1):
                    buy.append(df.iloc[i].Close)
                    i+=1
                while(i < len(df) and df.iloc[i].status ==  0):
                    sell.append(df.iloc[i].Close)
                    i+=1
            if(buy != [] and sell != 0):
                for m in range(len(buy)):
                    for n in range(len(sell)):
                        count+=1
                        if(buy[m] <= sell[n]):
                            success+=1
        else:
            i+=1

    success_rate = success/count * 100 if count > 0 else 0
    
    return success_rate