import os
import alpaca_trade_api as tradeapi
from datetime import datetime, timedelta
import pandas as pd
from config import ALPACA_API_KEY, ALPACA_API_SECRET, ALPACA_API_BASE_URL_PAPER

# Initialize the API
api = tradeapi.REST(
    ALPACA_API_KEY, ALPACA_API_SECRET, base_url=ALPACA_API_BASE_URL_PAPER
)

# Top 10 S&P 500 companies' tickers as an example (reduced for brevity)
top_10_tickers = ["AAPL"]  # You can uncomment other tickers as per your requirement

# Date range for historical data
end_date = datetime.now()
start_date = end_date - timedelta(days=5 * 365)  # Set to 5 years

# DataFrame to store historical data
historical_data = pd.DataFrame()


# Function to fetch data in chunks
def fetch_data_monthly(api, ticker, start, end):
    month_data = pd.DataFrame()
    current_start = start
    while current_start < end:
        current_end = min(
            current_start + timedelta(days=30), end
        )  # Fetch in one-month intervals
        bars = api.get_bars(
            ticker,
            tradeapi.TimeFrame.Minute,
            start=current_start.strftime("%Y-%m-%d"),
            end=current_end.strftime("%Y-%m-%d"),
            limit=10000,  # Adjust based on your subscription level
        ).df

        if not bars.empty:
            month_data = pd.concat([month_data, bars])
            current_start = current_end + timedelta(days=1)
        else:
            # Log or handle no data returned scenario
            print(
                f"Warning: No data returned for {ticker} from {current_start.strftime('%Y-%m-%d')} to {current_end.strftime('%Y-%m-%d')}"
            )
            current_start = current_end + timedelta(
                days=1
            )  # Continue to next interval even if no data

    return month_data


for ticker in top_10_tickers:
    print(f"Fetching data for {ticker}")
    barset = fetch_data_monthly(api, ticker, start_date, end_date)

    if not barset.empty:
        barset.index = pd.to_datetime(
            barset.index
        )  # Normalize the index to UTC datetime
        barset["ticker"] = ticker  # Label the data by ticker
        historical_data = pd.concat([historical_data, barset])
    else:
        print(f"No historical data available for {ticker}")

# Ensure the index is set to UTC for consistency
if not historical_data.index.tz:
    historical_data.index = historical_data.index.tz_localize("UTC")

# Save data
output_dir = "historical/data"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
file_path = os.path.join(output_dir, "five_year_minute_level_data.csv")
historical_data.to_csv(file_path)

# Final check for missing data
print("Final check for missing data:")
print(historical_data.isnull().sum())
