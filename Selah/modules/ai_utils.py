import re
from collections import Counter

def simple_summarize(text, max_len=100):
    if len(text) <= max_len:
        return text
    return text[:max_len].rsplit(' ', 1)[0] + "..."

def extract_keywords(text, top_k=5):
    words = re.findall(r'\w+', text.lower())
    stop_words = set(['the', 'is', 'and', 'to', 'a', 'of', 'in', 'it', 'that'])
    filtered_words = [w for w in words if w not in stop_words]
    freq = Counter(filtered_words)
    keywords = [word for word, count in freq.most_common(top_k)]
    return keywords
