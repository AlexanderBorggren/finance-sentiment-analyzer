from collections import Counter
from datetime import datetime
from typing import List, Dict

def summarize_sentiments(sentiments: List[Dict]) -> Dict:
    counts = Counter(item["sentiment"] for item in sentiments)
    total = sum(counts.values())

    return {
        "total_analyzed": total,
        "bull": counts.get("bull", 0),
        "neutral": counts.get("neutral", 0),
        "bear": counts.get("bear", 0),
        "most_common": counts.most_common(1)[0][0] if total else "N/A"
    }

def generate_conclusion(summary_data) -> str:
    SECOND_THIRD_THRESHOLD = 0.15
    TOP_SECOND_THRESHOLD = 0.2
    NEUTRAL_VARIANCE_THRESHOLD = 0.05
    
    bull = summary_data["bull"]
    neutral = summary_data["neutral"]
    bear = summary_data["bear"]
    total = summary_data["total_analyzed"]

    sentiment_raw = {"Bullish": bull, "Neutral": neutral, "Bearish": bear}
    total = sum(sentiment_raw.values())

    if total == 0:
        return "No sentiment data available."

    sentiment_norm = {k: v / total for k, v in sentiment_raw.items()}
    
    values = list(sentiment_norm.values())
    if max(values) - min(values) <= NEUTRAL_VARIANCE_THRESHOLD:
        return "Sentiment remains broadly neutral with no strong leanings."

    sorted_sentiments = sorted(sentiment_norm.items(), key=lambda x: x[1], reverse=True)
    top, second, third = sorted_sentiments

    top_label, top_val = top
    second_label, second_val = second
    third_label, third_val = third

    second_third_gap = second_val - third_val
    top_second_gap = top_val - second_val

    if top_label == "Neutral":
        if second_third_gap >= SECOND_THIRD_THRESHOLD:
            return (
                    f"Sentiment is overall neutral, but {second_label.lower()} sentiment is significantly more active "
                    f"than {third_label.lower()}, hinting at an emerging {second_label.lower()} bias."
                )
        else:
            return "Sentiment remains broadly neutral with no strong leanings."
    else:
        if top_second_gap >= TOP_SECOND_THRESHOLD:
            return f"{top_label} sentiment is dominant, with little challenge from other signals."
        elif second_third_gap >= SECOND_THIRD_THRESHOLD:
            return (
                    f"{top_label} sentiment leads, while {second_label.lower()} sentiment is clearly gaining ground "
                    f"against {third_label.lower()}, suggesting potential shifts in sentiment dynamics."
                )
        else:
            return f"{top_label} sentiment has the edge, but overall market sentiment remains mixed."

        
def generate_summary(summary_data: Dict, conclusion: str) -> str:
    bull = summary_data["bull"]
    neutral = summary_data["neutral"]
    bear = summary_data["bear"]
    total = summary_data["total_analyzed"]
    current_date = datetime.today().strftime("%Y-%m-%d")

    def percent(value: int) -> float:
        return round((value / total) * 100, 2) if total else 0

    summary = (
        f"\nDate Today: {current_date}\n"
        f"Total Analyzed Posts: {total}\n"
        f"Bullish: {bull} ({percent(bull)}%)\n"
        f"Neutral: {neutral} ({percent(neutral)}%)\n"
        f"Bearish: {bear} ({percent(bear)}%)\n\n"
        f"...:::{conclusion}:::...\n"
    )
    return summary
