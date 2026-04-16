"""utils/productivity_score.py - Standalone productivity score helper"""
from typing import List


def compute_score(tasks: List[dict]) -> float:
    total     = len(tasks)
    completed = [t for t in tasks if t.get("status") == "completed"]
    if total == 0:
        return 0.0
    base    = (len(completed) / total) * 100
    bonuses = sum(10 for t in completed if t.get("difficulty") == "Hard") + \
              sum(5  for t in completed if t.get("completed_mood") == "stressed")
    return min(round(base + bonuses, 1), 150)
