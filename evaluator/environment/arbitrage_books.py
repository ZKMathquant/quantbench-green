import numpy as np

def generate_books(seed=42):
    rng = np.random.default_rng(seed)
    mid = 100

    book_a = {
        "bids": [{"price": mid - 0.01, "size": 100}],
        "asks": [{"price": mid + 0.01, "size": 100}]
    }

    book_b = {
        "bids": [{"price": mid + 0.03, "size": 100}],
        "asks": [{"price": mid + 0.05, "size": 100}]
    }

    true_profit = book_b["bids"][0]["price"] - book_a["asks"][0]["price"]

    return {
        "books": {"A": book_a, "B": book_b},
        "true_profit": true_profit
    }
