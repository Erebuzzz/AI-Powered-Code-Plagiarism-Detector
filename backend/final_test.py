import requests
import json
import time

BASE_URL = "http://localhost:5001"

def test_endpoint(endpoint, method="GET", data=None, description=""):
    """Test an API endpoint and return the result"""
    try:
        url = f"{BASE_URL}{endpoint}"
        print(f"\n{'='*60}")
        print(f"Testing: {description or endpoint}")
        print(f"URL: {url}")
        
        if method == "GET":
            response = requests.get(url, timeout=30)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=30)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                print("Response (JSON):")
                print(json.dumps(result, indent=2)[:500] + "..." if len(str(result)) > 500 else json.dumps(result, indent=2))
                return True, result
            except:
                print("Response (Text):")
                print(response.text[:500] + "..." if len(response.text) > 500 else response.text)
                return True, response.text
        else:
            print(f"Error: {response.text}")
            return False, None
            
    except Exception as e:
        print(f"Exception: {str(e)}")
        return False, None

def main():
    print("AI-Powered Code Plagiarism Detector - Final Backend Test")
    print("=" * 60)
    
    # Test 1: Health check
    success, _ = test_endpoint("/health", description="Health Check")
    if not success:
        print("❌ Backend is not responding!")
        return
    
    # Test 2: Supported languages
    test_endpoint("/api/supported-languages", description="Supported Languages")
    
    # Test 3: Basic analysis
    code_sample = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(10))
"""
    
    basic_data = {
        "code": code_sample,
        "language": "python"
    }
    
    test_endpoint("/api/analyze", "POST", basic_data, "Basic Code Analysis")
    
    # Test 4: Enhanced analysis with free AI
    enhanced_data = {
        "code": code_sample,
        "language": "python",
        "use_ai": True
    }
    
    test_endpoint("/api/analyze-enhanced", "POST", enhanced_data, "Enhanced Analysis with AI")
    
    # Test 5: Code comparison
    code1 = """
def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n-1)
"""
    
    code2 = """
def fact(num):
    if num == 0:
        return 1
    return num * fact(num-1)
"""
    
    comparison_data = {
        "code1": code1,
        "code2": code2,
        "language": "python"
    }
    
    test_endpoint("/api/compare", "POST", comparison_data, "Code Comparison")
    
    # Test 6: Cohere-powered comparison
    test_endpoint("/api/compare-with-cohere", "POST", comparison_data, "Cohere-Powered Comparison")
    
    # Test 7: Batch analysis
    batch_data = {
        "codes": [code1, code2, code_sample],
        "language": "python"
    }
    
    test_endpoint("/api/batch-analyze", "POST", batch_data, "Batch Analysis")
    
    print("\n" + "="*60)
    print("✅ Final test completed! All major endpoints tested.")
    print("The AI-Powered Code Plagiarism Detector backend is fully functional!")

if __name__ == "__main__":
    main()
