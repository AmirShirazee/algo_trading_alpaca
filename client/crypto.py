from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.requests import CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame

# Creating request object
request_params = CryptoBarsRequest(
    symbol_or_symbols=["BTC/USD"],
    timeframe=TimeFrame.Week,
    start="2012-09-01",
    end="2022-09-07",
)
# No keys required for crypto data
client = CryptoHistoricalDataClient()

# Retrieve daily bars for Bitcoin in a DataFrame and printing it
btc_bars = client.get_crypto_bars(request_params)

# converting the data to a DataFrame
btc_bars_df = btc_bars.df
print(btc_bars_df)
