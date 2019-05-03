# Portfolio Analyst
[![Build Status](https://travis-ci.org/megc1/portfolio-analyst.svg?branch=master)](https://travis-ci.org/megc1/portfolio-analyst)

## About

This program provides extra information about the user's stock portfolio by allowing users to enter the ticker symbols for each of the stocks they are holding, and returning up-to-date information on important stock evaluation metrics. Users are provided information on their most promising and least promising stocks, based on whether the stock is expected to demonstrate positive or negative growth in the near future, as well as information on the high-to-low range of growth for the portfolio as a whole. This information is then copied to a PDF and formatted in a readable way, before being stored to the user's device.

## How to Get Started

Fork this repository and clone or download it to your local device. Create a virtual environment for this project, activate it, and install the necessary packages (listed under installations).

### Prerequisites

Python 3.7, Pip

### Installations

Using pip, install the following in your virtual environment:
```sh
+ pandas
+ matplotlib
+ python-dotenv
+ fpdf
+ yahoo-fin
+ quandl
```
Note: Yahoo fin has the following dependencies: io, pandas, requests, requests_html. Each of these comes with Anaconda, except for requests_html which you must install.

## Credentials

You will need a Quandl API key to run this program. Inside a .env file in the root directory of your repository, please enter the following: QUANDL_API_KEY = "MY-API-KEY" with your key in place of MY-API-KEY. 
```sh
Ex: QUANDLE_API_KEY = "AbCdE123456789"
```
You can sign up for Quandl and get an API key [here](https://www.quandl.com/sign-up-modal?defaultModal=showSignUp).

## To run

To run this program, navigate to the command line of your computer and activate your virtual environment. Use the command line to navigate to your portfolio-analyst folder and run:
```sh
python app/stock_analysis.py
```

## How to use

Follow the prompts given to you on the command line and enter the ticker symbols for each stock you would like to include in your portfolio. Enter "Done" when finished. The program will create a portfolio pdf for you, titled with the following format: Portfolio-AnalysisYYYY-MM-DD.pdf using the date you ran the analysis which you can refer to by navigating to your portfolio-analyst folder and going into the app folder.

## To test

This program can be tested using pytest, which can be downloaded to the virtual environment to run tests from the command line with the pytest command. 
```sh
pytest 
```
It is recommended to deploy the project to a continuous integration service, such as [Travis CI](https://travis-ci.org/) for continuous automated testing as further modifications are made to the code. 


## License

This program is licensed under the terms of the MIT License. For more detailed information see [LICENSE.md](LICENSE.md).

## Reference List

For a list of references, see [CREDITS.md](CREDITS.md).