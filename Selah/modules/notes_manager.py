import json
import os

DATA_PATH = 'data/notes_data.json'

def load_notes():
    if not os.path.exists(DATA_PATH):
        return []
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_notes(notes):
    with open(DATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(notes, f, indent=4)

def add_note(title, content):
    notes = load_notes()
    notes.append({"title": title, "content": content})
    save_notes(notes)

def edit_note(index, title=None, content=None):
    notes = load_notes()
    if 0 <= index < len(notes):
        if title:
            notes[index]['title'] = title
        if content:
            notes[index]['content'] = content
        save_notes(notes)

def delete_note(index):
    notes = load_notes()
    if 0 <= index < len(notes):
        notes.pop(index)
        save_notes(notes)
