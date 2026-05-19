from transformers import pipeline
from collections import Counter

_classifier = None

_LABEL_MAP = {
    'positive': 'positive', 'pos': 'positive',
    'negative': 'negative', 'neg': 'negative',
    'neutral':  'neutral',  'neu': 'neutral',
}


def get_classifier():
    global _classifier
    if _classifier is None:
        _classifier = pipeline(
            "text-classification",
            model="cardiffnlp/twitter-xlm-roberta-base-sentiment",
            top_k=1,
        )
    return _classifier


def classify_sentiment(text: str) -> str:
    if not text or not text.strip():
        return 'neutral'
    try:
        result = get_classifier()(text[:512])
        raw = result[0][0]['label'] if isinstance(result[0], list) else result[0]['label']
        return _LABEL_MAP.get(raw.lower(), 'neutral')
    except Exception:
        return 'neutral'


def analyze_comments(comments: list) -> dict:
    processed = [c for c in comments if c and c.strip()]
    sentiments = [classify_sentiment(c) for c in processed]
    counts = Counter(sentiments)
    total = len(processed) or 1
    return {
        'positive':     counts.get('positive', 0),
        'negative':     counts.get('negative', 0),
        'neutral':      counts.get('neutral',  0),
        'total':        len(processed),
        'positive_pct': round(counts.get('positive', 0) / total * 100, 1),
        'negative_pct': round(counts.get('negative', 0) / total * 100, 1),
        'neutral_pct':  round(counts.get('neutral',  0) / total * 100, 1),
        'per_comment':  list(zip(processed, sentiments)),
    }
