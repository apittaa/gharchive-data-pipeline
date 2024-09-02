from setuptools import find_packages, setup

setup(
    name="gharchive_dagster",
    packages=find_packages(exclude=["gharchive_dagster_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud",
        "boto3",
        "dagster-dbt",
        "dagster-pyspark",
        "pyarrow",
        "python-dotenv",
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
