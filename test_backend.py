#!/usr/bin/env python3
import requests
import json

# Test the basic analysis endpoint
payload = {
    'code': '''def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

for i in range(10):
    print(f"F({i}) = {fibonacci(i)}")''',
    'language': 'python',
    'checkDatabase': True
}

try:
    response = requests.post('http://localhost:5000/api/analyze', json=payload)
    if response.status_code == 200:
        data = response.json()
        print('SUCCESS: Analysis returned')
        print(f'Language: {data.get("analysis", {}).get("detected_language", "N/A")}')
        print(f'Total Lines: {data.get("analysis", {}).get("lines_of_code", {}).get("total", "N/A")}')
        print(f'Functions: {data.get("analysis", {}).get("complexity_metrics", {}).get("function_count", "N/A")}')
        print(f'Cyclomatic Complexity: {data.get("analysis", {}).get("complexity_metrics", {}).get("cyclomatic_complexity", "N/A")}')
        print("\nFull analysis structure:")
        print(json.dumps(data.get("analysis", {}), indent=2))
    else:
        print(f'ERROR: {response.status_code} - {response.text}')
except Exception as e:
    print(f'Error: {e}')
