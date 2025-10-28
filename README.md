# Navius - AI-Powered Health Management Platform

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)

A comprehensive, AI-powered health management platform backend built with FastAPI. This platform provides intelligent health data tracking, personalized health plan generation, and ML-driven recommendations using Scikit-learn, TensorFlow, and PyTorch.

## 🎯 Features

### Core Functionality
- **User Authentication**: Secure JWT-based authentication system
- **Health Data Management**: Track exercise, diet, and sleep data
- **AI-Powered Plan Generation**: ML-driven personalized health plans
- **Intelligent Recommendations**: Data-driven health suggestions
- **Statistics & Analytics**: Comprehensive health metrics and trends

### AI/ML Capabilities
- **K-Means Clustering**: User segmentation for personalized recommendations
- **KNN Regression**: Exercise duration and frequency prediction
- **Feature Engineering**: 11-dimensional user feature extraction
- **Progressive Recommendation**: Adaptive algorithm based on user progression
- **Calorie Target Prediction**: ML-based nutrition planning

## 🚀 Tech Stack

### Backend
- **FastAPI**: Modern, high-performance web framework
- **PostgreSQL**: Relational database
- **SQLAlchemy**: ORM for database operations
- **JWT**: Authentication and authorization
- **Alembic**: Database migrations

### AI/ML
- **Scikit-learn**: K-Means clustering, KNN regression
- **TensorFlow**: Deep learning capabilities
- **PyTorch**: Neural network models
- **Transformers**: Text generation (GPT-2)
- **NumPy/Pandas**: Data processing

### DevOps
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration
- **Pytest**: Unit and integration testing
- **Postman**: API testing

## 📁 Project Structure

```
Navius/
├── app/
│   ├── api/
│   │   └── endpoints/        # API routes
│   │       ├── auth.py       # Authentication endpoints
│   │       ├── users.py      # User management
│   │       └── health.py     # Health data & plans
│   ├── core/                 # Core configuration
│   │   ├── config.py         # Settings
│   │   ├── database.py       # DB connection
│   │   └── security.py      # JWT authentication
│   ├── models/               # Database models
│   │   ├── user.py           # User model
│   │   └── health_data.py    # Health data models
│   ├── schemas/              # Pydantic schemas
│   │   ├── user.py
│   │   └── health_data.py
│   ├── services/             # Business logic
│   │   ├── ai_service.py     # AI/ML engine ⭐
│   │   ├── health_data_service.py
│   │   └── user_service.py
│   └── main.py               # Application entry
├── tests/                    # Test suite
├── migrations/               # Database migrations
├── docker-compose.yml        # Docker configuration
├── Dockerfile                # Docker image
├── requirements.txt          # Dependencies
└── test_apis.py             # API testing script
```

## 🛠️ Installation

### Prerequisites
- Python 3.11+
- PostgreSQL 15+
- Docker & Docker Compose
- Git

### Quick Start with Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/Navius.git
cd Navius

# Start all services (Database + Backend)
docker-compose up -d

# The API will be available at http://localhost:8000
```

### Local Development Setup

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env with your database credentials

# 4. Start PostgreSQL
docker-compose up -d db

# 5. Run migrations
alembic upgrade head

# 6. Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 📚 API Documentation

Once the server is running:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 🔌 API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | User registration |
| POST | `/api/auth/login` | User login (JWT token) |

### User Management
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/users/me` | Get current user profile |

### Health Data
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/health/data` | Submit health data (exercise/diet/sleep) |
| GET | `/api/health/data` | Get health data with filters |
| GET | `/api/health/statistics` | Get health statistics |

### Health Plans (AI-Powered)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/health/plan` | Generate AI-powered health plan |
| GET | `/api/health/plan` | Get user's health plans |
| GET | `/api/health/recommendations` | Get AI recommendations |

## 🤖 AI/ML Features

### Machine Learning Models

#### 1. User Segmentation (K-Means)
```python
- Clusters users into 5 groups based on health patterns
- Enables personalized recommendations
- Identifies similar user profiles
```

#### 2. Exercise Prediction (KNN Regression)
```python
- Predicts optimal exercise duration
- Considers current fitness level
- Implements progressive overload algorithm
- Adjusts based on user goals
```

#### 3. Feature Engineering
```python
Features extracted:
- Demographics (height, weight, age, gender)
- Activity level encoding
- Exercise frequency & duration
- Calories burned
- Sleep quality
- Nutritional intake
```

### AI-Driven Recommendations

The system generates personalized recommendations based on:
- **User profile analysis**: Demographics, activity level, health goals
- **Historical data**: Past exercise, diet, and sleep patterns
- **Progress tracking**: Adaptive recommendations based on improvement
- **Goal optimization**: Tailored plans for weight loss, muscle gain, endurance

### Example AI-Generated Plan

```json
{
  "title": "Weight Loss Health Plan",
  "description": "A personalized AI-powered health plan... Our AI analysis shows...",
  "calories_target": 2013.0,
  "exercise_minutes_per_day": 26.0,
  "exercise_plan": "AI-Optimized Weekly Exercise Plan... Based on AI analysis...",
  "ai_generated_content": "..."
}
```

## 🧪 Testing

### Run All Tests
```bash
# Unit tests
pytest tests/

# API integration tests
python test_apis.py

# With Docker
docker-compose exec backend pytest tests/
```

### Test with Postman
Import `postman_collection.json` into Postman for API testing.

## 📊 Database Models

### User
- Authentication credentials
- Demographics (age, gender, height, weight)
- Activity level and health goals
- Relationship with health data and plans

### HealthData
- Unified model for exercise, diet, and sleep
- Timestamp tracking
- User-specific filtering

### HealthPlan
- AI-generated content
- Exercise and diet recommendations
- Goal-oriented planning
- Progress tracking

## 🐳 Docker Commands

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f backend

# Stop services
docker-compose down

# Rebuild services
docker-compose build --no-cache

# Execute commands in container
docker-compose exec backend python test_apis.py
```

## 🔐 Security

- **JWT Authentication**: Secure token-based auth
- **Password Hashing**: Bcrypt encryption
- **CORS Configuration**: Cross-origin security
- **Input Validation**: Pydantic schemas
- **SQL Injection Prevention**: SQLAlchemy ORM

## 🚦 Environment Variables

Create a `.env` file:

```bash
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/health_platform
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## 📈 Performance

- **Async I/O**: FastAPI's async capabilities
- **Connection Pooling**: Database connection optimization
- **Caching**: Model caching for AI predictions
- **Scalability**: Docker-based horizontal scaling

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License.

## 👥 Authors

- Your Name - [GitHub](https://github.com/yourusername)

## 🙏 Acknowledgments

- FastAPI community
- Scikit-learn for ML capabilities
- Docker for containerization
- PostgreSQL team

## 📞 Support

For support, email support@navius.com or create an issue in the repository.

---

**Built with ❤️ using FastAPI, PostgreSQL, and AI/ML**
