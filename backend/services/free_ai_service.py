"""
Free AI Service Integration
Provides access to powerful free AI models for code analysis without API costs
"""

import requests
import json
from typing import Dict, List, Any, Optional
import torch
from transformers import pipeline, AutoTokenizer, AutoModel
import time
import numpy as np
from utils.json_utils import convert_numpy_types

class FreeAIService:
    """
    Integrates with free AI models and services for advanced code analysis
    """
    
    def __init__(self):
        self.models = {}
        self.pipelines = {}
        self._initialize_local_models()
    
    def _initialize_local_models(self):
        """Initialize local free models"""
        try:
            # Code summarization pipeline
            self.pipelines['summarization'] = pipeline(
                "summarization",
                model="Salesforce/codet5-small",
                tokenizer="Salesforce/codet5-small"
            )
            print("CodeT5 summarization model loaded")
        except Exception as e:
            print(f"Could not load summarization model: {e}")
        
        try:
            # Code classification pipeline
            self.pipelines['classification'] = pipeline(
                "text-classification",
                model="microsoft/codebert-base-mlm"
            )
            print("CodeBERT classification model loaded")
        except Exception as e:
            print(f"Could not load classification model: {e}")
    
    def analyze_code_quality(self, code: str, language: str = 'python') -> Dict[str, Any]:
        """
        Analyze code quality using free models
        """
        results = {
            'quality_score': 0.0,
            'suggestions': [],
            'complexity': 'unknown',
            'readability': 'unknown'
        }
        
        try:
            # Use local analysis
            results.update(self._analyze_locally(code, language))
        except Exception as e:
            print(f"Local analysis failed: {e}")
        
        # Convert any numpy types to Python native types
        return convert_numpy_types(results)
    
    def _analyze_locally(self, code: str, language: str) -> Dict[str, Any]:
        """Local code analysis using transformer models"""
        analysis = {}
        
        # Calculate complexity score based on code structure
        complexity_score = self._calculate_complexity(code)
        analysis['complexity_score'] = complexity_score
        
        if complexity_score < 0.3:
            analysis['complexity'] = 'low'
        elif complexity_score < 0.7:
            analysis['complexity'] = 'medium'
        else:
            analysis['complexity'] = 'high'
        
        # Calculate readability score
        readability_score = self._calculate_readability(code)
        analysis['readability_score'] = readability_score
        
        if readability_score > 0.7:
            analysis['readability'] = 'good'
        elif readability_score > 0.4:
            analysis['readability'] = 'fair'
        else:
            analysis['readability'] = 'poor'
        
        # Generate suggestions
        analysis['suggestions'] = self._generate_suggestions(code, language)
        
        # Overall quality score
        analysis['quality_score'] = (readability_score + (1 - complexity_score)) / 2
        
        # Convert any numpy types to Python native types
        return convert_numpy_types(analysis)
    
    def _calculate_complexity(self, code: str) -> float:
        """Calculate code complexity score"""
        lines = code.split('\n')
        non_empty_lines = [line for line in lines if line.strip()]
        
        if not non_empty_lines:
            return 0.0
        
        # Count complexity indicators
        complexity_indicators = 0
        total_lines = len(non_empty_lines)
        
        for line in non_empty_lines:
            line = line.strip()
            # Count control structures
            if any(keyword in line for keyword in ['if', 'for', 'while', 'try', 'except', 'elif']):
                complexity_indicators += 1
            # Count nested structures
            if line.count('    ') > 2:  # More than 2 levels of indentation
                complexity_indicators += 0.5
        
        return min(complexity_indicators / total_lines, 1.0)
    
    def _calculate_readability(self, code: str) -> float:
        """Calculate code readability score"""
        lines = code.split('\n')
        non_empty_lines = [line for line in lines if line.strip()]
        
        if not non_empty_lines:
            return 0.0
        
        readability_score = 1.0
        
        # Check average line length
        avg_line_length = sum(len(line) for line in non_empty_lines) / len(non_empty_lines)
        if avg_line_length > 120:
            readability_score -= 0.2
        elif avg_line_length > 80:
            readability_score -= 0.1
        
        # Check for comments
        comment_lines = sum(1 for line in non_empty_lines if line.strip().startswith('#'))
        comment_ratio = comment_lines / len(non_empty_lines)
        if comment_ratio < 0.1:
            readability_score -= 0.2
        
        # Check for meaningful variable names
        meaningful_names = 0
        total_vars = 0
        for line in non_empty_lines:
            if '=' in line and not line.strip().startswith('#'):
                parts = line.split('=')[0].strip()
                if parts and len(parts.split()[-1]) > 2:  # Variable name longer than 2 chars
                    meaningful_names += 1
                total_vars += 1
        
        if total_vars > 0:
            name_ratio = meaningful_names / total_vars
            if name_ratio < 0.5:
                readability_score -= 0.3
        
        return max(readability_score, 0.0)
    
    def _generate_suggestions(self, code: str, language: str) -> List[str]:
        """Generate improvement suggestions"""
        suggestions = []
        lines = code.split('\n')
        
        # Check for long lines
        for i, line in enumerate(lines):
            if len(line) > 120:
                suggestions.append(f"Line {i+1}: Consider breaking long line for better readability")
        
        # Check for missing docstrings
        if 'def ' in code and '"""' not in code and "'''" not in code:
            suggestions.append("Consider adding docstrings to functions for better documentation")
        
        # Check for complex nested structures
        for i, line in enumerate(lines):
            if line.count('    ') > 3:  # More than 3 levels of indentation
                suggestions.append(f"Line {i+1}: Consider refactoring deeply nested code")
        
        # Language-specific suggestions
        if language == 'python':
            if 'import *' in code:
                suggestions.append("Avoid wildcard imports, import specific functions instead")
            if any(var.islower() and '_' not in var for var in code.split() if len(var) > 1):
                suggestions.append("Consider using snake_case for variable names (Python convention)")
        
        return suggestions[:5]  # Return top 5 suggestions
    
    def get_huggingface_model_suggestions(self, task: str = 'code-analysis') -> List[Dict[str, str]]:
        """
        Get suggestions for free HuggingFace models suitable for code analysis
        """
        models = [
            {
                'name': 'microsoft/unixcoder-base',
                'description': 'Unified pre-trained encoder for programming languages',
                'use_case': 'Code similarity, bug detection',
                'size': '125M parameters'
            },
            {
                'name': 'Salesforce/codet5-small',
                'description': 'Code-aware encoder-decoder model',
                'use_case': 'Code summarization, generation',
                'size': '60M parameters'
            },
            {
                'name': 'microsoft/codebert-base',
                'description': 'BERT model pre-trained on code',
                'use_case': 'Code understanding, classification',
                'size': '125M parameters'
            },
            {
                'name': 'huggingface/CodeBERTa-small-v1',
                'description': 'RoBERTa model trained on code',
                'use_case': 'Code analysis, similarity detection',
                'size': '84M parameters'
            },
            {
                'name': 'microsoft/DialoGPT-medium',
                'description': 'Conversational AI (can be fine-tuned for code)',
                'use_case': 'Code explanation, Q&A',
                'size': '345M parameters'
            }
        ]
        
        return models

