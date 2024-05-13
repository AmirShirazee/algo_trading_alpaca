import pandas as pd
import matplotlib.pyplot as plt


class MeanReversionStrategy:
    def __init__(self, filepath, window=100, threshold=2, moving_average_type="SMA"):
        self.filepath = filepath
        self.window = window
        self.threshold = threshold
        self.moving_average_type = moving_average_type
        self.data = None
        self.load_data()

    def load_data(self):
        self.data = pd.read_csv(
            self.filepath, parse_dates=["timestamp"], index_col="timestamp"
        )
        print(f"Data loaded successfully for {self.moving_average_type}.")

    def calculate_indicators(self):
        if self.moving_average_type == "EMA":
            self.data["Moving Average"] = (
                self.data["close"].ewm(span=self.window, adjust=False).mean()
            )
        elif self.moving_average_type == "DEMA":
            ema = self.data["close"].ewm(span=self.window, adjust=False).mean()
            self.data["Moving Average"] = (
                2 * ema - ema.ewm(span=self.window, adjust=False).mean()
            )
        elif self.moving_average_type == "TEMA":
            ema = self.data["close"].ewm(span=self.window, adjust=False).mean()
            ema_ema = ema.ewm(span=self.window, adjust=False).mean()
            self.data["Moving Average"] = (
                3 * ema
                - 3 * ema_ema
                + ema_ema.ewm(span=self.window, adjust=False).mean()
            )
        else:  # Default to SMA
            self.data["Moving Average"] = (
                self.data["close"].rolling(window=self.window).mean()
            )

        self.data["Standard Deviation"] = (
            self.data["close"].rolling(window=self.window).std()
        )
        self.data["Upper Bound"] = (
            self.data["Moving Average"]
            + self.threshold * self.data["Standard Deviation"]
        )
        self.data["Lower Bound"] = (
            self.data["Moving Average"]
            - self.threshold * self.data["Standard Deviation"]
        )
        print(f"Indicators calculated based on {self.moving_average_type}")

    def generate_signals(self):
        self.data["Buy Signal"] = self.data["close"] < self.data["Lower Bound"]
        self.data["Sell Signal"] = self.data["close"] > self.data["Upper Bound"]
        print(f"Trading signals generated for {self.moving_average_type}.")

    def plot_data(self):
        plt.figure(figsize=(14, 7))
        plt.plot(self.data["close"], label="Close Price", color="blue", alpha=0.5)
        plt.plot(
            self.data["Moving Average"], label="Moving Average", color="red", alpha=0.75
        )
        plt.fill_between(
            self.data.index,
            self.data["Lower Bound"],
            self.data["Upper Bound"],
            color="gray",
            alpha=0.3,
        )
        plt.legend()
        plt.title(f"Mean Reversion Strategy with {self.moving_average_type}")
        plt.xlabel("Timestamp")
        plt.ylabel("Price")
        plt.show()

    def backtest_strategy(self):
        """Backtests the trading strategy and calculates annualized returns."""
        self.data["Position"] = 0
        self.data.loc[self.data["Buy Signal"], "Position"] = 1
        self.data.loc[self.data["Sell Signal"], "Position"] = -1
        self.data["Portfolio Returns"] = (
            self.data["Position"].shift(1) * self.data["close"].pct_change()
        )
        self.data["Cumulative Returns"] = (
            1 + self.data["Portfolio Returns"]
        ).cumprod() - 1

        # Calculate the number of days the data spans
        days_span = (self.data.index.max() - self.data.index.min()).days
        years_span = days_span / 365.25  # accounting for leap years

        # Calculate the annualized return
        cumulative_return = self.data["Cumulative Returns"].iloc[-1]
        annualized_return = (1 + cumulative_return) ** (1 / years_span) - 1

        print(
            f"Backtest completed for {self.moving_average_type}: Cumulative return is {cumulative_return:.2f}%, Annualized return is {annualized_return:.2f}%"
        )

    def display_results(self):
        print(
            self.data[
                [
                    "close",
                    "Moving Average",
                    "Buy Signal",
                    "Sell Signal",
                    "Cumulative Returns",
                ]
            ].tail()
        )


if __name__ == "__main__":
    moving_average_types = ["SMA", "EMA", "DEMA", "TEMA"]
    for ma_type in moving_average_types:
        strategy = MeanReversionStrategy(
            "../data/cleaned_five_year_minute_level_data.csv",
            moving_average_type=ma_type,
        )
        strategy.calculate_indicators()
        strategy.generate_signals()
        # strategy.plot_data()
        strategy.backtest_strategy()
        # strategy.display_results()
