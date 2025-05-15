# Financial Sentiment Analyzer

A full-stack application that collects Reddit post titles from finance-related subreddits, filters and analyzes their sentiment (bullish, neutral, bearish) with AI/LLM, and presents summarized statistics and insights through a modern web dashboard.

## Tech Stack

- **Backend**: Python 3.12, PRAW (Reddit API), Hugging Face Transformers, Azure SDK
- **Cloud Services**: Azure Blob Storage, Azure Functions, API Management
- **Frontend**: React, JavaScript, TypeScript
- **Testing**: Pytest
- **AI/LLM models**:
  - FinBERT (https://huggingface.co/ProsusAI/finbert)
  - comprehend_it-base (https://huggingface.co/knowledgator/comprehend_it-base)

## Project Structure

```
finance-sentiment-analyzer/
├── app/                  # Python backend: data collection and analysis
├── azure-blob-api/       # Azure Function for serving API
├── frontend/             # React frontend dashboard
├── tests/                # Unit and integration tests
├── .env                  # Environment variables (not committed)
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.12
- Node.js (v16 or higher) and npm
- Azure CLI (for deployment)
- Git

### Installation

#### 1. Clone the Repository

```bash
git clone https://github.com/your-username/finance-sentiment-analyzer.git
cd finance-sentiment-analyzer
```

#### 2. Backend Setup

Navigate to the app directory and create a virtual environment:

```bash
cd app
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the app directory with the following content:

```
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
AZURE_STORAGE_CONNECTION_STRING=your_azure_storage_connection_string
PYTHONPATH=.
```

#### 3. Frontend Setup

Navigate to the frontend directory:

```bash
cd ../react-frontend
```

Install the frontend dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

## Running the Application

### Backend Processing

To run the data collection and sentiment analysis:

```bash
cd ../app
python main.py
```

This script will fetch Reddit posts, filter and analyze them using AI/LLM, generate summaries, and upload the results to Azure Blob Storage.

### Azure Function API

To serve the latest summary via an API endpoint:

1. Navigate to the azure-blob-api directory:
   ```bash
   cd ../azure-blob-api
   ```
2. Install Azure Functions Core Tools if not already installed.
3. Start the Azure Function locally:
   ```bash
   func start
   ```

### Frontend Web App

The frontend fetches the sentiment summary via the deployed Azure Function API. To test the full stack locally, ensure your Azure Function is running locally or remotely and update the fetch URL in `./react-frontend/src/services/apiService.js` if needed:

```ts
const res = await fetch("https://<your-function-app>.azurewebsites.net/api/fetch_summary");
```

## Testing

Run the unit and integration tests using pytest command in terminal:

```bash
pytest
```

## Deployment

### Deploying Azure Function

Ensure you are logged in to Azure CLI and have created a Function App:

```bash
az login
az functionapp create --resource-group your-resource-group --consumption-plan-location your-location --runtime python --functions-version 4 --name your-function-app-name --storage-account your-storage-account
```

Deploy the Azure Function:

```bash
cd ../azure-blob-api
func azure functionapp publish your-function-app-name
```

## Acknowledgments

- Creative Tim for frontend React template
- Knowledgator, Microsoft & ProsusAI for AI models