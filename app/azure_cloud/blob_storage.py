import json
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import AzureError
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def current_date_filename():
    return datetime.today().strftime("%Y-%m-%d")

def upload_to_blob(data: dict, summary_text: str, filetype: str = ".json"):
    try:
        connect_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        if not connect_str:
            raise ValueError("AZURE_STORAGE_CONNECTION_STRING is not set in environment variables.")

        container_name = "summaries"
        filename = current_date_filename() + "_summary" + filetype

        blob_service_client = BlobServiceClient.from_connection_string(connect_str)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=filename)

        payload = {
            "summary": summary_text,
            "data": data
        }
        json_data = json.dumps(payload, indent=2)
        blob_client.upload_blob(json_data, overwrite=True)

        print(f"Uploaded {filename} to Azure Blob Storage.")
        
    except AzureError as e:
        print(f"Azure Blob upload failed: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")