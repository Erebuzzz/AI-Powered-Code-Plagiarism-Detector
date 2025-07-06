#!/usr/bin/env python3
"""
Test API endpoints
"""
import requests
import json

def test_endpoints():
    base_url = "http://127.0.0.1:5000"
    
    print("🧪 Testing AI-Powered Code Plagiarism Detector API\n")
    
    # Test 1: Health check
    print("1. Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health")
        print(f"   ✅ Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    
    # Test 2: Supported languages
    print("2. Testing supported languages...")
    try:
        response = requests.get(f"{base_url}/api/supported-languages")
        print(f"   ✅ Status: {response.status_code}")
        data = response.json()
        print(f"   Languages supported: {len(data['languages'])}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    
    # Test 3: Basic code analysis
    print("3. Testing basic code analysis...")
    sample_code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(10))
"""
    
    try:
        payload = {
            "code": sample_code,
            "language": "python",
            "checkDatabase": True
        }
        response = requests.post(f"{base_url}/api/analyze", json=payload)
        print(f"   ✅ Status: {response.status_code}")
        data = response.json()
        print(f"   Detected language: {data.get('language', 'Unknown')}")
        print(f"   Similarity matches: {len(data.get('similarity', {}).get('matches', []))}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    
    # Test 4: Enhanced analysis with Cohere
    print("4. Testing enhanced analysis with Cohere...")
    try:
        payload = {
            "code": sample_code,
            "language": "python",
            "useCohere": True,
            "checkDatabase": True
        }
        response = requests.post(f"{base_url}/api/analyze-enhanced", json=payload)
        print(f"   ✅ Status: {response.status_code}")
        data = response.json()
        print(f"   Enhanced features enabled: {data.get('enhanced_features', {})}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    
    # Test 5: Code comparison with Cohere
    print("5. Testing code comparison with Cohere...")
    code1 = "def add(a, b): return a + b"
    code2 = "def sum_numbers(x, y): return x + y"
    
    try:
        payload = {
            "code1": code1,
            "code2": code2
        }
        response = requests.post(f"{base_url}/api/compare-with-cohere", json=payload)
        print(f"   ✅ Status: {response.status_code}")
        data = response.json()
        print(f"   Similarity: {data.get('similarity_percentage', 'Unknown')}")
        print(f"   Powered by: {data.get('powered_by', 'Unknown')}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n🎉 API testing complete!")

if __name__ == "__main__":
    test_endpoints()
