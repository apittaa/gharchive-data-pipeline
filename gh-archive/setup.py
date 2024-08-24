from setuptools import find_packages, setup

setup(
    name="gh_archive",
    packages=find_packages(exclude=["gh_archive_tests"]),
    install_requires=["dagster", "dagster-cloud"],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
