
###

from asyncio.windows_events import NULL
from pickle import NONE
from black import out
import requests
import json
from pprint import pprint
import pandas as pd

def get_and_save(ticker, region):
    url = "https://yh-finance.p.rapidapi.com/stock/v2/get-financials"

    querystring = {"symbol":ticker,"region":region}

    headers = {
        "X-RapidAPI-Host": "yh-finance.p.rapidapi.com",
        "X-RapidAPI-Key": "f2a083f14dmshf05953201a44851p1337f5jsnf17c2d8100b4"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(f"{type(response.json())=}")
    resp = response.json()

    with open(f"{ticker}.json", "w") as f:
        f.writelines(json.dumps(resp, indent=4))



def analyze_stock(ticker):
    with open(f"{ticker}.json", "r") as f:
        txt = f.read()
        input_dict = json.loads(txt)

    price = input_dict["price"]["regularMarketPrice"]["raw"]
    marketCap = input_dict["price"]["marketCap"]["raw"]
    sharesOutstanding = marketCap/price
    earnings = input_dict["earnings"]["financialsChart"]["yearly"][-1]["earnings"]["raw"]

    try:
        pe = input_dict["summaryDetail"]["trailingPE"]["raw"]
    except KeyError as e:
        print(e)
        pe = None

    forward_pe = input_dict["summaryDetail"]["forwardPE"]["raw"]

    yearly_earnings_dict = {}
    for i in input_dict["earnings"]["financialsChart"]["yearly"]:
        yearly_earnings_dict[i["date"]] = i["earnings"]["raw"]

    quarterly_earnings_dict = {}
    for i in input_dict["earnings"]["financialsChart"]["quarterly"]:
        quarterly_earnings_dict[i["date"]] = i["earnings"]["raw"]
    try:
        quarterly_earnings_dict[i["date"]] = input_dict["earnings"]["financialsChart"]["currentQuarterEstimate"]["raw"]
    except KeyError as e:
        print(f"Error: {e}")

    ebitda = input_dict["timeSeries"]["annualEbitda"][-1]["reportedValue"]["raw"]

    cash = input_dict["balanceSheetHistoryQuarterly"]["balanceSheetStatements"][0]["cash"]["raw"]
    shortTermDebt = input_dict["balanceSheetHistoryQuarterly"]["balanceSheetStatements"][0]["shortLongTermDebt"]["raw"]
    longTermDebt = input_dict["balanceSheetHistoryQuarterly"]["balanceSheetStatements"][0]["longTermDebt"]["raw"]
    totalDebt = shortTermDebt + longTermDebt

    enterpriseValue = marketCap + totalDebt - cash
    EV_to_EBITA = enterpriseValue / ebitda

    output_dict = {
        "ticker": ticker,
        "price": price,
        "marketCap": marketCap,
        "sharesOutstanding": sharesOutstanding,
        "earnings": earnings,
        "yearlyEarnings": yearly_earnings_dict,
        "quarterlyEarnings": quarterly_earnings_dict,
        "P/E": pe,
        "Forward P/E" : forward_pe,
        "EBITDA": ebitda,
        "EV": enterpriseValue,
        "EV/EBITDA": EV_to_EBITA
    }

    return output_dict


def get_comparison(sector):
    output_dict ={}

    pe_df = pd.read_excel("peGlobal.xls")
    #TODO make this work
    # print(pe_df["Retail"])



def main():
    ticker = input("Input ticker\n>>> ")
    if input("Region other than US? (y/n)\n>>> ") == "y":
        region = input("Enter region:\n>>> ")
    else:
        region = "US"

    if input("Fetch new data? (y/n)\n>>> ") == "y":
        get_and_save(ticker, region)
    
    data = analyze_stock(ticker)
    pprint(data, indent=4)

    print("THIS IS WRONG: WHERE ARE SHARES OUTSTANDING?")
    print("We want:\nDiscounted Cashflow Model\nComparison of P/E and EV/EBITDA\nMore?")


get_comparison("test")
# main()