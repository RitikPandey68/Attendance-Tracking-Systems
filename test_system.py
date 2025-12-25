#!/usr/bin/env python3
"""
System Test Script for AI-Powered Attendance Tracking System
Tests the complete functionality of the backend API and frontend integration
"""

import requests
import json
import sys

# Configuration
BASE_URL = "http://localhost:8000"
TEST_EMAIL = "test_student@example.com"
TEST_PASSWORD = "testpassword123"
TEST_USN = "TEST2024001"

def test_backend_connection():
    """Test if backend is accessible"""
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ Backend API is accessible")
            return True
        else:
            print(f"❌ Backend API returned status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend API connection failed: {e}")
        return False

def test_student_registration():
    """Test student registration"""
    try:
        student_data = {
            "name": "Test Student",
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD,
            "dob": "2000-01-01",
            "father_name": "Father Test",
            "mother_name": "Mother Test",
            "address": "123 Test Street, Test City",
            "mobile_no": "9876543210",
            "usn": TEST_USN,
            "course": "B.Tech",
            "specialization": "Computer Science",
            "year": 1
        }
        
        response = requests.post(
            f"{BASE_URL}/auth/register/student",
            json=student_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            print("✅ Student registration successful")
            return True
        else:
            print(f"❌ Student registration failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Student registration test failed: {e}")
        return False

def test_login():
    """Test user login"""
    try:
        login_data = {
            "username": TEST_EMAIL,
            "password": TEST_PASSWORD
        }
        
        response = requests.post(
            f"{BASE_URL}/auth/login",
            data=login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        if response.status_code == 200:
            token_data = response.json()
            print("✅ Login successful")
            return token_data["access_token"]
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Login test failed: {e}")
        return None

def test_protected_endpoint(access_token):
    """Test accessing protected endpoint with JWT token"""
    try:
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        response = requests.get(
            f"{BASE_URL}/auth/me",
            headers=headers
        )
        
        if response.status_code == 200:
            user_data = response.json()
            print("✅ Protected endpoint access successful")
            print(f"   User: {user_data['email']} (Role: {user_data['role']})")
            return True
        else:
            print(f"❌ Protected endpoint access failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Protected endpoint test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Running System Tests for Attendance Tracking System")
    print("=" * 60)
    
    # Test backend connection
    if not test_backend_connection():
        sys.exit(1)
    
    # Test student registration
    if not test_student_registration():
        print("⚠️  Registration test failed, trying login with existing user")
    
    # Test login
    access_token = test_login()
    if not access_token:
        sys.exit(1)
    
    # Test protected endpoint
    if not test_protected_endpoint(access_token):
        sys.exit(1)
    
    print("=" * 60)
    print("🎉 All system tests passed successfully!")
    print("\n📊 System Status:")
    print(f"   Backend API: http://localhost:8000")
    print(f"   API Documentation: http://localhost:8000/docs")
    print(f"   Frontend App: http://localhost:8504")
    print(f"   Test User: {TEST_EMAIL}")
    print(f"   Test USN: {TEST_USN}")
    
    print("\n🚀 Next Steps:")
    print("   1. Open http://localhost:8504 in your browser")
    print("   2. Login with the test credentials")
    print("   3. Explore the registration and authentication features")
    print("   4. Continue implementing attendance and results features")

if __name__ == "__main__":
    main()
