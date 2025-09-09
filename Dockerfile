# syntax=docker/dockerfile:1
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install build tools for psycopg2 and redis
RUN apt-get update && apt-get install -y \
    gcc libpq-dev build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY . .

# Expose the Cloud Run port
EXPOSE 8080

# Run with uvicorn (use Cloud Run's PORT env var)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
