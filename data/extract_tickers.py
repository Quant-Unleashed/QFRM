import json
import urllib.request
import pandas as pd


def get_stock_tickers(exchange='NASDAQ'):
    # Exchanges: 'NASDAQ', 'NYSE', 'AMEX'
    url = f"https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=0&offset=0&exchange={exchange}&download=true"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())

    # Extract symbols, filter for valid stock-like tickers (e.g., exclude warrants, preferreds if needed)
    tickers = [row['symbol'] for row in data['data']['rows'] if
               row['symbol'] and not row['symbol'].startswith('^') and '$' not in row['symbol']]
    return pd.DataFrame({'tickers': tickers})


# Example usage
nasdaq_tickers = get_stock_tickers('NASDAQ')
nyse_tickers = get_stock_tickers('NYSE')
amex_tickers = get_stock_tickers('AMEX')

all_us_stocks = pd.concat([nasdaq_tickers, nyse_tickers, amex_tickers], ignore_index=True)
print(all_us_stocks)  # Or save to CSV: all_us_stocks.to_csv('us_stock_tickers.csv', index=False)