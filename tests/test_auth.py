import pytest
from fastapi import status


def test_register_user(client):
    """Test user registration"""
    response = client.post("/api/auth/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123",
        "full_name": "Test User"
    })
    
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["username"] == "testuser"
    assert response.json()["email"] == "test@example.com"


def test_register_duplicate_username(client):
    """Test duplicate username registration"""
    # 第一次注册
    client.post("/api/auth/register", json={
        "username": "testuser",
        "email": "test1@example.com",
        "password": "testpass123"
    })
    
    # Try to register with the same username
    response = client.post("/api/auth/register", json={
        "username": "testuser",
        "email": "test2@example.com",
        "password": "testpass123"
    })
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_login_success(client):
    """Test successful login"""
    # 先注册
    client.post("/api/auth/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123"
    })
    
    # Login
    response = client.post("/api/auth/login", data={
        "username": "testuser",
        "password": "testpass123"
    })
    
    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()


def test_login_wrong_password(client):
    """Test wrong password login"""
    # 先注册
    client.post("/api/auth/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123"
    })
    
    # Login with wrong password
    response = client.post("/api/auth/login", data={
        "username": "testuser",
        "password": "wrongpass"
    })
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_current_user(client):
    """Test get current user information"""
    # 注册
    client.post("/api/auth/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123",
        "full_name": "Test User"
    })
    
    # Login to get token
    login_response = client.post("/api/auth/login", data={
        "username": "testuser",
        "password": "testpass123"
    })
    token = login_response.json()["access_token"]
    
    # Get current user information
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/auth/me", headers=headers)
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["username"] == "testuser"

