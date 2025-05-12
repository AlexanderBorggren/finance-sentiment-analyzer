import pytest
from unittest.mock import patch, MagicMock
from app.analyzer.filter_data import filter_data  

@pytest.mark.unit
@patch("app.analyzer.filter_data.pipeline")
def test_filter_data(mock_pipeline):

    mock_model = MagicMock()
    mock_pipeline.return_value = mock_model
    
    mock_model.return_value = [
        {"labels": ["relevant to economics or finance"], "scores": [0.9]},
        {"labels": ["irrelevant to economics or finance"], "scores": [0.1]},
        {"labels": ["relevant to economics or finance"], "scores": [0.8]},
    ]
    
    titles = [
        "How inflation affects the global economy",
        "Funniest cat videos",
        "Stock market trends in 2025"
    ]
    
    expected_filtered_titles = [
        "How inflation affects the global economy",
        "Stock market trends in 2025"
    ]

    filtered_titles = filter_data(titles)

    assert filtered_titles == expected_filtered_titles
    mock_pipeline.assert_called_once_with("zero-shot-classification", model="knowledgator/comprehend_it-base")
    print("Unit test passed successfully.")