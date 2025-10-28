#!/usr/bin/env python3
import requests
import json

BASE_URL = "http://localhost:8000"

# Test 1: Health check
print("1. Testing /health endpoint...")
r = requests.get(f"{BASE_URL}/health")
print(f"Status: {r.status_code}")
print(f"Response: {r.json()}\n")

# Test 2: Root endpoint
print("2. Testing / endpoint...")
r = requests.get(f"{BASE_URL}/")
print(f"Status: {r.status_code}")
print(f"Response: {r.json()}\n")

# Test 3: Register user
print("3. Testing /api/auth/register...")
user_data = {
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "full_name": "Test User"
}
r = requests.post(f"{BASE_URL}/api/auth/register", json=user_data)
print(f"Status: {r.status_code}")
print(f"Response: {r.json()}\n")

# Test 4: Login
print("4. Testing /api/auth/login...")
login_data = {
    "username": "testuser",
    "password": "testpass123"
}
r = requests.post(f"{BASE_URL}/api/auth/login", data=login_data)
print(f"Status: {r.status_code}")
token = r.json()["access_token"]
print(f"Got token: {token[:20]}...\n")

# Test 5: Get current user
print("5. Testing /api/users/me...")
headers = {"Authorization": f"Bearer {token}"}
r = requests.get(f"{BASE_URL}/api/users/me", headers=headers)
print(f"Status: {r.status_code}")
print(f"User: {r.json()['username']}\n")

print("✅ All basic tests passed!")

