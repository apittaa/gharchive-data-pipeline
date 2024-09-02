from dagster import resource
import boto3
import os
from dotenv import load_dotenv
from pathlib import Path

# Specify the path to the .env file
env_file_path = Path("../envs/minio.env")

# Load the environment variables from the specified file
load_dotenv(dotenv_path=env_file_path)

# Cccess the environment variables
access_key = os.getenv("ACCESS_KEY")
secret_key = os.getenv("SECRET_KEY")


@resource
def s3_connection():
    access_key = os.getenv("ACCESS_KEY")
    secret_key = os.getenv("SECRET_KEY")
    endpoint_url = "http://s3service:9000"  # Adjust as necessary

    # Create and return your S3 client here using access_key and secret_key
    s3_client = boto3.client(
        "s3",
        endpoint_url=endpoint_url,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
    )

    return s3_client
