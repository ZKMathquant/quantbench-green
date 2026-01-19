import numpy as np
import pandas as pd

def generate_task(env):
    returns = env["returns"]
    
    return {
        "task_type": "portfolio",
        "assets": list(returns.columns),
        "returns": returns.values.tolist()
    }

def score(response, env):
    returns = env["returns"]
    
    weights = response
    if not weights:
        return -1.0
    
    # Convert response to weights dict if it's not already
    if isinstance(weights, dict) and "weights" in weights:
        weights = weights["weights"]
    
    # Align weights with assets
    w = np.array([weights.get(a, 0.0) for a in returns.columns])
    if not np.isclose(w.sum(), 1.0):
        return -1.0
    
    portfolio_returns = returns.values @ w
    
    mean = portfolio_returns.mean()
    std = portfolio_returns.std()
    
    if std == 0:
        return -1.0
    
    sharpe = mean / std
    return float(sharpe)


