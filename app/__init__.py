import logging
import azure.functions as func
import json

from fetcher.reddit_client import fetch_titles
from analyzer.sentiment_model import analyze_sentiment
from analyzer.summarizer import summarize_sentiments, generate_summary
from analyzer.filter_data import filter_data

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("HTTP function triggered to generate sentiment summary.")

    try:
        subreddits = req.params.get('subreddits')
        if subreddits:
            subreddits = subreddits.split(',')
        else:
            subreddits = ["finance", "stocks", "economics"]

        all_titles = []
        for subreddit in subreddits:
            logging.info(f"Fetching from r/{subreddit}...")
            titles = fetch_titles(subreddit)
            all_titles.extend(titles)
            
        logging.info("Filtering relevant titles..")
        filtered_data = filter_data(all_titles)

        logging.info("Starting to analyze sentiment..")
        analyzed_data = analyze_sentiment(filtered_data)

        logging.info("Summarizing the data..")
        summarized_data = summarize_sentiments(analyzed_data)
        summary_text = generate_summary(summarized_data)

        return func.HttpResponse(summary_text, status_code=200)
    
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return func.HttpResponse(f"Internal Server Error: {str(e)}", status_code=500)