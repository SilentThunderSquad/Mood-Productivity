"""
recommendation_engine.py - Mood-based task recommendation logic
"""
from datetime import datetime, timezone
from typing import List, Optional

# How many days out a deadline is considered "urgent"
URGENT_DAYS = 2

MOOD_DIFFICULTY_MAP = {
    "motivated": ["Hard", "Medium"],
    "neutral":   ["Medium", "Easy"],
    "tired":     ["Easy"],
    "stressed":  ["Easy", "Medium"],
}

MOOD_TIPS = {
    "motivated": [
        "Great energy! Tackle your hardest tasks first.",
        "You're in flow state — push through the big challenges.",
        "Consider setting a 90-minute deep work block.",
    ],
    "neutral": [
        "Steady pace today. Focus on medium-priority tasks.",
        "Use the Pomodoro technique: 25 min work, 5 min break.",
        "Good time to clear your task backlog.",
    ],
    "tired": [
        "Low energy detected. Prioritise rest and easy wins.",
        "Try a 5-minute walk before starting work.",
        "Batch small tasks together to build momentum.",
    ],
    "stressed": [
        "Feeling stressed? Start with something achievable.",
        "Break large tasks into smaller, manageable steps.",
        "Consider a brief mindfulness exercise before working.",
    ],
}

import random


def recommend_tasks(mood: str, tasks: List[dict]) -> dict:
    """
    Given a mood and a list of pending tasks, return:
      - recommended: list of tasks best suited to the mood
      - urgent: tasks with imminent deadlines (override mood)
      - tip: a motivational/productivity tip
    """
    preferred_difficulties = MOOD_DIFFICULTY_MAP.get(mood, ["Medium", "Easy"])
    now = datetime.now(timezone.utc)

    recommended = []
    urgent      = []

    for task in tasks:
        if task.get("status") == "completed":
            continue

        # Check urgency
        deadline_str = task.get("deadline")
        is_urgent = False
        if deadline_str:
            try:
                deadline = datetime.fromisoformat(deadline_str.replace("Z", "+00:00"))
                if deadline.tzinfo is None:
                    deadline = deadline.replace(tzinfo=timezone.utc)
                days_left = (deadline - now).days
                if days_left <= URGENT_DAYS:
                    is_urgent = True
            except (ValueError, TypeError):
                pass

        if is_urgent:
            urgent.append(task)
        elif task.get("difficulty") in preferred_difficulties:
            recommended.append(task)

    # Sort recommended by difficulty preference order
    diff_rank = {d: i for i, d in enumerate(preferred_difficulties)}
    recommended.sort(key=lambda t: diff_rank.get(t.get("difficulty", "Medium"), 99))

    tip = random.choice(MOOD_TIPS.get(mood, MOOD_TIPS["neutral"]))

    return {
        "mood":        mood,
        "recommended": recommended[:5],
        "urgent":      urgent[:3],
        "tip":         tip,
    }


def get_focus_duration(mood: str) -> int:
    """Return recommended focus session duration in minutes."""
    durations = {
        "motivated": 90,
        "neutral":   45,
        "tired":     20,
        "stressed":  25,
    }
    return durations.get(mood, 45)
