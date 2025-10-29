#!/usr/bin/env python3
"""
Test script for Health Management Platform API
"""
import requests
import json
from datetime import date, datetime

BASE_URL = "http://localhost:8000"

def print_response(title, response):
    """Print API response"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except:
        print(f"Response: {response.text}")
    print(f"{'='*60}\n")

def test_apis():
    print("Starting API Tests...")
    
    # Test 1: Health Check
    print("\n1. Testing health check endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print_response("Health Check", response)
    assert response.status_code == 200
    
    # Test 2: Root endpoint
    print("\n2. Testing root endpoint...")
    response = requests.get(f"{BASE_URL}/")
    print_response("Root Endpoint", response)
    assert response.status_code == 200
    
    # Test 3: Register user
    print("\n3. Testing user registration...")
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123",
        "full_name": "Test User",
        "date_of_birth": "1990-01-01",
        "gender": "male",
        "height": 175.0,
        "weight": 70.0,
        "activity_level": "moderately_active",
        "health_goal": "weight_loss"
    }
    response = requests.post(f"{BASE_URL}/api/auth/register", json=user_data)
    print_response("User Registration", response)
    if response.status_code == 201:
        user_id = response.json()["id"]
        print("✓ User registered successfully")
    elif response.status_code == 400 and "already exists" in response.json().get("detail", "").lower():
        print("✓ User already exists, will use login instead")
    else:
        assert False, f"Registration failed: {response.status_code}"
    
    # Test 4: Login
    print("\n4. Testing user login...")
    login_data = {
        "username": "testuser",
        "password": "testpass123"
    }
    response = requests.post(
        f"{BASE_URL}/api/auth/login",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    print_response("User Login", response)
    assert response.status_code == 200
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test 5: Get current user
    print("\n5. Testing get current user...")
    response = requests.get(f"{BASE_URL}/api/users/me", headers=headers)
    print_response("Get Current User", response)
    assert response.status_code == 200
    
    # Test 6: Submit exercise data
    print("\n6. Testing submit exercise data...")
    exercise_data = {
        "data_type": "exercise",
        "date": str(date.today()),
        "exercise_type": "Running",
        "duration": 30.0,
        "calories_burned": 300.0,
        "distance": 5.0,
        "intensity": "moderate"
    }
    response = requests.post(f"{BASE_URL}/api/health/data", json=exercise_data, headers=headers)
    print_response("Submit Exercise Data", response)
    assert response.status_code == 201
    
    # Test 7: Submit diet data
    print("\n7. Testing submit diet data...")
    diet_data = {
        "data_type": "diet",
        "date": str(date.today()),
        "meal_type": "breakfast",
        "food_name": "Oatmeal",
        "calories": 200.0,
        "protein": 10.0,
        "carbs": 30.0,
        "fats": 5.0
    }
    response = requests.post(f"{BASE_URL}/api/health/data", json=diet_data, headers=headers)
    print_response("Submit Diet Data", response)
    assert response.status_code == 201
    
    # Test 8: Submit sleep data
    print("\n8. Testing submit sleep data...")
    sleep_data = {
        "data_type": "sleep",
        "date": str(date.today()),
        "sleep_duration": 7.5,
        "sleep_quality": "good"
    }
    response = requests.post(f"{BASE_URL}/api/health/data", json=sleep_data, headers=headers)
    print_response("Submit Sleep Data", response)
    assert response.status_code == 201
    
    # Test 9: Get health data
    print("\n9. Testing get health data...")
    response = requests.get(f"{BASE_URL}/api/health/data?data_type=exercise", headers=headers)
    print_response("Get Health Data", response)
    assert response.status_code == 200
    
    # Test 10: Get health statistics
    print("\n10. Testing get health statistics...")
    response = requests.get(f"{BASE_URL}/api/health/statistics?days=7", headers=headers)
    print_response("Get Health Statistics", response)
    assert response.status_code == 200
    
    # Test 11: Generate health plan
    print("\n11. Testing generate health plan...")
    response = requests.post(f"{BASE_URL}/api/health/plan", headers=headers)
    print_response("Generate Health Plan", response)
    assert response.status_code == 201
    
    # Test 12: Get health plans
    print("\n12. Testing get health plans...")
    response = requests.get(f"{BASE_URL}/api/health/plan", headers=headers)
    print_response("Get Health Plans", response)
    assert response.status_code == 200
    
    # Test 13: Get AI recommendations
    print("\n13. Testing get AI recommendations...")
    response = requests.get(f"{BASE_URL}/api/health/recommendations", headers=headers)
    print_response("Get AI Recommendations", response)
    assert response.status_code == 200
    
    print("\n" + "="*60)
    print("ALL TESTS PASSED! ✅")
    print("="*60 + "\n")

if __name__ == "__main__":
    try:
        test_apis()
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Cannot connect to the server.")
        print("Please make sure the server is running on http://localhost:8000")
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
    except Exception as e:
        print(f"\n❌ Error: {e}")

