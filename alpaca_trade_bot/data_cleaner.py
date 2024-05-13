import pandas as pd
import numpy as np


class DataCleaner:
    def __init__(self, filepath):
        self.filepath = filepath
        self.df = None
        self.load_data()

    def load_data(self):
        """Load data from CSV file."""
        self.df = pd.read_csv(self.filepath)
        print("Data loaded from file:", self.filepath)
        print("Initial data shape:", self.df.shape)

    def handle_missing_data(self):
        """Handle missing data by forward filling and then filling with median."""
        print("Handling missing data...")
        initial_missing = self.df.isnull().sum().sum()
        self.df.ffill(inplace=True)  # Updated based on deprecation warning
        self.df.fillna(
            self.df.select_dtypes(include=[np.number]).median(), inplace=True
        )
        final_missing = self.df.isnull().sum().sum()
        print(
            f"Missing values before cleaning: {initial_missing}, after cleaning: {final_missing}"
        )

    def remove_outliers(self, iqr_factor=2.5):
        """Remove outliers based on the IQR method for numeric columns only, with adjustable sensitivity."""
        print("Removing outliers with IQR factor:", iqr_factor)
        numeric_cols = self.df.select_dtypes(include=[np.number])
        initial_shape = self.df.shape
        Q1 = numeric_cols.quantile(0.25)
        Q3 = numeric_cols.quantile(0.75)
        IQR = Q3 - Q1
        filter = (numeric_cols >= (Q1 - iqr_factor * IQR)) & (
            numeric_cols <= (Q3 + iqr_factor * IQR)
        )
        self.df = self.df[filter.all(axis=1)]
        final_shape = self.df.shape
        print(
            f"Data shape before removing outliers: {initial_shape}, after removing outliers: {final_shape}"
        )

    def correct_errors(self):
        """Correct any obvious errors in the data."""
        print("Correcting errors in data...")
        numeric_cols = ["close", "high", "low", "open", "volume", "vwap"]
        for col in numeric_cols:
            if col in self.df.columns:
                initial_negative_values = (self.df[col] < 0).sum()
                self.df[col] = self.df[col].apply(lambda x: np.nan if x < 0 else x)
                final_negative_values = (self.df[col] < 0).sum()
                print(
                    f"Negative values in '{col}' before correction: {initial_negative_values}, after correction: {final_negative_values}"
                )

        # Re-handle missing data post-correction
        self.handle_missing_data()

    def clean_data(self):
        """Run all cleaning steps."""
        print("Starting data cleaning process...")
        self.handle_missing_data()
        self.remove_outliers(iqr_factor=3.6)
        self.correct_errors()
        print("Data cleaning process completed.")

    def save_clean_data(self, output_filepath):
        """Save the cleaned DataFrame to a CSV file."""
        self.df.to_csv(output_filepath, index=False)
        print("Cleaned data saved to:", output_filepath)

    def get_clean_data(self):
        """Return the cleaned DataFrame."""
        return self.df


if __name__ == "__main__":
    cleaner = DataCleaner("../data/five_year_minute_level_data.csv")
    cleaner.clean_data()
    clean_df = cleaner.get_clean_data()
    print(clean_df.head())

    # Specify the path to save the cleaned data
    output_filepath = "../data/cleaned_five_year_minute_level_data.csv"
    cleaner.save_clean_data(output_filepath)
