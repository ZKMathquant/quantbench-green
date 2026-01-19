import json
from pathlib import Path
from datetime import datetime
import hashlib

def write_results(agent_id: str, task_scores: list):
    # Generate run hash for tracking
    scores_str = json.dumps(task_scores, sort_keys=True)
    run_hash = hashlib.sha256(scores_str.encode()).hexdigest()[:8]
    
    out = {
        "participants": {"agent": agent_id},
        "results": [
            {"task": t, "score": s} for t, s in task_scores
        ],
        "metadata": {
            "timestamp": datetime.utcnow().isoformat(),
            "run_hash": run_hash,
            "reproducibility_id": f"{agent_id}-{run_hash}"
        }
    }

    Path("output").mkdir(exist_ok=True)
    
    # Write main results
    with open("output/results.json", "w") as f:
        json.dump(out, f, indent=2)
    
    # Append to activity log for reproducibility tracking
    log_entry = {
        "timestamp": out["metadata"]["timestamp"],
        "run_hash": run_hash,
        "scores": {t: s for t, s in task_scores}
    }
    
    activity_log = Path("output/activity_log.json")
    if activity_log.exists():
        with open(activity_log) as f:
            logs = json.load(f)
    else:
        logs = []
    
    logs.append(log_entry)
    
    with open(activity_log, "w") as f:
        json.dump(logs, indent=2, fp=f)
    
    print(f"📊 Evaluation complete. Run hash: {run_hash}")
    return out
