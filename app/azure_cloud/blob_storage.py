import json
from azure.storage.blob import BlobServiceClient
import os
from datetime import datetime



def current_date_filename():
    return datetime.today().strftime("%Y-%m-%d")



def upload_to_blob(data: dict, filetype: str = ".json"):
    connect_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    container_name = "summaries"
    filename = current_date_filename() + "_summary_" + filetype

    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=filename)

    json_data = json.dumps(data, indent=2)
    blob_client.upload_blob(json_data, overwrite=True)
    print("Uploaded JSON to Azure Blob Storage.")