"""
analytics_engine.py - Mood analytics and productivity insights
"""
from collections import Counter
from datetime import datetime, timezone, timedelta
from typing import List, Optional


def calculate_productivity_score(tasks: List[dict]) -> dict:
    """
    productivity_score = (completed / total) * 100
    Bonuses:
      +10 for each completed Hard task
      +5  for each task completed while mood was stressed
    """
    total     = len(tasks)
    completed = [t for t in tasks if t.get("status") == "completed"]
    n_comp    = len(completed)

    if total == 0:
        return {"score": 0, "total": 0, "completed": 0, "bonuses": 0}

    base    = (n_comp / total) * 100
    bonuses = 0

    for t in completed:
        if t.get("difficulty") == "Hard":
            bonuses += 10
        if t.get("completed_mood") == "stressed":
            bonuses += 5

    score = min(round(base + bonuses, 1), 150)  # cap at 150
    return {
        "score":     score,
        "base":      round(base, 1),
        "bonuses":   bonuses,
        "total":     total,
        "completed": n_comp,
        "pending":   total - n_comp,
    }


def analyze_moods(mood_records: List[dict]) -> dict:
    """
    Analyse mood history to produce insights.
    """
    if not mood_records:
        return {"message": "No mood data yet. Detect your mood to get started!"}

    moods = [r.get("detected_mood", "neutral") for r in mood_records]
    mood_counts = Counter(moods)
    most_common = mood_counts.most_common(1)[0]

    stress_count    = mood_counts.get("stressed", 0)
    stressed_pct    = round((stress_count / len(moods)) * 100, 1)
    motivated_count = mood_counts.get("motivated", 0)
    motivated_pct   = round((motivated_count / len(moods)) * 100, 1)

    # Trend: last 7 days
    now = datetime.now(timezone.utc)
    week_ago = now - timedelta(days=7)
    recent = []
    for r in mood_records:
        try:
            ts = r.get("timestamp")
            if isinstance(ts, str):
                ts = datetime.fromisoformat(ts.replace("Z", "+00:00"))
            if ts and ts.tzinfo is None:
                ts = ts.replace(tzinfo=timezone.utc)
            if ts and ts >= week_ago:
                recent.append(r.get("detected_mood", "neutral"))
        except Exception:
            pass

    recent_counts = Counter(recent)

    # Build daily mood trend (last 7 days)
    daily_trend = {}
    for i in range(7):
        day = (now - timedelta(days=i)).strftime("%Y-%m-%d")
        daily_trend[day] = {"motivated": 0, "neutral": 0, "tired": 0, "stressed": 0}

    for r in mood_records:
        try:
            ts = r.get("timestamp")
            if isinstance(ts, str):
                ts = datetime.fromisoformat(ts.replace("Z", "+00:00"))
            if ts and ts.tzinfo is None:
                ts = ts.replace(tzinfo=timezone.utc)
            day_key = ts.strftime("%Y-%m-%d")
            if day_key in daily_trend:
                m = r.get("detected_mood", "neutral")
                if m in daily_trend[day_key]:
                    daily_trend[day_key][m] += 1
        except Exception:
            pass

    # Generate insight message
    insights = []
    if motivated_pct > 50:
        insights.append(f"You're motivated {motivated_pct}% of the time — excellent!")
    if stressed_pct > 30:
        insights.append(f"Stress detected {stressed_pct}% of the time. Consider work-life balance.")
    if most_common[0] == "motivated":
        insights.append("You are most productive when your mood is motivated.")
    elif most_common[0] == "stressed":
        insights.append("High stress levels detected. Try breaking tasks into smaller steps.")

    if not insights:
        insights.append(f"Your most frequent mood is {most_common[0]}.")

    return {
        "total_detections": len(moods),
        "mood_distribution": dict(mood_counts),
        "most_frequent_mood": most_common[0],
        "stress_percentage": stressed_pct,
        "motivated_percentage": motivated_pct,
        "recent_week_moods": dict(recent_counts),
        "daily_trend": daily_trend,
        "insights": insights,
    }


def generate_weekly_report(tasks: List[dict], mood_records: List[dict]) -> dict:
    """Generate a weekly productivity summary."""
    now = datetime.now(timezone.utc)
    week_ago = now - timedelta(days=7)

    # Filter tasks from last 7 days
    weekly_tasks = []
    for t in tasks:
        try:
            created = t.get("created_at")
            if isinstance(created, str):
                created = datetime.fromisoformat(created.replace("Z", "+00:00"))
            if created and created.tzinfo is None:
                created = created.replace(tzinfo=timezone.utc)
            if created and created >= week_ago:
                weekly_tasks.append(t)
        except Exception:
            weekly_tasks.append(t)

    score_data = calculate_productivity_score(weekly_tasks)

    # Mood correlation with task completion
    mood_completion: dict = {}
    for t in weekly_tasks:
        if t.get("status") == "completed":
            mood = t.get("completed_mood", "unknown")
            mood_completion[mood] = mood_completion.get(mood, 0) + 1

    most_productive_mood = max(mood_completion, key=mood_completion.get) if mood_completion else "N/A"

    mood_analytics = analyze_moods(mood_records)

    return {
        "period":             "Last 7 Days",
        "total_tasks":        score_data["total"],
        "completed_tasks":    score_data["completed"],
        "productivity_score": score_data["score"],
        "most_productive_mood": most_productive_mood,
        "least_productive_mood": mood_analytics.get("most_frequent_mood", "N/A"),
        "stress_percentage":  mood_analytics.get("stress_percentage", 0),
        "insights":           mood_analytics.get("insights", []),
        "mood_distribution":  mood_analytics.get("mood_distribution", {}),
    }
