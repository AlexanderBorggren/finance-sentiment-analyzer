import os
import json
import pytest
from azure.storage.blob import BlobServiceClient
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def current_date_filename():
    return datetime.today().strftime("%Y-%m-%d")

@pytest.mark.integration
def test_upload_to_blob():
    connect_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    assert connect_str is not None, "Error: AZURE_STORAGE_CONNECTION_STRING is not applied from env"

    container_name = "summaries"
    test_data = {"test": "integration", "status": "ok"}
    filename = current_date_filename() + "_test_summary.json"

    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=filename)

    json_data = json.dumps(test_data, indent=2)
    blob_client.upload_blob(json_data, overwrite=True)

    exists = blob_client.exists()
    assert exists, "Error: Blob not uploaded properly."

    print("Integration-test: Upload to Azure Blob success") 