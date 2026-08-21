# Use the official Python slim image for a smaller footprint
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
# libpq-dev is required for psycopg2 (PostgreSQL adapter)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
# First copy only requirements.txt to cache the pip install step
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install gunicorn psycopg2-binary redis celery

# Copy the entire project into the container
COPY . /app/

# Expose port 8000 for Gunicorn
EXPOSE 8000

# Start Gunicorn server (Wait for DB and collect static in docker-compose.yml)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "config.wsgi:application"]
