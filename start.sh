#!/bin/bash

echo "=== Health Management Platform Startup Script ==="

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Check .env file
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "Please edit the .env file to configure database connection and other parameters"
fi

# Check database
echo "Checking database connection..."
if ! pg_isready -h localhost -p 5432 -U postgres > /dev/null 2>&1; then
    echo "PostgreSQL is not running, starting with Docker Compose..."
    docker-compose up -d db
    echo "Waiting for database to start..."
    sleep 5
fi

# Run database migrations
echo "Running database migrations..."
alembic upgrade head

# Start service
echo "Starting service..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

