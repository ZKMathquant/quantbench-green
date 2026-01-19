def aggregate(task_scores: list[tuple[str, float]]) -> dict:
    total = sum(score for _, score in task_scores)
    return {
        "per_task": {k: round(v, 4) for k, v in task_scores},
        "overall": round(total / len(task_scores), 4)
    }

