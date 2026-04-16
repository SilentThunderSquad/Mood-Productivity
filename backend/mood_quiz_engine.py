"""
mood_quiz_engine.py
Analyses answers to daily check-in questions and derives:
  - a productivity mood  (motivated / neutral / tired / stressed)
  - an energy level      (1-10)
  - a focus level        (1-10)
  - personalised insights + tips
"""
from typing import List, Dict

# ── Question bank ─────────────────────────────────────────────────────────────
QUESTIONS = [
    {
        "id": "q1",
        "text": "How would you describe your energy level right now?",
        "emoji": "⚡",
        "options": [
            {"label": "Pumped & ready to go",    "value": "high",    "score": {"energy": 4, "focus": 2}},
            {"label": "Pretty good, feeling okay","value": "medium",  "score": {"energy": 2, "focus": 2}},
            {"label": "A bit low, need a push",  "value": "low",     "score": {"energy": 0, "focus": 1}},
            {"label": "Completely drained",       "value": "drained", "score": {"energy": -2,"focus": 0}},
        ],
    },
    {
        "id": "q2",
        "text": "How did you sleep last night?",
        "emoji": "😴",
        "options": [
            {"label": "Great — felt fully rested",      "value": "great",    "score": {"energy": 3, "stress": -1}},
            {"label": "Okay — decent enough",           "value": "okay",     "score": {"energy": 1, "stress":  0}},
            {"label": "Not great — woke up a few times","value": "poor",     "score": {"energy":-1, "stress":  1}},
            {"label": "Terrible — barely slept",        "value": "terrible", "score": {"energy":-3, "stress":  2}},
        ],
    },
    {
        "id": "q3",
        "text": "How is your stress level today?",
        "emoji": "🧠",
        "options": [
            {"label": "Calm and relaxed",           "value": "calm",     "score": {"stress": -2, "focus": 3}},
            {"label": "Mild stress, manageable",    "value": "mild",     "score": {"stress":  0, "focus": 2}},
            {"label": "Quite stressed",             "value": "high",     "score": {"stress":  2, "focus": 0}},
            {"label": "Overwhelmed and anxious",    "value": "overwhelm","score": {"stress":  4, "focus":-1}},
        ],
    },
    {
        "id": "q4",
        "text": "How is your mood overall today?",
        "emoji": "😊",
        "options": [
            {"label": "Happy and positive",     "value": "happy",   "score": {"mood_boost":  3, "energy": 1}},
            {"label": "Neutral, just existing", "value": "neutral", "score": {"mood_boost":  0, "energy": 0}},
            {"label": "A bit down or sad",      "value": "sad",     "score": {"mood_boost": -2, "energy":-1}},
            {"label": "Irritable or frustrated","value": "angry",   "score": {"mood_boost": -1, "stress": 2}},
        ],
    },
    {
        "id": "q5",
        "text": "How well can you concentrate right now?",
        "emoji": "🎯",
        "options": [
            {"label": "Laser focused — bring it on",  "value": "laser",    "score": {"focus": 4}},
            {"label": "Reasonably focused",           "value": "good",     "score": {"focus": 2}},
            {"label": "Easily distracted",            "value": "distract", "score": {"focus": 0}},
            {"label": "Can't focus at all",           "value": "none",     "score": {"focus":-2}},
        ],
    },
    {
        "id": "q6",
        "text": "How motivated are you to tackle tasks today?",
        "emoji": "🚀",
        "options": [
            {"label": "Very motivated — let's crush it", "value": "high",   "score": {"mood_boost": 3, "energy": 2}},
            {"label": "Somewhat motivated",              "value": "medium", "score": {"mood_boost": 1, "energy": 0}},
            {"label": "Barely motivated",                "value": "low",    "score": {"mood_boost":-1, "energy":-1}},
            {"label": "Zero motivation today",           "value": "none",   "score": {"mood_boost":-3, "energy":-2}},
        ],
    },
    {
        "id": "q7",
        "text": "What best describes your day so far?",
        "emoji": "📅",
        "options": [
            {"label": "Productive and on track",       "value": "productive","score": {"mood_boost": 2, "focus": 1}},
            {"label": "Slow but steady",               "value": "slow",      "score": {"mood_boost": 0, "focus": 0}},
            {"label": "Full of interruptions",         "value": "interrupt", "score": {"focus":-1, "stress": 1}},
            {"label": "Chaotic and stressful",         "value": "chaotic",   "score": {"stress": 3, "focus":-2}},
        ],
    },
]


