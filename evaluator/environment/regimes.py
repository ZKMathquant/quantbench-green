import numpy as np
import pandas as pd

def apply_regime(prices: pd.DataFrame, regime: str, seed: int):
    """
    Applies adversarial market regimes.
    Assumes prices is numeric float DataFrame.
    """
    prices = prices.copy()
    rng = np.random.default_rng(seed)

    if regime == "flash_crash":
        idx = rng.integers(20, len(prices) - 5)
        prices.iloc[idx : idx + 3, :] *= 0.7

    elif regime == "volatility_spike":
        vol = prices.pct_change().std().values
        noise = rng.normal(0, vol * 4, size=(len(prices), len(prices.columns)))
        prices *= (1 + noise)

    elif regime == "correlation_break":
        prices = prices.sample(
            frac=1, axis=1, random_state=seed
        )

    return prices


