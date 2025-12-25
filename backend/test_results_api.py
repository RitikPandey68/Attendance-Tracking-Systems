import requests

BASE_URL = "http://localhost:8000/results"

def test_add_result():
    result_data = {
        "usn": "TEST2024001",
        "test_date": "2023-10-01",
        "subject": "Mathematics",
        "marks": 85,
        "max_marks": 100,
        "test_type": "Class Test"
    }
    response = requests.post(f"{BASE_URL}/", json=result_data)
    assert response.status_code == 200, "Failed to add result"

def test_get_results():
    response = requests.get(f"{BASE_URL}/TEST2024001")
    assert response.status_code == 200, "Failed to retrieve results"

def test_get_semester_results():
    response = requests.get(f"{BASE_URL}/semester/TEST2024001/1")
    assert response.status_code == 200, "Failed to retrieve semester results"

if __name__ == "__main__":
    test_add_result()
    test_get_results()
    test_get_semester_results()
    print("All results tests passed!")
