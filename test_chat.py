import requests
import json

def test_chat():
    try:
        # Test the chat endpoint
        response = requests.post(
            "http://127.0.0.1:8000/chat/",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"query": "What is robotics?"})
        )
        print(f"Chat endpoint status: {response.status_code}")
        print(f"Response: {response.text}")
    except requests.exceptions.ConnectionError:
        print("Cannot connect to the server. Make sure it's running on http://127.0.0.1:8000")
    except Exception as e:
        print(f"Error testing chat: {e}")

if __name__ == "__main__":
    test_chat()