class LocalLLMService:
    """
    Service for running local language models without API costs
    """
    
    def __init__(self):
        self.available_models = [
            'microsoft/DialoGPT-small',  # 117M params
            'distilgpt2',                # 82M params  
            'gpt2',                      # 124M params
        ]
        self.current_model = None
        self.tokenizer = None
    
    def load_model(self, model_name: str = 'distilgpt2'):
        """Load a local model for text generation"""
        try:
            from transformers import GPT2LMHeadModel, GPT2Tokenizer
            
            self.tokenizer = GPT2Tokenizer.from_pretrained(model_name)
            self.current_model = GPT2LMHeadModel.from_pretrained(model_name)
            
            # Add pad token if it doesn't exist
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            print(f"Loaded local model: {model_name}")
            return True
        except Exception as e:
            print(f"Failed to load model {model_name}: {e}")
            return False
    
    def generate_code_explanation(self, code: str, max_length: int = 150) -> str:
        """Generate explanation for code using local model"""
        if not self.current_model or not self.tokenizer:
            return "Local model not loaded. Please load a model first."
        
        try:
            prompt = f"Explain this code: {code[:200]}..."  # Limit input length
            
            inputs = self.tokenizer.encode(prompt, return_tensors='pt', max_length=512, truncation=True)
            
            with torch.no_grad():
                outputs = self.current_model.generate(
                    inputs,
                    max_length=max_length,
                    num_return_sequences=1,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id
                )
            
            explanation = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract only the generated part (after the prompt)
            if prompt in explanation:
                explanation = explanation.replace(prompt, "").strip()
            
            return explanation
            
        except Exception as e:
            return f"Error generating explanation: {e}"
