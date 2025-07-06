"""
Lightweight API routes for Render free tier deployment
Uses external APIs instead of heavy local models
"""
from flask import Blueprint, request, jsonify, current_app
import os
import json
import difflib
import ast
import re
from datetime import datetime

api_bp = Blueprint('api', __name__)

def basic_similarity_check(code1, code2):
    """Simple text-based similarity without heavy ML models"""
    # Normalize whitespace and remove comments
    def normalize_code(code):
        # Remove comments
        code = re.sub(r'#.*', '', code)
        code = re.sub(r'//.*', '', code)
        code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
        # Normalize whitespace
        return ' '.join(code.split())
    
    norm_code1 = normalize_code(code1)
    norm_code2 = normalize_code(code2)
    
    # Use difflib for similarity
    similarity = difflib.SequenceMatcher(None, norm_code1, norm_code2).ratio()
    
    return {
        'similarity_score': similarity,
        'is_similar': similarity > 0.7,
        'method': 'text_based'
    }

def analyze_code_structure(code, language):
    """Basic code analysis without heavy dependencies"""
    try:
        if language.lower() == 'python':
            # Try to parse as AST for Python
            tree = ast.parse(code)
            functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
            classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
            return {
                'functions': functions,
                'classes': classes,
                'lines_of_code': len(code.split('\n')),
                'complexity': 'basic'
            }
    except:
        pass
    
    # Fallback analysis for any language
    lines = code.split('\n')
    return {
        'lines_of_code': len(lines),
        'non_empty_lines': len([line for line in lines if line.strip()]),
        'complexity': 'basic'
    }

@api_bp.route('/analyze', methods=['POST'])
def analyze_code():
    """Lightweight code analysis endpoint"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        code = data.get('code', '').strip()
        language = data.get('language', 'text').lower()
        
        if not code:
            return jsonify({'error': 'Code is required'}), 400
        
        # Basic analysis
        analysis = analyze_code_structure(code, language)
        
        result = {
            'status': 'success',
            'analysis': analysis,
            'similarity_results': [],
            'language': language,
            'timestamp': datetime.now().isoformat(),
            'method': 'lightweight'
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'error': f'Analysis failed: {str(e)}',
            'status': 'error'
        }), 500

@api_bp.route('/compare', methods=['POST'])
def compare_code():
    """Compare two code snippets"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        code1 = data.get('code1', '').strip()
        code2 = data.get('code2', '').strip()
        language = data.get('language', 'text').lower()
        
        if not code1 or not code2:
            return jsonify({'error': 'Both code snippets are required'}), 400
        
        # Perform comparison
        similarity_result = basic_similarity_check(code1, code2)
        
        result = {
            'status': 'success',
            'comparison': similarity_result,
            'language': language,
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'error': f'Comparison failed: {str(e)}',
            'status': 'error'
        }), 500

@api_bp.route('/supported-languages', methods=['GET'])
def get_supported_languages():
    """Return list of supported programming languages"""
    languages = [
        'python', 'javascript', 'java', 'cpp', 'c', 'csharp',
        'php', 'ruby', 'go', 'rust', 'swift', 'kotlin', 'text'
    ]
    
    return jsonify({
        'languages': languages,
        'total': len(languages)
    })

@api_bp.route('/statistics', methods=['GET'])
def get_statistics():
    """Basic statistics endpoint"""
    return jsonify({
        'total_analyses': 0,
        'unique_languages': 13,
        'average_similarity': 0.0,
        'uptime': '100%',
        'version': 'lite'
    })

@api_bp.route('/upload', methods=['POST'])
def upload_file():
    """Handle file uploads for analysis"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Read file content
        content = file.read().decode('utf-8')
        language = request.form.get('language', 'text')
        
        # Analyze the uploaded code
        analysis = analyze_code_structure(content, language)
        
        return jsonify({
            'status': 'success',
            'filename': file.filename,
            'analysis': analysis,
            'language': language
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Upload failed: {str(e)}',
            'status': 'error'
        }), 500
