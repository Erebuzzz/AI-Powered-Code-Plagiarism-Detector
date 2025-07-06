"""
Enhanced Hugging Face Integration Service
Provides access to state-of-the-art free models for code analysis
"""

import os
import torch
from transformers import (
    AutoTokenizer, AutoModel, AutoModelForSequenceClassification,
    pipeline, AutoModelForCausalLM
)
from sentence_transformers import SentenceTransformer
import numpy as np
from typing import Dict, List, Any, Optional
import logging
from flask import current_app

class HuggingFaceService:
    """
    Service for integrating with Hugging Face models using your token
    """
    
    def __init__(self):
        self.token = None
        self.models = {}
        self.tokenizers = {}
        self.pipelines = {}
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.logger = logging.getLogger(__name__)
        
    def initialize(self, token: str):
        """Initialize the service with Hugging Face token"""
        self.token = token
        os.environ['HUGGINGFACE_HUB_TOKEN'] = token
        self.logger.info(f"HuggingFace service initialized on device: {self.device}")
        
    def load_code_model(self, model_name: str = "microsoft/GraphCodeBERT-base"):
        """Load a code understanding model"""
        try:
            if model_name not in self.models:
                self.logger.info(f"Loading code model: {model_name}")
                self.tokenizers[model_name] = AutoTokenizer.from_pretrained(
                    model_name, 
                    use_auth_token=self.token
                )
                self.models[model_name] = AutoModel.from_pretrained(
                    model_name, 
                    use_auth_token=self.token
                ).to(self.device)
                
            return True
        except Exception as e:
            self.logger.error(f"Failed to load model {model_name}: {str(e)}")
            return False
    
    def get_code_embeddings(self, code: str, model_name: str = "microsoft/GraphCodeBERT-base"):
        """Get embeddings for code using advanced models"""
        try:
            if not self.load_code_model(model_name):
                return None
                
            tokenizer = self.tokenizers[model_name]
            model = self.models[model_name]
            
            # Tokenize and encode
            inputs = tokenizer(
                code, 
                return_tensors="pt", 
                max_length=512, 
                truncation=True, 
                padding=True
            ).to(self.device)
            
            with torch.no_grad():
                outputs = model(**inputs)
                embeddings = outputs.last_hidden_state.mean(dim=1).cpu().numpy()
                
            return embeddings
            
        except Exception as e:
            self.logger.error(f"Failed to get embeddings: {str(e)}")
            return None
    
    def calculate_advanced_similarity(self, code1: str, code2: str):
        """Calculate similarity using GraphCodeBERT"""
        try:
            embeddings1 = self.get_code_embeddings(code1)
            embeddings2 = self.get_code_embeddings(code2)
            
            if embeddings1 is None or embeddings2 is None:
                return None
            
            # Calculate cosine similarity
            similarity = np.dot(embeddings1[0], embeddings2[0]) / (
                np.linalg.norm(embeddings1[0]) * np.linalg.norm(embeddings2[0])
            )
            
            return float(similarity)
            
        except Exception as e:
            self.logger.error(f"Failed to calculate similarity: {str(e)}")
            return None
    
    def load_code_generation_pipeline(self):
        """Load code generation pipeline"""
        try:
            if 'code_generation' not in self.pipelines:
                self.logger.info("Loading code generation pipeline...")
                self.pipelines['code_generation'] = pipeline(
                    "text-generation",
                    model="Salesforce/codegen-350M-mono",
                    tokenizer="Salesforce/codegen-350M-mono",
                    device=0 if self.device == 'cuda' else -1,
                    use_auth_token=self.token
                )
            return True
        except Exception as e:
            self.logger.error(f"Failed to load generation pipeline: {str(e)}")
            return False
    
    def generate_code_explanation(self, code: str, max_length: int = 150):
        """Generate code explanation using free models"""
        try:
            if not self.load_code_generation_pipeline():
                return "Code generation model not available"
            
            prompt = f"# Explain this code:\n{code}\n# Explanation:"
            
            result = self.pipelines['code_generation'](
                prompt,
                max_length=max_length,
                num_return_sequences=1,
                temperature=0.7,
                do_sample=True,
                pad_token_id=50256
            )
            
            explanation = result[0]['generated_text'].split("# Explanation:")[-1].strip()
            return explanation
            
        except Exception as e:
            self.logger.error(f"Failed to generate explanation: {str(e)}")
            return f"Error generating explanation: {str(e)}"
    
    def load_classification_pipeline(self):
        """Load code classification pipeline"""
        try:
            if 'classification' not in self.pipelines:
                self.logger.info("Loading classification pipeline...")
                self.pipelines['classification'] = pipeline(
                    "text-classification",
                    model="huggingface/CodeBERTa-small-v1",
                    use_auth_token=self.token,
                    device=0 if self.device == 'cuda' else -1
                )
            return True
        except Exception as e:
            self.logger.error(f"Failed to load classification pipeline: {str(e)}")
            return False
    
    def classify_code_intent(self, code: str):
        """Classify code intent/purpose"""
        try:
            if not self.load_classification_pipeline():
                return {"intent": "unknown", "confidence": 0.0}
            
            result = self.pipelines['classification'](code)
            
            return {
                "intent": result[0]['label'],
                "confidence": result[0]['score'],
                "all_predictions": result
            }
            
        except Exception as e:
            self.logger.error(f"Failed to classify code: {str(e)}")
            return {"intent": "error", "confidence": 0.0, "error": str(e)}
    
    def load_semantic_search_model(self):
        """Load semantic search model"""
        try:
            if 'semantic_search' not in self.models:
                self.logger.info("Loading semantic search model...")
                self.models['semantic_search'] = SentenceTransformer(
                    'sentence-transformers/all-mpnet-base-v2',
                    use_auth_token=self.token
                )
            return True
        except Exception as e:
            self.logger.error(f"Failed to load semantic search model: {str(e)}")
            return False
    
    def semantic_code_search(self, query_code: str, code_database: List[str], top_k: int = 5):
        """Perform semantic search across code database"""
        try:
            if not self.load_semantic_search_model():
                return []
            
            model = self.models['semantic_search']
            
            # Encode query and database
            query_embedding = model.encode([query_code])
            db_embeddings = model.encode(code_database)
            
            # Calculate similarities
            similarities = model.similarity(query_embedding, db_embeddings)[0]
            
            # Get top results
            top_indices = torch.topk(similarities, min(top_k, len(code_database))).indices
            
            results = []
            for idx in top_indices:
                results.append({
                    'code': code_database[idx],
                    'similarity_score': float(similarities[idx]),
                    'index': int(idx)
                })
            
            return results
            
        except Exception as e:
            self.logger.error(f"Failed to perform semantic search: {str(e)}")
            return []
    
    def analyze_code_quality_advanced(self, code: str, language: str = 'python'):
        """Advanced code quality analysis using multiple models"""
        try:
            analysis = {
                'timestamp': torch.tensor([]).device,
                'model_info': {
                    'primary_model': 'microsoft/GraphCodeBERT-base',
                    'classification_model': 'huggingface/CodeBERTa-small-v1',
                    'generation_model': 'Salesforce/codegen-350M-mono'
                }
            }
            
            # Get code embeddings for complexity analysis
            embeddings = self.get_code_embeddings(code)
            if embeddings is not None:
                complexity_score = float(np.mean(np.abs(embeddings)))
                analysis['complexity'] = {
                    'score': complexity_score,
                    'level': 'high' if complexity_score > 0.5 else 'medium' if complexity_score > 0.3 else 'low'
                }
            
            # Classify code intent
            intent_result = self.classify_code_intent(code)
            analysis['intent_analysis'] = intent_result
            
            # Generate code explanation
            explanation = self.generate_code_explanation(code, max_length=100)
            analysis['explanation'] = explanation
            
            # Basic metrics
            analysis['metrics'] = {
                'lines_of_code': len(code.split('\n')),
                'character_count': len(code),
                'estimated_complexity': analysis.get('complexity', {}).get('level', 'medium')
            }
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Failed to analyze code quality: {str(e)}")
            return {'error': str(e)}
    
    def get_model_status(self):
        """Get status of loaded models"""
        return {
            'loaded_models': list(self.models.keys()),
            'loaded_pipelines': list(self.pipelines.keys()),
            'device': self.device,
            'token_configured': self.token is not None,
            'cuda_available': torch.cuda.is_available()
        }
    
    def clear_models(self):
        """Clear loaded models to free memory"""
        self.models.clear()
        self.tokenizers.clear()
        self.pipelines.clear()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        self.logger.info("Cleared all models from memory")

# Global instance
huggingface_service = HuggingFaceService()
