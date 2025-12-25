import requests

BASE_URL = "http://localhost:8000/attendance"

def test_mark_attendance():
    attendance_data = {
        "usn": "TEST2024001",
        "date": "2023-10-01",
        "period": "1"
    }
    response = requests.post(f"{BASE_URL}/", json=attendance_data)
    assert response.status_code == 200, "Failed to mark attendance"

def test_get_attendance():
    response = requests.get(f"{BASE_URL}/TEST2024001")
    assert response.status_code == 200, "Failed to retrieve attendance records"

def test_get_attendance_report():
    response = requests.get(f"{BASE_URL}/report/TEST2024001")
    assert response.status_code == 200, "Failed to generate attendance report"

if __name__ == "__main__":
    test_mark_attendance()
    test_get_attendance()
    test_get_attendance_report()
    print("All attendance tests passed!")
