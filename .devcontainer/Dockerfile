# Use the official Python 3.12 image provided by Microsoft for development containers.
# This image is based on the Debian "Bookworm" distribution and is tailored for Python development.
FROM mcr.microsoft.com/devcontainers/python:3.12-bookworm

# Set the working directory inside the container to /workspace.
# This is where all the project files will reside and be worked on.
WORKDIR /workspace

# Copy the entire content of the current directory on the host machine into the /workspace directory in the container.
# This step makes sure that all your project files are available in the container.
COPY . /workspace/

# Update the package list and install Git.
# Install Poetry, a tool for managing Python project dependencies, without using the cache to reduce the image size.
RUN apt-get update && apt-get install -y git && \
    pip install poetry --no-cache-dir

# Configure Poetry not to create virtual environments (so dependencies are installed directly in the container's environment).
# Install the main dependencies listed in the pyproject.toml file, excluding any development or optional dependencies.
# The --no-root flag skips installing the current project as a package.
RUN poetry config virtualenvs.create false && \
    poetry install --only main --no-root
