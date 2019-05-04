#make sure ticker symbol is value by testing using start date 04-01-2019
def check_ticker(ticker_symbol):
    return get_data(ticker_symbol)

#sort list of string percentages and return float version
#Reference: Python #1
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

#create table of stock data
#Reference: Python #4
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
    from fpdf import FPDF
    load_dotenv()
    #References: Python #2, FPDF #1, Quandl #1

    #API Configuration
    quandl.ApiConfig.api_key = os.environ.get('QUANDL_API_KEY')

    #Welcome message
    print("Welcome to your portfolio analysis tool!")
    stock_tickers = [] #ticker symbols of stocks in portfolio
    data = []

    #Input validation of stock tickers
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
    #prevent error from entering a portfolio with no stocks from reaching user
    if len(stock_tickers) == 0:
        print("Your portfolio is empty. To create an analysis PDF, you must enter at least one stock into your portfolio.")
    else:
        #References: Quandl #2/3, Matplotlib #1
        #Yahoo Finance Workaround, scrapes data off of Yahoo Finance webpage
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

        min_value = 0.0
        max_value = 0.0

        #growth estimates sorted and converted to float:
        sorted_growth = sort_growth(growth_estimates)

        #find smallest growth, highest growth, and average growth
        lowest_growth = (min_growth(sorted_growth))
        highest_growth = (max_growth(sorted_growth))


        #Quandl wiki no longer updating: Gives good historical overview of trends, in the future (2+ years) would be wise to take advantage of one of the stock data APIs currently in development to replace the deprecated ones for more up-to-date data
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
            #Reference: Matplotlib #2
        plt.savefig('past_returns.png') #Save chart to png

            
        #Reference: FPDF #2
        written_date = dt.datetime.today().strftime('%Y-%m-%d')
        portfolio_list = []
        for ticker in stock_tickers:
            portfolio_list.append(ticker)
        portfolio_string = ", ".join(portfolio_list)

        analysis_table = [[' Stock '], stock_tickers, [' Earnings Estimate '], earnings_estimates, [' EPS Trend '], eps_trends, [' Growth Estimate '], growth_estimates]
        
        #Reference: FPDF #3, #4            
        pdf = FPDF('L', 'mm', 'A4')
        pdf.add_page('L')
        pdf.set_font("Arial", size=24)
        pdf.cell(80, 10, "Your Portfolio Analysis", 0, 2, True, 'C')
        pdf.set_font("Arial", size = 14)
        pdf.cell(80, 25, "Your portfolio includes " + portfolio_string + " .")
        pdf.cell(20, 20, " ", 0, 2, 'C')
        pdf.set_font('Arial', size = 12)
        pdf.multi_cell(0, 10, maketable(analysis_table), 0, 4, 'C')
        pdf.cell(10, 5, " ", 0, 2, 'C')
        pdf.cell(10, 2, "Positive growth stocks may indicate future profitability. Consider further evaluating negative growth stocks within your portfolio.", 0, 1, 'L')
        pdf.cell(10, 5, " ", 0, 2, 'C')
        pdf.cell(10, 2, "The growth estimates in your portfolio range from "  + lowest_growth + " to " + highest_growth + ".", 0, 1, 'L')
        pdf.cell(20, 10, " ", 0, 2, 'C')
        if len(positive_growth_stocks)>0:
            pdf.cell(0, 0, "Your positive growth stocks: " + pos_growth_string + ".", 0, 1, 'L')
        else:
            pdf.cell(0, 0, "You have no positive growth stocks.", 1, 1, 'L')
        pdf.cell(20, 8, " ", 0, 2, 'C')
        if len(negative_growth_stocks)>0:
            pdf.cell(0, 0, "Your negative growth stocks: " + neg_growth_string + ".", 0, 1, 'L')
        else:
            pdf.cell(0, 0, "You have no negative growth stocks.", 6, 4, 'L')
        pdf.add_page('L')
        w = 70
        h = 60
        pdf.set_font("Arial", size=24)
        pdf.cell(80, 15, "Historical Performance of Your Stocks", 0, 2, True, 'C')
        pdf.set_font("Arial", size = 12)
        pdf.image('past_returns.png', x=0, y=35, w=290, h=140)
        pdf.cell(10, 3, "Historical returns may present insights into the stability and long-term viability of each of the stocks in your portfolio.", 0, 1, 'L')
        pdf.cell(10, 5, " ", 0, 1, 'C')
        pdf.cell(20, 3, "Look for relative consistency and a history of positive returns to identify more trustworthy long-term investments.", 0, 1, 'L')
        pdf.output("PortfolioAnalysis" + written_date + ".pdf", 'F')          