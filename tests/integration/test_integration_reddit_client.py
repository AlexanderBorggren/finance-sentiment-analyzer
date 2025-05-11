import pytest
from app.fetcher.reddit_client import fetch_titles

@pytest.mark.integration
def test_fetch_titles_real_api():
    titles = fetch_titles("python", limit=5)
    assert isinstance(titles, list)
    assert all(isinstance(title, str) for title in titles)
    assert len(titles) > 0