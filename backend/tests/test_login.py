#!/usr/bin/env python3
"""
Test login functionality directly
"""
import requests
import json

def test_login_endpoint():
    """Test the login endpoint directly"""
    url = "http://localhost:8000/login"
    
    # Test data
    login_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    print("Testing login endpoint...")
    print(f"URL: {url}")
    print(f"Data: {login_data}")
    
    try:
        response = requests.post(url, json=login_data)
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Body: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            token = data.get('access_token')
            print(f"✓ Login successful!")
            print(f"Token: {token[:50]}..." if token else "No token received")
            
            # Test the /auth/me endpoint
            if token:
                print("\nTesting /auth/me endpoint...")
                me_response = requests.get(
                    "http://localhost:8000/auth/me",
                    headers={"Authorization": f"Bearer {token}"}
                )
                print(f"Auth/me Status: {me_response.status_code}")
                print(f"Auth/me Response: {me_response.text}")
                
            return True
        else:
            print(f"✗ Login failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_register_endpoint():
    """Test user registration"""
    url = "http://localhost:8000/register"
    
    register_data = {
        "email": "test@example.com",
        "password": "testpassword123",
        "role": "community"
    }
    
    print("\nTesting register endpoint...")
    try:
        response = requests.post(url, json=register_data)
        print(f"Register Status Code: {response.status_code}")
        print(f"Register Response: {response.text}")
        
        if response.status_code in [200, 400]:  # 400 might mean user already exists
            return True
        return False
        
    except Exception as e:
        print(f"Register Error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("LOGIN ENDPOINT TEST")
    print("=" * 60)
    
    # First try to register (in case user doesn't exist)
    register_success = test_register_endpoint()
    
    # Then test login
    login_success = test_login_endpoint()
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Register: {'✓' if register_success else '✗'}")
    print(f"Login: {'✓' if login_success else '✗'}")