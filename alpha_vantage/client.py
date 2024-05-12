import pandas as pd
import matplotlib.pyplot as plt
import requests

from config import ALPHA_VANTAGE_API_KEY

# Configuration for Alpha Vantage API (assumed to be set)
API_KEY = ALPHA_VANTAGE_API_KEY
BASE_URL = "https://www.alphavantage.co/query"


def fetch_daily_data(symbol):
    """Fetches daily adjusted close prices for a symbol from Alpha Vantage."""
    params = {
        "function": "TIME_SERIES_DAILY_ADJUSTED",
        "symbol": symbol,
        "apikey": API_KEY,
        "outputsize": "full",
        "datatype": "json",
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    # Create a DataFrame and select the 'adjusted close' prices
    df = pd.DataFrame(data["Time Series (Daily)"]).T
    df = df.rename(columns={"5. adjusted close": "adj_close"}).astype(
        {"adj_close": float}
    )
    df.index = pd.to_datetime(df.index)
    return df


def calculate_sma(data, window=50):
    """Calculate Simple Moving Average (SMA)."""
    return data.rolling(window=window).mean()
