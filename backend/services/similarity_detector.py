import numpy as np
from typing import Dict, List, Any, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import difflib
from transformers import AutoTokenizer, AutoModel
import torch
from sentence_transformers import SentenceTransformer
import hashlib
import json
from .cohere_service import CohereService
from utils.json_utils import convert_numpy_types

class SimilarityDetector:
    """
    Detects code similarity using multiple approaches:
    1. Semantic similarity using transformer models
    2. Structural similarity using AST comparison
    3. Text-based similarity using TF-IDF
    4. Token-level similarity
    """
    
    def __init__(self, model_name: str = 'microsoft/unixcoder-base'):
        self.model_name = model_name
        self.tokenizer = None
        self.model = None
        self.sentence_model = None
        self.cohere_service = CohereService()
        self.tfidf_vectorizer = TfidfVectorizer(
            ngram_range=(1, 3),
            max_features=5000,
            stop_words=None  # Don't remove stop words for code
        )
        self.similarity_threshold = 0.7
        
        # Initialize models lazily
        self._initialize_models()
        
        # In-memory database for demo purposes
        # In production, this would be a proper database
        self.code_database = []
        self._load_sample_database()
    
    def _initialize_models(self):
        """Initialize transformer models"""
        try:
            # Use better sentence transformer for code similarity
            self.sentence_model = SentenceTransformer('all-mpnet-base-v2')
            print("Sentence transformer model loaded successfully")
        except Exception as e:
            print(f"Warning: Could not load sentence transformer model: {e}")
            try:
                # Fallback to lighter model
                self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
                print("Fallback sentence transformer model loaded")
            except Exception as e2:
                print(f"Could not load any sentence transformer model: {e2}")
                self.sentence_model = None
    
    def _load_sample_database(self):
        """Load sample code snippets for comparison"""
        sample_codes = [
            {
                'id': 1,
                'code': '''
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr
                ''',
                'language': 'python',
                'description': 'Bubble sort implementation',
                'source': 'public_algorithms'
            },
            {
                'id': 2,
                'code': '''
function fibonacci(n) {
    if (n <= 1) return n;
    return fibonacci(n - 1) + fibonacci(n - 2);
}
                ''',
                'language': 'javascript',
                'description': 'Recursive Fibonacci',
                'source': 'public_algorithms'
            },
            {
                'id': 3,
                'code': '''
def binary_search(arr, target):
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
                ''',
                'language': 'python',
                'description': 'Binary search implementation',
                'source': 'public_algorithms'
            }
        ]
        
        self.code_database.extend(sample_codes)
    
    def find_similar_code(self, code: str, language: str, check_database: bool = True) -> Dict[str, Any]:
        """
        Find similar code using multiple similarity metrics
        """
        results = {
            'matches': [],
            'highest_similarity': 0.0,
            'similarity_breakdown': {},
            'risk_level': 'low',
            'total_checked': 0
        }
        
        if not check_database or not self.code_database:
            return results
        
        # Filter database by language if specified
        candidates = self.code_database
        if language != 'auto' and language != 'unknown':
            candidates = [item for item in self.code_database if item['language'] == language]
        
        results['total_checked'] = len(candidates)
        
        for candidate in candidates:
            similarity_score = self.calculate_similarity(code, candidate['code'], language)
            
            if similarity_score > 0.3:  # Lower threshold for reporting
                match = {
                    'id': candidate['id'],
                    'similarity_score': similarity_score,
                    'code_snippet': candidate['code'][:200] + '...' if len(candidate['code']) > 200 else candidate['code'],
                    'description': candidate.get('description', 'No description'),
                    'source': candidate.get('source', 'unknown'),
                    'language': candidate['language'],
                    'similarity_breakdown': self.get_similarity_breakdown(code, candidate['code'], language)
                }
                results['matches'].append(match)
                
                if similarity_score > results['highest_similarity']:
                    results['highest_similarity'] = similarity_score
        
        # Sort matches by similarity score
        results['matches'].sort(key=lambda x: x['similarity_score'], reverse=True)
        
        # Determine risk level
        if results['highest_similarity'] >= 0.8:
            results['risk_level'] = 'high'
        elif results['highest_similarity'] >= 0.6:
            results['risk_level'] = 'medium'
        else:
            results['risk_level'] = 'low'
        
        return convert_numpy_types(results)
    
    def calculate_similarity(self, code1: str, code2: str, language: str = 'auto') -> float:
        """
        Calculate overall similarity score between two code snippets
        """
        # Normalize codes
        norm_code1 = self.normalize_for_comparison(code1)
        norm_code2 = self.normalize_for_comparison(code2)
        
        # Calculate different similarity metrics
        semantic_sim = self.semantic_similarity(norm_code1, norm_code2)
        structural_sim = self.structural_similarity(code1, code2, language)
        textual_sim = self.textual_similarity(norm_code1, norm_code2)
        token_sim = self.token_similarity(norm_code1, norm_code2)
        
        # Weighted combination of similarities
        weights = {
            'semantic': 0.4,
            'structural': 0.3,
            'textual': 0.2,
            'token': 0.1
        }
        
        overall_similarity = (
            weights['semantic'] * semantic_sim +
            weights['structural'] * structural_sim +
            weights['textual'] * textual_sim +
            weights['token'] * token_sim
        )
        
        return float(min(overall_similarity, 1.0))
    
    def semantic_similarity(self, code1: str, code2: str) -> float:
        """
        Calculate semantic similarity using transformer embeddings
        """
        if not self.sentence_model:
            return 0.0
        
        try:
            # Generate embeddings
            embeddings = self.sentence_model.encode([code1, code2])
            
            # Calculate cosine similarity
            similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
            return max(0.0, similarity)
            
        except Exception as e:
            print(f"Error in semantic similarity: {e}")
            return 0.0
    
    def structural_similarity(self, code1: str, code2: str, language: str) -> float:
        """
        Calculate structural similarity based on code patterns
        """
        # Extract structural features
        features1 = self.extract_structural_features(code1, language)
        features2 = self.extract_structural_features(code2, language)
        
        # Compare features
        similarity_scores = []
        
        # Compare function signatures
        func_sim = self.compare_lists(features1['functions'], features2['functions'])
        similarity_scores.append(func_sim)
        
        # Compare control flow patterns
        control_sim = self.compare_dicts(features1['control_flow'], features2['control_flow'])
        similarity_scores.append(control_sim)
        
        # Compare variable patterns
        var_sim = self.compare_lists(features1['variables'], features2['variables'])
        similarity_scores.append(var_sim * 0.5)  # Lower weight for variables
        
        return np.mean(similarity_scores) if similarity_scores else 0.0
    
    def textual_similarity(self, code1: str, code2: str) -> float:
        """
        Calculate textual similarity using TF-IDF
        """
        try:
            # Tokenize code into meaningful tokens
            tokens1 = self.tokenize_code(code1)
            tokens2 = self.tokenize_code(code2)
            
            if not tokens1 or not tokens2:
                return 0.0
            
            # Convert to text documents
            doc1 = ' '.join(tokens1)
            doc2 = ' '.join(tokens2)
            
            # Calculate TF-IDF similarity
            tfidf_matrix = self.tfidf_vectorizer.fit_transform([doc1, doc2])
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            
            return max(0.0, similarity)
            
        except Exception as e:
            print(f"Error in textual similarity: {e}")
            return 0.0
    
    def token_similarity(self, code1: str, code2: str) -> float:
        """
        Calculate token-level similarity using sequence matching
        """
        tokens1 = self.tokenize_code(code1)
        tokens2 = self.tokenize_code(code2)
        
        if not tokens1 or not tokens2:
            return 0.0
        
        # Use sequence matcher for token similarity
        matcher = difflib.SequenceMatcher(None, tokens1, tokens2)
        return matcher.ratio()
    
    def extract_structural_features(self, code: str, language: str) -> Dict[str, Any]:
        """
        Extract structural features from code
        """
        features = {
            'functions': [],
            'variables': [],
            'control_flow': {},
            'imports': [],
            'classes': []
        }
        
        # Extract function names
        if language == 'python':
            func_pattern = r'def\s+(\w+)\s*\('
        elif language in ['javascript', 'typescript']:
            func_pattern = r'function\s+(\w+)\s*\(|(\w+)\s*:\s*function'
        else:
            func_pattern = r'(\w+)\s*\('
        
        functions = re.findall(func_pattern, code)
        features['functions'] = [f for f in functions if isinstance(f, str) and f]
        
        # Extract control flow
        features['control_flow'] = {
            'if_count': len(re.findall(r'\bif\b', code, re.IGNORECASE)),
            'loop_count': len(re.findall(r'\b(for|while)\b', code, re.IGNORECASE)),
            'try_count': len(re.findall(r'\b(try|except|catch)\b', code, re.IGNORECASE))
        }
        
        # Extract variable assignments (simplified)
        var_pattern = r'(\w+)\s*='
        variables = re.findall(var_pattern, code)
        features['variables'] = variables
        
        return features
    
    def tokenize_code(self, code: str) -> List[str]:
        """
        Tokenize code into meaningful tokens
        """
        # Remove comments and strings for better tokenization
        cleaned_code = re.sub(r'#.*$', '', code, flags=re.MULTILINE)  # Python comments
        cleaned_code = re.sub(r'//.*$', '', cleaned_code, flags=re.MULTILINE)  # JS/Java comments
        cleaned_code = re.sub(r'/\*.*?\*/', '', cleaned_code, flags=re.DOTALL)  # Multi-line comments
        cleaned_code = re.sub(r'["\'].*?["\']', 'STRING', cleaned_code)  # String literals
        
        # Tokenize using regex
        tokens = re.findall(r'\b\w+\b|[{}();,]', cleaned_code)
        
        # Filter out common noise tokens
        noise_tokens = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        meaningful_tokens = [token.lower() for token in tokens if token.lower() not in noise_tokens and len(token) > 1]
        
        return meaningful_tokens
    
    def normalize_for_comparison(self, code: str) -> str:
        """
        Normalize code for better comparison
        """
        # Remove excessive whitespace
        normalized = re.sub(r'\s+', ' ', code)
        
        # Remove comments
        normalized = re.sub(r'#.*$', '', normalized, flags=re.MULTILINE)
        normalized = re.sub(r'//.*$', '', normalized, flags=re.MULTILINE)
        normalized = re.sub(r'/\*.*?\*/', '', normalized, flags=re.DOTALL)
        
        # Normalize brackets and parentheses
        normalized = re.sub(r'\s*([{}();\[\],])\s*', r'\1', normalized)
        
        return normalized.strip().lower()
    
    def compare_lists(self, list1: List[str], list2: List[str]) -> float:
        """
        Compare two lists and return similarity score
        """
        if not list1 and not list2:
            return 1.0
        if not list1 or not list2:
            return 0.0
        
        set1 = set(list1)
        set2 = set(list2)
        
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        
        return intersection / union if union > 0 else 0.0
    
    def compare_dicts(self, dict1: Dict, dict2: Dict) -> float:
        """
        Compare two dictionaries and return similarity score
        """
        if not dict1 and not dict2:
            return 1.0
        if not dict1 or not dict2:
            return 0.0
        
        all_keys = set(dict1.keys()).union(set(dict2.keys()))
        if not all_keys:
            return 1.0
        
        similarities = []
        for key in all_keys:
            val1 = dict1.get(key, 0)
            val2 = dict2.get(key, 0)
            
            if val1 == 0 and val2 == 0:
                similarities.append(1.0)
            elif val1 == 0 or val2 == 0:
                similarities.append(0.0)
            else:
                # Normalized similarity for numeric values
                similarity = 1.0 - abs(val1 - val2) / max(val1, val2)
                similarities.append(max(0.0, similarity))
        
        return np.mean(similarities)
    
    def get_similarity_breakdown(self, code1: str, code2: str, language: str) -> Dict[str, float]:
        """
        Get detailed breakdown of similarity scores
        """
        norm_code1 = self.normalize_for_comparison(code1)
        norm_code2 = self.normalize_for_comparison(code2)
        
        breakdown = {
            'semantic_similarity': self.semantic_similarity(norm_code1, norm_code2),
            'structural_similarity': self.structural_similarity(code1, code2, language),
            'textual_similarity': self.textual_similarity(norm_code1, norm_code2),
            'token_similarity': self.token_similarity(norm_code1, norm_code2)
        }
        
        return breakdown
    
    def detailed_comparison(self, code1: str, code2: str, language: str) -> Dict[str, Any]:
        """
        Provide detailed comparison between two code snippets
        """
        # Get similarity breakdown
        breakdown = self.get_similarity_breakdown(code1, code2, language)
        
        # Get structural comparison
        features1 = self.extract_structural_features(code1, language)
        features2 = self.extract_structural_features(code2, language)
        
        # Find common and different elements
        common_functions = set(features1['functions']).intersection(set(features2['functions']))
        different_functions = {
            'code1_only': list(set(features1['functions']) - set(features2['functions'])),
            'code2_only': list(set(features2['functions']) - set(features1['functions']))
        }
        
        # Calculate line-by-line diff
        lines1 = code1.split('\n')
        lines2 = code2.split('\n')
        diff = list(difflib.unified_diff(lines1, lines2, lineterm='', n=3))
        
        result = {
            'similarity_breakdown': breakdown,
            'overall_similarity': self.calculate_similarity(code1, code2, language),
            'structural_comparison': {
                'common_functions': list(common_functions),
                'different_functions': different_functions,
                'control_flow_comparison': {
                    'code1': features1['control_flow'],
                    'code2': features2['control_flow']
                }
            },
            'line_diff': diff[:50],  # Limit diff output
            'statistics': {
                'lines_code1': len(lines1),
                'lines_code2': len(lines2),
                'functions_code1': len(features1['functions']),
                'functions_code2': len(features2['functions'])
            }
        }
        
        return convert_numpy_types(result)
    
    def add_to_database(self, code: str, language: str, description: str = '', source: str = 'user'):
        """
        Add code snippet to the comparison database
        """
        new_entry = {
            'id': len(self.code_database) + 1,
            'code': code,
            'language': language,
            'description': description,
            'source': source,
            'hash': hashlib.md5(code.encode()).hexdigest()
        }
        
        # Check for duplicates
        for existing in self.code_database:
            if existing.get('hash') == new_entry['hash']:
                return False  # Duplicate found
        
        self.code_database.append(new_entry)
        return True
    
    def find_similar_code_with_cohere(self, code: str, language: str, check_database: bool = True) -> Dict[str, Any]:
        """
        Enhanced similarity detection using Cohere API for better semantic understanding
        """
        results = {
            'matches': [],
            'highest_similarity': 0.0,
            'similarity_breakdown': {},
            'risk_level': 'low',
            'total_checked': 0,
            'cohere_analysis': None,
            'code_intent': None
        }
        
        # Get Cohere analysis first
        if self.cohere_service.is_available():
            results['cohere_analysis'] = self.cohere_service.analyze_code_intent(code)
            results['code_intent'] = self.cohere_service.classify_code_type(code)
        
        if not check_database or not self.code_database:
            return results
        
        # Filter database by language if specified
        candidates = self.code_database
        if language != 'auto' and language != 'unknown':
            candidates = [item for item in self.code_database if item['language'] == language]
        
        results['total_checked'] = len(candidates)
        
        # Use Cohere for semantic similarity if available
        if self.cohere_service.is_available():
            db_codes = [candidate['code'] for candidate in candidates]
            cohere_matches = self.cohere_service.find_similar_code_semantic(code, db_codes, top_k=10)
            
            if cohere_matches:
                for match in cohere_matches:
                    candidate = candidates[match['index']]
                    
                    # Combine Cohere similarity with traditional methods
                    traditional_score = self.calculate_similarity(code, candidate['code'], language)
                    cohere_score = match['similarity']
                    
                    # Weighted combination (60% Cohere, 40% traditional)
                    combined_score = 0.6 * cohere_score + 0.4 * traditional_score
                    
                    if combined_score > 0.3:
                        match_result = {
                            'id': candidate['id'],
                            'similarity_score': combined_score,
                            'cohere_similarity': cohere_score,
                            'traditional_similarity': traditional_score,
                            'code_snippet': candidate['code'][:200] + '...' if len(candidate['code']) > 200 else candidate['code'],
                            'description': candidate.get('description', 'No description'),
                            'source': candidate.get('source', 'unknown'),
                            'language': candidate['language'],
                            'similarity_breakdown': self.get_similarity_breakdown(code, candidate['code'], language),
                            'enhanced_with_cohere': True
                        }
                        results['matches'].append(match_result)
                        
                        if combined_score > results['highest_similarity']:
                            results['highest_similarity'] = combined_score
        
        else:
            # Fallback to traditional method if Cohere is not available
            return self.find_similar_code(code, language, check_database)
        
        # Sort matches by similarity score
        results['matches'].sort(key=lambda x: x['similarity_score'], reverse=True)
        
        # Determine risk level based on highest similarity
        if results['highest_similarity'] > 0.85:
            results['risk_level'] = 'very_high'
        elif results['highest_similarity'] > 0.7:
            results['risk_level'] = 'high'
        elif results['highest_similarity'] > 0.5:
            results['risk_level'] = 'medium'
        else:
            results['risk_level'] = 'low'
        
        return results
    
    def get_cohere_code_analysis(self, code: str) -> Dict[str, Any]:
        """
        Get comprehensive code analysis using Cohere
        """
        if not self.cohere_service.is_available():
            return {'error': 'Cohere service not available'}
        
        analysis = {}
        
        # Get code intent analysis
        intent = self.cohere_service.analyze_code_intent(code)
        if intent:
            analysis['intent_analysis'] = intent
        
        # Get pattern detection
        patterns = self.cohere_service.detect_code_patterns(code)
        if patterns:
            analysis['pattern_analysis'] = patterns
        
        # Get code classification
        classification = self.cohere_service.classify_code_type(code)
        if classification:
            analysis['classification'] = classification
        
        return analysis
