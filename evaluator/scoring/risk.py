import numpy as np

def sharpe_ratio(returns: np.ndarray):
    return returns.mean() / (returns.std() + 1e-9)

def cvar(returns: np.ndarray, alpha=0.05):
    cutoff = int(len(returns) * alpha)
    return returns[np.argsort(returns)[:cutoff]].mean()

def risk_adjusted_score(returns: np.ndarray):
    s = sharpe_ratio(returns)
    c = cvar(returns)
    return max(0.0, s + c)
