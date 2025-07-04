import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.ai_service import AIService

def test_calculate_similarity():
    """Test the calculate_similarity function with simple code examples"""
    ai_service = AIService()
    
    code1 = "def hello(): print('Hello')"
    code2 = "def greet(): print('Hello')"
    
    result = ai_service.calculate_similarity(code1, code2, "python", "python")
    
    assert "semantic_similarity" in result
    assert 0 <= result["semantic_similarity"] <= 1
    assert isinstance(result["is_plagiarized"], bool)
    
    # Test with identical code
    code3 = "def add(a, b): return a + b"
    result2 = ai_service.calculate_similarity(code3, code3, "python", "python")
    assert result2["semantic_similarity"] == 1.0
    
    # Test with completely different code
    code4 = "def subtract(a, b): return a - b"
    result3 = ai_service.calculate_similarity(code3, code4, "python", "python")
    assert result3["semantic_similarity"] < 1.0

def test_preprocess_code():
    """Test the preprocess_code function"""
    ai_service = AIService()
    
    # Test Python code preprocessing
    python_code = "# This is a comment\ndef hello():\n    print('Hello')  # inline comment"
    result = ai_service.preprocess_code(python_code, "python")
    assert "#" not in result
    assert "comment" not in result
    assert "hello" in result.lower()
    
    # Test JavaScript code preprocessing
    js_code = "// This is a comment\nfunction hello() {\n    console.log('Hello'); // inline comment\n}"
    result = ai_service.preprocess_code(js_code, "javascript")
    assert "//" not in result
    assert "comment" not in result
    assert "hello" in result.lower()