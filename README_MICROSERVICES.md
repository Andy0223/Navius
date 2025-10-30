# Navius - Microservices Architecture

This project has been converted from a monolithic FastAPI application to a microservices architecture.

## Architecture Overview

The application is now split into the following microservices:

1. **Auth Service** (Port 8001) - Handles user authentication and authorization
2. **User Service** (Port 8002) - Manages user profiles and user-related operations
3. **Health Data Service** (Port 8003) - Handles health data, plans, and statistics
4. **AI Service** (Port 8004) - Provides AI/ML capabilities for personalized health plans
5. **API Gateway** (Port 8000) - Routes requests to appropriate microservices

All services share a common PostgreSQL database and use JWT tokens for authentication.

## Directory Structure

```
Navius_backend/
├── shared/                      # Shared libraries and models
│   ├── config.py               # Shared configuration
│   ├── database.py             # Database setup
│   ├── security.py             # JWT and authentication utilities
│   └── models.py               # Shared database models
├── services/
│   ├── auth-service/           # Authentication service
│   ├── user-service/           # User management service
│   ├── health-data-service/    # Health data service
│   ├── ai-service/             # AI/ML service
│   └── api-gateway/            # API Gateway
└── docker-compose.microservices.yml
```

## Running the Microservices

### Using Docker Compose (Recommended)

```bash
# Start all services
docker-compose -f docker-compose.microservices.yml up -d

# View logs
docker-compose -f docker-compose.microservices.yml logs -f

# Stop all services
docker-compose -f docker-compose.microservices.yml down
```

### Individual Service Access

- **API Gateway**: http://localhost:8000
- **Auth Service**: http://localhost:8001
- **User Service**: http://localhost:8002
- **Health Data Service**: http://localhost:8003
- **AI Service**: http://localhost:8004

## API Endpoints

All client requests should go through the API Gateway at `http://localhost:8000`:

- `/api/auth/*` - Authentication endpoints (register, login)
- `/api/users/*` - User management endpoints
- `/api/health/*` - Health data and plans endpoints
- `/api/ai/*` - AI-powered recommendations and plan generation

## Service Communication

Services communicate via:
- **HTTP/REST** - For synchronous requests through the API Gateway
- **Shared Database** - All services access the same PostgreSQL database
- **JWT Tokens** - For authentication and authorization

## Environment Variables

Create a `.env` file in the root directory:

```env
DATABASE_URL=postgresql://postgres:postgres@db:5432/health_platform
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Development

To run services individually for development:

```bash
# Auth Service
cd services/auth-service
uvicorn app.main:app --port 8001 --reload

# User Service
cd services/user-service
uvicorn app.main:app --port 8002 --reload

# Health Data Service
cd services/health-data-service
uvicorn app.main:app --port 8003 --reload

# AI Service
cd services/ai-service
uvicorn app.main:app --port 8004 --reload

# API Gateway
cd services/api-gateway
uvicorn app.main:app --port 8000 --reload
```

## Benefits of Microservices Architecture

1. **Scalability** - Each service can be scaled independently
2. **Maintainability** - Services can be developed and deployed independently
3. **Technology Diversity** - Each service can use different technologies if needed
4. **Fault Isolation** - Failure in one service doesn't affect others
5. **Team Autonomy** - Different teams can work on different services

## Notes

- All services currently share the same database for simplicity
- For production, consider service-specific databases
- Consider adding message queue (RabbitMQ/Kafka) for async communication
- Add service discovery mechanism (Consul/Eureka) for dynamic service routing
- Implement circuit breakers for resilience

