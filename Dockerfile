# Use Python 3.12 as the base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy application and requirements files
ADD application.py /app/application.py
ADD requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the application port
EXPOSE 8000

# Run the FastAPI application
ENTRYPOINT ["uvicorn", "application:app", "--host", "0.0.0.0", "--port", "8000"]
