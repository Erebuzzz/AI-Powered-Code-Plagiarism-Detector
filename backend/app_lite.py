"""
Lightweight Flask app for Render free tier deployment
"""
from flask import Flask, jsonify
from flask_cors import CORS
import os

def create_app(config_name='production'):
    app = Flask(__name__)
    
    # Basic configuration for minimal memory usage
    app.config.update(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev-secret-key'),
        MAX_CONTENT_LENGTH=16 * 1024 * 1024,  # 16MB
        CORS_ORIGINS=os.environ.get('CORS_ORIGINS', '*').split(',')
    )
    
    # Initialize CORS
    CORS(app, origins=app.config['CORS_ORIGINS'])
    
    # Register lightweight API routes
    from routes.api_lite import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Health check route
    @app.route('/health')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'version': 'lite',
            'memory_optimized': True
        })
    
    @app.route('/')
    def root():
        return jsonify({
            'message': 'AI Code Plagiarism Detector API (Lite)',
            'status': 'running',
            'version': 'lite'
        })
    
    return app

# Create app instance for gunicorn
app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
