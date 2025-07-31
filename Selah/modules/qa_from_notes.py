import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def load_notes(notes_path='data/notes_data.json'):
    try:
        with open(notes_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def answer_query(query, notes):
    if not notes:
        return "No notes available to answer questions."
    corpus = [note['content'] for note in notes]
    corpus.append(query)

    vectorizer = TfidfVectorizer(stop_words='english').fit_transform(corpus)
    cosine_similarities = cosine_similarity(vectorizer[-1], vectorizer[:-1]).flatten()
    best_idx = cosine_similarities.argmax()
    best_score = cosine_similarities[best_idx]
    if best_score < 0.1:
        return "Sorry, no relevant answer found in notes."
    return notes[best_idx]['content']
