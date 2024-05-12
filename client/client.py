import asyncio
import pandas as pd
from typing import Callable
from alpaca_trade_api.stream import Stream
from config import ALPACA_API_KEY, ALPACA_API_SECRET, ALPACA_API_BASE_URL_PAPER

# Shared DataFrame to store data
data_store = pd.DataFrame(columns=["timestamp", "ask_price", "bid_price"])


class AlpacaTrader:
    def __init__(self, strategy, on_trade_callback: Callable, use_paper: bool = True):
        self.strategy = strategy
        self.on_trade_callback = on_trade_callback
        self.stream = Stream(
            key_id=ALPACA_API_KEY,
            secret_key=ALPACA_API_SECRET,
            base_url=(
                ALPACA_API_BASE_URL_PAPER if use_paper else ALPACA_API_BASE_URL_PAPER
            ),
            data_feed="iex",
        )
        self.stream.subscribe_quotes(self.on_quote_update, "AAPL")
        self.exit_event = asyncio.Event()

    @staticmethod
    async def on_quote_update(quote):
        global data_store
        print(f"Quote update: {quote}")
        timestamp = (
            pd.to_datetime(quote.timestamp, unit="ns")
            .tz_convert("UTC")
            .tz_localize(None)
        )
        new_data = pd.DataFrame(
            {
                "timestamp": [timestamp],
                "ask_price": [quote.ask_price],
                "bid_price": [quote.bid_price],
            }
        )

        # Clean or fill empty/NA data before concatenation
        new_data.fillna(
            {
                "timestamp": pd.Timestamp.now(),  # Default current time if missing
                "ask_price": 0,  # Assume zero if missing
                "bid_price": 0,  # Assume zero if missing
            },
            inplace=True,
        )

        # Check for columns that are entirely NA and drop them
        cols_fully_na = new_data.columns[new_data.isna().all()]
        new_data.drop(columns=cols_fully_na, inplace=True)

        # Concatenation with data type checking
        if not new_data.empty:
            data_store = pd.concat([data_store, new_data], ignore_index=True)

    async def start_trading(self):
        trading_task = asyncio.create_task(self.stream._run_forever())
        await self.exit_event.wait()
        trading_task.cancel()

    def stop_trading(self):
        self.exit_event.set()
        self.stream.stop()


async def handle_trade_update(trade_update):
    print("Received trade update:", trade_update)


async def run_trader():
    trader = AlpacaTrader(
        strategy="basic_strategy", on_trade_callback=handle_trade_update
    )
    await trader.start_trading()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_trader())
