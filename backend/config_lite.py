import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = 'uploads'
    
    # Lightweight configuration - use APIs instead of local models
    SIMILARITY_THRESHOLD = 0.7
    USE_LOCAL_MODELS = False  # Disable heavy local models
    
    # API Keys for external services
    COHERE_API_KEY = os.environ.get('COHERE_API_KEY')
    HUGGINGFACE_TOKEN = os.environ.get('HUGGINGFACE_API_KEY')
    
    # CORS settings
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'http://localhost:3000').split(',')
    
    # Memory optimization settings
    WORKERS = 1  # Single worker for free tier
    MAX_REQUESTS = 100  # Restart worker after 100 requests to prevent memory leaks

class DevelopmentConfig(Config):
    DEBUG = True
    
class ProductionConfig(Config):
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'prod-fallback-secret-change-this')
    SIMILARITY_THRESHOLD = 0.75
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    PORT = int(os.environ.get('PORT', 10000))

class RenderConfig(ProductionConfig):
    """Lightweight configuration for Render free tier"""
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Memory optimization
    WORKERS = 1
    WORKER_CLASS = 'sync'
    MAX_REQUESTS = 50  # More aggressive restart on free tier

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'render': RenderConfig,
    'default': DevelopmentConfig
}
