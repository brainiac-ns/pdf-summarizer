import logging
import os

from azure.storage.blob import BlobServiceClient

logging.basicConfig(level=logging.INFO)


def upload_file_to_azure(file_path: str, container_name: str, blob_name: str) -> bool:
    """
    Uploads a file to Azure Blob Storage

    Args:
        file_path (str): Path to PDF file locally
        container_name (str): Name of container
        blob_name (str): Name of blob (folder on azure blob storage)

    Returns:
        bool: True if file is uploaded successfully, False otherwise

    Examples:
        >>> upload_file_to_azure("uploads/input.pdf", "uploads", "input.pdf")
    """
    try:
        connect_str = os.getenv("AZURE_BLOB_CONNECTION_STRING")
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)

        container_client = blob_service_client.get_container_client(container_name)

        blob_client = container_client.get_blob_client(blob_name)
        with open(file_path, "rb") as data:
            blob_client.upload_blob(data)

        logging.info("File uploaded to Azure Blob Storage")
        return True
    except Exception as e:
        logging.exception(e)
        return False
