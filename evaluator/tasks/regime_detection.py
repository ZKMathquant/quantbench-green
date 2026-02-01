def generate_task(env):
    # Convert DataFrame to JSON-serializable format
    prices_data = env["prices"].iloc[-100:].copy()
    prices_data.index = prices_data.index.strftime('%Y-%m-%d')  # Convert timestamps to strings
    
    return {
        "task_type": "regime_detection",
        "prices": prices_data.to_dict(),
        "instructions": "Classify the market regime."
    }

def score(pred, true):
    return 1.0 if pred == true else 0.0
