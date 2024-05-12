import logging
from alpaca_trade_api import Stream
from flask_socketio import SocketIO
from config import ALPACA_API_KEY, ALPACA_API_SECRET, ALPACA_API_BASE_URL_PAPER


class AlpacaAPIManager:
    def __init__(self, socketio: SocketIO, strategy, use_paper=True):
        self.socketio = socketio
        self.strategy = strategy
        self.stream = Stream(
            key_id=ALPACA_API_KEY,
            secret_key=ALPACA_API_SECRET,
            base_url=ALPACA_API_BASE_URL_PAPER,
            data_feed="iex",
        )

    def subscribe_and_stream(self, symbol):
        self.stream.subscribe_quotes(self.on_quote_update, symbol)
        self.stream.run()

    def on_quote_update(self, quote):
        logging.info(f"Received quote update: {quote}")
        data = {
            "timestamp": quote.timestamp,
            "ask_price": quote.ask_price,
            "bid_price": quote.bid_price,
        }
        self.socketio.emit("quote_update", data)

    def start_trading(self):
        pass

    def stop_trading(self):
        if (
            self.stream
            and getattr(self.stream, "_loop", None)
            and self.stream._loop.is_running()
        ):
            self.stream.stop()
        else:
            logging.warning(
                "Attempted to stop trading, but the stream was not running."
            )
