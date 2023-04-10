import logging
import azure.functions as func
import azure.durable_functions as df
from azure.storage.blob import BlobServiceClient
import pyodbc

def combine_data(context: df.DurableOrchestrationContext) -> str:
    # Retrieve the connection strings for Azure SQL DB and Azure Blob Storage
    sql_connection_string = "your_sql_connection_string"
    blob_storage_connection_string = "your_blob_storage_connection_string"

    # Retrieve the data from Azure SQL DB
    sql_data = yield context.call_activity('get_data_from_sql', sql_connection_string)

    # Retrieve the data from Azure Blob Storage
    blob_data = yield context.call_activity('get_data_from_blob_storage', blob_storage_connection_string)

    # Combine the data
    combined_data = sql_data + blob_data

    # Return the combined data
    return combined_data

def get_data_from_sql(sql_connection_string: str) -> str:
    # Connect to the Azure SQL DB
    connection = pyodbc.connect(sql_connection_string)

    # Retrieve the data from the database
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM TableName")
    sql_data = cursor.fetchall()

    # Close the database connection
    connection.close()

    # Return the data
    return sql_data

def get_data_from_blob_storage(blob_storage_connection_string: str) -> str:
    # Connect to the Azure Blob Storage
    blob_service_client = BlobServiceClient.from_connection_string(blob_storage_connection_string)
    container_client = blob_service_client.get_container_client("container_name")

    # Retrieve the data from the blob
    blob_client = container_client.get_blob_client("blob_name")
    blob_data = blob_client.download_blob().content_as_text()

    # Return the data
    return blob_data

main = df.Orchestrator.create(combine_data)
