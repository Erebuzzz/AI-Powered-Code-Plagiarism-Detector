#!/usr/bin/env python3
import requests
import json

# Test with a more complex code sample to show all analysis features
complex_code = '''
import os
import sys
from typing import List, Dict

class DataProcessor:
    """A class for processing data with various algorithms."""
    
    def __init__(self, data_source: str):
        self.data_source = data_source
        self.cache = {}
        self.results = []
    
    def bubble_sort(self, arr: List[int]) -> List[int]:
        """Bubble sort implementation."""
        n = len(arr)
        for i in range(n):
            for j in range(0, n-i-1):
                if arr[j] > arr[j+1]:
                    arr[j], arr[j+1] = arr[j+1], arr[j]
        return arr
    
    def binary_search(self, arr: List[int], target: int) -> int:
        """Binary search implementation."""
        left, right = 0, len(arr) - 1
        
        while left <= right:
            mid = (left + right) // 2
            if arr[mid] == target:
                return mid
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        
        return -1
    
    def process_data(self, data: Dict[str, any]) -> Dict[str, any]:
        """Process data with error handling."""
        try:
            if not data:
                raise ValueError("Data cannot be empty")
            
            processed = {}
            for key, value in data.items():
                if isinstance(value, list):
                    processed[key] = self.bubble_sort(value.copy())
                else:
                    processed[key] = value
            
            return processed
        except Exception as e:
            print(f"Error processing data: {e}")
            return {}

# Usage example
if __name__ == "__main__":
    processor = DataProcessor("example.csv")
    sample_data = {
        "numbers": [64, 34, 25, 12, 22, 11, 90],
        "name": "test_dataset"
    }
    result = processor.process_data(sample_data)
    print("Processed data:", result)
'''

# Test the enhanced analysis endpoint
payload = {
    'code': complex_code,
    'language': 'python',
    'checkDatabase': True
}

try:
    response = requests.post('http://localhost:5000/api/analyze', json=payload)
    if response.status_code == 200:
        data = response.json()
        print('✅ SUCCESS: Enhanced Analysis returned')
        print('=' * 60)
        
        analysis = data.get("analysis", {})
        
        print(f'🔍 Language: {analysis.get("detected_language", "N/A")}')
        print(f'📊 Total Lines: {analysis.get("lines_of_code", {}).get("total", "N/A")}')
        print(f'⚙️ Functions: {analysis.get("complexity_metrics", {}).get("function_count", "N/A")}')
        print(f'🧮 Cyclomatic Complexity: {analysis.get("complexity_metrics", {}).get("cyclomatic_complexity", "N/A")}')
        
        # Structure Analysis
        structure = analysis.get("structure_analysis", {})
        print(f'\n🏗️ STRUCTURE ANALYSIS:')
        print(f'  Functions: {structure.get("function_names", [])}')
        print(f'  Imports: {structure.get("imports", [])}')
        print(f'  Variables: {structure.get("variable_names", [])}')
        control_flow = structure.get("control_flow", {})
        print(f'  Control Flow: {control_flow.get("if_statements", 0)} ifs, {control_flow.get("loops", 0)} loops, {control_flow.get("try_catch", 0)} try/catch')
        
        # Pattern Analysis
        patterns = analysis.get("patterns", {})
        print(f'\n🧩 PATTERNS:')
        print(f'  Algorithm Patterns: {patterns.get("algorithm_patterns", [])}')
        print(f'  Data Structures: {patterns.get("data_structures", [])}')
        print(f'  Design Patterns: {patterns.get("design_patterns", [])}')
        
        # Code Quality
        quality = analysis.get("code_quality", {})
        print(f'\n📈 CODE QUALITY:')
        print(f'  Readability Score: {quality.get("readability_score", "N/A"):.1f}%')
        print(f'  Maintainability Index: {quality.get("maintainability_index", "N/A"):.1f}')
        print(f'  Code Smells: {quality.get("code_smells", [])}')
        print(f'  Best Practices: {quality.get("best_practices", {})}')
        
        print(f'\n🔍 SIMILARITY:')
        similarity = data.get("similarity", {})
        print(f'  Risk Level: {similarity.get("risk_level", "N/A")}')
        print(f'  Matches Found: {len(similarity.get("matches", []))}')
        print(f'  Highest Similarity: {similarity.get("highest_similarity", 0) * 100:.1f}%')
        
    else:
        print(f'❌ ERROR: {response.status_code} - {response.text}')
except Exception as e:
    print(f'❌ Error: {e}')
