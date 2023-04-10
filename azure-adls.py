from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

# Set the Azure Storage account name and the container name
account_name = "<your-storage-account-name>"
container_name = "<your-container-name>"

# Create a DefaultAzureCredential object to authenticate with Azure AD
credential = DefaultAzureCredential()

# Create a BlobServiceClient object using the account name, credential, and HTTPS endpoint
blob_service_client = BlobServiceClient(account_url=f"https://{account_name}.blob.core.windows.net", credential=credential)

# Get a reference to the container
container_client = blob_service_client.get_container_client(container_name)

# List all the blobs (files and folders) in the container
blobs = container_client.list_blobs()

# Iterate through the blobs and check if they are folders
for blob in blobs:
    if blob.name[-1] == '/':
        print(f"Found folder: {blob.name}")
        # Get a reference to the folder
        folder_client = container_client.get_blob_client(blob.name)
        
        # List all the blobs (files and subfolders) in the folder
        sub_blobs = folder_client.list_blobs()
        
        # Iterate through the blobs and check if they are subfolders or files
        for sub_blob in sub_blobs:
            if sub_blob.name[-1] == '/':
                print(f"Found subfolder: {sub_blob.name}")
            else:
                print(f"Found file: {sub_blob.name}")
