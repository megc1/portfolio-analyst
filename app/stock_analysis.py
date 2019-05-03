#make sure ticker symbol is value by testing using start date 04-01-2019
def check_ticker(ticker_symbol):
    return get_data(ticker_symbol)

#sorting percentages tutorial: https://www.geeksforgeeks.org/python-sort-a-list-of-percentage/
def sort_growth(a_list):
    a_list.sort(key = lambda x: float (x[:-1]))
    return a_list

#gets smallest growth percentage
def min_growth(b_list):
    min_value = sort_growth(b_list)[0]
    return min_value

#gets largest growth percentage
def max_growth(c_list):
    max_value = sort_growth(c_list)[-1]
    return max_value

def maketable(analysis_table):
    #header
    output = " Performance Metrics by Stock "
    output += "\n------------------------------------------------------------------"
    #rows
    for item in analysis_table[0:]:
        output += "\n"
        for est in item:
            output += "  |   " + str(est)  +   "  |   "
    return output

if __name__ == "__main__":

    import datetime as dt
    import pandas as pd
    import quandl
    import matplotlib.pyplot as plt
    import os
    from dotenv import load_dotenv
    from yahoo_fin.stock_info import get_analysts_info, get_data
    #http://www.fpdf.org/en/tutorial/index.php
    from fpdf import FPDF
    #REFERENCED: https://www.programcreek.com/python/example/90889/dotenv.load_dotenv
    load_dotenv()

    #API Configuration
    #REFERENCED: https://docs.quandl.com/docs/python-installation#section-authentication
    quandl.ApiConfig.api_key = os.environ.get('QUANDL_API_KEY')

    #welcome message
    print("Welcome to your portfolio analysis tool!")
    stock_tickers = [] #ticker symbols of stocks in portfolio
    data = []

    #Input validation of stock tickers
    #TO DO: add validation to look up stock ticker and make sure it exists 
    while True: 
        ticker_choice = input("Which stock would you like to add to your portfolio? Please enter its ticker symbol or enter \"DONE\" if finished. ")
        if ticker_choice == "DONE":
            break
        elif ticker_choice == "done":
            break
        elif not ticker_choice.isalpha():
            print("This doesn't seem to be a valid stock ticker. Please try again!")
            continue
        else:
            try:
                check_ticker(ticker_choice)
                stock_tickers.append(ticker_choice)
            except ValueError:
                print("Having trouble finding that ticker symbol! Please check if it is correct and try again.")

    #REFERENCED: https://www.quandl.com/tools/python
    #REFERENCED: https://pythonprogramming.net/using-quandl-data/
    #REFERENCED: https://plot.ly/matplotlib/figure-labels/
    #REFERENCED: https://docs.quandl.com/docs/python-tables
    #REFERENCED: https://stackoverflow.com/questions/32490629/getting-todays-date-in-yyyy-mm-dd-in-python, https://stackoverflow.com/questions/5158160/python-get-datetime-for-3-years-ago-today
    end = dt.datetime.today() - dt.timedelta(days=1)
    start = dt.datetime.today() - dt.timedelta(days=365)
    end = end.strftime('%Y-%m-%d')
    start = start.strftime('%Y-%m-%d')

    #Yahoo Finance Workaround
    next_year = str(dt.date.today().year + 1)
    year_category = "Next Year (" + next_year + ")"
    earnings_estimates = []
    eps_trends = []
    growth_estimates = []
    negative_growth_stocks = []
    positive_growth_stocks = []

    for ticker in stock_tickers:
        analysts_data = get_analysts_info(ticker)
        this_earnings_est = analysts_data['Earnings Estimate'].iloc[1][4]
        earnings_estimates.append(this_earnings_est)
        this_eps_trend = analysts_data['EPS Trend'].iloc[0][4]
        eps_trends.append(this_eps_trend)
        this_gest = analysts_data['Growth Estimates'].iloc[0][1]
        growth_estimates.append(this_gest)
        if '-' in this_gest:
            negative_growth_stocks.append(ticker)
            
        else:
            positive_growth_stocks.append(ticker)
        
    neg_growth_string = ", ".join(negative_growth_stocks)
    pos_growth_string = ", ".join(positive_growth_stocks)

    average_value = 0.0
    min_value = 0.0
    max_value = 0.0
    list_length = 0

    #growth estimates sorted and converted to float:
    sorted_growth = sort_growth(growth_estimates)

    #find smallest growth, highest growth, and average growth
    lowest_growth = (min_growth(sorted_growth))
    highest_growth = (max_growth(sorted_growth))


    #Quandl wiki no longer updating, useful for 2017-2018 fiscal year data but not today's data
    data = quandl.get_table('WIKI/PRICES', ticker = stock_tickers, qopts = { 'columns': ['date', 'ticker', 'adj_close'] }, date = { 'gte': '2017-01-01', 'lte': '2018-12-31'}, paginate=True)
    df = data.set_index('date')
    table = df.pivot(columns='ticker')
    returns = table.pct_change()


    #Returns chart
    plt.figure(figsize=(20, 8))
    for col in returns.columns.values:
        plt.plot(returns.index, returns[col], lw=3, alpha=0.8,label=col)
        plt.legend(loc=1, fontsize=12)
        plt.ylabel('Individual Daily Returns')
        plt.xlabel('Date')
        plt.title('How have your stocks performed in the past?')
    #REFERENCE: https://matplotlib.org/api/_as_gen/matplotlib.pyplot.savefig.html
    plt.savefig('past_returns.png') #Save chart to png


    #Reference: https://stackoverflow.com/questions/51864730/python-what-is-the-process-to-create-pdf-reports-with-charts-from-a-db
    #Reference (FPDF documentation/tutorial/examples): https://github.com/reingart/pyfpdf
    written_date = dt.datetime.today().strftime('%Y-%m-%d')
    portfolio_list = []
    for ticker in stock_tickers:
        portfolio_list.append(ticker)
    portfolio_string = ", ".join(portfolio_list)

    #REFERENCED: https://www.youtube.com/watch?v=1tw9KW6JspY
    analysis_table = [[' Stock '], stock_tickers, [' Earnings Estimate '], earnings_estimates, [' EPS Trend '], eps_trends, [' Growth Estimate '], growth_estimates]


    pdf = FPDF('L', 'mm', 'A4')
    pdf.add_page('L')
    pdf.set_font("Arial", size=24)
    pdf.cell(80, 10, "Your Portfolio Analysis", 0, 2, 'C')
    pdf.set_font("Arial", size = 14)
    pdf.cell(80, 25, "Your portfolio includes " + portfolio_string + " .")
    pdf.cell(20, 20, " ", 0, 2, 'C')
    pdf.set_font('Arial', size = 12)
    #REFERENCE: https://pyfpdf.readthedocs.io/en/latest/reference/multi_cell/index.html
    pdf.multi_cell(0, 10, maketable(analysis_table), 0, 4, 'C')
    #pdf.cell(-30)
    pdf.cell(10, 15, "Positive growth stocks may indicate future profitability. Consider further evaluating negative growth stocks within your portfolio.")
    pdf.cell(10, 5, " ", 0, 2, 'C')
    pdf.cell(10, 15, "The growth estimaates in your portfolio range from "  + lowest_growth + " to " + highest_growth + ".")
    pdf.cell(20, 10, " ", 0, 2, 'C')
    pdf.cell(0, 10, "Your positive growth stocks: " + pos_growth_string + ".", 6, 4, 'C')
    pdf.cell(20, 10, " ", 0, 2, 'C')
    pdf.cell(0, 10, "Your negative growth stocks: " + neg_growth_string + ".", 6, 4, 'C')
    #Referenced documentation: https://pyfpdf.readthedocs.io/en/latest/reference/image/index.html
    pdf.add_page('L')
    w = 70
    h = 60
    pdf.image('past_returns.png', x=0, y=25, w=290, h=140)
    pdf.output("PortfolioAnalysis" + written_date + ".pdf", 'F')



