
# Most shorted stocks
# r/WSB Hardy method?

from tkinter import N
import requests
from bs4 import BeautifulSoup as bs

print("Welcome!")

class stock:
    def __init__(self, ticker):
        self.ticker = ticker
        self.name = None
        self.price = None
        self.shortInterest = None
        self.shortDate = None
        self.float = None
        self.floatShorted = None
        self.gammaMax = None
        self.deltaNeutral = None
        self.GammaNeutral = None
        self.changeDay = None
        self.changeWeek = None
        self.changeMonth = None
        self.changeYear = None

    def present(self):
        print(f"{self.ticker}: {self.price} (Shorted {self.shortInterest})")

def get_shorted_stocks():
    url = "https://www.marketwatch.com/tools/screener/short-interest"

    req = requests.get(url)
    # reqJSON = req.json()
    soup = bs(req.text, 'html.parser')
    cells = soup.find_all("div", class_="cell__content")

    listOfStocks = []
    col = 1
    for cell in cells:
        if col == 1:
            newStock = stock(cell.contents)
        elif col == 2:
            newStock.name = cell.contents
        elif col == 3:
            newStock.price = cell.contents
        elif col == 4:
            newStock.changeDay = cell.contents
        elif col == 5:
            newStock.changeYear = cell.contents
        elif col == 6:
            newStock.shortInterest = cell.contents
        elif col == 7:
            newStock.shortDate = cell.contents
        elif col == 8:
            newStock.foat = cell.contents
        elif col == 9:
            newStock.floatShorted = cell.contents

        col += 1
        if col == 10:
            col = 1


        
        listOfStocks.append(newStock)
    return listOfStocks

output = get_shorted_stocks()
for i in output:
    i.present()

print(len(output))
print(len(output)/51)