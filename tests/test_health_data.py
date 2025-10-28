import pytest
from fastapi import status
from datetime import date


@pytest.fixture
def auth_headers(client):
    """创建认证用户的 headers"""
    # 注册
    client.post("/api/auth/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123"
    })
    
    # 登录
    login_response = client.post("/api/auth/login", data={
        "username": "testuser",
        "password": "testpass123"
    })
    
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_create_exercise_data(client, auth_headers):
    """测试创建运动数据"""
    response = client.post("/api/health/data", json={
        "data_type": "exercise",
        "date": str(date.today()),
        "exercise_type": "跑步",
        "duration": 30,
        "calories_burned": 300,
        "distance": 5.0,
        "intensity": "中等"
    }, headers=auth_headers)
    
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["exercise_type"] == "跑步"


def test_create_diet_data(client, auth_headers):
    """测试创建饮食数据"""
    response = client.post("/api/health/data", json={
        "data_type": "diet",
        "date": str(date.today()),
        "meal_type": "breakfast",
        "food_name": "燕麦粥",
        "calories": 200,
        "protein": 10,
        "carbs": 30,
        "fats": 5
    }, headers=auth_headers)
    
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["food_name"] == "燕麦粥"


def test_create_sleep_data(client, auth_headers):
    """测试创建睡眠数据"""
    response = client.post("/api/health/data", json={
        "data_type": "sleep",
        "date": str(date.today()),
        "sleep_duration": 7.5,
        "sleep_quality": "good"
    }, headers=auth_headers)
    
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["sleep_duration"] == 7.5


def test_get_health_data(client, auth_headers):
    """测试获取健康数据"""
    # 创建一些测试数据
    client.post("/api/health/data", json={
        "data_type": "exercise",
        "date": str(date.today()),
        "exercise_type": "跑步",
        "duration": 30
    }, headers=auth_headers)
    
    # 获取数据
    response = client.get("/api/health/data", headers=auth_headers)
    
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) > 0


def test_get_health_statistics(client, auth_headers):
    """测试获取健康统计"""
    # 创建一些测试数据
    client.post("/api/health/data", json={
        "data_type": "exercise",
        "date": str(date.today()),
        "duration": 30,
        "calories_burned": 300
    }, headers=auth_headers)
    
    response = client.get("/api/health/statistics?days=7", headers=auth_headers)
    
    assert response.status_code == status.HTTP_200_OK
    assert "total_exercise_minutes" in response.json()
    assert "total_calories_burned" in response.json()

