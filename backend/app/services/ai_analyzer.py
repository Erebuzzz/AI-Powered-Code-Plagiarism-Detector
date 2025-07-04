import asyncio
import openai
import numpy as np
from typing import List, Dict, Optional
from sentence_transformers import SentenceTransformer
from app.core.config import settings

class AIAnalyzer:
    """AI-powered code analysis using LLMs and embeddings"""
    
    def __init__(self):
        # Initialize OpenAI client
        if settings.OPENAI_API_KEY:
            openai.api_key = settings.OPENAI_API_KEY
        
        # Initialize sentence transformer for embeddings
        try:
            self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
        except:
            self.sentence_model = None
    
    async def calculate_semantic_similarity(self, code1: str, code2: str, language: str) -> float:
        """Calculate semantic similarity using embeddings"""
        try:
            if self.sentence_model:
                # Use sentence transformers for embeddings
                embeddings1 = self.sentence_model.encode([code1])
                embeddings2 = self.sentence_model.encode([code2])
                
                # Calculate cosine similarity
                similarity = np.dot(embeddings1[0], embeddings2[0]) / (
                    np.linalg.norm(embeddings1[0]) * np.linalg.norm(embeddings2[0])
                )
                
                return float(similarity)
            else:
                # Fallback to simple text similarity
                return self._calculate_text_similarity(code1, code2)
        
        except Exception as e:
            print(f"Error calculating semantic similarity: {e}")
            return self._calculate_text_similarity(code1, code2)
    
    def _calculate_text_similarity(self, text1: str, text2: str) -> float:
        """Fallback text similarity calculation"""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 and not words2:
            return 1.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0
    
    async def analyze_code_with_gpt(self, code1: str, code2: str, language: str) -> Dict:
        """Analyze code similarity using GPT-4"""
        try:
            if not settings.OPENAI_API_KEY:
                return {"error": "OpenAI API key not configured"}
            
            prompt = f"""
            Analyze the following two {language} code snippets for plagiarism:
            
            Code 1:
            ```{language}
            {code1}
            ```
            
            Code 2:
            ```{language}
            {code2}
            ```
            
            Please provide:
            1. Similarity score (0-1)
            2. Explanation of similarities
            3. Potential plagiarism indicators
            4. Recommendations
            
            Respond in JSON format.
            """
            
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a code plagiarism detection expert."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.1
            )
            
            return {
                "gpt_analysis": response.choices[0].message.content,
                "model": "gpt-4"
            }
        
        except Exception as e:
            return {"error": f"GPT analysis failed: {str(e)}"}
    
    def extract_code_features(self, code: str, language: str) -> Dict:
        """Extract features from code for analysis"""
        features = {
            "length": len(code),
            "lines": len(code.split('\n')),
            "complexity": self._calculate_complexity(code),
            "language": language
        }
        
        return features
    
    def _calculate_complexity(self, code: str) -> float:
        """Calculate cyclomatic complexity (simplified)"""
        # Count control flow statements
        control_keywords = ['if', 'else', 'elif', 'for', 'while', 'try', 'except', 'finally']
        complexity = 1  # Base complexity
        
        for keyword in control_keywords:
            complexity += code.lower().count(keyword)
        
        return complexity
