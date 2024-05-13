import pandas as pd


def convert_csv_to_hdf5(csv_filepath, hdf5_filepath):
    # Read the CSV file using pandas
    data = pd.read_csv(csv_filepath)

    # Write the data to an HDF5 file
    data.to_hdf(hdf5_filepath, key="data", mode="w", format="table")

    print(f"Data from {csv_filepath} has been written to {hdf5_filepath} successfully.")


# Example usage
csv_path = "../data/five_year_minute_level_data.csv"
hdf5_path = "../data/five_year_minute_level_data.h5"
convert_csv_to_hdf5(csv_path, hdf5_path)
