from dagster import resource
from pyspark.sql import SparkSession
from dotenv import load_dotenv
from pathlib import Path
import os

# Specify the path to the .env file
env_file_path = Path("../envs/minio.env")

# Load the environment variables from the specified file
load_dotenv(dotenv_path=env_file_path)


@resource
def spark_session():
    """
    A resource that provides a SparkSession configured for Apache Iceberg.

    Returns:
        SparkSession: The initialized SparkSession with Iceberg support.
    """
    access_key = os.getenv("ACCESS_KEY")
    secret_key = os.getenv("SECRET_KEY")
    endpoint_url = "http://s3service:9000"
    return (
        SparkSession.builder.appName("SparkSession")
        .config(
            "spark.sql.catalog.spark_catalog", "org.apache.iceberg.spark.SparkCatalog"
        )
        .config("spark.sql.catalog.spark_catalog.type", "hive")
        .config("spark.sql.catalog.spark_catalog.uri", "thrift://localhost:9083")
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
        .config("spark.hadoop.fs.s3a.endpoint", f"{endpoint_url}")
        .config("spark.hadoop.fs.s3a.access.key", f"{access_key}")
        .config("spark.hadoop.fs.s3a.secret.key", f"{secret_key}")
        .config("spark.hadoop.fs.s3a.path.style.access", "true")
        .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false")
        .config(
            "spark.sql.extensions",
            "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions",
        )
        .config(
            "spark.jars.packages",
            "org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.6.1,"
            "org.apache.hadoop:hadoop-aws:3.3.4,"
            "com.amazonaws:aws-java-sdk-bundle:1.12.770",
        )
        .config("spark.network.timeout", "800s")
        .config("spark.executor.heartbeatInterval", "60s")
        .config("spark.driver.memory", "4g")
        .config("spark.executor.memory", "4g")
        .getOrCreate()
    )
