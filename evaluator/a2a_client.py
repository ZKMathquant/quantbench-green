import requests
import time
from loguru import logger

class A2AClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def execute(self, payload: dict) -> dict:
        start = time.time()
        try:
            r = requests.post(
                f"{self.base_url}/execute",
                json=payload,
                timeout=30
            )
            r.raise_for_status()
            out = r.json()
            out["_latency"] = time.time() - start
            return out
        except Exception as e:
            logger.error(f"A2A failure: {e}")
            return {"error": str(e), "_latency": time.time() - start}
