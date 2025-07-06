import requests
import json

# Test the enhanced analysis endpoint
data = {
    "code": """def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(10))""",
    "language": "python",
    "useCohere": False  # Disable Cohere to avoid timeout
}

try:
    response = requests.post("http://localhost:5000/api/analyze-enhanced", json=data, timeout=15)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Analysis completed successfully!")
        print(f"Language detected: {result.get('language')}")
        print(f"Enhanced features: {result.get('enhanced_features')}")
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"Error: {e}")
