import pytest
from fastapi import status


def test_register_user(client):
    """测试用户注册"""
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
    """测试重复用户名注册"""
    # 第一次注册
    client.post("/api/auth/register", json={
        "username": "testuser",
        "email": "test1@example.com",
        "password": "testpass123"
    })
    
    # 尝试用相同用户名注册
    response = client.post("/api/auth/register", json={
        "username": "testuser",
        "email": "test2@example.com",
        "password": "testpass123"
    })
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_login_success(client):
    """测试成功登录"""
    # 先注册
    client.post("/api/auth/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123"
    })
    
    # 登录
    response = client.post("/api/auth/login", data={
        "username": "testuser",
        "password": "testpass123"
    })
    
    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()


def test_login_wrong_password(client):
    """测试错误密码登录"""
    # 先注册
    client.post("/api/auth/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123"
    })
    
    # 用错误密码登录
    response = client.post("/api/auth/login", data={
        "username": "testuser",
        "password": "wrongpass"
    })
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_current_user(client):
    """测试获取当前用户信息"""
    # 注册
    client.post("/api/auth/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123",
        "full_name": "Test User"
    })
    
    # 登录获取 token
    login_response = client.post("/api/auth/login", data={
        "username": "testuser",
        "password": "testpass123"
    })
    token = login_response.json()["access_token"]
    
    # 获取当前用户信息
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/auth/me", headers=headers)
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["username"] == "testuser"

