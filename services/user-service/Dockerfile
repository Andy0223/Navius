FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy shared code first
COPY ../../shared /app/shared

# Copy service code
COPY app /app/app
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8002

# Start command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8002"]

