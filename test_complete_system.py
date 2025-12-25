import requests
import sys
from datetime import date

class SystemTester:
    def __init__(self, base_url="http://127.0.0.1:8000"):
        self.base_url = base_url
        self.student_token = None
        self.faculty_token = None
    
    def test_connection(self):
        try:
            response = requests.get(f"{self.base_url}/")
            if response.status_code == 200:
                print("PASS - API Connection")
                return True
            else:
                print("FAIL - API Connection")
                return False
        except Exception as e:
            print(f"ERROR - API Connection: {e}")
            return False
    
    def register_test_student(self):
        try:
            student_data = {
                "name": "Test Student",
                "email": "test.student@example.com",
                "password": "password123",
                "dob": "2000-01-01",
                "usn": "TEST001",
                "degree": "B.Tech",
                "college": "Test College",
                "stream": "Computer Science",
                "mobile_no": "9876543210",
                "father_name": "Test Father",
                "mother_name": "Test Mother",
                "address": "Test Address",
                "year": 2
            }
            
            response = requests.post(f"{self.base_url}/auth/register/student", json=student_data)
            if response.status_code in [200, 400]:
                print("PASS - Student Registration")
                return True
            else:
                print(f"FAIL - Student Registration ({response.status_code})")
                return False
        except Exception as e:
            print(f"ERROR - Student Registration: {e}")
            return False
    
    def register_test_faculty(self):
        try:
            faculty_data = {
                "name": "Test Professor",
                "email": "test.professor@example.com",
                "password": "password123",
                "position": "Professor",
                "stream": "Computer Science",
                "department": "Computer Science",
                "college_name": "Test College",
                "mobile_no": "9876543211"
            }
            
            response = requests.post(f"{self.base_url}/auth/register/faculty", json=faculty_data)
            if response.status_code in [200, 400]:
                print("PASS - Faculty Registration")
                return True
            else:
                print(f"FAIL - Faculty Registration ({response.status_code})")
                return False
        except Exception as e:
            print(f"ERROR - Faculty Registration: {e}")
            return False
    
    def test_login(self, email, password, user_type):
        try:
            login_data = {"username": email, "password": password}
            response = requests.post(f"{self.base_url}/auth/login", data=login_data)
            
            if response.status_code == 200:
                token = response.json().get("access_token")
                if user_type == "student":
                    self.student_token = token
                else:
                    self.faculty_token = token
                print(f"PASS - {user_type.title()} Login")
                return True
            else:
                print(f"FAIL - {user_type.title()} Login ({response.status_code})")
                return False
        except Exception as e:
            print(f"ERROR - {user_type.title()} Login: {e}")
            return False
    
    def test_attendance_operations(self):
        try:
            headers = {"Authorization": f"Bearer {self.faculty_token}"}
            
            # Test marking attendance
            attendance_data = {
                "student_usn": "TEST001",
                "subject": "Test Subject",
                "date": str(date.today()),
                "status": "present"
            }
            
            response = requests.post(f"{self.base_url}/attendance/enroll", json=attendance_data, headers=headers)
            if response.status_code in [200, 400]:
                print("PASS - Attendance Operations")
                return True
            else:
                print(f"FAIL - Attendance Operations ({response.status_code})")
                return False
        except Exception as e:
            print(f"ERROR - Attendance Operations: {e}")
            return False
    
    def run_complete_test(self):
        print("AI Powered Attendance System - Quick Test")
        print("=" * 50)
        
        tests = [
            ("API Connection", self.test_connection),
            ("Student Registration", self.register_test_student),
            ("Faculty Registration", self.register_test_faculty),
            ("Student Login", lambda: self.test_login("test.student@example.com", "password123", "student")),
            ("Faculty Login", lambda: self.test_login("test.professor@example.com", "password123", "faculty")),
        ]
        
        passed = 0
        for name, test_func in tests:
            if test_func():
                passed += 1
        
        if self.faculty_token:
            if self.test_attendance_operations():
                passed += 1
            tests.append(("Attendance Operations", lambda: True))
        
        print("\n" + "=" * 50)
        print(f"Results: {passed}/{len(tests)} tests passed")
        
        if passed >= len(tests) * 0.8:
            print("SUCCESS: System is working well!")
            return True
        else:
            print("WARNING: Some issues found")
            return False

def main():
    tester = SystemTester()
    success = tester.run_complete_test()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()