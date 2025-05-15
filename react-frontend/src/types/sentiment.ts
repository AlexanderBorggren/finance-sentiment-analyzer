export interface Source {
  platform: string;
  channel: string;
}

export interface SentimentDataDetails {
  total_analyzed: number;
  bull: number;
  neutral: number;
  bear: number;
  most_common: string;
  sources: { [key: string]: Source };
}

export interface ApiSentimentResponse {
  summary: string;
  data: SentimentDataDetails;
}

export interface ParsedSummary {
  dateToday?: string;
  totalAnalyzedPosts?: string;
  bullish?: string;
  neutral?: string;
  bearish?: string;
  overallSentiment?: string;
}
