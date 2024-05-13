import numpy as np
import pandas as pd


def simulate_sorting_times(n_samples):
    np.random.seed(42)  # Voor reproduceerbaarheid

    # Kenmerken: grootte van de array, en een feature die de "geordendheid" simuleert
    data_features = np.random.randint(1, 1000, (n_samples, 2))

    # Gesimuleerde tijden: deze functies simuleren de uitvoertijd gebaseerd op array grootte en geordendheid
    merge_sort_times = np.log(data_features[:, 0]) * data_features[:, 1] / 500
    quick_sort_times = np.log(data_features[:, 0]) * data_features[:, 1] / 400
    heap_sort_times = np.log(data_features[:, 0]) * data_features[:, 1] / 450

    # Dataframe samenstellen
    df = pd.DataFrame(data_features, columns=["Array Size", "Orderliness"])
    df["Merge Sort Time"] = merge_sort_times
    df["Quicksort Time"] = quick_sort_times
    df["Heapsort Time"] = heap_sort_times

    return df


# Aantal samples die je wilt genereren
n_samples = 1000
df = simulate_sorting_times(n_samples)

# Opslaan naar CSV
df.to_csv("sort_algorithm_simulation_data.csv", index=False)
print("Dataset generated and saved to sort_algorithm_simulation_data.csv")
