import datetime as dt
import pandas as pd
import quandl
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv
#http://www.fpdf.org/en/tutorial/index.php

from fpdf import FPDF
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
#REFERENCED: https://stackoverflow.com/questions/32490629/getting-todays-date-in-yyyy-mm-dd-in-python, https://stackoverflow.com/questions/5158160/python-get-datetime-for-3-years-ago-today
end = dt.datetime.today() - dt.timedelta(days=1)
start = dt.datetime.today() - dt.timedelta(days=365)
end = end.strftime('%Y-%m-%d')
start = start.strftime('%Y-%m-%d')

#####Quandl wiki no longer updating, useful for 2017-2018 fiscal year data but not today's data
data = quandl.get_table('WIKI/PRICES', ticker = stock_tickers, qopts = { 'columns': ['date', 'ticker', 'adj_close'] }, date = { 'gte': '2017-01-01', 'lte': '2018-12-31'}, paginate=True)
df = data.set_index('date')
table = df.pivot(columns='ticker')
returns = table.pct_change()

######Returns chart
plt.figure(figsize=(20, 8))
for col in returns.columns.values:
    plt.plot(returns.index, returns[col], lw=3, alpha=0.8,label=col)
    plt.legend(loc=1, fontsize=12)
    plt.ylabel('Individual Daily Returns')
    plt.xlabel('Date')
    plt.title('Individual Stock Returns in the Last Fiscal Year')
#REFERENCE: https://matplotlib.org/api/_as_gen/matplotlib.pyplot.savefig.html
plt.savefig('past_returns.png') #Save chart to png
######plt.show()

#TO DO: Output analysis
#TO DO: create summary document


#Reference: https://stackoverflow.com/questions/51864730/python-what-is-the-process-to-create-pdf-reports-with-charts-from-a-db
#Rerence (FPDF documentation/tutorial/examples): https://github.com/reingart/pyfpdf

written_date = dt.datetime.today().strftime('%Y-%m-%d')

pdf = FPDF('P', 'mm', 'A4')
pdf.add_page('P')
pdf.set_font("Arial", size=14)
pdf.cell(80, 10, "Your Portfolio Analysis", 0, 2, 'C')

pdf.output("PortfolioAnalysis" + written_date + ".pdf", 'F')



