#!/usr/bin/env python3
import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_register():
    """Test user registration"""
    data = {
        "username": "testuser2",
        "password": "password123",
        "full_name": "Test User 2",
        "email": "test2@example.com",
        "description": "Test user for profile updates"
    }
    
    response = requests.post(f"{BASE_URL}/register", json=data)
    print(f"Registration Response: {response.status_code}")
    print(f"Response data: {response.json()}")
    
    if response.status_code == 200:
        return response.json()["access_token"]
    return None

def test_login(username="testuser2", password="password123"):
    """Test user login"""
    data = {
        "username": username,
        "password": password
    }
    
    response = requests.post(f"{BASE_URL}/token", data=data)
    print(f"Login Response: {response.status_code}")
    if response.status_code == 200:
        print(f"Login successful: {response.json()}")
        return response.json()["access_token"]
    else:
        print(f"Login failed: {response.json()}")
    return None

def test_get_profile(token):
    """Test getting user profile"""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/users/me", headers=headers)
    print(f"Get Profile Response: {response.status_code}")
    print(f"Profile data: {response.json()}")
    return response.json() if response.status_code == 200 else None

def test_update_profile(token):
    """Test updating user profile"""
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "full_name": "Updated Test User 2",
        "email": "updated@example.com",
        "description": "Updated description for testing profile update functionality"
    }
    
    response = requests.put(f"{BASE_URL}/users/me", headers=headers, json=data)
    print(f"Update Profile Response: {response.status_code}")
    if response.status_code == 200:
        print(f"Profile updated successfully: {response.json()}")
        return True
    else:
        print(f"Profile update failed: {response.json()}")
        return False

if __name__ == "__main__":
    print("=== Testing API functionality ===")
    
    # Test registration
    print("\n1. Testing Registration...")
    token = test_register()
    
    if not token:
        # If registration fails, try login with existing user
        print("\n2. Testing Login...")
        token = test_login()
    
    if token:
        # Test getting profile
        print("\n3. Testing Get Profile...")
        profile = test_get_profile(token)
        
        # Test updating profile
        print("\n4. Testing Update Profile...")
        update_success = test_update_profile(token)
        
        if update_success:
            print("\n5. Verifying Updated Profile...")
            updated_profile = test_get_profile(token)
    else:
        print("Could not obtain valid token. Cannot test profile operations.")
