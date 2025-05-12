from fetcher.reddit_client import fetch_titles
from analyzer.sentiment_model import analyze_sentiment
from analyzer.summarizer import summarize_sentiments, generate_summary, generate_conclusion
from analyzer.filter_data import filter_data
from azure_cloud.blob_storage import upload_to_blob

def main():
    sources = [
    {"platform": "Reddit", "channel": "finance"},
    {"platform": "Reddit", "channel": "stocks"},
    {"platform": "Reddit", "channel": "economics"}
    ]    
    all_titles = []
    sources_used = []

    for source in sources:
        if source["platform"] == "Reddit":
            subreddit = source["channel"]
            print(f"Fetching from r/{subreddit}...")
            titles = fetch_titles(subreddit)
            all_titles.extend(titles)
            sources_used.append(source)

    print("Filtering relevant titles..")
    filtered_data = filter_data(all_titles)

    print("Starting to analyze sentiment..")
    analyzed_data = analyze_sentiment(filtered_data)

    print("Summerizing the data..")
    summerized_data = summarize_sentiments(analyzed_data)
    generated_conclusion_string = generate_conclusion(summerized_data)
    summary_text = generate_summary(summerized_data, generated_conclusion_string)
    print(summary_text)

    upload_to_blob(summerized_data, summary_text, sources_used)  

if __name__ == "__main__":
    main()

