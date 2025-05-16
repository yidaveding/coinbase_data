import requests

# Get product list
# response = requests.get('https://api.exchange.coinbase.com/products')
# products = response.json()
# print(f"Available products: {products}")

# # Get BTC-USD ticker data
# ticker = requests.get('https://api.exchange.coinbase.com/products/BTC-USD/ticker')
# ticker_data = ticker.json()
# print(f"Current BTC price: ${ticker_data['price']}")

# Get historical candle data (1-hour intervals)
# candles = requests.get('https://api.exchange.coinbase.com/products/BTC-USD/candles?granularity=3600')
candles = requests.get('https://api.exchange.coinbase.com/products/BTC-USD/candles?granularity=86400&start=2024-05-01T00:00:00&end=2024-05-31T23:59:59')
candle_data = candles.json()
print(f"Recent candles: {len(candle_data)}")

# 60 = 1 minute candles
# 300 = 5 minute candles
# 900 = 15 minute candles
# 3600 = 1 hour candles
# 21600 = 6 hour candles
# 86400 = 1 day candles