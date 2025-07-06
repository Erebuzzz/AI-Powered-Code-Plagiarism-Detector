import cohere
import numpy as np
from typing import List, Dict, Any, Optional
from flask import current_app

class CohereService:
    """
    Service for integrating with Cohere API for advanced code analysis
    """
    
    def __init__(self):
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Cohere client with API key"""
        try:
            # Try to get API key from Flask app context first, then fall back to environment
            try:
                from flask import current_app
                api_key = current_app.config.get('COHERE_API_KEY')
            except RuntimeError:
                # Working outside of application context, try environment variable
                import os
                api_key = os.environ.get('COHERE_API_KEY') or 'F3dnVKxBTB5V20BhUqP5GFdZHMrS6wGBekVzuCCm'
            
            if api_key:
                self.client = cohere.Client(api_key)
            else:
                raise ValueError("Cohere API key not found in configuration")
        except Exception as e:
            print(f"Warning: Could not initialize Cohere client: {e}")
            self.client = None
    
    def get_embeddings(self, texts: List[str], model: str = "embed-english-v3.0") -> Optional[np.ndarray]:
        """
        Get embeddings for text/code using Cohere's embedding models
        
        Args:
            texts: List of text/code snippets to embed
            model: Cohere embedding model to use
        
        Returns:
            Numpy array of embeddings or None if failed
        """
        if not self.client:
            return None
        
        try:
            response = self.client.embed(
                texts=texts,
                model=model,
                input_type="search_document"
            )
            return np.array(response.embeddings)
        except Exception as e:
            print(f"Error getting embeddings: {e}")
            return None
    
    def calculate_similarity(self, code1: str, code2: str) -> Optional[float]:
        """
        Calculate semantic similarity between two code snippets using Cohere embeddings
        
        Args:
            code1: First code snippet
            code2: Second code snippet
        
        Returns:
            Similarity score (0-1) or None if failed
        """
        if not self.client:
            return None
        
        try:
            embeddings = self.get_embeddings([code1, code2])
            if embeddings is not None and len(embeddings) == 2:
                # Calculate cosine similarity
                emb1, emb2 = embeddings[0], embeddings[1]
                similarity = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
                return float(similarity)  # Convert numpy float to Python float
            return None
        except Exception as e:
            print(f"Error calculating similarity: {e}")
            return None
    
    def analyze_code_intent(self, code: str) -> Optional[Dict[str, Any]]:
        """
        Analyze code intent and purpose using Cohere's generation capabilities
        
        Args:
            code: Code snippet to analyze
        
        Returns:
            Analysis results or None if failed
        """
        if not self.client:
            return None
        
        try:
            prompt = f"""
            Analyze the following code and provide:
            1. What the code does (main purpose)
            2. Key algorithms or patterns used
            3. Complexity level (beginner/intermediate/advanced)
            4. Programming concepts demonstrated
            
            Code:
            ```
            {code}
            ```
            
            Provide a concise analysis:
            """
            
            response = self.client.generate(
                model="command",  # Use basic command model instead of command-r
                prompt=prompt,
                max_tokens=300,
                temperature=0.3
            )
            
            return {
                "analysis": response.generations[0].text.strip(),
                "model_used": "command-r"
            }
        except Exception as e:
            print(f"Error analyzing code intent: {e}")
            return None
    
    def detect_code_patterns(self, code: str) -> Optional[Dict[str, Any]]:
        """
        Detect common code patterns and potential issues using Cohere
        
        Args:
            code: Code snippet to analyze
        
        Returns:
            Pattern detection results or None if failed
        """
        if not self.client:
            return None
        
        try:
            prompt = f"""
            Analyze this code for:
            1. Design patterns used (if any)
            2. Code quality issues
            3. Potential security concerns
            4. Best practices followed or violated
            5. Suggestions for improvement
            
            Code:
            ```
            {code}
            ```
            
            Provide structured feedback:
            """
            
            response = self.client.generate(
                model="command",  # Use basic command model
                prompt=prompt,
                max_tokens=400,
                temperature=0.2
            )
            
            return {
                "patterns": response.generations[0].text.strip(),
                "model_used": "command-r"
            }
        except Exception as e:
            print(f"Error detecting patterns: {e}")
            return None
    
    def classify_code_type(self, code: str) -> Optional[Dict[str, Any]]:
        """
        Classify the type and category of code using Cohere
        
        Args:
            code: Code snippet to classify
        
        Returns:
            Classification results or None if failed
        """
        if not self.client:
            return None
        
        try:
            # Use generation instead of classification for free tier
            prompt = f"""
Analyze this code snippet and classify it into one of these categories:
- algorithm: Mathematical or computational algorithms
- data_structure: Classes, data containers, or structures
- web_framework: Web development code (Flask, Django, etc.)
- data_analysis: Data processing, analysis, or visualization
- testing: Unit tests or test code
- utility: Helper functions or utilities
- other: Any other type of code

Code to classify:
```
{code}
```

Response should be just the category name (one word):"""
            
            response = self.client.generate(
                prompt=prompt,
                max_tokens=50,
                temperature=0.1
            )
            
            if response.generations and response.generations[0].text:
                category = response.generations[0].text.strip().lower()
                return {
                    "category": category,
                    "confidence": 0.8,  # Default confidence for generation-based classification
                    "model_used": "command"
                }
            return None
        except Exception as e:
            print(f"Error classifying code: {e}")
            return None
    
    def find_similar_code_semantic(self, query_code: str, code_database: List[str], top_k: int = 5) -> Optional[List[Dict[str, Any]]]:
        """
        Find semantically similar code snippets using Cohere embeddings
        
        Args:
            query_code: Code to find similarities for
            code_database: List of code snippets to search through
            top_k: Number of top results to return
        
        Returns:
            List of similar code snippets with similarity scores
        """
        if not self.client or not code_database:
            return None
        
        try:
            # Get embeddings for all code snippets
            all_texts = [query_code] + code_database
            embeddings = self.get_embeddings(all_texts)
            
            if embeddings is None:
                return None
            
            query_embedding = embeddings[0]
            db_embeddings = embeddings[1:]
            
            # Calculate similarities
            similarities = []
            for i, db_embedding in enumerate(db_embeddings):
                similarity = np.dot(query_embedding, db_embedding) / (
                    np.linalg.norm(query_embedding) * np.linalg.norm(db_embedding)
                )
                similarities.append({
                    "index": i,
                    "code": code_database[i],
                    "similarity": float(similarity)
                })
            
            # Sort by similarity and return top k
            similarities.sort(key=lambda x: x["similarity"], reverse=True)
            return similarities[:top_k]
            
        except Exception as e:
            print(f"Error finding similar code: {e}")
            return None
    
    def is_available(self) -> bool:
        """Check if Cohere service is available"""
        return self.client is not None
