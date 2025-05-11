import pytest
from unittest.mock import patch, MagicMock
from app.fetcher.reddit_client import fetch_titles

@patch("app.fetcher.reddit_client.reddit")
def test_fetch_titles_success(mock_reddit):
    mock_post = MagicMock()
    mock_post.title = "Test Title"
    
    mock_subreddit = MagicMock()
    mock_subreddit.hot.return_value = [mock_post]
    mock_subreddit.top.return_value = [mock_post]
    mock_reddit.subreddit.return_value = mock_subreddit

    titles = fetch_titles("python")
    assert len(titles) == 2
    assert titles == ["Test Title", "Test Title"]
    mock_subreddit.hot.assert_called_once()
    mock_subreddit.top.assert_called_once_with(time_filter="day")