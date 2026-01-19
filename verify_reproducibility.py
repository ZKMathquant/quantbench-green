
"""
Reproducibility verification script for QuantBench.
Runs evaluation multiple times and verifies identical results.
"""
import json
import subprocess
import sys
from pathlib import Path

def run_evaluation():
    """Run single evaluation and return results."""
    result = subprocess.run([
        sys.executable, "-m", "evaluator.agent"
    ], capture_output=True, text=True)
    
    if result.returncode != 0:
        raise RuntimeError(f"Evaluation failed: {result.stderr}")
    
    # Read results
    with open("output/results.json") as f:
        return json.load(f)

def main():
    print("QuantBench Reproducibility Verification")
    print("=" * 50)
    
    results = []
    
    for run_id in range(1, 4):  # 3 runs
        print(f" Run {run_id}/3...")
        
        # Clean previous output
        Path("output").mkdir(exist_ok=True)
        if Path("output/results.json").exists():
            Path("output/results.json").unlink()
        
        # Run evaluation
        result = run_evaluation()
        results.append(result)
        
        # Show scores
        scores = {r["task"]: r["score"] for r in result["results"]}
        print(f"   Scores: {scores}")
    
    # Verify reproducibility
    print("\n Reproducibility Check:")
    
    baseline = results[0]["results"]
    all_identical = True
    
    for i, result in enumerate(results[1:], 2):
        for j, task_result in enumerate(result["results"]):
            baseline_score = baseline[j]["score"]
            current_score = task_result["score"]
            
            if abs(baseline_score - current_score) > 1e-10:
                print(f"❌ Run {i}: {task_result['task']} differs: {baseline_score} vs {current_score}")
                all_identical = False
    
    if all_identical:
        print("All runs produced identical results!")
        print(" Reproducibility requirement satisfied")
        return 0
    else:
        print("NOPE, Results differ across runs")
        print("NOPE,Reproducibility requirement NOT satisfied")
        return 1

if __name__ == "__main__":
    sys.exit(main())
