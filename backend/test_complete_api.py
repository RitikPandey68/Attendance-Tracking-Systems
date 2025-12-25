import requests
import json
import random
from datetime import date, datetime

BASE_URL = "http://127.0.0.1:8000"

def get_auth_token(email, password):
    """Get authentication token"""
    login_data = {
        "username": email,
        "password": password
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
        if response.status_code == 200:
            return response.json()["access_token"]
    except Exception as e:
        print(f"Login error: {e}")
    return None

def test_attendance_endpoints():
    """Test attendance endpoints"""
    print("\nTesting Attendance Endpoints...")
    
    # Get faculty token
    faculty_token = get_auth_token("jane.smith6925@example.com", "password123")
    if not faculty_token:
        print("Failed to get faculty token")
        return
    
    headers = {"Authorization": f"Bearer {faculty_token}"}
    
    # Test enrolling attendance
    attendance_data = {
        "student_id": "68ac9c320a1edb72993d3628",  # Correct student ID from database
        "date": str(date.today()),
        "period": 2,  # Changed period to avoid conflict with previous test
        "status": "present",
        "subject": "Mathematics",
        "semester": 3
    }
    
    try:
        response = requests.post(f"{BASE_URL}/attendance/enroll", json=attendance_data, headers=headers)
        print(f"Enroll attendance: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Enroll attendance error: {e}")

def test_results_endpoints():
    """Test results endpoints"""
    print("\nTesting Results Endpoints...")
    
    # Get faculty token
    faculty_token = get_auth_token("jane.smith6925@example.com", "password123")
    if not faculty_token:
        print("Failed to get faculty token")
        return
    
    headers = {"Authorization": f"Bearer {faculty_token}"}
    
    # Test creating result
    result_data = {
        "student_id": "68ac9c320a1edb72993d3628",  # Correct student ID from database
        "test_type": "semester_exam",  # Change to a valid test type
        "subject": "Mathematics",
        "test_date": str(date.today()),
        "marks_obtained": 85,
        "total_marks": 100,
        "semester": 3
    }
    
    try:
        response = requests.post(f"{BASE_URL}/results/create", json=result_data, headers=headers)
        print(f"Create result: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Create result error: {e}")

def test_student_dashboard():
    """Test student dashboard endpoints"""
    print("\nTesting Student Dashboard Endpoints...")
    
    # Get student token
    student_token = get_auth_token("john.doe9816@example.com", "password123")
    if not student_token:
        print("Failed to get student token")
        return
    
    headers = {"Authorization": f"Bearer {student_token}"}
    
    # Test getting student attendance
    try:
        response = requests.get(f"{BASE_URL}/attendance/student/68ac9c320a1edb72993d3628", headers=headers)
        print(f"Get student attendance: {response.status_code} - {len(response.json())} records")
    except Exception as e:
        print(f"Get student attendance error: {e}")
    
    # Test getting student results
    try:
        response = requests.get(f"{BASE_URL}/results/student/68ac9c320a1edb72993d3628", headers=headers)
        print(f"Get student results: {response.status_code} - {len(response.json())} records")
    except Exception as e:
        print(f"Get student results error: {e}")

if __name__ == "__main__":
    print("Testing Complete API Functionality...")
    
    test_attendance_endpoints()
    test_results_endpoints()
    test_student_dashboard()
    
    print("\nComplete API testing completed!")
