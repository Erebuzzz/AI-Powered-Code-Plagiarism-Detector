import ast
import re
import os
import math
from typing import Dict, List, Any, Optional
from collections import Counter
import math

class CodeAnalyzer:
    """
    Analyzes code structure, complexity, and extracts features
    """
    
    def __init__(self):
        self.supported_languages = {
            'python': ['.py'],
            'javascript': ['.js', '.jsx'],
            'typescript': ['.ts', '.tsx'],
            'java': ['.java'],
            'cpp': ['.cpp', '.cc', '.cxx'],
            'c': ['.c'],
            'csharp': ['.cs'],
            'php': ['.php'],
            'ruby': ['.rb'],
            'go': ['.go'],
            'rust': ['.rs'],
            'swift': ['.swift'],
            'kotlin': ['.kt']
        }
    
    def analyze(self, code: str, language: str = 'auto') -> Dict[str, Any]:
        """
        Comprehensive code analysis
        """
        if language == 'auto':
            language = self.detect_language(code)
        
        analysis = {
            'detected_language': language,
            'lines_of_code': self.count_lines(code),
            'complexity_metrics': self.calculate_complexity(code, language),
            'structure_analysis': self.analyze_structure(code, language),
            'patterns': self.extract_patterns(code, language),
            'normalized_code': self.normalize_code(code, language),
            'code_quality': self.analyze_code_quality(code, language)
        }
        
        return analysis
    
    def detect_language(self, code: str) -> str:
        """
        Detect programming language from code content
        """
        # Simple heuristics for language detection
        patterns = {
            'python': [
                r'def\s+\w+\s*\(',
                r'import\s+\w+',
                r'from\s+\w+\s+import',
                r'if\s+__name__\s*==\s*["\']__main__["\']'
            ],
            'javascript': [
                r'function\s+\w+\s*\(',
                r'const\s+\w+\s*=',
                r'let\s+\w+\s*=',
                r'var\s+\w+\s*=',
                r'console\.log\s*\('
            ],
            'java': [
                r'public\s+class\s+\w+',
                r'public\s+static\s+void\s+main',
                r'System\.out\.print',
                r'import\s+java\.'
            ],
            'cpp': [
                r'#include\s*<\w+>',
                r'int\s+main\s*\(',
                r'std::\w+',
                r'cout\s*<<'
            ],
            'csharp': [
                r'using\s+System',
                r'public\s+class\s+\w+',
                r'Console\.Write',
                r'namespace\s+\w+'
            ]
        }
        
        scores = {}
        for lang, lang_patterns in patterns.items():
            score = 0
            for pattern in lang_patterns:
                matches = len(re.findall(pattern, code, re.IGNORECASE))
                score += matches
            scores[lang] = score
        
        if not scores or max(scores.values()) == 0:
            return 'unknown'
        
        return max(scores, key=scores.get)
    
    def detect_language_from_filename(self, filename: str) -> str:
        """
        Detect language from file extension
        """
        ext = os.path.splitext(filename)[1].lower()
        
        for lang, extensions in self.supported_languages.items():
            if ext in extensions:
                return lang
        
        return 'unknown'
    
    def count_lines(self, code: str) -> Dict[str, int]:
        """
        Count different types of lines in code
        """
        lines = code.split('\n')
        
        total_lines = len(lines)
        blank_lines = sum(1 for line in lines if not line.strip())
        comment_lines = self.count_comment_lines(lines)
        code_lines = total_lines - blank_lines - comment_lines
        
        return {
            'total': total_lines,
            'code': code_lines,
            'comments': comment_lines,
            'blank': blank_lines
        }
    
    def count_comment_lines(self, lines: List[str]) -> int:
        """
        Count comment lines (simplified)
        """
        comment_count = 0
        in_multiline_comment = False
        
        for line in lines:
            stripped = line.strip()
            
            # Single line comments
            if stripped.startswith('#') or stripped.startswith('//'):
                comment_count += 1
            # Multi-line comments (simplified)
            elif '/*' in stripped:
                comment_count += 1
                if '*/' not in stripped:
                    in_multiline_comment = True
            elif in_multiline_comment:
                comment_count += 1
                if '*/' in stripped:
                    in_multiline_comment = False
        
        return comment_count
    
    def calculate_complexity(self, code: str, language: str) -> Dict[str, Any]:
        """
        Calculate code complexity metrics
        """
        complexity = {
            'cyclomatic_complexity': self.calculate_cyclomatic_complexity(code),
            'nesting_depth': self.calculate_max_nesting_depth(code),
            'function_count': self.count_functions(code, language),
            'class_count': self.count_classes(code, language)
        }
        
        return complexity
    
    def calculate_cyclomatic_complexity(self, code: str) -> int:
        """
        Calculate cyclomatic complexity (simplified)
        """
        # Count decision points
        decision_keywords = ['if', 'elif', 'else', 'while', 'for', 'try', 'except', 'case', 'switch']
        complexity = 1  # Base complexity
        
        for keyword in decision_keywords:
            # Simple regex to find keywords
            pattern = r'\b' + keyword + r'\b'
            matches = len(re.findall(pattern, code, re.IGNORECASE))
            complexity += matches
        
        return complexity
    
    def calculate_max_nesting_depth(self, code: str) -> int:
        """
        Calculate maximum nesting depth
        """
        lines = code.split('\n')
        max_depth = 0
        current_depth = 0
        
        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue
            
            # Count indentation
            leading_spaces = len(line) - len(line.lstrip())
            indent_level = leading_spaces // 4  # Assuming 4-space indentation
            
            # Rough approximation of nesting
            if stripped.endswith(':') or stripped.endswith('{'):
                current_depth = indent_level + 1
                max_depth = max(max_depth, current_depth)
        
        return max_depth
    
    def count_functions(self, code: str, language: str) -> int:
        """
        Count function definitions
        """
        patterns = {
            'python': r'def\s+\w+\s*\(',
            'javascript': r'function\s+\w+\s*\(',
            'java': r'(public|private|protected)?\s*(static)?\s*\w+\s+\w+\s*\(',
            'cpp': r'\w+\s+\w+\s*\([^)]*\)\s*{',
            'csharp': r'(public|private|protected)?\s*(static)?\s*\w+\s+\w+\s*\('
        }
        
        pattern = patterns.get(language, r'function\s+\w+\s*\(|def\s+\w+\s*\(')
        return len(re.findall(pattern, code, re.IGNORECASE))
    
    def count_classes(self, code: str, language: str) -> int:
        """
        Count class definitions
        """
        patterns = {
            'python': r'class\s+\w+',
            'javascript': r'class\s+\w+',
            'java': r'(public|private)?\s*class\s+\w+',
            'cpp': r'class\s+\w+',
            'csharp': r'(public|private|internal)?\s*class\s+\w+'
        }
        
        pattern = patterns.get(language, r'class\s+\w+')
        return len(re.findall(pattern, code, re.IGNORECASE))
    
    def analyze_structure(self, code: str, language: str) -> Dict[str, Any]:
        """
        Analyze code structure and patterns
        """
        structure = {
            'imports': self.extract_imports(code, language),
            'function_names': self.extract_function_names(code, language),
            'variable_names': self.extract_variable_names(code, language),
            'string_literals': self.extract_string_literals(code),
            'control_flow': self.analyze_control_flow(code)
        }
        
        return structure
    
    def extract_imports(self, code: str, language: str) -> List[str]:
        """
        Extract import statements more accurately
        """
        imports = []
        
        if language == 'python':
            # Python imports using AST
            try:
                tree = ast.parse(code)
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            imports.append(alias.name)
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            imports.append(node.module)
            except:
                # Fallback to regex
                import_patterns = [
                    r'import\s+([^\s\n,]+)',
                    r'from\s+([^\s\n]+)\s+import'
                ]
                for pattern in import_patterns:
                    matches = re.findall(pattern, code)
                    imports.extend(matches)
        elif language in ['javascript', 'typescript']:
            # JavaScript/TypeScript imports
            import_patterns = [
                r'import\s+.*?from\s+["\']([^"\']+)["\']',
                r'require\s*\(\s*["\']([^"\']+)["\']\s*\)',
                r'import\s+["\']([^"\']+)["\']'  # import 'module'
            ]
            for pattern in import_patterns:
                matches = re.findall(pattern, code)
                imports.extend(matches)
        elif language == 'java':
            pattern = r'import\s+([^\s;]+);'
            imports = re.findall(pattern, code)
        elif language in ['cpp', 'c']:
            pattern = r'#include\s*[<"]([^>"]+)[>"]'
            imports = re.findall(pattern, code)
        
        # Clean up and return unique imports
        cleaned_imports = []
        for imp in imports:
            imp = imp.strip()
            if imp and not imp.startswith('.') and len(imp) > 1:
                cleaned_imports.append(imp)
        
        return list(set(cleaned_imports))
    
    def extract_function_names(self, code: str, language: str) -> List[str]:
        """
        Extract function names using AST for Python, regex for others
        """
        functions = []
        
        if language == 'python':
            try:
                tree = ast.parse(code)
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        functions.append(node.name)
            except:
                # Fallback to regex if AST parsing fails
                pattern = r'def\s+(\w+)\s*\('
                functions = re.findall(pattern, code)
        elif language in ['javascript', 'typescript']:
            patterns = [
                r'function\s+(\w+)\s*\(',  # function name()
                r'(\w+)\s*:\s*function',   # name: function
                r'(\w+)\s*=\s*function',   # name = function
                r'(\w+)\s*=\s*\([^)]*\)\s*=>'  # arrow functions
            ]
            for pattern in patterns:
                functions.extend(re.findall(pattern, code))
        elif language == 'java':
            pattern = r'(?:public|private|protected)?\s*(?:static)?\s*\w+\s+(\w+)\s*\([^)]*\)\s*\{'
            functions = re.findall(pattern, code)
        else:
            pattern = r'(\w+)\s*\([^)]*\)\s*\{'
            functions = re.findall(pattern, code)
        
        return list(set(functions))  # Remove duplicates
    
    def extract_variable_names(self, code: str, language: str) -> List[str]:
        """
        Extract variable names using AST for Python, regex for others
        """
        variables = []
        
        if language == 'python':
            try:
                tree = ast.parse(code)
                for node in ast.walk(tree):
                    if isinstance(node, ast.Assign):
                        for target in node.targets:
                            if isinstance(target, ast.Name):
                                variables.append(target.id)
                    elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
                        variables.append(node.target.id)
            except:
                # Fallback to regex
                pattern = r'(\w+)\s*='
                variables = re.findall(pattern, code)
        elif language in ['javascript', 'typescript']:
            patterns = [
                r'(?:var|let|const)\s+(\w+)',
                r'(\w+)\s*=\s*[^=]'  # assignment
            ]
            for pattern in patterns:
                variables.extend(re.findall(pattern, code))
        else:
            pattern = r'(\w+)\s*='
            variables = re.findall(pattern, code)
        
        # Filter out common keywords and return unique variables
        keywords = {'if', 'for', 'while', 'def', 'class', 'import', 'from', 'return', 'print'}
        return list(set([var for var in variables if var not in keywords and len(var) > 1]))
    
    def extract_string_literals(self, code: str) -> List[str]:
        """
        Extract string literals more accurately
        """
        strings = []
        
        # Match different quote styles
        patterns = [
            r'"([^"\\\\]|\\\\.)*"',    # Double quotes
            r"'([^'\\\\]|\\\\.)*'",    # Single quotes
            r'`([^`\\\\]|\\\\.)*`',    # Backticks (template literals)
            r'f"([^"\\\\]|\\\\.)*"',   # f-strings
            r"f'([^'\\\\]|\\\\.)*'"    # f-strings with single quotes
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, code)
            for match in matches:
                # Extract content between quotes
                if isinstance(match, tuple):
                    content = match[0] if match[0] else match[1] if len(match) > 1 else ''
                else:
                    content = match
                if content and len(content.strip()) > 0:
                    strings.append(content)
        
        # Also get the full quoted strings for better analysis
        full_pattern = r'["\']([^"\'\\\\]|\\\\.)*["\']'
        full_matches = re.findall(full_pattern, code)
        strings.extend([s for s in full_matches if len(s.strip()) > 2])
        
        return list(set(strings[:10]))  # Return unique strings, max 10
    
    def analyze_control_flow(self, code: str) -> Dict[str, int]:
        """
        Analyze control flow constructs
        """
        constructs = {
            'if_statements': len(re.findall(r'\bif\b', code, re.IGNORECASE)),
            'loops': len(re.findall(r'\b(for|while)\b', code, re.IGNORECASE)),
            'try_catch': len(re.findall(r'\b(try|catch|except)\b', code, re.IGNORECASE)),
            'switches': len(re.findall(r'\b(switch|case)\b', code, re.IGNORECASE))
        }
        
        return constructs
    
    def extract_patterns(self, code: str, language: str) -> Dict[str, Any]:
        """
        Extract common programming patterns
        """
        patterns = {
            'design_patterns': self.detect_design_patterns(code),
            'algorithm_patterns': self.detect_algorithm_patterns(code),
            'data_structures': self.detect_data_structures(code, language)
        }
        
        return patterns
    
    def detect_design_patterns(self, code: str) -> List[str]:
        """
        Detect common design patterns (simplified)
        """
        patterns = []
        
        # Singleton pattern
        if re.search(r'class.*Singleton|__new__.*instance', code, re.IGNORECASE):
            patterns.append('Singleton')
        
        # Factory pattern
        if re.search(r'class.*Factory|def.*create.*\(', code, re.IGNORECASE):
            patterns.append('Factory')
        
        # Observer pattern
        if re.search(r'notify|observer|subscribe', code, re.IGNORECASE):
            patterns.append('Observer')
        
        return patterns
    
    def detect_algorithm_patterns(self, code: str) -> List[str]:
        """
        Detect algorithmic patterns more comprehensively
        """
        patterns = []
        
        # Recursion - look for function calling itself
        function_names = re.findall(r'def\s+(\w+)', code)
        for func_name in function_names:
            if re.search(rf'\b{func_name}\s*\(', code):
                patterns.append('Recursion')
                break
        
        # Iteration patterns
        if re.search(r'\bfor\b.*\brange\b', code):
            patterns.append('Iteration')
        
        # Mathematical sequences
        if re.search(r'fibonacci|fib', code, re.IGNORECASE):
            patterns.append('Fibonacci')
        if re.search(r'factorial', code, re.IGNORECASE):
            patterns.append('Factorial')
        
        # Sorting algorithms
        sorting_patterns = [
            ('bubble.*sort', 'Bubble Sort'),
            ('quick.*sort', 'Quick Sort'),
            ('merge.*sort', 'Merge Sort'),
            ('insertion.*sort', 'Insertion Sort'),
            ('selection.*sort', 'Selection Sort'),
            (r'sorted?\(', 'Built-in Sort')
        ]
        for pattern, name in sorting_patterns:
            if re.search(pattern, code, re.IGNORECASE):
                patterns.append(name)
        
        # Search algorithms
        if re.search(r'binary.*search', code, re.IGNORECASE):
            patterns.append('Binary Search')
        if re.search(r'linear.*search', code, re.IGNORECASE):
            patterns.append('Linear Search')
        
        # Dynamic Programming indicators
        if re.search(r'memo|dp\[|cache|@lru_cache', code, re.IGNORECASE):
            patterns.append('Dynamic Programming')
        
        # Graph algorithms
        if re.search(r'dfs|depth.*first', code, re.IGNORECASE):
            patterns.append('Depth-First Search')
        if re.search(r'bfs|breadth.*first', code, re.IGNORECASE):
            patterns.append('Breadth-First Search')
        
        return patterns
    
    def detect_data_structures(self, code: str, language: str) -> List[str]:
        """
        Detect data structure usage more comprehensively
        """
        structures = []
        
        if language == 'python':
            # Python-specific structures
            if re.search(r'\[.*\]|list\(|\.append\(|\.pop\(', code):
                structures.append('List')
            if re.search(r'\{.*:.*\}|dict\(|\.keys\(\)|\.values\(\)', code):
                structures.append('Dictionary')
            if re.search(r'set\(|\{.*\}.*add\(', code):
                structures.append('Set')
            if re.search(r'tuple\(|\(.*,.*\)', code):
                structures.append('Tuple')
            if re.search(r'deque|collections\.deque', code):
                structures.append('Deque')
        elif language in ['javascript', 'typescript']:
            if re.search(r'\[.*\]|Array\(|\.push\(|\.pop\(', code):
                structures.append('Array')
            if re.search(r'\{.*:.*\}|Object\(|new Map\(', code):
                structures.append('Object/Map')
            if re.search(r'new Set\(', code):
                structures.append('Set')
        elif language == 'java':
            if re.search(r'ArrayList|List<|Vector', code):
                structures.append('ArrayList')
            if re.search(r'HashMap|Map<', code):
                structures.append('HashMap')
            if re.search(r'HashSet|Set<', code):
                structures.append('HashSet')
        
        # Language-agnostic patterns
        if re.search(r'stack|push.*pop|LIFO', code, re.IGNORECASE):
            structures.append('Stack')
        if re.search(r'queue|enqueue|dequeue|FIFO', code, re.IGNORECASE):
            structures.append('Queue')
        if re.search(r'tree|node|left.*right|parent.*child', code, re.IGNORECASE):
            structures.append('Tree')
        if re.search(r'graph|vertex|edge|adjacency', code, re.IGNORECASE):
            structures.append('Graph')
        if re.search(r'linked.*list|next.*node', code, re.IGNORECASE):
            structures.append('Linked List')
        if re.search(r'heap|priority.*queue|heapify', code, re.IGNORECASE):
            structures.append('Heap')
        
        return structures
    
    def normalize_code(self, code: str, language: str) -> str:
        """
        Normalize code for better comparison
        """
        # Remove comments
        normalized = self.remove_comments(code, language)
        
        # Normalize whitespace
        normalized = re.sub(r'\s+', ' ', normalized)
        
        # Remove extra blank lines
        normalized = re.sub(r'\n\s*\n', '\n', normalized)
        
        # Normalize variable names (replace with placeholders)
        normalized = self.normalize_variable_names(normalized, language)
        
        return normalized.strip()
    
    def remove_comments(self, code: str, language: str) -> str:
        """
        Remove comments from code
        """
        if language == 'python':
            # Remove # comments
            code = re.sub(r'#.*$', '', code, flags=re.MULTILINE)
        elif language in ['javascript', 'java', 'cpp', 'csharp']:
            # Remove // comments
            code = re.sub(r'//.*$', '', code, flags=re.MULTILINE)
            # Remove /* */ comments
            code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
        
        return code
    
    def normalize_variable_names(self, code: str, language: str) -> str:
        """
        Replace variable names with generic placeholders
        """
        # This is a simplified version - in practice, you'd want more sophisticated AST-based normalization
        
        if language == 'python':
            # Replace variable assignments
            code = re.sub(r'(\w+)\s*=', r'VAR\1 =', code)
        
        return code
    
    def get_supported_languages(self) -> List[str]:
        """
        Get list of supported programming languages
        """
        return list(self.supported_languages.keys())
    
    def analyze_code_quality(self, code: str, language: str) -> Dict[str, Any]:
        """
        Analyze code quality metrics
        """
        quality_metrics = {
            'readability_score': self.calculate_readability_score(code),
            'maintainability_index': self.calculate_maintainability_index(code),
            'code_smells': self.detect_code_smells(code, language),
            'best_practices': self.check_best_practices(code, language)
        }
        return quality_metrics
    
    def calculate_readability_score(self, code: str) -> float:
        """
        Calculate a simple readability score based on various factors
        """
        lines = code.split('\n')
        non_empty_lines = [line for line in lines if line.strip()]
        
        if not non_empty_lines:
            return 0.0
        
        # Factors for readability
        avg_line_length = sum(len(line) for line in non_empty_lines) / len(non_empty_lines)
        comment_ratio = len([line for line in lines if line.strip().startswith('#')]) / len(non_empty_lines)
        whitespace_ratio = len([line for line in lines if not line.strip()]) / len(lines)
        
        # Score calculation (0-100)
        score = 100
        
        # Penalize very long lines
        if avg_line_length > 80:
            score -= min(20, (avg_line_length - 80) * 0.5)
        
        # Reward comments
        score += min(10, comment_ratio * 50)
        
        # Reward appropriate whitespace
        if 0.1 <= whitespace_ratio <= 0.3:
            score += 5
        
        return max(0, min(100, score))
    
    def calculate_maintainability_index(self, code: str) -> float:
        """
        Calculate maintainability index (simplified version)
        """
        lines_of_code = len([line for line in code.split('\n') if line.strip()])
        complexity = self.calculate_complexity(code, 'python').get('cyclomatic_complexity', 1)
        
        if lines_of_code == 0:
            return 0
        
        # Simplified MI calculation
        mi = 171 - 5.2 * math.log(lines_of_code) - 0.23 * complexity
        return max(0, min(100, mi))
    
    def detect_code_smells(self, code: str, language: str) -> List[str]:
        """
        Detect common code smells
        """
        smells = []
        
        # Long method (too many lines)
        if language == 'python':
            functions = re.findall(r'def\s+\w+.*?(?=def\s+\w+|$)', code, re.DOTALL)
            for func in functions:
                func_lines = len([line for line in func.split('\n') if line.strip()])
                if func_lines > 20:
                    smells.append('Long Method')
                    break
        
        # Too many parameters
        if re.search(r'def\s+\w+\([^)]{50,}\)', code):
            smells.append('Long Parameter List')
        
        # Duplicate code patterns
        lines = [line.strip() for line in code.split('\n') if line.strip()]
        if len(set(lines)) < len(lines) * 0.8:
            smells.append('Duplicate Code')
        
        # Deep nesting
        max_indentation = 0
        for line in code.split('\n'):
            if line.strip():
                indentation = len(line) - len(line.lstrip())
                max_indentation = max(max_indentation, indentation)
        
        if max_indentation > 16:  # More than 4 levels of nesting
            smells.append('Deep Nesting')
        
        # Magic numbers
        if re.search(r'\b\d{2,}\b', code) and not re.search(r'range\(', code):
            smells.append('Magic Numbers')
        
        return smells
    
    def check_best_practices(self, code: str, language: str) -> Dict[str, bool]:
        """
        Check adherence to best practices
        """
        practices = {}
        
        if language == 'python':
            # PEP 8 style checks
            practices['uses_snake_case'] = bool(re.search(r'def\s+[a-z_]+\(', code))
            practices['has_docstrings'] = bool(re.search(r'""".*?"""', code, re.DOTALL))
            practices['proper_imports'] = not bool(re.search(r'import\s+\*', code))
            practices['no_trailing_whitespace'] = not bool(re.search(r'\s+$', code, re.MULTILINE))
        
        return practices
