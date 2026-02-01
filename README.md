# QuantBench

QuantBench is a **green agent benchmark** for evaluating finance agents under:

- multi-asset portfolios
- real market data (Yahoo Finance frozen snapshots)
- adversarial regimes (flash crash, vol spike, correlation breaks)
- risk-aware scoring (Sharpe + CVaR)

## Why it matters

This benchmark **cannot be solved by heuristics**.
Agents must reason, adapt, and survive stress.

Our project structure:
```
quantbench-green
├── Dockerfile
├── README.md
├── baseline_purple
│   ├── Dockerfile
│   ├── __init__.py
│   ├── agent.py
│   └── requirements.txt
├── data
│   ├── __init__.py
│   ├── frozen
│   │   ├── AAPL.csv
│   │   ├── BTC-USD.csv
│   │   ├── GLD.csv
│   │   ├── MSFT.csv
│   │   ├── SPY.csv
│   │   ├── TLT.csv
│   │   ├── hashes.json
│   │   └── metadata.json
│   └── ingest_yahoo.py
├── evaluator
│   ├── __init__.py
│   ├── a2a_client.py
│   ├── agent.py
│   ├── environment
│   │   ├── __init__.py
│   │   ├── arbitrage_books.py
│   │   ├── loader.py
│   │   └── regimes.py
│   ├── output.py
│   ├── scoring
│   │   ├── aggregate.py
│   │   └── risk.py
│   ├── tasks
│   │   ├── __init__.py
│   │   ├── arbitrage.py
│   │   ├── execution.py
│   │   ├── portfolio.py
│   │   └── regime_detection.py
│   ├── tests
│   │   ├── test_determinism.py
│   │   └── test_regimes.py
│   └── visualization
│       ├── __init__.py
│       └── failure_modes.py
├── leaderboard
│   ├── README.md
│   ├── scenario.toml
│   └── workflow.yml
├── pyproject.toml
├── requirements.txt
├── scenario.toml
└── verify_reproducibility.py
```


## Quick Start

