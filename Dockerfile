# Use the official Python image as the base
FROM python:3.11-slim AS base

# Set working directory
WORKDIR /app

# Install dependencies for OCR, Tkinter, and other utilities
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    poppler-utils \
    tesseract-ocr \
    build-essential \
    python3-tk \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app/

# Copy the application code: means copy dir ./ (on host) to /app/ (on container)
COPY . /app/

# Expose the port that the service will run on (matching FastAPI port)
EXPOSE 8000

# Build Argument for Environment
ARG ENVIRONMENT=production
ENV ENVIRONMENT=${ENVIRONMENT}

# Expose the application port
EXPOSE 8000

# Run the FastAPI application
ENTRYPOINT ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
