import urllib.request
import json
import pandas as pd
from typing import List


def get_fred_api(url: str) -> dict:
    """Helper to make API calls."""
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode())
    return data


def get_child_categories(category_id: int, api_key: str) -> List[dict]:
    """Get child categories for a given category ID."""
    url = f"https://api.stlouisfed.org/fred/category/children?category_id={category_id}&api_key={api_key}&file_type=json"
    data = get_fred_api(url)
    return data['categories']


def get_series_in_category(category_id: int, api_key: str) -> List[str]:
    """Get series IDs in a specific category."""
    url = f"https://api.stlouisfed.org/fred/category/series?category_id={category_id}&api_key={api_key}&file_type=json"
    data = get_fred_api(url)
    return [s['id'] for s in data['seriess']]


def get_all_series_ids_under_category(category_id: int, api_key: str) -> List[str]:
    """Recursively get all series IDs under a category and its subcategories."""
    series_ids = []
    children = get_child_categories(category_id, api_key)

    # If no children (leaf category), get series directly
    if len(children) == 0 or (len(children) == 1 and children[0]['id'] == category_id):
        series_ids.extend(get_series_in_category(category_id, api_key))
    else:
        # Recurse into children
        for child in children:
            if child['id'] != category_id:  # Avoid self-loop
                series_ids.extend(get_all_series_ids_under_category(child['id'], api_key))

    return list(set(series_ids))  # Deduplicate if any overlaps


def get_series_data(series_id: str, api_key: str, start_date: str = None, end_date: str = None) -> pd.DataFrame:
    """Fetch observations for a series ID as a DataFrame."""
    url = f"https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key={api_key}&file_type=json"
    if start_date:
        url += f"&observation_start={start_date}"
    if end_date:
        url += f"&observation_end={end_date}"

    data = get_fred_api(url)
    observations = data['observations']

    df = pd.DataFrame(observations)[['date', 'value']]
    df['date'] = pd.to_datetime(df['date'])
    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    return df.set_index('date').rename(columns={'value': series_id})


# Example usage
api_key = '11843c1faabba7e38517ca6000e3d10f'  # Replace with your actual API key

# Get all series IDs under Interest Rates (category ID 22)
interest_rates_category_id = 22
all_series_ids = get_all_series_ids_under_category(interest_rates_category_id, api_key)
print(f"Found {len(all_series_ids)} interest rate series IDs.")
# Optionally save: pd.DataFrame({'series_id': all_series_ids}).to_csv('all_interest_rate_series.csv', index=False)

# Common interest rate series IDs (examples; mix of daily, weekly, monthly)
common_series = [
    'DFF',  # Federal Funds Effective Rate (daily)
    'SOFR',  # Secured Overnight Financing Rate (daily)
    'DGS1',  # 1-Year Treasury Constant Maturity Rate (daily)
    'DGS2',  # 2-Year Treasury
    'DGS5',  # 5-Year Treasury
    'DGS10',  # 10-Year Treasury
    'DGS30',  # 30-Year Treasury
    'MORTGAGE30US',  # 30-Year Fixed Rate Mortgage Average (weekly)
    'AAA',  # Moody's Seasoned Aaa Corporate Bond Yield (monthly)
    'BAA',  # Moody's Seasoned Baa Corporate Bond Yield (monthly)
    'TB3MS'  # 3-Month Treasury Bill Secondary Market Rate (monthly)
]

# Fetch data for common series (e.g., from 2000-01-01 to current)
data_frames = []
for sid in common_series:
    try:
        df = get_series_data(sid, api_key, start_date='2000-01-01')
        data_frames.append(df)
        print(f"Fetched {sid}")
    except Exception as e:
        print(f"Failed to fetch {sid}: {e}")

# Combine into a single DataFrame (handles different frequencies by aligning on dates)
if data_frames:
    all_data = pd.concat(data_frames, axis=1)
    all_data = all_data.ffill()  # Optional: forward-fill missing values for alignment
    # all_data.to_csv('interest_rates_data.csv')
    print(all_data.tail())  # Preview last few rows