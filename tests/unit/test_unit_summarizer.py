import pytest
from app.analyzer.summarizer import summarize_sentiments, generate_conclusion, generate_summary
from datetime import datetime

@pytest.mark.unit
def test_summarize_sentiments():
    sentiments = [
        {"sentiment": "bull"},
        {"sentiment": "bull"},
        {"sentiment": "neutral"},
        {"sentiment": "bear"},
        {"sentiment": "bear"},
        {"sentiment": "bear"}
    ]

    expected_summary = {
        "total_analyzed": 6,
        "bull": 2,
        "neutral": 1,
        "bear": 3,
        "most_common": "bear"
    }

    result = summarize_sentiments(sentiments)
    assert result == expected_summary
    print("Unit test for summarize_sentiments ran successfully.")


@pytest.mark.unit
@pytest.mark.parametrize("summary_data, expected_start", [
    (
        {"bull": 30, "neutral": 30, "bear": 30, "total_analyzed": 90},
        "Sentiment remains broadly neutral with no strong leanings."
    ),
    (
        {"bull": 40, "neutral": 42, "bear": 18, "total_analyzed": 100},
        "Sentiment is overall neutral, but bullish sentiment is significantly more active"
    ),
        (
        {"bull": 18, "neutral": 42, "bear": 40, "total_analyzed": 100},
        "Sentiment is overall neutral, but bearish sentiment is significantly more active"
    ),
    (
        {"bull": 80, "neutral": 10, "bear": 10, "total_analyzed": 100},
        "Bullish sentiment is dominant, with little challenge from other signals."
    ),
    (
        {"bull": 40, "neutral": 35, "bear": 25, "total_analyzed": 100},
        "Bullish sentiment has the edge"
    ),
    (
        {"bull": 10, "neutral": 10, "bear": 80, "total_analyzed": 100},
        "Bearish sentiment is dominant, with little challenge from other signals."
    ),
    (
        {"bull": 33, "neutral": 17, "bear": 50, "total_analyzed": 100},
        "Bearish sentiment leads, while bullish sentiment is clearly gaining ground"
    ),
])
def test_generate_conclusion_scenarios(summary_data, expected_start):
    result = generate_conclusion(summary_data)
    assert result.startswith(expected_start)

@pytest.mark.unit
def test_generate_summary_output_format():
    summary_data = {
        "bull": 20,
        "neutral": 50,
        "bear": 30,
        "total_analyzed": 100
    }
    conclusion = "Neutral sentiment is dominant with mild bullish presence."

    expected_summary = (
        f"\nDate Today: {datetime.today().strftime('%Y-%m-%d')}\n"
        f"Total Analyzed Posts: 100\n"
        f"Bullish: 20 (20.0%)\n"
        f"Neutral: 50 (50.0%)\n"
        f"Bearish: 30 (30.0%)\n\n"
        f"{conclusion}\n"
    )

    result = generate_summary(summary_data, conclusion)
    assert result == expected_summary
