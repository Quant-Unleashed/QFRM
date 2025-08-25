import urllib.request
import json
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Optional


def get_openexchangerates_api(url: str, api_key: str) -> dict:
    """Helper to make API calls with App ID."""
    url = f"{url}&app_id={api_key}"
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode())
    if 'error' in data:
        raise Exception(f"API Error: {data['description']}")
    return data


def get_currency_list(api_key: str) -> List[str]:
    """Fetch list of supported currency codes."""
    url = "https://openexchangerates.org/api/currencies.json"
    data = get_openexchangerates_api(url, api_key)
    return list(data.keys())


def get_latest_rates(api_key: str, base: str = 'USD') -> pd.DataFrame:
    """Fetch latest exchange rates."""
    url = f"https://openexchangerates.org/api/latest.json?base={base}"
    data = get_openexchangerates_api(url, api_key)
    rates = data['rates']
    timestamp = pd.to_datetime(data['timestamp'], unit='s')
    df = pd.DataFrame([rates])
    df['timestamp'] = timestamp
    return df.set_index('timestamp')


def get_historical_rates(api_key: str, date: str, base: str = 'USD') -> pd.DataFrame:
    """Fetch historical exchange rates for a specific date (YYYY-MM-DD)."""
    url = f"https://openexchangerates.org/api/historical/{date}.json?base={base}"
    data = get_openexchangerates_api(url, api_key)
    rates = data['rates']
    timestamp = pd.to_datetime(data['timestamp'], unit='s')
    df = pd.DataFrame([rates])
    df['date'] = date
    return df.set_index('date')


def get_historical_range(api_key: str, start_date: str, end_date: str, base: str = 'USD') -> pd.DataFrame:
    """Fetch historical rates for a date range (YYYY-MM-DD)."""
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    delta = end - start
    data_frames = []

    for i in range(delta.days + 1):
        date = (start + timedelta(days=i)).strftime('%Y-%m-%d')
        try:
            df = get_historical_rates(api_key, date, base)
            data_frames.append(df)
            print(f"Fetched data for {date}")
        except Exception as e:
            print(f"Failed to fetch {date}: {e}")

    if data_frames:
        return pd.concat(data_frames)
    return pd.DataFrame()


# Example usage
api_key = 'your_api_key'  # Replace with your actual API key

# Get list of currencies
currencies = get_currency_list(api_key)
print(f"Supported currencies: {currencies}")
# Save to CSV
# pd.DataFrame({'currency': currencies}).to_csv('currencies.csv', index=False)

# Get latest rates
latest = get_latest_rates(api_key)
print("\nLatest rates:")
print(latest)
# latest.to_csv('latest_exchange_rates.csv')

# Get historical rates for a single date
historical = get_historical_rates(api_key, '2025-08-01')
print("\nHistorical rates (2025-08-01):")
print(historical)
# historical.to_csv('historical_exchange_rates_20250801.csv')

# Get historical rates for a date range
historical_range = get_historical_range(api_key, '2025-07-01', '2025-08-01')
print("\nHistorical range (2025-07-01 to 2025-08-01):")
print(historical_range.tail())
# if not historical_range.empty:
#     historical_range.to_csv('historical_exchange_rates_range.csv')