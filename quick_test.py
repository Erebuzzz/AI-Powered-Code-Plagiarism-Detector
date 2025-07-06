#!/usr/bin/env python3
"""
Quick integration test for the AI-Powered Code Plagiarism Detector
Tests the main API endpoints with sample code
"""

import requests
import json

# Test configuration
BASE_URL = "http://localhost:5000"
SAMPLE_CODE = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# Test the function
for i in range(10):
    print(f"F({i}) = {fibonacci(i)}")
"""

def test_health_endpoint():
    """Test the health check endpoint"""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_basic_analysis():
    """Test the basic analysis endpoint"""
    print("\n🔍 Testing basic analysis endpoint...")
    try:
        payload = {
            "code": SAMPLE_CODE,
            "language": "python",
            "checkDatabase": True
        }
        
        response = requests.post(
            f"{BASE_URL}/api/analyze",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Basic analysis successful")
            print(f"   Language detected: {data.get('analysis', {}).get('detected_language', 'Unknown')}")
            print(f"   Lines of code: {data.get('analysis', {}).get('lines_of_code', {}).get('total', 'Unknown')}")
            print(f"   Similarity matches: {len(data.get('similarity', {}).get('matches', []))}")
            print(f"   Risk level: {data.get('similarity', {}).get('risk_level', 'Unknown')}")
            return True
        else:
            print(f"❌ Basic analysis failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Basic analysis error: {e}")
        return False

def test_enhanced_analysis():
    """Test the enhanced analysis endpoint with AI"""
    print("\n🔍 Testing enhanced AI analysis endpoint...")
    try:
        payload = {
            "code": SAMPLE_CODE,
            "language": "python",
            "checkDatabase": True,
            "useCohere": True
        }
        
        response = requests.post(
            f"{BASE_URL}/api/analyze-enhanced",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Enhanced AI analysis successful")
            print(f"   Language detected: {data.get('analysis', {}).get('detected_language', 'Unknown')}")
            print(f"   AI similarity score: {data.get('similarity', {}).get('highest_similarity', 'Unknown')}")
            print(f"   Enhanced matches: {len(data.get('similarity', {}).get('matches', []))}")
            return True
        else:
            print(f"❌ Enhanced analysis failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Enhanced analysis error: {e}")
        return False

def test_supported_languages():
    """Test the supported languages endpoint"""
    print("\n🔍 Testing supported languages endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/supported-languages")
        if response.status_code == 200:
            languages = response.json()
            print("✅ Supported languages retrieved")
            print(f"   Available languages: {', '.join(languages.get('languages', []))}")
            return True
        else:
            print(f"❌ Supported languages failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Supported languages error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting AI-Powered Code Plagiarism Detector Integration Test\n")
    
    tests = [
        test_health_endpoint,
        test_supported_languages,
        test_basic_analysis,
        test_enhanced_analysis
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The system is fully operational.")
        print("\n🌐 You can now:")
        print("   • Visit http://localhost:3000 to use the web interface")
        print("   • Paste code samples to analyze for plagiarism")
        print("   • Enable 'Enhanced AI Analysis' for better results")
        print("   • Try the demo examples at http://localhost:3000/demo")
    else:
        print("⚠️  Some tests failed. Check the backend logs for details.")

if __name__ == "__main__":
    main()
