from transformers import pipeline

def analyze_sentiment(titles: list[str]) -> list[dict]:

    fin_sentiment_analyser = pipeline("sentiment-analysis", model="ProsusAI/finbert", tokenizer="ProsusAI/finbert")
    
    output = fin_sentiment_analyser(titles)

    sentiment_map = {
        "positive": "bull",
        "neutral": "neutral",
        "negative": "bear"
    }

    results = []
    for title, result in zip(titles, output):
        sentiment = sentiment_map[result["label"].lower()]
        results.append({
            "title": title,
            "sentiment": sentiment
        })

    return results