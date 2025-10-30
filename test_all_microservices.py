#!/usr/bin/env python3
"""
Comprehensive test script for all microservices APIs
Tests all endpoints through API Gateway (port 8000)
Updated to test new independent health data endpoints
"""
import requests
import json
import time
from datetime import date, datetime, timedelta
from typing import Optional
import sys

# Configuration
BASE_URL = "http://localhost:8000"
SERVICES = {
    "auth-service": "http://localhost:8001",
    "user-service": "http://localhost:8002",
    "health-data-service": "http://localhost:8003",
    "ai-service": "http://localhost:8004",
    "api-gateway": "http://localhost:8000"
}

# Test results
test_results = []
passed_tests = 0
failed_tests = 0

def print_test(title: str, test_num: int = None):
    """Print test header"""
    prefix = f"{test_num}. " if test_num else ""
    print(f"\n{'='*70}")
    print(f"{prefix}{title}")
    print(f"{'='*70}")

def print_response(response: requests.Response, expected_status: int = None):
    """Print API response in a formatted way"""
    status_icon = "✅" if response.status_code == expected_status else "❌"
    print(f"Status: {status_icon} {response.status_code}")
    if expected_status and response.status_code != expected_status:
        print(f"Expected: {expected_status}")
    
    try:
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2, ensure_ascii=False)}")
        return data
    except:
        print(f"Response: {response.text}")
        return None

def record_test(name: str, passed: bool, details: str = ""):
    """Record test result"""
    global passed_tests, failed_tests
    test_results.append({
        "name": name,
        "passed": passed,
        "details": details
    })
    if passed:
        passed_tests += 1
        print(f"✅ {name} - PASSED")
    else:
        failed_tests += 1
        print(f"❌ {name} - FAILED: {details}")

