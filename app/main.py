from fetcher.reddit_client import fetch_titles
from analyzer.sentiment_model import analyze_sentiment

def main():
    subreddits = ["finance", "stocks", "economics"]
    all_titles = []

    for subreddit in subreddits:
        print(f"Fetching from r/{subreddit}...")
        titles = fetch_titles(subreddit)
        all_titles.extend(titles)
    
    print("\nAll collected titles:")
    for i, title in enumerate(all_titles, start=1):
        print(f"{i}. {title}")

if __name__ == "__main__":
    main()

