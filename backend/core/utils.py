import csv
import os
import requests

def load_stock_symbols():
    symbols = set()
    file_path = os.path.join(os.path.dirname(__file__), 'stocks.csv')
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # skip header
        for row in reader:
            symbols.add(row[0].strip())  # Assuming the symbol is in the first column
    return symbols

def get_current_stock_price(symbol):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1m&range=1d"
    response = requests.get(url)
    data = response.json()
    try:
        latest_price = data["chart"]["result"][0]["meta"]["regularMarketPrice"]
        return latest_price
    except (KeyError, IndexError, TypeError):
        return None