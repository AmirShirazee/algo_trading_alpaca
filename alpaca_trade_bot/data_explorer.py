import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class DataExplorer:
    def __init__(self, filepath):
        self.df = pd.read_csv(filepath)
        self.df["timestamp"] = pd.to_datetime(
            self.df["timestamp"]
        )  # Ensure datetime is correct
        print(f"Data loaded from {filepath} with shape {self.df.shape}")

    def summary_statistics(self):
        """Print summary statistics of the dataframe."""
        print("Summary Statistics:")
        print(self.df.describe())

    def plot_histograms(self, bins=None, log_scale=False, figsize=(20, 15)):
        """Plot histograms for each numerical feature with optional log scaling."""
        print("Plotting histograms...")
        numeric_cols = self.df.select_dtypes(include=[np.number])
        for column in numeric_cols.columns:
            plt.figure(figsize=figsize)
            if log_scale:
                sns.histplot(
                    numeric_cols[column], bins=bins or "auto", log_scale=True, kde=False
                )
            else:
                sns.histplot(numeric_cols[column], bins=bins or "auto", kde=False)
            plt.title(f"Histogram of {column} (Log scale: {log_scale})")
            plt.xlabel(column)
            plt.ylabel("Frequency")
            plt.show()

    def plot_correlation_matrix(self):
        """Plot correlation matrix of all numerical features."""
        print("Plotting correlation matrix...")
        numeric_cols = self.df.select_dtypes(include=[np.number])
        correlation_matrix = numeric_cols.corr()
        plt.figure(figsize=(10, 8))
        sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap="coolwarm")
        plt.title("Correlation Matrix")
        plt.show()

    def plot_pairwise_relationships(self, columns=None):
        """Plot pairwise relationships for a subset of columns or all columns."""
        if columns is None:
            columns = self.df.select_dtypes(include=[np.number]).columns
        print("Plotting pairwise relationships...")
        sns.pairplot(self.df[columns])
        plt.suptitle("Pairwise Scatter Plots", y=1.02)
        plt.show()

    def plot_time_series(
        self, time_column, value_column, title="Time Series Plot", window=12
    ):
        """Plot a time series graph of a single column with rolling mean."""
        print(f"Plotting time series for {value_column}...")
        plt.figure(figsize=(12, 6))
        plt.plot(
            self.df[time_column], self.df[value_column], label=value_column, alpha=0.5
        )
        plt.plot(
            self.df[time_column],
            self.df[value_column].rolling(window=window).mean(),
            "r-",
            linewidth=2,
            label=f"Rolling Mean (window={window})",
        )
        plt.title(title)
        plt.xlabel("Timestamp")
        plt.ylabel(value_column)
        plt.legend()
        plt.show()

    def plot_boxplots(self, column_list):
        """Plot boxplots for a list of columns."""
        print("Plotting boxplots...")
        for column in column_list:
            plt.figure(figsize=(8, 4))
            sns.boxplot(x=self.df[column])
            plt.title(f"Boxplot of {column}")
            plt.show()

    def missing_values_report(self):
        """Report the number of missing values per column."""
        missing_data = self.df.isnull().sum()
        total_cells = np.prod(self.df.shape)
        total_missing = missing_data.sum()
        print("Missing Values Report:")
        print(missing_data[missing_data > 0])
        print(
            f"Total missing values: {total_missing} out of {total_cells} ({(total_missing / total_cells) * 100:.2f}%)"
        )


if __name__ == "__main__":
    explorer = DataExplorer("../data/cleaned_five_year_minute_level_data.csv")
    explorer.summary_statistics()
    explorer.plot_histograms()
    explorer.plot_correlation_matrix()
    explorer.plot_pairwise_relationships()
    explorer.plot_time_series("timestamp", "close")
    explorer.plot_boxplots(["open", "high", "low", "close", "volume"])
    explorer.missing_values_report()
