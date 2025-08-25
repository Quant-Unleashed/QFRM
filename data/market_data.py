import yfinance as yf

# Function to download data
def download_data(ticker, period='1y', interval='1d'):
    data = yf.download(ticker, period=period, interval=interval)
    return data

# Examples for daily data (interval='1d')
stock_daily = download_data('AAPL', period='1y', interval='1d')  # Stock (cash)
index_daily = download_data('^GSPC', period='1y', interval='1d')  # Index
futures_daily = download_data('CL=F', period='1y', interval='1d')  # Futures (derivative)

# Examples for intra-day data (e.g., 5-minute bars, shorter period due to limits)
stock_intra = download_data('AAPL', period='5d', interval='5m')  # Stock
index_intra = download_data('^GSPC', period='5d', interval='5m')  # Index
futures_intra = download_data('CL=F', period='5d', interval='5m')  # Futures

# For options (derivative): First get chain, then download historical for a specific contract
ticker_obj = yf.Ticker('AAPL')
exp_dates = ticker_obj.options  # List of expiration dates
chain = ticker_obj.option_chain(exp_dates[0])  # Get calls/puts for first expiration
option_symbol = chain.calls.iloc[0]['contractSymbol']  # e.g., 'AAPL250829C00180000'
option_daily = download_data(option_symbol, period='1mo', interval='1d')  # Options data (may be limited)
option_intra = download_data(option_symbol, period='5d', interval='5m')  # Intra-day if available

# Save to CSV example
# stock_daily.to_csv('aapl_daily.csv')

# Print sample
print(stock_daily.head())