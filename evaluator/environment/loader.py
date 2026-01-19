from pathlib import Path
import pandas as pd
import numpy as np

from evaluator.environment.regimes import apply_regime

PROJECT_ROOT = Path(__file__).resolve().parents[2]
FROZEN_DIR = PROJECT_ROOT / "data" / "frozen"

def _load_single_asset(path: Path) -> pd.Series:
    # Read CSV with proper header handling - skip first 2 rows, use first column as date index
    df = pd.read_csv(path, skiprows=2, index_col=0, parse_dates=True)
    
    # Use the first data column (Close price)
    prices = pd.to_numeric(df.iloc[:, 0], errors="coerce")
    prices = prices.dropna()
    
    return prices.astype(float)

def load_assets(regime: str, seed: int = 0) -> dict:
    if not FROZEN_DIR.exists():
        raise RuntimeError(f"Frozen data directory not found: {FROZEN_DIR}")

    series = {}
    for csv_path in sorted(FROZEN_DIR.glob("*.csv")):
        series[csv_path.stem] = _load_single_asset(csv_path)

    if not series:
        raise RuntimeError("No CSV files found in data/frozen")

    prices = pd.concat(series.values(), axis=1, keys=series.keys())
    prices = prices.sort_index()
    prices = prices.dropna(how="any")
    prices = prices.astype(float)

    np.random.seed(seed)
    prices = apply_regime(prices, regime=regime, seed=seed)
    
    # Calculate returns
    returns = prices.pct_change().dropna()
    
    return {
        "prices": prices,
        "returns": returns,
        "true_regime": regime
    }





