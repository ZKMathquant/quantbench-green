from evaluator.environment.loader import load_assets

def test_deterministic_loading():
    e1 = load_assets("volatility_spike", seed=42)
    e2 = load_assets("volatility_spike", seed=42)

    p1, p2 = e1["prices"], e2["prices"]

    assert p1.shape == p2.shape
    assert (p1.values == p2.values).all()
