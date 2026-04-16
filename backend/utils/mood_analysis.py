"""utils/mood_analysis.py - Mood analysis utilities"""
from collections import Counter
from typing import List


def most_frequent_mood(mood_records: List[dict]) -> str:
    if not mood_records:
        return "neutral"
    counts = Counter(r.get("detected_mood", "neutral") for r in mood_records)
    return counts.most_common(1)[0][0]


def mood_distribution(mood_records: List[dict]) -> dict:
    counts = Counter(r.get("detected_mood", "neutral") for r in mood_records)
    return dict(counts)
