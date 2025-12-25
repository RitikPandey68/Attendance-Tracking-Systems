import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_permission_edges():
    """Test edge cases for permission system"""
    print("Testing Permission Edge Cases...")
    
    # Login as student
    student_login = {
        "username": "john.doe9816@example.com",  # Correct email
        "password": "password123"  # Password
    }
    student_response = requests.post(f"{BASE_URL}/auth/login", data=student_login)
    student_token = student_response.json()["access_token"]
    student_headers = {"Authorization": f"Bearer {student_token}"}
    
    # Login as faculty
    faculty_login = {
        "username": "jane.smith6925@example.com",  # Correct faculty email
        "password": "password123"  # Password
    }
    faculty_response = requests.post(f"{BASE_URL}/auth/login", data=faculty_login)
    faculty_token = faculty_response.json()["access_token"]
    faculty_headers = {"Authorization": f"Bearer {faculty_token}"}
    
    # Test 1: Student trying to access another student's data
    print("\n1. Testing student access to other student's data...")
    other_student_id = "68ac9c320a1edb72993d3629"  # Different student ID
    response = requests.get(f"{BASE_URL}/attendance/student/{other_student_id}", headers=student_headers)
    print(f"   Student accessing other student attendance: {response.status_code} - {response.text}")
    
    response = requests.get(f"{BASE_URL}/results/student/{other_student_id}", headers=student_headers)
    print(f"   Student accessing other student results: {response.status_code} - {response.text}")
    
    # Test 2: Faculty accessing student data (should work)
    print("\n2. Testing faculty access to student data...")
    student_id = "68ac9c320a1edb72993d3628"  # Valid student ID
    response = requests.get(f"{BASE_URL}/attendance/student/{student_id}", headers=faculty_headers)
    print(f"   Faculty accessing student attendance: {response.status_code} - {len(response.json())} records")
    
    response = requests.get(f"{BASE_URL}/results/student/{student_id}", headers=faculty_headers)
    print(f"   Faculty accessing student results: {response.status_code} - {len(response.json())} records")
    
    # Test 3: Invalid student ID format
    print("\n3. Testing invalid student ID format...")
    invalid_id = "invalid_id"
    response = requests.get(f"{BASE_URL}/attendance/student/{invalid_id}", headers=student_headers)
    print(f"   Invalid student ID attendance: {response.status_code} - {response.text}")
    
    response = requests.get(f"{BASE_URL}/results/student/{invalid_id}", headers=student_headers)
    print(f"   Invalid student ID results: {response.status_code} - {response.text}")
    
    # Test 4: Non-existent student ID
    print("\n4. Testing non-existent student ID...")
    nonexistent_id = "68ac9c320a1edb72993d9999"  # Valid format but doesn't exist
    response = requests.get(f"{BASE_URL}/attendance/student/{nonexistent_id}", headers=student_headers)
    print(f"   Non-existent student attendance: {response.status_code} - {response.text}")
    
    response = requests.get(f"{BASE_URL}/results/student/{nonexistent_id}", headers=student_headers)
    print(f"   Non-existent student results: {response.status_code} - {response.text}")
    
    print("\nPermission edge case testing completed!")

def test_unauthorized_access():
    """Test unauthorized access attempts"""
    print("\nTesting Unauthorized Access...")
    
    # Test without authentication
    student_id = "68ac9c320a1edb72993d3628"
    response = requests.get(f"{BASE_URL}/attendance/student/{student_id}")
    print(f"   No auth - attendance: {response.status_code}")
    
    response = requests.get(f"{BASE_URL}/results/student/{student_id}")
    print(f"   No auth - results: {response.status_code}")
    
    # Test with invalid token
    invalid_headers = {"Authorization": "Bearer invalid_token"}
    response = requests.get(f"{BASE_URL}/attendance/student/{student_id}", headers=invalid_headers)
    print(f"   Invalid token - attendance: {response.status_code}")
    
    response = requests.get(f"{BASE_URL}/results/student/{student_id}", headers=invalid_headers)
    print(f"   Invalid token - results: {response.status_code}")
    
    print("Unauthorized access testing completed!")

if __name__ == "__main__":
    print("Starting Edge Case Testing...")
    test_permission_edges()
    test_unauthorized_access()
    print("\nAll edge case testing completed successfully!")
