import yfinance as yf
import pandas as pd
import json
import hashlib
from pathlib import Path
import time

ASSETS = {
    "equity": ["AAPL", "MSFT", "SPY"],
    "bond": ["TLT"],
    "commodity": ["GLD"],
    "crypto": ["BTC-USD"]
}

OUT = Path("data/frozen")
OUT.mkdir(parents=True, exist_ok=True)

hashes = {}
meta = {}

def download_safe(ticker):
    for attempt in range(3):
        try:
            df = yf.download(
                ticker,
                start="2018-01-01",
                end="2024-01-01",
                auto_adjust=True,
                progress=False,
                threads=False
            )
            if not df.empty:
                return df
        except Exception as e:
            print(f"[WARN] {ticker} attempt {attempt+1} failed: {e}")
        time.sleep(2)
    return pd.DataFrame()

for cls, tickers in ASSETS.items():
    for t in tickers:
        print(f"Downloading {t}...")
        df = download_safe(t)

        if df.empty:
            raise RuntimeError(
                f"FAILED to download {t}. "
                "Yahoo Finance blocked the request. "
                "See fallback instructions."
            )

        path = OUT / f"{t}.csv"
        df.to_csv(path)

        h = hashlib.sha256(path.read_bytes()).hexdigest()
        hashes[t] = h
        meta[t] = {
            "class": cls,
            "rows": len(df),
            "start": str(df.index.min()),
            "end": str(df.index.max())
        }

(Path("data/frozen/hashes.json")).write_text(json.dumps(hashes, indent=2))
(Path("data/frozen/metadata.json")).write_text(json.dumps(meta, indent=2))

print("Data ingestion complete.")


