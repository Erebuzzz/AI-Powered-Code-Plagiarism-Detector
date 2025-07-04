import re
import ast
from typing import List, Dict, Optional

class CodeProcessor:
    """Handles code preprocessing and normalization"""
    
    def __init__(self):
        self.language_parsers = {
            'python': self._process_python,
            'javascript': self._process_javascript,
            'java': self._process_java,
            'cpp': self._process_cpp,
            'c': self._process_c,
            'csharp': self._process_csharp
        }
    
    def preprocess_code(self, code: str, language: str) -> str:
        """Preprocess code by removing comments, normalizing whitespace, etc."""
        # Remove comments
        code = self._remove_comments(code, language)
        
        # Normalize whitespace
        code = self._normalize_whitespace(code)
        
        # Language-specific processing
        if language.lower() in self.language_parsers:
            code = self.language_parsers[language.lower()](code)
        
        return code
    
    def _remove_comments(self, code: str, language: str) -> str:
        """Remove comments based on language"""
        if language.lower() in ['python']:
            # Remove Python comments
            lines = code.split('\n')
            cleaned_lines = []
            for line in lines:
                # Remove inline comments
                if '#' in line:
                    line = line[:line.index('#')]
                cleaned_lines.append(line)
            code = '\n'.join(cleaned_lines)
        
        elif language.lower() in ['javascript', 'java', 'cpp', 'c', 'csharp']:
            # Remove single-line comments
            code = re.sub(r'//.*', '', code)
            # Remove multi-line comments
            code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
        
        return code
    
    def _normalize_whitespace(self, code: str) -> str:
        """Normalize whitespace and indentation"""
        # Remove extra whitespace
        code = re.sub(r'\s+', ' ', code)
        # Remove leading/trailing whitespace
        code = code.strip()
        return code
    
    def _process_python(self, code: str) -> str:
        """Python-specific processing"""
        try:
            # Parse the AST to extract structure
            tree = ast.parse(code)
            # This is a simplified version - in practice, you'd extract
            # function signatures, class definitions, etc.
            return code
        except SyntaxError:
            return code
    
    def _process_javascript(self, code: str) -> str:
        """JavaScript-specific processing"""
        return code
    
    def _process_java(self, code: str) -> str:
        """Java-specific processing"""
        return code
    
    def _process_cpp(self, code: str) -> str:
        """C++-specific processing"""
        return code
    
    def _process_c(self, code: str) -> str:
        """C-specific processing"""
        return code
    
    def _process_csharp(self, code: str) -> str:
        """C#-specific processing"""
        return code
    
    def extract_functions(self, code: str, language: str) -> List[Dict]:
        """Extract function definitions from code"""
        functions = []
        
        if language.lower() == 'python':
            try:
                tree = ast.parse(code)
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        functions.append({
                            'name': node.name,
                            'line_start': node.lineno,
                            'arguments': [arg.arg for arg in node.args.args]
                        })
            except SyntaxError:
                pass
        
        return functions
    
    def calculate_structural_similarity(self, code1: str, code2: str) -> float:
        """Calculate structural similarity between two code snippets"""
        # Simple token-based similarity
        tokens1 = set(re.findall(r'\w+', code1))
        tokens2 = set(re.findall(r'\w+', code2))
        
        if not tokens1 and not tokens2:
            return 1.0
        
        intersection = tokens1.intersection(tokens2)
        union = tokens1.union(tokens2)
        
        return len(intersection) / len(union) if union else 0.0
