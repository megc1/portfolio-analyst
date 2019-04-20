import datetime as dt
import pandas as pd
import quandl
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv
#REFERENCED: https://www.programcreek.com/python/example/90889/dotenv.load_dotenv
load_dotenv()

#REFERENCED: https://docs.quandl.com/docs/python-installation#section-authentication
quandl.ApiConfig.api_key = os.environ.get('QUANDL_API_KEY')

#welcome message
print("Welcome to your portfolio analysis tool!")
stock_tickers = [] #ticker symbols of stocks in portfolio

#Input validation of stock tickers
#TO DO: add validation to look up stock ticker and make sure it exists 
while True: 
    ticker_choice = input("Which stock would you like to add to your portfolio? Please enter its ticker symbol or enter \"DONE\" if finished. ")
    if ticker_choice == "DONE":
        break
    elif not ticker_choice.isalpha():
        print("This doesn't seem to be a valid stock ticker. Please try again!")
        continue
    else:
        stock_tickers.append(ticker_choice)
#TO DO: Create necessary charts
#To DO: Create necessary Graphs
#REFERENCED: https://www.quandl.com/tools/python
#REFERENCED: https://pythonprogramming.net/using-quandl-data/
#REFERENCED: https://plot.ly/matplotlib/figure-labels/
#REFERENCED: https://docs.quandl.com/docs/python-tables
data = quandl.get_table('WIKI/PRICES', ticker = stock_tickers, qopts = { 'columns': ['date', 'ticker', 'adj_close'] }, date = { 'gte': '2017-1-1', 'lte': '2018-12-31' }, paginate=True)
data.head()
df = data.set_index('date')
table = df.pivot(columns='ticker')
returns = table.pct_change()
plt.figure(figsize=(20, 8))
for col in returns.columns.values:
    plt.plot(returns.index, returns[col], lw=3, alpha=0.8,label=col)
    plt.legend(loc=1, fontsize=12)
plt.show()
#TO DO: make dates dynamic
#TO DO: Output analysis
#TO DO: create summary document


