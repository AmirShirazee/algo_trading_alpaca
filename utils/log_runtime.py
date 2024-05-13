import time
from utils import generate_large_array


def log_runtime(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        # Get the name of the algorithm if provided, or set a default message
        algo_name = (
            kwargs.get("sort_algo", func).__name__
            if "sort_algo" in kwargs
            else func.__name__
        )
        print(
            f"{func.__name__} with {algo_name} completed in: {end_time - start_time:.6f} seconds"
        )
        return result

    return wrapper


@log_runtime
def run_sorting_algorithm(sort_algo):
    array = generate_large_array(1000)
    sorted_arr = sort_algo(array)
    print(f"First 10 elements: {sorted_arr[:10]}")
    print(f"Last 10 elements: {sorted_arr[-10:]}")
