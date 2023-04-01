import os

from dotenv import load_dotenv

load_dotenv()

config_data = dict()

config_data['SERVER'] = os.getenv('SERVER')
config_data['DATABASE'] = os.getenv('DATABASE')
config_data['DB_USERNAME'] = os.getenv('DB_USERNAME')
config_data['DB_PASSWORD'] = os.getenv('DB_PASSWORD')
config_data['PORT'] = os.getenv('PORT')
config_data['BLOB_STORAGE'] = os.getenv('BLOB_STORAGE_ACCOUNT_CON_STR')
config_data['BLOB_ACCOUNT_NAME'] = os.getenv('BLOB_ACCOUNT_NAME')
config_data['BLOB_CONTAINER_NAME'] = os.getenv('BLOB_CONTAINER_NAME')
config_data['BLOB_ACCOUNT_KEY'] = os.getenv('BLOB_ACCOUNT_KEY')

model_schema = 'ASDASDASDASD'