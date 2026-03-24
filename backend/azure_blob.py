from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from azure.core.exceptions import ResourceExistsError, ResourceNotFoundError
from config import settings
import io
from typing import List, Optional


class AzureBlobStorage:
    """
    Azure Blob Storage utility class for managing blobs in Azure Storage.

    Usage Examples:
        from azure_blob import azure_blob

        # Upload data
        success = azure_blob.upload_blob("myfile.txt", b"Hello World", "text/plain")

        # Upload file
        success = azure_blob.upload_file("document.pdf", "/path/to/document.pdf")

        # Download data
        data = azure_blob.download_blob("myfile.txt")

        # Download to file
        success = azure_blob.download_blob_to_file("myfile.txt", "/path/to/save.txt")

        # Delete blob
        success = azure_blob.delete_blob("myfile.txt")

        # List blobs
        blobs = azure_blob.list_blobs(prefix="folder/")

        # Get blob properties
        props = azure_blob.get_blob_properties("myfile.txt")

        # Generate SAS token for read access (1 hour)
        sas_token = azure_blob.generate_sas_token("myfile.txt", permission="r", expiry_hours=1)

        # Get blob URL with SAS
        url = azure_blob.get_blob_url("myfile.txt", sas_token)
    """
    def __init__(self):
    def __init__(self):
        self.account_name = settings.azure_storage_account_name
        self.account_key = settings.azure_storage_account_key
        self.connection_string = settings.azure_storage_connection_string
        self.container_name = settings.azure_storage_container_name

        # Initialize BlobServiceClient
        if self.connection_string:
            self.blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
        elif self.account_name and self.account_key:
            account_url = f"https://{self.account_name}.blob.core.windows.net"
            self.blob_service_client = BlobServiceClient(account_url=account_url, credential=self.account_key)
        else:
            raise ValueError("Azure Storage credentials not provided. Set AZURE_STORAGE_CONNECTION_STRING or AZURE_STORAGE_ACCOUNT_NAME and AZURE_STORAGE_ACCOUNT_KEY")

        # Get container client
        self.container_client = self.blob_service_client.get_container_client(self.container_name)

    def create_container_if_not_exists(self):
        """Create the container if it doesn't exist."""
        try:
            self.container_client.create_container()
            print(f"Container '{self.container_name}' created.")
        except ResourceExistsError:
            print(f"Container '{self.container_name}' already exists.")
        except Exception as e:
            print(f"Error creating container: {e}")

    def upload_blob(self, blob_name: str, data: bytes, content_type: str = "application/octet-stream", overwrite: bool = True) -> bool:
        """Upload data to a blob."""
        try:
            blob_client = self.blob_service_client.get_blob_client(container=self.container_name, blob=blob_name)
            blob_client.upload_blob(data, blob_type="BlockBlob", content_type=content_type, overwrite=overwrite)
            return True
        except Exception as e:
            print(f"Error uploading blob {blob_name}: {e}")
            return False

    def upload_file(self, blob_name: str, file_path: str, content_type: Optional[str] = None, overwrite: bool = True) -> bool:
        """Upload a file to blob storage."""
        try:
            with open(file_path, "rb") as data:
                blob_client = self.blob_service_client.get_blob_client(container=self.container_name, blob=blob_name)
                blob_client.upload_blob(data, blob_type="BlockBlob", content_type=content_type, overwrite=overwrite)
            return True
        except Exception as e:
            print(f"Error uploading file {file_path} to blob {blob_name}: {e}")
            return False

    def download_blob(self, blob_name: str) -> Optional[bytes]:
        """Download a blob as bytes."""
        try:
            blob_client = self.blob_service_client.get_blob_client(container=self.container_name, blob=blob_name)
            download_stream = blob_client.download_blob()
            return download_stream.readall()
        except ResourceNotFoundError:
            print(f"Blob {blob_name} not found.")
            return None
        except Exception as e:
            print(f"Error downloading blob {blob_name}: {e}")
            return None

    def download_blob_to_file(self, blob_name: str, file_path: str) -> bool:
        """Download a blob to a local file."""
        try:
            blob_client = self.blob_service_client.get_blob_client(container=self.container_name, blob=blob_name)
            with open(file_path, "wb") as download_file:
                download_stream = blob_client.download_blob()
                download_file.write(download_stream.readall())
            return True
        except ResourceNotFoundError:
            print(f"Blob {blob_name} not found.")
            return False
        except Exception as e:
            print(f"Error downloading blob {blob_name} to file {file_path}: {e}")
            return False

    def delete_blob(self, blob_name: str) -> bool:
        """Delete a blob."""
        try:
            blob_client = self.blob_service_client.get_blob_client(container=self.container_name, blob=blob_name)
            blob_client.delete_blob()
            return True
        except ResourceNotFoundError:
            print(f"Blob {blob_name} not found.")
            return False
        except Exception as e:
            print(f"Error deleting blob {blob_name}: {e}")
            return False

    def list_blobs(self, prefix: Optional[str] = None) -> List[str]:
        """List blobs in the container, optionally with a prefix."""
        try:
            blobs = self.container_client.list_blobs(name_starts_with=prefix)
            return [blob.name for blob in blobs]
        except Exception as e:
            print(f"Error listing blobs: {e}")
            return []

    def get_blob_properties(self, blob_name: str) -> Optional[dict]:
        """Get properties of a blob."""
        try:
            blob_client = self.blob_service_client.get_blob_client(container=self.container_name, blob=blob_name)
            properties = blob_client.get_blob_properties()
            return {
                "name": properties.name,
                "size": properties.size,
                "last_modified": properties.last_modified,
                "content_type": properties.content_settings.content_type,
                "etag": properties.etag
            }
        except ResourceNotFoundError:
            print(f"Blob {blob_name} not found.")
            return None
        except Exception as e:
            print(f"Error getting properties for blob {blob_name}: {e}")
            return None

    def generate_sas_token(self, blob_name: str, permission: str = "r", expiry_hours: int = 1) -> Optional[str]:
        """Generate a SAS token for a blob (requires azure-storage-blob[aio] for advanced features)."""
        # Note: For production, consider using User Delegation SAS or proper key management
        from datetime import datetime, timedelta
        from azure.storage.blob import generate_blob_sas, BlobSasPermissions

        try:
            sas_permissions = BlobSasPermissions(read=permission == "r", write="w" in permission, delete="d" in permission)
            sas_token = generate_blob_sas(
                account_name=self.account_name,
                container_name=self.container_name,
                blob_name=blob_name,
                account_key=self.account_key,
                permission=sas_permissions,
                expiry=datetime.utcnow() + timedelta(hours=expiry_hours)
            )
            return sas_token
        except Exception as e:
            print(f"Error generating SAS token for blob {blob_name}: {e}")
            return None

    def get_blob_url(self, blob_name: str, sas_token: Optional[str] = None) -> str:
        """Get the URL for a blob, optionally with SAS token."""
        blob_client = self.blob_service_client.get_blob_client(container=self.container_name, blob=blob_name)
        url = blob_client.url
        if sas_token:
            url += f"?{sas_token}"
        return url


# Global instance
azure_blob = AzureBlobStorage()