# ── Mood derivation logic ──────────────────────────────────────────────────────
def derive_mood(answers: List[Dict]) -> Dict:
    """
    Given a list of {question_id, value, scores} answers,
    compute cumulative scores and derive mood + insights.
    """
    total = {"energy": 5, "stress": 2, "focus": 5, "mood_boost": 2}  # baseline

    answer_map = {a["question_id"]: a for a in answers}

    for ans in answers:
        for key, val in ans.get("scores", {}).items():
            total[key] = total.get(key, 0) + val

    # Normalise to 0–10
    energy     = max(0, min(10, total["energy"] + 2))
    stress     = max(0, min(10, total["stress"]))
    focus      = max(0, min(10, total["focus"] + 2))
    mood_boost = total["mood_boost"]

    # Determine mood
    if stress >= 6:
        mood = "stressed"
    elif energy <= 3 or focus <= 2:
        mood = "tired"
    elif energy >= 7 and focus >= 6 and mood_boost >= 2:
        mood = "motivated"
    else:
        mood = "neutral"

    # Generate insights based on answers
    insights = _build_insights(mood, energy, stress, focus, answer_map)
    tip      = _build_tip(mood, energy, stress, focus)

    mood_meta = {
        "motivated": {"icon": "🚀", "color": "#22c55e", "label": "Motivated",
                      "description": "Your energy and focus are high — perfect for tackling hard challenges!"},
        "neutral":   {"icon": "😐", "color": "#3b82f6", "label": "Neutral",
                      "description": "You're in a steady state. Good for consistent, medium-effort work."},
        "tired":     {"icon": "😴", "color": "#f59e0b", "label": "Tired",
                      "description": "Energy is low today. Focus on easy wins and take regular breaks."},
        "stressed":  {"icon": "😰", "color": "#ef4444", "label": "Stressed",
                      "description": "High stress detected. Start small, breathe, and build momentum."},
    }

    meta = mood_meta[mood]

    return {
        "mood":        mood,
        "icon":        meta["icon"],
        "color":       meta["color"],
        "label":       meta["label"],
        "description": meta["description"],
        "scores": {
            "energy":     energy,
            "stress":     stress,
            "focus":      focus,
            "mood_boost": mood_boost,
        },
        "insights": insights,
        "tip":      tip,
        "success":  True,
    }


def _build_insights(mood, energy, stress, focus, answer_map):
    insights = []
    if energy <= 3:
        insights.append("⚡ Your energy is low — consider a short walk or some water before diving in.")
    if stress >= 6:
        insights.append("🧘 High stress levels detected. Try 2 minutes of deep breathing first.")
    if focus >= 8:
        insights.append("🎯 Your focus is excellent right now — use this window for deep work.")
    if energy >= 8 and focus >= 7:
        insights.append("🚀 You're in an optimal productive state — tackle your hardest task now!")
    if not insights:
        if mood == "neutral":
            insights.append("📋 A steady day ahead — work through your task list at a comfortable pace.")
        elif mood == "motivated":
            insights.append("💪 Great mindset! Push through challenging tasks while this energy lasts.")
    return insights


def _build_tip(mood, energy, stress, focus):
    tips = {
        "motivated": "Block 90 minutes for your most important task — you have the energy for it!",
        "neutral":   "Use the Pomodoro method: 25 min focused work, 5 min break. Repeat 4x.",
        "tired":     "Start with your easiest task to build momentum, then take a 10-min break.",
        "stressed":  "Write down your top 3 tasks and tackle only one at a time. Small steps win.",
    }
    return tips.get(mood, tips["neutral"])


def get_questions():
    """Return all questions (without internal scoring data exposed to frontend)."""
    return [
        {
            "id":      q["id"],
            "text":    q["text"],
            "emoji":   q["emoji"],
            "options": [{"label": o["label"], "value": o["value"]} for o in q["options"]],
        }
        for q in QUESTIONS
    ]


def get_scores_for_answer(question_id: str, value: str) -> Dict:
    """Look up the score dict for a given question + answer value."""
    for q in QUESTIONS:
        if q["id"] == question_id:
            for o in q["options"]:
                if o["value"] == value:
                    return o.get("score", {})
    return {}
