# This file will define how to build Django container
FROM python:3.8-slim-buster

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        netcat \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

# no-cache
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Run migrations
RUN python3 manage.py makemigrations api
RUN python3 manage.py migrate

ENTRYPOINT [ "python", "manage.py", "runserver", "0.0.0.0:8000"]