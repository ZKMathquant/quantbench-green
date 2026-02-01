import pandas as pd
import numpy as np
from evaluator.environment.regimes import apply_regime

def test_flash_crash():
    prices = pd.DataFrame({"A": np.linspace(100, 101, 100)})
    out = apply_regime(prices, "flash_crash", seed=42)
    assert out.min().values[0] < 80
