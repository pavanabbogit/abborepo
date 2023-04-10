from azure.storage.filedatalake import DataLakeServiceClient

# Set up connection to your Data Lake account using SAS
account_url = 'https://<your-account-name>.dfs.core.windows.net'
sas_token = '<your-sas-token>'
service_client = DataLakeServiceClient(account_url=account_url, credential=sas_token)

# Set up path to your desired container or folder
container_name = '<your-container-name>'
folder_path = '<your-folder-path>'
 yar205
# Use the service client to get a list of paths in the container or folder
paths = service_client.get_paths(container_name=container_name, path=folder_path)

# Loop through the paths to get a list of files (excluding directories)
files = []
for path in paths:
    if path.is_directory == False:
        files.append(path.name)

# Print the list of files
print(files)

https://github.com/pavanabbogit/abborepo.git