"""Simple test to check alerts endpoint"""
import requests

BASE_URL = "http://localhost:8000"

# First, create a test user if needed
print("Testing alerts endpoint...")

# Try to get alerts without auth (should fail)
response = requests.get(f"{BASE_URL}/alerts")
print(f"GET /alerts without auth: {response.status_code}")

# Check if we can reach the server
health = requests.get(f"{BASE_URL}/health")
print(f"Health check: {health.status_code}")
if health.status_code == 200:
    print("✅ Server is running")
else:
    print("❌ Server is not responding")
