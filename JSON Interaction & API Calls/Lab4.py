# https://github.com/pimeas/Lab-4.git
import json
import requests
import pandas
import yfinance as yf
from datetime import date

try:
    stock = input("Enter stock Ticker Symbol: ")
    # data = yf.download(stock, start="2020-01-01", end="2020-04-30")
    data = yf.Ticker(stock)

# step 1 set up url where is this enpoint that I want
# base url https://query1.finance.yahoo.com/v7/finance/quote
    urlQuote = 'https://query1.finance.yahoo.com/v7/finance/quote'
    querystring = {"symbols": stock}
    header_var = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    response = requests.request("GET", urlQuote, headers = header_var, params = querystring)
    stock_json = response.json()

    # Displaying the Name Ticker, Full Name of the Stock
    name_ticker = stock_json['quoteResponse']['result'][0]['symbol']
    full_name = stock_json['quoteResponse']['result'][0]['longName']

    # 2nd endpoint
    urlQuote2 = "https://query1.finance.yahoo.com/v10/finance/quoteSummary/"
    querystring2 = {"symbol": stock, "modules" : "financialData"}

    response = requests.request("GET", urlQuote2, headers = header_var, params = querystring2)
    stock_json = response.json()

    # Displaying the Current Price, Target Mean Price, Cash on Hand, Profit Margins
    current_price = stock_json['quoteSummary']['result'][0]['financialData']['currentPrice']
    target_mean_price = stock_json['quoteSummary']['result'][0]['financialData']['targetMeanPrice']
    cash_on_hand = stock_json['quoteSummary']['result'][0]['financialData']['totalCash']
    profit_margins = stock_json['quoteSummary']['result'][0]['financialData']['profitMargins']

    print("Name Ticker: ", name_ticker, "\n",
          "Full Name of the Stock: ", full_name, "\n",
          "Current Price: ", current_price, "\n",
          "Target Mean Price: ", target_mean_price, "\n",
          "Cash on Hand: ", cash_on_hand, "\n",
          "Profit Margins: ", profit_margins)

    # date
    today = date.today()
    today1 = today.strftime("%d/%m/%Y")

    stocks = {"Date" : today1,
              "Name Ticker" : name_ticker,
              "Full Name of the Stock" : full_name,
              "Current Price" : current_price,
              "Target Mean Price" : target_mean_price,
              "Cash on Hand" : cash_on_hand,
              "Profit Margins" : profit_margins}

    # json format
    json_form = json.dumps(stocks)

    with open("stockInformation.json", "w") as json_file:
        json_file.write(json_form)

except:
    print("The stock doesn’t exist and/or the API is not returning information")

