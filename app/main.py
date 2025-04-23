from fetcher.reddit_client import fetch_titles
from analyzer.sentiment_model import analyze_sentiment
from analyzer.summarizer import summarize_sentiments
from analyzer.summarizer import generate_natural_summary

def main():
    subreddits = ["finance", "stocks", "economics"]
    all_titles = []

    for subreddit in subreddits:
        print(f"Fetching from r/{subreddit}...")
        titles = fetch_titles(subreddit)
        all_titles.extend(titles)

    print("Starting to analyze sentiment..")
    analyzed_data = analyze_sentiment(all_titles)
    #print(analyzed_data)
    print("Summerizing the data..")
    summerized_data = summarize_sentiments(analyzed_data)
    #print(summerized_data)
    #print(generate_natural_summary(summerized_data))
    

if __name__ == "__main__":
    main()

