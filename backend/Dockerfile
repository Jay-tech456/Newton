FROM python:3.11-slim

WORKDIR /app

# Install system dependencies including curl for healthcheck
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create storage directories with proper permissions
RUN mkdir -p storage/frames storage/datasets && \
    chmod -R 777 storage

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "run.py"]
