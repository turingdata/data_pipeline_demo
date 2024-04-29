
#%%
from datetime import datetime
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
def check_and_create_bucket(bucket_name):
    """Check if S3 bucket exists, create if not."""
    try:
        # Check if the bucket exists
        s3_client.head_bucket(Bucket=bucket_name)
        logging.debug(f"Bucket '{bucket_name}' already exists.")
        return
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            # Bucket does not exist, create it
            s3_client.create_bucket(Bucket=bucket_name)
            logging.info(f"Bucket '{bucket_name}' created successfully.")
        else:
            # Unexpected error, raise it
            raise

def get_last_processed_id():
    """Retrieve the last processed ID from a file."""
    try:
        with open('last_id.txt', 'r') as f:
            last_id = int(f.read().strip())
            logging.info("Last processed ID retrieved.")
    except (FileNotFoundError, ValueError):
        last_id = 0  # Default to 0 if the file doesn't exist or contains invalid data
    return last_id

def update_last_processed_id(last_id):
    """Update the last processed ID in a file."""
    with open('last_id.txt', 'w') as f:
        f.write(str(last_id))
    logging.info("Last processed ID updated.")

def fetch_new_entries(last_id):
    """Fetch new entries from the database with IDs greater than the last processed ID."""
    new_entries = []
    with conn.cursor(cursor_factory=DictCursor) as cur:
        cur.execute("SELECT * FROM trips WHERE id > %s ORDER BY id ASC", (last_id,))
        new_entries = cur.fetchall()
    logging.info(f"Fetched {len(new_entries)} new entries from the database.")
    return new_entries

def upload_to_s3(data, file_name):
    """Upload data to S3."""
    logging.info("Uploading file to S3.")
    try: 
        s3_client.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=file_name,
            Body=json.dumps(data, default=str)  # Convert data to JSON, handling dates etc.
        )
        logging.info(f"File '{file_name}' uploaded to S3.")
    except:
        logging.error(f"Could not upload file: '{file_name}'  to S3.")

def main():
    """Main function to fetch new entries and upload them to S3."""
    logging.info("Starting main function...")
    check_and_create_bucket(S3_BUCKET_NAME)
    last_id = get_last_processed_id()
    new_entries = fetch_new_entries(last_id)
    if new_entries:
        # Update the last processed ID based on the entries fetched
        last_processed_id = new_entries[-1]['id']  # Assuming 'id' is the name of your unique ID column
        update_last_processed_id(last_processed_id)
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        file_name = f"data_{timestamp}.json"
        upload_to_s3(new_entries, file_name)
    else:
        logging.info("No new entries to upload.")

if __name__ == "__main__":
    main()

#%% 