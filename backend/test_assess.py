import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_assess_mood():
    email = "test_assess_bug_123@example.com"
    password = "password123"
    
    # 0. Register first to ensure user exists
    reg_payload = {"name": "Test Assess", "email": email, "password": password}
    try:
        requests.post(f"{BASE_URL}/register", json=reg_payload)
    except:
        pass

    # 1. Login to get token
    login_payload = {"email": email, "password": password}
    try:
        login_res = requests.post(f"{BASE_URL}/login", json=login_payload)
        login_res.raise_for_status()
        token = login_res.json()["token"]
    except Exception as e:
        print(f"Login failed: {e}")
        return

    # 2. Submit quiz
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    quiz_payload = {
        "answers": [
            {"question_id": "q1", "value": "high"},
            {"question_id": "q2", "value": "great"},
            {"question_id": "q3", "value": "calm"},
            {"question_id": "q4", "value": "happy"},
            {"question_id": "q5", "value": "laser"},
            {"question_id": "q6", "value": "high"},
            {"question_id": "q7", "value": "productive"}
        ]
    }
    
    print("Submitting quiz...")
    try:
        res = requests.post(f"{BASE_URL}/assess-mood", headers=headers, json=quiz_payload)
        print(f"Status: {res.status_code}")
        if res.status_code != 200:
            print(f"Error: {res.text}")
        else:
            print("Success!")
            print(json.dumps(res.json(), indent=2))
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    test_assess_mood()
