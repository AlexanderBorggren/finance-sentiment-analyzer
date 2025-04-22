import os
import praw
from dotenv import load_dotenv

load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent="sentiment-analyzer"
)

def fetch_titles(subreddit_name: str, limit: int = 100):
    
    titles = []
    try:
        subreddit = reddit.subreddit(subreddit_name)
        for post in subreddit.hot(limit=limit):
            titles.append(post.title)
        for post in subreddit.top(time_filter="day"):
            titles.append(post.title)

    except Exception as e:
        print(f"Error: {e}")

    return titles

# Test
if __name__ == "__main__":
    titles = fetch_titles("finance", limit=10)
    for i, title in enumerate(titles, start=1):
        print(f"{i}. {title}")

fetch_titles("stocks")
fetch_titles("finance")
fetch_titles("economics")
