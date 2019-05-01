# Portfolio Analyst

## About
This program provides extra information about the user's stock portfolio by allowing users to enter the ticker symbols for each of the stocks they are holding, and returning up-to-date information on important stock evaluation metrics. This information is then copied to a PDF and formatted in a readable way, before being stored to the user's device.

## How to Get Started
Fork this repository to your local device. Create a virtual environment for this project, activate it, and install the necessary packages (listed under installations).

## Prerequisites
Python 3.7, Pip

## Installations:
Using pip, install the following:
pandas, 
matplotlib, 
python-dotenv, 
fpdf, 
yahoo-fin, 
quandl

Yahoo fin has the following dependencies: io, pandas, requests, requests_html. Each of these comes with Anaconda, except for requests_html which you must install.

## Credentials:

You will need a Quandl API key to run this program. Inside a .env file, please enter the following: QUANDL_API_KEY = "MY-API-KEY" with your key in place of MY-API-KEY. You can sign up for Quandl and get an API key here: https://www.quandl.com/sign-up-modal?defaultModal=showSignUp

## To run:

To run this program, navigate to the command line of your computer and activate your virtual environment. Use the command line to navigate to your portfolio-analyst folder and run python portfolio-analyst/app/stock-analysis.py

## How to use:

Follow the prompts given to you on the command line and enter the ticker symbols for each stock you would like to include in your portfolio. Enter "Done" when finished. The program will create a portfolio pdf for you, titled with the following format: Portfolio-AnalysisYYYY-MM-DD.pdf using the date you ran the analysis which you can refer to by navigating to your portfolio-analyst folder and going into the app folder. 

