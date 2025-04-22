from transformers import pipeline

classifier = pipeline("zero-shot-classification",model="MoritzLaurer/mDeBERTa-v3-base-mnli-xnli")

def analyze_sentiment(titles: list[str]) -> list[dict]:

    candidate_labels = ["bull", "neutral", "bear"]
    output = classifier(titles, candidate_labels, multi_label=False)

    results = []
    for result in output:
        results.append({
            "title": result["sequence"],
            "sentiment": result["labels"][0]
        })

    return results

if __name__ == "__main__":
    test_titles = [
        "Stock market is booming!",
        "Major crash expected next week.",
        "Nothing much happening in the market today."
    ]
    sentiments = analyze_sentiment(test_titles)
    print(sentiments)