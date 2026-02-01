import numpy as np

def generate_task(env):
    return {
        "task_type": "execution",
        "price_path": env["prices"].iloc[-50:].mean(axis=1).tolist(),
        "target_volume": 10_000,
        "instructions": "Return a list of slice sizes over time."
    }

def score(response, env):
    slices = response.get("slices", [])
    if not slices or sum(slices) != 10_000:
        return 0.0

    prices = np.array(env["prices"].iloc[-50:].mean(axis=1))
    
    # Ensure slices and prices have same length
    min_len = min(len(slices), len(prices))
    slices = slices[:min_len]
    prices = prices[:min_len]
    
    if len(slices) == 0:
        return 0.0
    
    impact = np.dot(slices, prices) / 10_000

    # lower is better
    return max(0.0, 1.0 - impact / prices.mean())
