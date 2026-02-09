import requests
import json

# Test the API endpoints
BASE_URL = "http://127.0.0.1:8001"

def test_register():
    print("Testing registration...")
    response = requests.post(
        f"{BASE_URL}/api/auth/register",
        headers={"Content-Type": "application/json"},
        json={"email": "testuser3@example.com", "password": "pass123"}
    )
    print(f"Register status: {response.status_code}")
    print(f"Register response: {response.text}")
    return response

def test_login():
    print("\nTesting login...")
    response = requests.post(
        f"{BASE_URL}/api/auth/login?email=testuser3@example.com&password=pass123",
        headers={"Content-Type": "application/json"}
    )
    print(f"Login status: {response.status_code}")
    print(f"Login response: {response.text}")
    return response

if __name__ == "__main__":
    # Test registration
    reg_resp = test_register()

    # Test login if registration was successful
    if reg_resp.status_code == 200:
        login_resp = test_login()
    else:
        print(f"\nRegistration failed with status {reg_resp.status_code}")