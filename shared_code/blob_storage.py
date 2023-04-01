from urllib.parse import quote_plus
from azure.identity import DefaultAzureCredential
from azure.storage.blob import generate_blob_sas
from azure.storage.blob import BlobServiceClient, ResourceTypes, AccountSasPermissions
from datetime import datetime, timedelta, date
import pandas as pd
import logging

from .config import config_data
from .models import Job, Department, HiredEmployee


class BlobStorage():
    def __init__(self, account_name, container_name, account_key) -> None:
        self.account_name = account_name
        self.container_name = container_name
        self.account_key = account_key
        self.params = f"DefaultEndpointsProtocol=https;AccountName={self.account_name};AccountKey={self.account_key};EndpointSuffix=core.windows.net"
        self.blob_service_client = BlobServiceClient.from_connection_string(
            self.params)

    def list_of_files_in_blob(self):
        logging.info('Getting the list of files in a blob container')
        container_client = self.blob_service_client.get_container_client(
            self.container_name)
        blobs_list = container_client.list_blobs()
        files = []
        for blob in blobs_list:
            files.append(blob.name)
            logging.info(f'file name: {blob.name} appended.')
        return files

    def get_sas_url(self, blob_name):

        sas_blob = generate_blob_sas(account_name=self.account_name,
                                     container_name=self.container_name,
                                     blob_name=blob_name,
                                     account_key=self.account_key,
                                     resource_types=ResourceTypes(object=True),
                                     permission=AccountSasPermissions(
                                         read=True),
                                     expiry=datetime.utcnow() + timedelta(hours=1))
        url = f'https://{self.account_name}.blob.core.windows.net/{self.container_name}/{blob_name}?{sas_blob}'
        return url


# Initialize the Blob Storage class to make the connection to the Blob Storage account
blob_storage = BlobStorage(config_data['BLOB_ACCOUNT_NAME'],
                           config_data['BLOB_CONTAINER_NAME'],
                           config_data['BLOB_ACCOUNT_KEY'])

# Get the list of files in the blob storage
files = blob_storage.list_of_files_in_blob()

# Create each dataframe with the values of the csvs
for file in files:
    if file == 'hired_employees.csv':
        hired_employees = pd.read_csv(blob_storage.get_sas_url(file), names=[
                                      'id', 'name', 'datetime', 'department_id', 'job_id'])
    if file == 'jobs.csv':
        jobs = pd.read_csv(blob_storage.get_sas_url(file),
                           names=['id', 'job_id'])
    if file == 'departments.csv':
        departments = pd.read_csv(blob_storage.get_sas_url(
            file), names=['id', 'department_id'])
