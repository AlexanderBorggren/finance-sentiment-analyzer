from transformers import pipeline

finbert = pipeline("sentiment-analysis", model="ProsusAI/finbert", tokenizer="ProsusAI/finbert")

def analyze_sentiment(titles: list[str]) -> list[dict]:
    
    output = finbert(titles)
    print(output)

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