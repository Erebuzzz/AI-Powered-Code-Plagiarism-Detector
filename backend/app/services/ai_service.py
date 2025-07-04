import numpy as np
from typing import List, Dict, Any
import hashlib
import re
from app.core.config import settings

class AIService:
    def __init__(self):
        # For now, we'll use basic similarity without external APIs
        self.use_basic_similarity = True
        
    def preprocess_code(self, code: str, language: str) -> str:
        """Clean and normalize code for comparison"""
        if not code:
            return ""
            
        # Remove comments
        if language == "python":
            code = re.sub(r'#.*', '', code)
            code = re.sub(r'""".*?"""', '', code, flags=re.DOTALL)
            code = re.sub(r"'''.*?'''", '', code, flags=re.DOTALL)
        elif language in ["java", "cpp", "c", "javascript", "csharp"]:
            code = re.sub(r'//.*', '', code)
            code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
        
        # Remove extra whitespace
        code = re.sub(r'\s+', ' ', code)
        code = code.strip()
        
        return code

    def calculate_similarity(self, code1: str, code2: str, language1: str, language2: str) -> Dict[str, Any]:
        """Calculate similarity between two code snippets"""
        try:
            # Preprocess code
            clean_code1 = self.preprocess_code(code1, language1)
            clean_code2 = self.preprocess_code(code2, language2)
            
            if not clean_code1 or not clean_code2:
                return {
                    "semantic_similarity": 0.0,
                    "lexical_similarity": 0.0,
                    "is_plagiarized": False,
                    "confidence": 0.0,
                    "analysis": {
                        "code1_tokens": 0,
                        "code2_tokens": 0,
                        "common_tokens": 0,
                        "language1": language1,
                        "language2": language2
                    }
                }
            
            # Calculate lexical similarity (simple token overlap)
            tokens1 = set(clean_code1.lower().split())
            tokens2 = set(clean_code2.lower().split())
            
            if not tokens1 and not tokens2:
                lexical_similarity = 1.0
            elif not tokens1 or not tokens2:
                lexical_similarity = 0.0
            else:
                intersection = tokens1 & tokens2
                union = tokens1 | tokens2
                lexical_similarity = len(intersection) / len(union) if union else 0.0
            
            # For now, use lexical similarity as semantic similarity
            semantic_similarity = lexical_similarity
            
            # Determine if plagiarized
            is_plagiarized = semantic_similarity > settings.SIMILARITY_THRESHOLD
            
            return {
                "semantic_similarity": float(semantic_similarity),
                "lexical_similarity": float(lexical_similarity),
                "is_plagiarized": is_plagiarized,
                "confidence": float(semantic_similarity),
                "analysis": {
                    "code1_tokens": len(tokens1),
                    "code2_tokens": len(tokens2),
                    "common_tokens": len(tokens1 & tokens2),
                    "language1": language1,
                    "language2": language2
                }
            }
            
        except Exception as e:
            print(f"Error in calculate_similarity: {e}")
            return {
                "semantic_similarity": 0.0,
                "lexical_similarity": 0.0,
                "is_plagiarized": False,
                "confidence": 0.0,
                "analysis": {
                    "code1_tokens": 0,
                    "code2_tokens": 0,
                    "common_tokens": 0,
                    "language1": language1,
                    "language2": language2,
                    "error": str(e)
                }
            }

    async def get_ai_explanation(self, code1: str, code2: str, similarity_score: float) -> str:
        """Get AI explanation of similarity"""
        try:
            if similarity_score > 0.7:
                return f"The codes show high similarity ({similarity_score:.2f}). They have very similar structure and logic patterns, suggesting potential plagiarism."
            elif similarity_score > 0.4:
                return f"The codes show moderate similarity ({similarity_score:.2f}). They share some common patterns but have notable differences."
            else:
                return f"The codes show low similarity ({similarity_score:.2f}). They appear to be significantly different with minimal overlap."
        except Exception as e:
            return f"Analysis completed with similarity score: {similarity_score:.2f}"

# Global instance
ai_service = AIService()