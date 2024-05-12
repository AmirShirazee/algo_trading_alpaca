import os
from dotenv import load_dotenv

load_dotenv()

# Load configuration from environment variables
ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
ALPACA_API_SECRET = os.getenv("ALPACA_API_SECRET")

# URL
ALPACA_BASE_URL = os.getenv("ALPACA_BASE_URL", "https://paper-api.alpaca.markets")
ALPACA_API_BASE_URL = "https://api.alpaca.markets"
ALPACA_API_BASE_URL_PAPER = "https://paper-api.alpaca.markets"
ALPACA_STREAM_BASE_URL = "https://data.alpaca.markets"
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
