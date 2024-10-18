# Base image using Python 3.12
FROM python:3.12-slim

# Set environment variables for Python and Poetry
ENV PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

# Install system dependencies and Poetry
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    libssl-dev \
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir poetry \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

COPY pyproject.toml poetry.lock update.py README.md /app/

# Install the dependencies using Poetry
RUN poetry install --no-root

# Command to run the Python script
CMD ["python", "update.py"]