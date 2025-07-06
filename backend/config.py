import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = 'uploads'
    
    # Model configurations
    SIMILARITY_THRESHOLD = 0.7
    MODEL_NAME = 'microsoft/codebert-base'
    CACHE_DIR = 'model_cache'
    
    # Alternative free models for different use cases
    CODE_MODELS = {
        'codebert': 'microsoft/codebert-base',           # Good for general code understanding
        'unixcoder': 'microsoft/unixcoder-base',         # Better for code similarity
        'codet5': 'Salesforce/codet5-small',             # Good for code generation/understanding
        'codegen': 'Salesforce/codegen-350M-mono',       # Fast code generation
        'starcoder': 'bigcode/starcoder',                # Large but very powerful (15B params)
    }
    
    # Sentence transformer models for semantic similarity
    SENTENCE_MODELS = {
        'lightweight': 'all-MiniLM-L6-v2',              # Fast, 22MB
        'balanced': 'all-mpnet-base-v2',                # Better quality, 420MB
        'code_specific': 'sentence-transformers/all-distilroberta-v1',  # Good for code
    }
    
    # API Keys (should be set in environment variables for production)
    COHERE_API_KEY = os.environ.get('COHERE_API_KEY')
    HUGGINGFACE_TOKEN = os.environ.get('HUGGINGFACE_API_KEY')
    
    # Advanced model configurations
    ADVANCED_MODELS = {
        'code_similarity': 'microsoft/GraphCodeBERT-base',
        'code_generation': 'Salesforce/codegen-350M-mono',
        'code_classification': 'huggingface/CodeBERTa-small-v1',
        'semantic_search': 'sentence-transformers/all-mpnet-base-v2'
    }
    
    # CORS settings - get from environment variable for production
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'http://localhost:3000').split(',')

class DevelopmentConfig(Config):
    DEBUG = True
    
class ProductionConfig(Config):
    DEBUG = False
    # Additional production-specific settings
    SECRET_KEY = os.environ.get('SECRET_KEY', 'prod-fallback-secret-change-this')  # Fallback for easier deployment
    
    # Performance settings for Render
    SIMILARITY_THRESHOLD = 0.75  # Slightly higher threshold for production
    
    # Logging configuration
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    
    # Render-specific settings
    PORT = int(os.environ.get('PORT', 10000))

class RenderConfig(ProductionConfig):
    """Configuration specifically for Render.com deployment"""
    # Render provides HTTPS by default
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'render': RenderConfig,
    'default': DevelopmentConfig
}
