# Health Management Platform - Backend Service

## Project Overview

A comprehensive health management platform backend service built with FastAPI, providing user authentication, health data management, and AI-driven personalized health plan generation.

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL (via SQLAlchemy ORM)
- **Authentication**: JWT (JSON Web Token)
- **AI/ML**: TensorFlow, PyTorch, Scikit-learn
- **Testing**: PyTest

## Project Structure

```
backend/
├── app/
│   ├── core/              # Core configuration modules
│   ├── models/            # Database models
│   ├── schemas/           # Pydantic schemas
│   ├── api/              # API routes
│   ├── services/         # Business logic services
│   └── main.py           # Application entry point
├── tests/                 # Test files
├── migrations/            # Database migration files
├── requirements.txt       # Dependencies
└── .env                  # Environment configuration
```

## Installation Steps

1. Clone the repository
```bash
git clone <repository-url>
cd health-management-platform
```

2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Configure environment variables
```bash
cp .env.example .env
# Edit .env file, configure database connection and other parameters
```

5. Initialize database
```bash
# Ensure PostgreSQL is running
# Create database
createdb health_platform

# Run migrations
alembic upgrade head
```

6. Start the service
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation

After starting the service, visit the following addresses to view API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Key Features

### 1. User Authentication
- User registration
- User login (JWT authentication)
- Password encryption storage

### 2. Health Data Management
- Record exercise data
- Record diet data
- Record sleep data
- Data query and analysis

### 3. AI Health Plan Generation
- Generate personalized exercise plans based on user data
- Diet suggestions generation
- Health trend analysis

### 4. API Endpoints

#### User Related
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/users/me` - Get current user information

#### Health Data
- `POST /api/health/data` - Submit health data
- `GET /api/health/data` - Get health data
- `GET /api/health/statistics` - Get health statistics

#### Health Plans
- `POST /api/health/plan` - Generate health plan
- `GET /api/health/plan` - Get health plans
- `GET /api/health/recommendations` - Get AI recommendations

## Testing

Run tests:
```bash
pytest tests/
```

Test API with Postman by importing `postman_collection.json`

## Development Guide

### Database Migration
```bash
# Create new migration
alembic revision --autogenerate -m "description"

# Apply migration
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

## License

MIT License



