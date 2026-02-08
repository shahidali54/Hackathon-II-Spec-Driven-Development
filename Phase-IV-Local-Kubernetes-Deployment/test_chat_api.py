import requests
import json

# Base URL for the API
BASE_URL = "http://localhost:8000"

def test_api_endpoints():
    print("Testing AI Chat Agent & Integration API endpoints...")

    # Test the root endpoint
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Root endpoint: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Error testing root endpoint: {e}")

    # Test the /api/chat endpoint (without auth - should return 422 or 401)
    try:
        response = requests.post(f"{BASE_URL}/api/chat", json={"message": "Test message"})
        print(f"Chat endpoint (no auth): {response.status_code}")
    except Exception as e:
        print(f"Error testing chat endpoint: {e}")

    # Test other endpoints
    try:
        response = requests.get(f"{BASE_URL}/api/conversations")
        print(f"Conversations endpoint (no auth): {response.status_code}")
    except Exception as e:
        print(f"Error testing conversations endpoint: {e}")

    print("\nTo fully test the chat functionality:")
    print("1. Register and login at http://localhost:3000")
    print("2. Navigate to the dashboard and then to the chat page")
    print("3. Try sending messages like 'Add a task: Buy groceries'")
    print("4. The AI agent should create tasks through the existing task APIs")

if __name__ == "__main__":
    test_api_endpoints()