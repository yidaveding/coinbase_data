# # Get BTC-USD ticker data
# ticker = requests.get('https://api.exchange.coinbase.com/products/BTC-USD/ticker')
# Get historical candle data (1-hour intervals)
# candles = requests.get('https://api.exchange.coinbase.com/products/BTC-USD/candles?granularity=3600')
# candle granularity
# 60 = 1 minute candles
# 300 = 5 minute candles
# 900 = 15 minute candles
# 3600 = 1 hour candles
# 21600 = 6 hour candles
# 86400 = 1 day candles

import requests, os
import pandas as pd

# Get product list
response = requests.get('https://api.exchange.coinbase.com/products')
products = response.json()
df_products = pd.json_normalize(products)
df_products.to_csv('output\coinbase_products.csv', index=False)

df_active_products = df_products[
        (df_products['trading_disabled'] == False) \
        & (df_products['fx_stablecoin'] == True)
    ]

# Get historical candle data (1-day intervals)
granularity = 86400 # 1 day candles

# Get a list of start of month since Jan 2022 to last month based on today's date
start_date = pd.to_datetime('2022-01-01')
end_date = pd.to_datetime(pd.Timestamp.now().replace(day=1) - pd.DateOffset(seconds=1))
date_range = pd.date_range(start=start_date, end=end_date, freq='MS')
date_ranges = []

# Check existing files in the output folder
output_folder = 'output'
existing_files = os.listdir(output_folder)

for start in date_range:
    end = start + pd.DateOffset(months=1) - pd.DateOffset(seconds=1)
    start_str = start.strftime('%Y-%m-%dT%H:%M:%S')
    end_str = end.strftime('%Y-%m-%dT%H:%M:%S')
    # Check if the file for this date range already exists
    file_exists = any(
        f"_{start.strftime('%Y-%m-%d')}_{end.strftime('%Y-%m-%d')}.csv" in filename
        for filename in existing_files
    )
    if not file_exists:
        date_ranges.append((start_str, end_str))

# for each active product in df_active_products, get the candle data
for index, row in df_active_products.iterrows():
    product_id = row['id']
    print(f"Getting candle data for {product_id}...")
    for start, end in date_ranges:
        # Get the candle data
        candles = requests.get(f'https://api.exchange.coinbase.com/products/{product_id}/candles?granularity={granularity}&start={start}&end={end}')
        candle_data = candles.json()
        # Save the data to a CSV file
        df_candle_data = pd.DataFrame(candle_data, columns=['time', 'low', 'high', 'open', 'close', 'volume'])
        df_candle_data['time'] = pd.to_datetime(df_candle_data['time'], unit='s')
        df_candle_data.to_csv(f'output\coinbase_{product_id}_{start[:10]}_{end[:10]}.csv', index=False)

