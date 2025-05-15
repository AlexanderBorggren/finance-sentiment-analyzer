const API_URL =
  "https://func-sentiment-plan.azurewebsites.net/api/fetch_summary";

export const fetchSentimentData = async () => {
  const response = await fetch(API_URL);

  if (!response.ok) {
    let errorMessage = `HTTP error! status: ${response.status} - Failed to fetch ${API_URL}`;
    try {
      const errorBody = await response.text();
      errorMessage += `\nResponse: ${errorBody}`;
    } catch (e) {
    }
    throw new Error(errorMessage);
  }

  try {
    const data = await response.json();
    return data;
  } catch (e) {
    const errorDetail = e instanceof Error ? e.message : String(e);
    throw new Error(`Failed to parse JSON from ${API_URL}: ${errorDetail}`);
  }
};