def test_service_health(service_name: str, url: str):
    """Test individual service health check"""
    try:
        response = requests.get(f"{url}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data.get("status") == "healthy" or "healthy" in str(data).lower()
        return False
    except:
        return False

def test_all_microservices():
    """Test all microservices APIs"""
    global passed_tests, failed_tests
    
    print("\n" + "="*70)
    print("🧪 COMPREHENSIVE MICROSERVICES API TEST SUITE")
    print("="*70)
    
    # ========================================
    # Phase 1: Service Health Checks
    # ========================================
    print_test("Phase 1: Service Health Checks")
    
    # Test API Gateway health
    print("\n1.1. Testing API Gateway Health")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        health_ok = response.status_code == 200
        print_response(response, 200)
        record_test("API Gateway Health", health_ok)
    except Exception as e:
        record_test("API Gateway Health", False, str(e))
    
    # Test individual services health
    for service_name, service_url in SERVICES.items():
        if service_name != "api-gateway":
            print(f"\n1.2. Testing {service_name} Health")
            health_ok = test_service_health(service_name, service_url)
            print(f"Status: {'✅ Healthy' if health_ok else '❌ Unhealthy'}")
            record_test(f"{service_name} Health", health_ok)
    
    # Test API Gateway root endpoint
    print("\n1.3. Testing API Gateway Root Endpoint")
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        root_ok = response.status_code == 200
        print_response(response, 200)
        record_test("API Gateway Root", root_ok)
    except Exception as e:
        record_test("API Gateway Root", False, str(e))
    
    # ========================================
    # Phase 2: Authentication Service Tests
    # ========================================
    print_test("Phase 2: Authentication Service Tests")
    
    # Generate unique user credentials
    timestamp = int(time.time())
    username = f"testuser_{timestamp}"
    email = f"test_{timestamp}@example.com"
    password = "testpass123"
    token = None
    
    # Test 2.1: User Registration
    print("\n2.1. Testing User Registration")
    try:
        register_data = {
            "username": username,
            "email": email,
            "password": password,
            "full_name": "Test User",
            "date_of_birth": "1990-01-01",
            "gender": "male",
            "height": 175.0,
            "weight": 70.0,
            "activity_level": "moderately_active",
            "health_goal": "weight_loss"
        }
        response = requests.post(
            f"{BASE_URL}/api/auth/register",
            json=register_data,
            timeout=10
        )
        register_ok = response.status_code in [200, 201]
        data = print_response(response, 201)
        if register_ok and data and "id" in data:
            user_id = data["id"]
            print(f"Registered user ID: {user_id}")
        record_test("User Registration", register_ok)
    except Exception as e:
        record_test("User Registration", False, str(e))
    
    # Test 2.2: User Login
    print("\n2.2. Testing User Login")
    try:
        login_data = {
            "username": username,
            "password": password
        }
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            data=login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=10
        )
        login_ok = response.status_code == 200
        data = print_response(response, 200)
        if login_ok and data and "access_token" in data:
            token = data["access_token"]
            print(f"Token obtained: {token[:50]}...")
        record_test("User Login", login_ok)
    except Exception as e:
        record_test("User Login", False, str(e))
        print("❌ Cannot continue without token. Exiting...")
        return
    
    # Prepare headers for authenticated requests
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test 2.3: Token Verification
    print("\n2.3. Testing Token Verification")
    try:
        response = requests.get(
            f"{BASE_URL}/api/auth/verify",
            params={"token": token},
            timeout=10
        )
        verify_ok = response.status_code == 200
        print_response(response, 200)
        record_test("Token Verification", verify_ok)
    except Exception as e:
        record_test("Token Verification", False, str(e))
    
    # ========================================
    # Phase 3: User Service Tests
    # ========================================
    print_test("Phase 3: User Service Tests")
    
    # Test 3.1: Get Current User
    print("\n3.1. Testing Get Current User")
    try:
        response = requests.get(
            f"{BASE_URL}/api/users/me",
            headers=headers,
            timeout=10
        )
        get_user_ok = response.status_code == 200
        data = print_response(response, 200)
        if data and "id" in data:
            user_id = data["id"]
            print(f"Current user ID: {user_id}")
        record_test("Get Current User", get_user_ok)
    except Exception as e:
        record_test("Get Current User", False, str(e))
    
    # Test 3.2: Update User Profile
    print("\n3.2. Testing Update User Profile")
    try:
        update_data = {
            "full_name": "Updated Test User",
            "height": 180.0,
            "weight": 72.0
        }
        response = requests.put(
            f"{BASE_URL}/api/users/me",
            json=update_data,
            headers=headers,
            timeout=10
        )
        update_ok = response.status_code == 200
        data = print_response(response, 200)
        record_test("Update User Profile", update_ok)
    except Exception as e:
        record_test("Update User Profile", False, str(e))
    
    # ========================================
    # Phase 4: Health Data Service Tests
    # ========================================
    print_test("Phase 4: Health Data Service Tests (Updated for New Structure)")
    
    health_data_ids = []
    plan_id = None
    
    # Test 4.1: Create Exercise Data (New Independent Endpoint)
    print("\n4.1. Testing Create Exercise Data (New /exercise endpoint)")
    try:
        exercise_data = {
            "exercise_type": "Running",
            "duration": 30.0,
            "calories_burned": 300.0,
            "distance": 5.0,
            "intensity": "moderate",
            "date": str(date.today())
        }
        response = requests.post(
            f"{BASE_URL}/api/health/exercise",
            json=exercise_data,
            headers=headers,
            timeout=10
        )
        create_exercise_ok = response.status_code == 201
        data = print_response(response, 201)
        if data and "id" in data:
            health_data_ids.append(data["id"])
        record_test("Create Exercise Data (New Endpoint)", create_exercise_ok)
    except Exception as e:
        record_test("Create Exercise Data (New Endpoint)", False, str(e))
    
    # Test 4.2: Create Sleep Data (New Independent Endpoint)
    print("\n4.2. Testing Create Sleep Data (New /sleep endpoint)")
    try:
        sleep_data = {
            "sleep_duration": 8.0,
            "sleep_quality": "good",
            "date": str(date.today())
        }
        response = requests.post(
            f"{BASE_URL}/api/health/sleep",
            json=sleep_data,
            headers=headers,
            timeout=10
        )
        create_sleep_ok = response.status_code == 201
        data = print_response(response, 201)
        if data and "id" in data:
            health_data_ids.append(data["id"])
        record_test("Create Sleep Data (New Endpoint)", create_sleep_ok)
    except Exception as e:
        record_test("Create Sleep Data (New Endpoint)", False, str(e))
    
    # Test 4.3: Create Diet Data (New Independent Endpoint)
    print("\n4.3. Testing Create Diet Data (New /diet endpoint)")
    try:
        diet_data = {
            "meal_type": "lunch",
            "food_name": "Salad",
            "calories": 500.0,
            "protein": 30.0,
            "carbs": 40.0,
            "fats": 20.0,
            "date": str(date.today())
        }
        response = requests.post(
            f"{BASE_URL}/api/health/diet",
            json=diet_data,
            headers=headers,
            timeout=10
        )
        create_diet_ok = response.status_code == 201
        data = print_response(response, 201)
        if data and "id" in data:
            health_data_ids.append(data["id"])
        record_test("Create Diet Data (New Endpoint)", create_diet_ok)
    except Exception as e:
        record_test("Create Diet Data (New Endpoint)", False, str(e))
    
    # Test 4.4: Test Backward Compatibility Endpoint
    print("\n4.4. Testing Backward Compatibility (/api/health/data endpoint)")
    try:
        exercise_data_old = {
            "data_type": "exercise",
            "exercise_type": "Cycling",
            "duration": 45.0,
            "calories_burned": 450.0,
            "date": str(date.today())
        }
        response = requests.post(
            f"{BASE_URL}/api/health/data",
            json=exercise_data_old,
            headers=headers,
            timeout=10
        )
        backward_compat_ok = response.status_code == 201
        data = print_response(response, 201)
        record_test("Backward Compatibility (/api/health/data)", backward_compat_ok)
    except Exception as e:
        record_test("Backward Compatibility (/api/health/data)", False, str(e))
    
    # Test 4.5: Get Exercise Data (New Independent Endpoint)
    print("\n4.5. Testing Get Exercise Data (New /exercise endpoint)")
    try:
        response = requests.get(
            f"{BASE_URL}/api/health/exercise",
            headers=headers,
            timeout=10
        )
        get_exercise_ok = response.status_code == 200
        data = print_response(response, 200)
        if isinstance(data, list):
            print(f"Retrieved {len(data)} exercise records")
        record_test("Get Exercise Data (New Endpoint)", get_exercise_ok)
    except Exception as e:
        record_test("Get Exercise Data (New Endpoint)", False, str(e))
    
    # Test 4.6: Get Diet Data (New Independent Endpoint)
    print("\n4.6. Testing Get Diet Data (New /diet endpoint)")
    try:
        response = requests.get(
            f"{BASE_URL}/api/health/diet",
            headers=headers,
            timeout=10
        )
        get_diet_ok = response.status_code == 200
        data = print_response(response, 200)
        if isinstance(data, list):
            print(f"Retrieved {len(data)} diet records")
        record_test("Get Diet Data (New Endpoint)", get_diet_ok)
    except Exception as e:
        record_test("Get Diet Data (New Endpoint)", False, str(e))
    
    # Test 4.7: Get Sleep Data (New Independent Endpoint)
    print("\n4.7. Testing Get Sleep Data (New /sleep endpoint)")
    try:
        response = requests.get(
            f"{BASE_URL}/api/health/sleep",
            headers=headers,
            timeout=10
        )
        get_sleep_ok = response.status_code == 200
        data = print_response(response, 200)
        if isinstance(data, list):
            print(f"Retrieved {len(data)} sleep records")
        record_test("Get Sleep Data (New Endpoint)", get_sleep_ok)
    except Exception as e:
        record_test("Get Sleep Data (New Endpoint)", False, str(e))
    
    # Test 4.8: Get All Health Data (Unified Endpoint - Backward Compatibility)
    print("\n4.8. Testing Get All Health Data (Unified /data endpoint)")
    try:
        response = requests.get(
            f"{BASE_URL}/api/health/data",
            headers=headers,
            timeout=10
        )
        get_all_ok = response.status_code == 200
        data = print_response(response, 200)
        if isinstance(data, list):
            print(f"Retrieved {len(data)} total health data records")
            # Count by type
            type_counts = {}
            for item in data:
                item_type = item.get("data_type", "unknown")
                type_counts[item_type] = type_counts.get(item_type, 0) + 1
            for item_type, count in type_counts.items():
                print(f"  - {item_type}: {count} records")
        record_test("Get All Health Data (Unified)", get_all_ok)
    except Exception as e:
        record_test("Get All Health Data (Unified)", False, str(e))
    
    # Test 4.9: Get Health Data with Filter (Backward Compatibility)
    print("\n4.9. Testing Get Health Data (Filtered by Type - Unified Endpoint)")
    try:
        response = requests.get(
            f"{BASE_URL}/api/health/data",
            params={"data_type": "exercise"},
            headers=headers,
            timeout=10
        )
        get_filtered_ok = response.status_code == 200
        data = print_response(response, 200)
        if isinstance(data, list):
            print(f"Retrieved {len(data)} filtered records")
        record_test("Get Health Data (Filtered by Type)", get_filtered_ok)
    except Exception as e:
        record_test("Get Health Data (Filtered by Type)", False, str(e))
    
    # Test 4.10: Get Health Statistics
    print("\n4.10. Testing Get Health Statistics")
    try:
        response = requests.get(
            f"{BASE_URL}/api/health/statistics",
            params={"days": 7},
            headers=headers,
            timeout=10
        )
        stats_ok = response.status_code == 200
        data = print_response(response, 200)
        if data and "total_exercise_minutes" in data:
            print("✅ Statistics fields present")
        record_test("Get Health Statistics", stats_ok)
    except Exception as e:
        record_test("Get Health Statistics", False, str(e))
    
    # Test 4.11: Create Health Plan
    print("\n4.11. Testing Create Health Plan")
    try:
        plan_data = {
            "plan_type": "weight_loss",
            "title": "Test Health Plan",
            "description": "A test health plan",
            "duration_days": 30,
            "calories_target": 2000.0,
            "exercise_minutes_per_day": 30.0,
            "weekly_exercise_days": 5
        }
        response = requests.post(
            f"{BASE_URL}/api/health/plan",
            json=plan_data,
            headers=headers,
            timeout=10
        )
        create_plan_ok = response.status_code == 201
        data = print_response(response, 201)
        if data and "id" in data:
            plan_id = data["id"]
            print(f"Created plan ID: {plan_id}")
        record_test("Create Health Plan", create_plan_ok)
    except Exception as e:
        record_test("Create Health Plan", False, str(e))
    
    # Test 4.12: Get Health Plans
    print("\n4.12. Testing Get Health Plans")
    try:
        response = requests.get(
            f"{BASE_URL}/api/health/plan",
            headers=headers,
            timeout=10
        )
        get_plans_ok = response.status_code == 200
        data = print_response(response, 200)
        if isinstance(data, list):
            print(f"Retrieved {len(data)} health plans")
        record_test("Get Health Plans", get_plans_ok)
    except Exception as e:
        record_test("Get Health Plans", False, str(e))
    
    # Test 4.13: Get Specific Health Plan (if plan was created)
    if plan_id:
        print(f"\n4.13. Testing Get Specific Health Plan (ID: {plan_id})")
        try:
            response = requests.get(
                f"{BASE_URL}/api/health/plan/{plan_id}",
                headers=headers,
                timeout=10
            )
            get_plan_ok = response.status_code == 200
            print_response(response, 200)
            record_test("Get Specific Health Plan", get_plan_ok)
        except Exception as e:
            record_test("Get Specific Health Plan", False, str(e))
    
    # Test 4.14: Update Health Plan (if plan was created)
    if plan_id:
        print(f"\n4.14. Testing Update Health Plan (ID: {plan_id})")
        try:
            update_plan_data = {
                "status": "active",
                "title": "Updated Test Health Plan"
            }
            response = requests.put(
                f"{BASE_URL}/api/health/plan/{plan_id}",
                json=update_plan_data,
                headers=headers,
                timeout=10
            )
            update_plan_ok = response.status_code == 200
            print_response(response, 200)
            record_test("Update Health Plan", update_plan_ok)
        except Exception as e:
            record_test("Update Health Plan", False, str(e))
    
    # ========================================
    # Phase 5: AI Service Tests
    # ========================================
    print_test("Phase 5: AI Service Tests")
    
    # Test 5.1: AI Analyze Health Data
    print("\n5.1. Testing AI Analyze Health Data")
    try:
        response = requests.get(
            f"{BASE_URL}/api/ai/analyze",
            headers=headers,
            timeout=30  # AI analysis may take longer
        )
        analyze_ok = response.status_code == 200
        data = print_response(response, 200)
        if data and "analysis" in data and "recommendations" in data:
            print("✅ Analysis and recommendations present")
        record_test("AI Analyze Health Data", analyze_ok)
    except Exception as e:
        record_test("AI Analyze Health Data", False, str(e))
    
    # Test 5.2: Generate AI Health Plan
    print("\n5.2. Testing Generate AI Health Plan")
    try:
        response = requests.post(
            f"{BASE_URL}/api/ai/plan/generate",
            headers=headers,
            timeout=60  # AI plan generation may take longer
        )
        generate_plan_ok = response.status_code == 200
        data = print_response(response, 200)
        if data and ("plan_type" in data or "title" in data):
            print("✅ AI-generated plan data present")
        record_test("Generate AI Health Plan", generate_plan_ok)
    except Exception as e:
        record_test("Generate AI Health Plan", False, str(e))
    
    # ========================================
    # Final Summary
    # ========================================
    print_test("Test Summary")
    
    print(f"\nTotal Tests: {len(test_results)}")
    print(f"✅ Passed: {passed_tests}")
    print(f"❌ Failed: {failed_tests}")
    print(f"Success Rate: {(passed_tests/len(test_results)*100):.1f}%")
    
    print("\nDetailed Results:")
    for i, result in enumerate(test_results, 1):
        status = "✅" if result["passed"] else "❌"
        print(f"{i}. {status} {result['name']}")
        if not result["passed"] and result["details"]:
            print(f"   Error: {result['details']}")
    
    if failed_tests == 0:
        print("\n" + "="*70)
        print("🎉 ALL TESTS PASSED!")
        print("="*70 + "\n")
        return 0
    else:
        print("\n" + "="*70)
        print(f"⚠️  {failed_tests} TEST(S) FAILED")
        print("="*70 + "\n")
        return 1

if __name__ == "__main__":
    try:
        exit_code = test_all_microservices()
        sys.exit(exit_code)
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Cannot connect to the API Gateway.")
        print(f"Please make sure the services are running on {BASE_URL}")
        print("\nStart services with:")
        print("  docker-compose -f docker-compose.microservices.yml up -d")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
