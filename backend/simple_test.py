import requests
import time

print("Waiting for server to be ready...")
time.sleep(3)

print("Testing health endpoint...")
try:
    response = requests.get("http://127.0.0.1:5001/health", timeout=5)
    print(f"Status: {response.status_code}")
    print(f"Headers: {dict(response.headers)}")
    print(f"Content: {response.text}")
except requests.exceptions.RequestException as e:
    print(f"Request error: {e}")
except Exception as e:
    print(f"Other error: {e}")
