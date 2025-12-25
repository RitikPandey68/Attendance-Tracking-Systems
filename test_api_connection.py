import requests
import time

def test_api():
    max_retries = 5
    retry_delay = 2
    
    for i in range(max_retries):
        try:
            response = requests.get('http://127.0.0.1:3000/', timeout=5)
            if response.status_code == 200:
                print(f"✅ API is working! Response: {response.json()}")
                return True
            else:
                print(f"❌ API returned status code: {response.status_code}")
        except requests.exceptions.ConnectionError:
            print(f"⏳ Connection attempt {i+1}/{max_retries} failed. Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    print("❌ Failed to connect to API after multiple attempts")
    return False

if __name__ == "__main__":
    test_api()
