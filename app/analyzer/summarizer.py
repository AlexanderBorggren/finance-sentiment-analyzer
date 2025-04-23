from collections import Counter
from datetime import datetime
from transformers import pipeline

text_model = pipeline("text2text-generation", model="google/flan-t5-large")

def summarize_sentiments(sentiments: list[dict]) -> dict:
    counts = Counter([item["sentiment"] for item in sentiments])
    total = sum(counts.values())

    summary_data = {
        "total_analyzed": total,
        "bull": counts.get("bull", 0),
        "neutral": counts.get("neutral", 0),
        "bear": counts.get("bear", 0),
        "most_common": counts.most_common(1)[0][0] if total else "N/A"
    }

    return summary_data

def generate_natural_summary(summary_data: dict) -> str:
    bull = summary_data["bull"]
    neutral = summary_data["neutral"]
    bear = summary_data["bear"]
    total = summary_data["total_analyzed"]
    current_date = datetime.today().strftime("%Y-%m-%d")

    def percent(part):
        return round((part / total) * 100, 2) if total else 0

    prompt = (
        f"Date: {current_date}\n"
        f"Total analyzed posts: {total}\n"
        f"Bullish: {bull} ({percent(bull)}%)\n"
        f"Neutral: {neutral} ({percent(neutral)}%)\n"
        f"Bearish: {bear} ({percent(bear)}%)\n\n"
        "Write a professional and concise market sentiment review like a financial news anchor, based on the data presented above."
    )

    result = text_model(prompt, max_length=300, do_sample=False)
    return result[0]['generated_text']

