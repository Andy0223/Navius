import pytest
from fastapi import status


@pytest.fixture
def auth_headers(client):
    """Create authentication user headers"""
    # Register user and set health goal
    client.post("/api/auth/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123",
        "full_name": "Test User",
        "gender": "male",
        "height": 175,
        "weight": 70,
        "date_of_birth": "1990-01-01",
        "activity_level": "moderately_active",
        "health_goal": "weight_loss"
    })
    
    # Login
    login_response = client.post("/api/auth/login", data={
        "username": "testuser",
        "password": "testpass123"
    })
    
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_generate_health_plan(client, auth_headers):
    """Test generate health plan"""
    response = client.post("/api/health/plan", headers=auth_headers)
    
    assert response.status_code == status.HTTP_201_CREATED
    assert "title" in response.json()
    assert "exercise_plan" in response.json()
    assert "diet_suggestions" in response.json()


def test_get_health_plans(client, auth_headers):
    """Test get health plans"""
    # Generate a plan first
    client.post("/api/health/plan", headers=auth_headers)
    
    # Get plan list
    response = client.get("/api/health/plan", headers=auth_headers)
    
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) > 0


def test_get_ai_recommendations(client, auth_headers):
    """Test get AI recommendations"""
    response = client.get("/api/health/recommendations", headers=auth_headers)
    
    assert response.status_code == status.HTTP_200_OK
    assert "analysis" in response.json()
    assert "recommendations" in response.json()

