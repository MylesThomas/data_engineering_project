import os
import time
import datetime
import timeit
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf

SCRIPT_DIR = os.getcwd()
PARENT_DIR = os.path.dirname(SCRIPT_DIR)
print(f"script directory: {SCRIPT_DIR}")

start_of_script_time = (

    timeit.default_timer()

)

today = datetime.date.today()
delta = datetime.timedelta(days=7)

tix = ['BTC-USD', 'ETH-USD', 'SOL-USD']
start = today - delta
end = today

data = yf.download(
    tickers=tix,
    period='1d',   # Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
    interval="1h", # Valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
    start=start,
    end=end,
)

data = data['Adj Close']
data.index = pd.to_datetime(data.index)
data.reset_index(inplace=True)

data_melted = pd.melt(
    data,
    id_vars=['Datetime'], # id
    value_vars=['BTC-USD', 'ETH-USD', 'SOL-USD'], # values are in these 3 columns
    var_name='Ticker', # name of the category in value_vars
    value_name='Adj Close' # what the tickers are measuring
)

data_melted.to_csv(os.path.join(SCRIPT_DIR, f"{today}.csv"), index=False)

print("The Modeling Script has finished running.")

print(

    f"Entire Script Runtime (Minutes): {(timeit.default_timer() - start_of_script_time) / 60:.2f}"

)  # make sure to remove from final version of document
