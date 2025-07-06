"""
WSGI entry point for production deployment (Lite version)
"""
import os

# Use lite version for memory optimization
try:
    from app_lite import app
except ImportError:
    # Fallback to regular app if lite version has issues
    from app import app

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
