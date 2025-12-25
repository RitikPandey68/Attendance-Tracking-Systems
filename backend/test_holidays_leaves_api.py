import requests

BASE_URL = "http://localhost:8000"

def test_add_holiday():
    holiday_data = {
        "date": "2023-12-25",
        "name": "Christmas Day",
        "description": "Public holiday"
    }
    response = requests.post(f"{BASE_URL}/holidays/", json=holiday_data)
    assert response.status_code == 200, "Failed to add holiday"

def test_get_holidays():
    response = requests.get(f"{BASE_URL}/holidays/")
    assert response.status_code == 200, "Failed to retrieve holidays"

def test_apply_leave():
    leave_data = {
        "usn": "TEST2024001",
        "leave_type": "Sick Leave",
        "reason": "Medical appointment",
        "start_date": "2023-10-05",
        "end_date": "2023-10-06"
    }
    response = requests.post(f"{BASE_URL}/leaves/", json=leave_data)
    assert response.status_code == 200, "Failed to apply for leave"

def test_get_leaves():
    response = requests.get(f"{BASE_URL}/leaves/TEST2024001")
    assert response.status_code == 200, "Failed to retrieve leaves"

if __name__ == "__main__":
    test_add_holiday()
    test_get_holidays()
    test_apply_leave()
    test_get_leaves()
    print("All holidays and leaves tests passed!")
