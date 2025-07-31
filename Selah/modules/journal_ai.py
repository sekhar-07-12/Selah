import json
import os
import datetime

DATA_PATH = 'data/user_stats.json'

def load_journal():
    if not os.path.exists(DATA_PATH):
        return []
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def add_journal_entry(text):
    entries = load_journal()
    entry = {"date": str(datetime.date.today()), "entry": text}
    entries.append(entry)
    with open(DATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(entries, f, indent=4)

def get_mood_feedback(entry):
    text = entry.lower()
    if any(word in text for word in ["happy", "excited", "good", "great", "joy"]):
        return "Great to hear! Keep your positive momentum going! 🎉"
    if any(word in text for word in ["sad", "tired", "stressed", "down", "bad"]):
        return "Take a deep breath and remember that tomorrow is a new day. 🌱"
    return "Your journal entry was recorded. Keep reflecting and improving!"
