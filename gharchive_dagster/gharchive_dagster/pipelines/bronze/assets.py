from dagster import asset
from pathlib import Path
import os
import requests
from dotenv import load_dotenv
import sys
import tempfile

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

# Path to s3_connection resource
from resources.pyspark_resource import spark_session

# Specify the path to the .env file
env_file_path = Path("../envs/minio.env")

# Load the environment variables from the specified file
load_dotenv(dotenv_path=env_file_path)

# Cccess the environment variables
s3_bucket = os.getenv("BRONZE_BUCKET")


def download_file(url):
    """Download a file from a URL and return the response stream."""
    response = requests.get(url, stream=True)
    response.raise_for_status()  # Raise an error for bad responses
    return response.raw


def upload_to_s3(s3_client, data_stream, s3_bucket, s3_key):
    """Upload data stream directly to S3."""
    s3_client.upload_fileobj(data_stream, s3_bucket, s3_key)
    print(f"Uploaded to s3://{s3_bucket}/{s3_key}")


@asset(required_resource_keys={"s3_connection"})
# Create a function to get file from url: https://data.gharchive.org/2015-01-01-15.json.gz
# And return the file to transform it into a iceberg format in another function
def gharchive_data(year: int, month: int, day: int) -> Path:
    for chunk in range(1, 2):
        # s3_client = s3_connection()
        spark = spark_session()

        name = f"{year}-{month:02}-{day:02}"
        url = f"https://data.gharchive.org/{name}-{chunk}.json.gz"

        # Stream download the file
        response = requests.get(url, stream=True)

        # Create a temporary file to store the JSON data
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=".json.gz", dir="./"
        ) as temp_file:
            temp_file.write(response.content)
            temp_file_path = temp_file.name

        # Load the streamed JSON data into a PySpark DataFrame
        df = spark.read.json(temp_file_path)

        # # Define the S3 key for this JSON file
        # file_name = f"gharchive/{name}-{chunk}.json.gz"

        # Define the S3 key for the Parquet file
        parquet_file_name = f"gharchive/{name}-{chunk}.parquet"

        # # Upload the response content directly to S3
        # s3_client.upload_fileobj(response.raw, s3_bucket, file_name)

        # Write the DataFrame to Parquet format in S3
        df.write.mode("overwrite").parquet(f"s3a://{s3_bucket}/{parquet_file_name}")

        print(f"Uploaded {url} to s3://{s3_bucket}/{parquet_file_name}")

        # Cleanup: Remove the temporary files
        os.remove(temp_file_path)  # Remove the JSON temp file
        print(f"Removed {temp_file_path}")


if __name__ == "__main__":
    year = 2024
    month = 1
    day = 1
    gharchive_data(year, month, day)
