# %%

from datetime import datetime
import pytz
import os
import boto3
import psycopg2
import json
from psycopg2.extras import DictCursor
import time
from botocore.exceptions import ClientError
from botocore.config import Config
import logging

# Configure the logging format
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
#%%
#Set up destination table and schema
table_name = "raw_trips"
table_schema = "schema_datawarehouse_landingzone"

#%%
# Retrieve environment variables

POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', "password")
POSTGRES_DB = os.environ.get('POSTGRES_DB', "postgres")
POSTGRES_USER = os.environ.get('POSTGRES_USER', "admin")
POSTGRES_HOST = os.environ.get('POSTGRES_HOST', "localhost")
POSTGRES_PORT = int(os.environ.get('POSTGRES_PORT', "5433"))
S3_BUCKET_NAME = os.environ.get('BUCKET_NAME', "webapp-bucket")
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', 'GNotw4aO1P6w5rtQmSHR')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', 'BprZP4bmZTBVpxK6ApkLSS3G1v7qYZadYW1bKwyL')
AWS_END_POINT = os.environ.get('AWS_END_POINT', "http://localhost:9000")
AWS_REGION = os.environ.get('AWS_REGION' , "us-east-6") 
logging.info("Imported environmental variables")


#%%

# Connect to PostgreSQL database
DATABASE_URL = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
conn = psycopg2.connect(DATABASE_URL)
logging.info("Connected to database")

#%%
# S3 client setup
s3_client = boto3.client(
    service_name='s3',
    region_name=AWS_REGION,
    endpoint_url=AWS_END_POINT,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    config=Config(signature_version='s3v4')
)
logging.info("Created the S3 Client")

#%%

def check_bucket(bucket_name):
    try:
        # Check if the bucket exists
        s3_client.head_bucket(Bucket=bucket_name)
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            logging.info(f"Bucket '{bucket_name}' does not exist.")
        else:
            # Unexpected error, raise it
            raise


# Function to retrieve JSON files from S3
def retrieve_files_from_s3():
    """Retrieve JSON files from S3."""
    files = []
    try:
        response = s3_client.list_objects_v2(Bucket=S3_BUCKET_NAME)
        if 'Contents' in response:
            for obj in response['Contents']:
                if obj['Key'].endswith('.json'):
                    files.append(obj['Key'])
        else:
            logging.info("No files found in the S3 bucket.")
    except ClientError as e:
        logging.error(f"Failed to retrieve files from S3: {e}")
    return files


# Function to retrieve data from a JSON file in S3
def retrieve_data_from_file(file_name):
    """Retrieve data from a JSON file in S3."""
    data = []
    try:
        response = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=file_name)
        content = response['Body'].read().decode('utf-8')
        data = json.loads(content)
    except ClientError as e:
        logging.error(f"Failed to retrieve data from file {file_name}: {e}")
    return data


# Function to retrieve column names from the PostgreSQL table
def get_table_columns(table_name="raw_trips", table_schema="schema_datawarehouse_landingzone"):
    """Retrieve column names from the PostgreSQL table."""
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}' and table_schema = '{table_schema}'")
            columns = [row[0] for row in cursor.fetchall()]
            return columns
    except psycopg2.Error as e:
        logging.error(f"Failed to retrieve column names from table: {e}")
        return None


# Function to insert data into PostgreSQL
def insert_data_to_postgres(data, table_name="raw_trips", table_schema="schema_datawarehouse_landingzone"):
    """Insert data into PostgreSQL."""
    try:
        with conn.cursor() as cursor:
            columns = get_table_columns(table_name, table_schema)[:-1]
            if columns:
                for entry in data:
                    if isinstance(entry, dict):
                        column_values = [entry.get(col, None) for col in columns]
                    elif isinstance(entry, list):
                        # Pad the entry list with None values to match the length of columns
                        padded_entry = entry + [None] * (len(columns) - len(entry))
                        column_values = padded_entry
                    else:
                        logging.warning(f"Invalid data type encountered: {type(entry)}")
                        continue
                    placeholders = ', '.join(['%s'] * len(columns))
                    column_names = ', '.join(columns)
                    query = f"""
                        INSERT INTO {table_schema}.{table_name} ({column_names})
                        VALUES ({placeholders})
                        ON CONFLICT DO NOTHING
                    """
                    cursor.execute(query, column_values)
                conn.commit()
                logging.info("Data inserted into PostgreSQL successfully.")
    except psycopg2.Error as e:
        logging.error(f"Failed to insert data into PostgreSQL: {e}")

#%%
# Main function to process S3 data and insert it into PostgreSQL
def process_s3_data():
    """Retrieve data from S3 and insert it into PostgreSQL."""
    files = retrieve_files_from_s3()
    for file_name in files[-1:]:
        data = retrieve_data_from_file(file_name)
        time.sleep(10)
        if data:
            insert_data_to_postgres(data, table_name, table_schema)
            # Optionally, delete the file from S3 after processing
            try:
                s3_client.delete_object(Bucket=S3_BUCKET_NAME, Key=file_name)
                logging.info(f"Deleted file: {file_name}")
            except:
                logging.error(f"Could not delete file: {file_name}")



if __name__ == "__main__":
    process_s3_data()

# %%
