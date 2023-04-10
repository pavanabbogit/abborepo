import logging
import azure.functions as func
import azure.durable_functions as df
from azure.storage.blob import BlobServiceClient
import pyodbc
from typing import List

def combine_data(context: df.DurableOrchestrationContext) -> str:
    # Retrieve the connection strings for Azure SQL DB and Azure Blob Storage
    sql_connection_string = "your_sql_connection_string"
    blob_storage_connection_string = "your_blob_storage_connection_string"

    # Create a list of tasks to retrieve data from SQL DB and Blob Storage in parallel
    tasks = [
        context.call_activity('get_data_from_sql', sql_connection_string),
        context.call_activity('get_data_from_blob_storage', blob_storage_connection_string)
    ]

    # Wait for all tasks to complete
    results: List[str] = yield context.task_all(tasks)

    # Combine the data
    combined_data = "".join(results)

    # Return the combined data
    return combined_data

@df.task()
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

@df.task()
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
