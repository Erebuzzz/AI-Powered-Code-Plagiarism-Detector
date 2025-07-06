import requests
import json

# Test the compare endpoint
data = {
    "code1": "def test():\n    print('hello')",
    "code2": "def test():\n    print('world')", 
    "language": "python"
}

try:
    response = requests.post("http://localhost:5000/api/compare", json=data, timeout=10)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
