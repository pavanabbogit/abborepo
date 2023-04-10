import requests
import json
import adal

# Azure AD Authentication
tenant_id = "your-tenant-id"
client_id = "your-client-id"
client_secret = "your-client-secret"
resource = "https://analysis.windows.net/powerbi/api"
authority_url = "https://login.microsoftonline.com/" + tenant_id
context = adal.AuthenticationContext(authority_url)
token = context.acquire_token_with_client_credentials(resource, client_id, client_secret)

# Power BI REST API endpoint
group_id = "your-group-id"
dataset_id = "your-dataset-id"
api_url = f"https://api.powerbi.com/v1.0/myorg/groups/{group_id}/datasets/{dataset_id}/"

# File path and name
file_path = "your-file-path"
file_name = "your-file-name"

# Read file content
with open(file_path, "rb") as f:
    file_content = f.read()

# Prepare request headers and body
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token['accessToken']}"
}
request_body = {
    "fileData": base64.b64encode(file_content).decode('utf-8'),
    "name": file_name,
    "conflictHandler": "Abort"
}

# Send request to Power BI REST API
response = requests.post(api_url + "Import", headers=headers, data=json.dumps(request_body))

# Check response status
if response.status_code == 202:
    operation_id = response.json()['operation']
    headers = {
        "Authorization": f"Bearer {token['accessToken']}"
    }
    while True:
        operation_response = requests.get(api_url + f"Operations/{operation_id}", headers=headers).json()
        if operation_response['status'] == 'Succeeded':
            break
        elif operation_response['status'] == 'Failed':
            raise Exception("Import failed")
    print("Import completed successfully")
else:
    raise Exception(f"Import failed with status code {response.status_code}")