```bash
python data/ingest_yahoo.py
docker build -t qb-purple baseline_purple
docker run -p 9009:9009 qb-purple
docker build -t qb-green .
docker run --network host qb-green


Step 1: Environment Setup
# Create virtual environment
```
python3 -m venv venv
source venv/bin/activate 
```
(Linux environment expected)

# Install dependencies
```
pip install -r requirements.txt
```
Verifies: All required packages are installed for deterministic evaluation

Step 2: Data Integrity Check
# Verify frozen data exists and is valid
ls data/frozen/
cat data/frozen/hashes.json

Verifies: Historical market data is present and immutable (frozen snapshots)

Step 3: Test Deterministic Loading
```
pytest evaluator/tests/test_determinism.py -v
```
Expected Output: PASSED

Verifies: Same seed produces identical numeric DataFrames (core requirement)

Step 4: Test Regime Application
```
pytest evaluator/tests/test_regimes.py -v
```
Expected Output: PASSED
Verifies: Synthetic market regimes are applied deterministically

Step 5: Run All Tests
```
pytest -v
```

Expected Output: All tests PASSED
Verifies: Complete system passes all determinism and correctness checks

Step 6: Start Baseline Agent (Terminal 1)
```
cd baseline_purple
docker build -t qb-purple .
docker run -p 9009:9009 qb-purple
```

Expected Output: Running on http://0.0.0.0:9009
Verifies: Purple agent serves on port 9009 and handles all task types

Step 7: Run Evaluation (Terminal 2 )
# Different Terminal,go to the working dir and repeat the venv commands,no need to install requirements,however feel free to do it anyway,to be sure
```
python -m evaluator.agent
```

Expected Output:  Evaluation complete. Run hash: 5335c045
Verifies:

Loads frozen data deterministically

Applies flash_crash regime with seed=42

Executes all 4 tasks (portfolio, regime_detection, arbitrage, execution)

Generates scores and writes results.json

Step 8: Check Results
```
cat output/results.json
```
Expected Output:

{
  "participants": {"agent": "baseline-agent"},
  "results": [
    {"task": "portfolio", "score": 0.049508012333796474},
    {"task": "regime_detection", "score": 1.0},
    {"task": "arbitrage", "score": 0.999999999999801},
    {"task": "execution", "score": 0.0}
  ],
  "metadata": {
    "timestamp": "2026-01-19T08:41:59.012029",
    "run_hash": "5335c045",
    "reproducibility_id": "baseline-agent-5335c045"
  }
}


Verifies: JSON contains scores for all tasks with proper schema

Step 9: Explicit Reproducibility Verification
python verify_reproducibility.py

Expected Output:

 QuantBench Reproducibility Verification
==================================================
 Run 1/3...
   Scores: {'portfolio': 0.049508012333796474, 'regime_detection': 1.0, 'arbitrage': 0.999999999999801, 'execution': 0.0}
Run 2/3...
   Scores: {'portfolio': 0.049508012333796474, 'regime_detection': 1.0, 'arbitrage': 0.999999999999801, 'execution': 0.0}
Run 3/3...
   Scores: {'portfolio': 0.049508012333796474, 'regime_detection': 1.0, 'arbitrage': 0.999999999999801, 'execution': 0.0}

Reproducibility Check:
All runs produced identical results!
Reproducibility requirement satisfied

Verifies: CRITICAL - Perfect reproducibility across multiple runs (AgentBeats requirement)

Step 10: Check Activity Log
```
cat output/activity_log.json
```

Expected Output: Multiple runs logged with identical scores and different timestamps
Verifies: Multiple runs logged with identical scores (AgentBeats evidence)

Step 11: Docker End-to-End Test
```
docker build -t qb-green .
docker run --network host qb-green
```


Expected Output: Same scores as local runs
Verifies: Cross-environment reproducibility (local vs Docker)

Step 12: Docker-to-Docker Consistency
```
docker run --rm --network host qb-green > docker_run1.log 2>&1
docker run --rm --network host qb-green > docker_run2.log 2>&1
diff docker_run1.log docker_run2.log
```

Expected Output: No differences (empty diff)
Verifies: Container-to-container reproducibility

What We Achieved

Results - System Working Perfectly
Current Scores:

Portfolio: 0.0495 (positive Sharpe ratio - good)

Regime Detection: 1.0 (perfect - correctly identifies flash_crash)

Arbitrage: 0.999999999999801 (near perfect - correctly calculates profit)

Execution: 0.0 (deterministic but needs optimization)

- Perfect Reproducibility Achieved
- Same run hash: 5335c045 across all runs
- Identical scores in every single run
- Zero diff between Docker runs = perfect reproducibility
- only 0 execution is something we are getting too often,might look into that.

AgentBeats Phase 1 Requirements: FULLY SATISFIED

- Reproducibility Verification
- QuantBench guarantees deterministic results:

# Verify reproducibility (required for submissions)
```
python verify_reproducibility.py
```

# Expected output:
# All runs produced identical results!
# Reproducibility requirement satisfied


Each run generates an entry in output/activity_log.json:

[
  {
    "timestamp": "2026-01-19T08:41:59.012029",
    "run_hash": "5335c045",
    "scores": {"portfolio": 0.049508012333796474, "regime_detection": 1.0, "arbitrage": 0.999999999999801, "execution": 0.0}
  }
]

This demonstrates the same Purple Agent evaluated multiple times with consistent scores.

Final Goal Achievement
Deterministic Quantitative Trading Evaluation Framework - COMPLETE

Frozen Data - Immutable market snapshots loaded consistently

Deterministic Loading - Same seed = identical DataFrames

Synthetic Regimes - Flash crash applied deterministically
Task Evaluation - All 4 tasks executed and scored

Perfect Reproducibility - Identical results across multiple runs

AgentBeats Ready - Activity log shows consistent evaluations

Cross-Platform - Local and Docker produce same outputs

Status: Complete quantitative trading benchmark ready for AgentBeats Phase 1 submission.

AgentBeats Submission instructions:
- Repo is submission-ready:
- Fork the leaderboard repo on AgentBeats
- Update leaderboard/scenario.toml with agent ID
- Push to trigger CI evaluation
- Results will appear as artifacts

