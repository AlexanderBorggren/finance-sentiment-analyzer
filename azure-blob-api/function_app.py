import azure.functions as func
import logging
from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential
import os

app = func.FunctionApp()

@app.function_name(name="fetch_summary")
@app.route(route="fetch_summary", auth_level=func.AuthLevel.ANONYMOUS)
def fetch_summary(req: func.HttpRequest) -> func.HttpResponse:
    try:
        account_url = f"https://{os.getenv('AZURE_STORAGE_ACCOUNT_NAME')}.blob.core.windows.net"
        container_name = "summaries"
        credential = DefaultAzureCredential()
        blob_service_client = BlobServiceClient(account_url=account_url, credential=credential)
        container_client = blob_service_client.get_container_client(container_name)
        blobs = list(container_client.list_blobs())
        if not blobs:
            return func.HttpResponse("No files found.", status_code=404)
        latest_blob = sorted(blobs, key=lambda b: b.last_modified, reverse=True)[0]
        blob_client = container_client.get_blob_client(latest_blob.name)
        content = blob_client.download_blob().readall()
        return func.HttpResponse(content, mimetype="application/json")
    except Exception as e:
        logging.error(f"Error: {e}")
        return func.HttpResponse(f"Internal Server Error: {str(e)}", status_code=500)