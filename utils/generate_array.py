import random


def generate_large_array(size, min_val=0, max_val=1000000):
    return [random.randint(min_val, max_val) for _ in range(size)]
