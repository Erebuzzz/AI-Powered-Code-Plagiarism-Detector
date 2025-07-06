#!/usr/bin/env python3
"""
Test script to verify Flask app and routes
"""
import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app

def test_app():
    """Test the Flask application"""
    print("Creating Flask app...")
    app = create_app('development')
    
    print("Registered routes:")
    for rule in app.url_map.iter_rules():
        print(f"  {rule.rule} -> {rule.endpoint} ({list(rule.methods)})")
    
    print(f"\nStarting server on http://0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)

if __name__ == '__main__':
    test_app()
