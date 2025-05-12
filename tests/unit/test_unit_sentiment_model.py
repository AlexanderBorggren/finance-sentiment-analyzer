import pytest
from unittest.mock import patch, MagicMock
from app.analyzer.sentiment_model import analyze_sentiment

@pytest.mark.unit
@patch("app.analyzer.sentiment_model.pipeline")
def test_analyze_sentiment(mock_pipeline):
    mock_model = MagicMock()
    mock_pipeline.return_value = mock_model
    
    mock_model.return_value = [
        {"label": "positive", "score": 0.99},
        {"label": "neutral", "score": 0.5},
        {"label": "negative", "score": 0.8}
    ]
    
    titles = [
        "How inflation affects the global economy",
        "Funniest cat videos",
        "Stock market crashes"
    ]
    
    expected_results = [
        {"title": "How inflation affects the global economy", "sentiment": "bull"},
        {"title": "Funniest cat videos", "sentiment": "neutral"},
        {"title": "Stock market crashes", "sentiment": "bear"}
    ]

    results = analyze_sentiment(titles)

    assert results == expected_results
    mock_pipeline.assert_called_once_with("sentiment-analysis", model="ProsusAI/finbert", tokenizer="ProsusAI/finbert")
    print("Unit test passed successfully.")