import os
import alpaca_trade_api as tradeapi
from datetime import datetime, timedelta
import pandas as pd
from config import ALPACA_API_KEY, ALPACA_API_SECRET, ALPACA_API_BASE_URL_PAPER

# Initialize the API
api = tradeapi.REST(
    ALPACA_API_KEY, ALPACA_API_SECRET, base_url=ALPACA_API_BASE_URL_PAPER
)

# Top 10 S&P 500 companies' tickers as an example
top_10_tickers = [
    "AAPL",
    "MSFT",
    "AMZN",
    "FB",
    "GOOGL",
    "GOOG",
    "BRK.B",
    "JNJ",
    "JPM",
    "V",
]

# Date range for historical data
end_date = datetime.now()
start_date = end_date - timedelta(days=3650)  # 1 year ago

# DataFrame to store historical data
historical_data = pd.DataFrame()

for ticker in top_10_tickers:
    barset = api.get_bars(
        ticker,
        tradeapi.TimeFrame.Day,
        start=start_date.strftime("%Y-%m-%d"),
        end=end_date.strftime("%Y-%m-%d"),
        limit=1000,
    ).df

    print(f"Data for {ticker}: {barset.head()}")  # Debug: Check the initial data

    if not barset.empty:
        barset.index = pd.to_datetime(
            barset.index
        )  # Normalize the index to UTC datetime
        barset["ticker"] = ticker  # Label the data by ticker
        historical_data = pd.concat([historical_data, barset])
    else:
        print(f"No data returned for {ticker}")

# Ensure the index is set to UTC for consistency
if not historical_data.index.tz:
    historical_data.index = historical_data.index.tz_localize("UTC")

# Save data
output_dir = "historical/data"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
file_path = os.path.join(output_dir, "historical_data.csv")
historical_data.to_csv(file_path)

# Final check for missing data
print("Final check for missing data:")
print(historical_data.isnull().sum())
