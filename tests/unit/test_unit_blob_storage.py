import json
import pytest
from unittest.mock import patch, MagicMock
from app.azure_cloud.blob_storage import upload_to_blob

@pytest.mark.unit
@patch("app.azure_cloud.blob_storage.BlobServiceClient")
def test_upload_to_blob_json(mock_blob_service_client):

    mock_blob_service = MagicMock()
    mock_blob_client = MagicMock()
    mock_blob_service_client.from_connection_string.return_value = mock_blob_service
    mock_blob_service.get_blob_client.return_value = mock_blob_client

    test_data = {"sentiment": "bull", "confidence": 0.83}
    summary_text = "dummy_summary"
    sources_used = "dummy sources"

    payload = {
    "summary": summary_text,
    "data": test_data,
    "sources": sources_used
    }
    expected_payload = {
        "summary": summary_text,
        "data": test_data,
        "sources": sources_used,
    }

    upload_to_blob(test_data, summary_text=summary_text, sources_used=sources_used, filetype=".json")

    mock_blob_service_client.from_connection_string.assert_called()
    mock_blob_service.get_blob_client.assert_called()
    mock_blob_client.upload_blob.assert_called_once()

    uploaded_arg = mock_blob_client.upload_blob.call_args[0][0]
    assert json.loads(uploaded_arg) == expected_payload
    print("Unit-test: upload_to_blob ran successfully with mocked blob-service.")