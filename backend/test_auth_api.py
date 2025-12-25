import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_student_registration():
    """Test student registration endpoint"""
    import random
    random_id = random.randint(1000, 9999)
    student_data = {
        "usn": f"1MS22CS{random_id}",
        "name": f"John Doe {random_id}",
        "email": f"john.doe{random_id}@example.com",
        "password": "password123",
        "father_name": "Robert Doe",
        "mother_name": "Mary Doe",
        "dob": "2000-01-01",
        "address": "123 Main St, Bangalore",
        "course": "B.Tech",
        "specialization": "Computer Science",
        "mobile_no": f"9876543{random_id}",
        "year": 2022
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register/student", json=student_data)
        print(f"Student registration: {response.status_code} - {response.json()}")
        return response.json()
    except Exception as e:
        print(f"Student registration error: {e}")
        return None

def test_faculty_registration():
    """Test faculty registration endpoint"""
    import random
    random_id = random.randint(1000, 9999)
    faculty_data = {
        "name": f"Dr. Jane Smith {random_id}",
        "email": f"jane.smith{random_id}@example.com",
        "password": "password123",
        "mobile_no": f"9876543{random_id}",
        "department": "Computer Science",
        "designation": "Professor"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register/faculty", json=faculty_data)
        print(f"Faculty registration: {response.status_code} - {response.json()}")
        return response.json()
    except Exception as e:
        print(f"Faculty registration error: {e}")
        return None

def test_login(email, password):
    """Test login endpoint"""
    login_data = {
        "username": email,
        "password": password
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
        print(f"Login: {response.status_code} - {response.json()}")
        return response.json()
    except Exception as e:
        print(f"Login error: {e}")
        return None

def test_get_current_user(token):
    """Test getting current user info"""
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
        print(f"Current user: {response.status_code} - {response.json()}")
        return response.json()
    except Exception as e:
        print(f"Current user error: {e}")
        return None

if __name__ == "__main__":
    print("Testing Authentication API endpoints...")
    
    # Test student registration
    student = test_student_registration()
    
    # Test faculty registration
    faculty = test_faculty_registration()
    
    # Test login for student
    if student:
        student_login = test_login(student["email"], "password123")
        if student_login:
            test_get_current_user(student_login["access_token"])
    
    # Test login for faculty
    if faculty:
        faculty_login = test_login(faculty["email"], "password123")
        if faculty_login:
            test_get_current_user(faculty_login["access_token"])
    
    print("Authentication API testing completed!")
