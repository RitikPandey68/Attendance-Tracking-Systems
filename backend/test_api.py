import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_root_endpoint():
    """Test the root endpoint"""
    response = requests.get(f"{BASE_URL}/")
    print(f"Root endpoint: {response.status_code} - {response.json()}")

def test_auth_endpoints():
    """Test authentication endpoints"""
    # Test if auth endpoints are accessible
    try:
        response = requests.get(f"{BASE_URL}/auth/")
        print(f"Auth endpoint: {response.status_code}")
    except Exception as e:
        print(f"Auth endpoint error: {e}")

def test_attendance_endpoints():
    """Test attendance endpoints"""
    try:
        response = requests.get(f"{BASE_URL}/attendance/")
        print(f"Attendance endpoint: {response.status_code}")
    except Exception as e:
        print(f"Attendance endpoint error: {e}")

def test_results_endpoints():
    """Test results endpoints"""
    try:
        response = requests.get(f"{BASE_URL}/results/")
        print(f"Results endpoint: {response.status_code}")
    except Exception as e:
        print(f"Results endpoint error: {e}")

if __name__ == "__main__":
    print("Testing API endpoints...")
    test_root_endpoint()
    test_auth_endpoints()
    test_attendance_endpoints()
    test_results_endpoints()
    print("API testing completed!")
