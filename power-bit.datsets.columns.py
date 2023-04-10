import requests
import json

# Replace with your own values
client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"
workspace_id = "YOUR_WORKSPACE_ID"

# Authenticate with the Power BI REST API
auth_url = "https://login.microsoftonline.com/common/oauth2/token"
auth_data = {
    "grant_type": "client_credentials",
    "client_id": client_id,
    "client_secret": client_secret,
    "resource": "https://analysis.windows.net/powerbi/api"
}
auth_headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}
auth_response = requests.post(auth_url, data=auth_data, headers=auth_headers)
access_token = json.loads(auth_response.text)["access_token"]
headers = {
    "Authorization": "Bearer " + access_token,
    "Content-Type": "application/json"
}

# Get a list of all datasets in the workspace
datasets_url = f"https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/datasets"
datasets_response = requests.get(datasets_url, headers=headers)
datasets = json.loads(datasets_response.text)["value"]

# Get a list of all tables and columns in each dataset
for dataset in datasets:
    dataset_id = dataset["id"]
    tables_url = f"https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/datasets/{dataset_id}/tables"
    tables_response = requests.get(tables_url, headers=headers)
    tables = json.loads(tables_response.text)["value"]
    for table in tables:
        table_name = table["name"]
        columns_url = f"https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/datasets/{dataset_id}/tables/{table_name}/columns"
        columns_response = requests.get(columns_url, headers=headers)
        columns = json.loads(columns_response.text)["value"]
        for column in columns:
            column_name = column["name"]
            data_type = column["dataType"]
            print(f"{dataset['name']}, {table_name}, {column_name}, {data_type}")
