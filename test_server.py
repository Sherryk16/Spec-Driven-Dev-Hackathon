import requests

def test_server():
    try:
        # Test the health endpoint
        response = requests.get("http://127.0.0.1:8000/health")
        print(f"Health check status: {response.status_code}")
        print(f"Response: {response.text}")
    except requests.exceptions.ConnectionError:
        print("Cannot connect to the server. Make sure it's running on http://127.0.0.1:8000")
    except Exception as e:
        print(f"Error testing server: {e}")

if __name__ == "__main__":
    test_server()