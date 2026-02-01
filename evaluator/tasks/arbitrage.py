def generate_task(env):
    return {
        "task_type": "arbitrage",
        "order_books": env["books"],
        "instructions": "Detect risk-free arbitrage and expected profit."
    }

def score(response, env):
    true = env["true_profit"]
    claimed = response.get("profit", 0)
    return max(0, 1 - abs(claimed - true) / max(true, 1e-3))
