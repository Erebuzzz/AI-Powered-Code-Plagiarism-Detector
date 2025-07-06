from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
import os
import json
from datetime import datetime
from services.code_analyzer import CodeAnalyzer
from services.similarity_detector import SimilarityDetector
from services.free_ai_service import FreeAIService, LocalLLMService
from utils.validators import validate_code_input, allowed_file
from utils.json_utils import convert_numpy_types

api_bp = Blueprint('api', __name__)

# Initialize services
code_analyzer = CodeAnalyzer()
similarity_detector = SimilarityDetector()
free_ai_service = FreeAIService()
local_llm_service = LocalLLMService()

@api_bp.route('/analyze', methods=['POST'])
def analyze_code():
    """
    Main endpoint for code plagiarism analysis
    Accepts code input and returns similarity analysis
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        # Validate input
        validation_result = validate_code_input(data)
        if not validation_result['valid']:
            return jsonify({'error': validation_result['message']}), 400
        
        code_content = data.get('code')
        language = data.get('language', 'auto')
        check_database = data.get('checkDatabase', True)
        
        # Analyze code structure and extract features
        analysis_result = code_analyzer.analyze(code_content, language)
        
        # Perform similarity detection
        similarity_results = similarity_detector.find_similar_code(
            code_content, 
            language, 
            check_database=check_database
        )
        
        # Prepare response
        response = {
            'analysis': analysis_result,
            'similarity': similarity_results,
            'timestamp': datetime.utcnow().isoformat(),
            'language': analysis_result.get('detected_language', language)
        }
        
        # Convert numpy types to JSON-serializable types
        response = convert_numpy_types(response)
        
        return jsonify(response)
        
    except Exception as e:
        current_app.logger.error(f"Error in analyze_code: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@api_bp.route('/upload', methods=['POST'])
def upload_file():
    """
    Upload code file for analysis
    """
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not supported'}), 400
        
        # Secure filename and save
        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Read file content
        with open(filepath, 'r', encoding='utf-8') as f:
            code_content = f.read()
        
        # Clean up uploaded file
        os.remove(filepath)
        
        # Detect language from file extension
        language = code_analyzer.detect_language_from_filename(filename)
        
        return jsonify({
            'code': code_content,
            'filename': filename,
            'language': language,
            'size': len(code_content)
        })
        
    except Exception as e:
        current_app.logger.error(f"Error in upload_file: {str(e)}")
        return jsonify({'error': 'Failed to process file'}), 500

@api_bp.route('/compare', methods=['POST'])
def compare_codes():
    """
    Compare two pieces of code directly
    """
    try:
        data = request.get_json()
        
        if not data or 'code1' not in data or 'code2' not in data:
            return jsonify({'error': 'Two code snippets required'}), 400
        
        code1 = data['code1']
        code2 = data['code2']
        language = data.get('language', 'auto')
        
        # Analyze both codes
        analysis1 = code_analyzer.analyze(code1, language)
        analysis2 = code_analyzer.analyze(code2, language)
        
        # Calculate similarity
        similarity_score = similarity_detector.calculate_similarity(code1, code2, language)
        
        # Detailed comparison
        detailed_comparison = similarity_detector.detailed_comparison(code1, code2, language)
        
        response = {
            'similarity_score': similarity_score,
            'analysis1': analysis1,
            'analysis2': analysis2,
            'detailed_comparison': detailed_comparison,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        return jsonify(response)
        
    except Exception as e:
        current_app.logger.error(f"Error in compare_codes: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@api_bp.route('/supported-languages', methods=['GET'])
def get_supported_languages():
    """
    Get list of supported programming languages
    """
    languages = code_analyzer.get_supported_languages()
    return jsonify({'languages': languages})

@api_bp.route('/analyze-quality', methods=['POST'])
def analyze_code_quality():
    """
    Analyze code quality using free AI models
    """
    try:
        data = request.get_json()
        
        if not data or 'code' not in data:
            return jsonify({'error': 'Code content required'}), 400
        
        code_content = data['code']
        language = data.get('language', 'python')
        
        # Use free AI service for quality analysis
        quality_analysis = free_ai_service.analyze_code_quality(code_content, language)
        
        response = {
            'quality_analysis': quality_analysis,
            'timestamp': datetime.utcnow().isoformat(),
            'model_used': 'free_local_models'
        }
        
        return jsonify(response)
        
    except Exception as e:
        current_app.logger.error(f"Error in analyze_code_quality: {str(e)}")
        return jsonify({'error': 'Failed to analyze code quality'}), 500

@api_bp.route('/explain-code', methods=['POST'])
def explain_code():
    """
    Generate code explanation using local LLM
    """
    try:
        data = request.get_json()
        
        if not data or 'code' not in data:
            return jsonify({'error': 'Code content required'}), 400
        
        code_content = data['code']
        max_length = data.get('max_length', 150)
        
        # Load model if not already loaded
        if not local_llm_service.current_model:
            model_loaded = local_llm_service.load_model('distilgpt2')
            if not model_loaded:
                return jsonify({'error': 'Could not load local language model'}), 500
        
        # Generate explanation
        explanation = local_llm_service.generate_code_explanation(code_content, max_length)
        
        response = {
            'explanation': explanation,
            'model_used': 'distilgpt2_local',
            'timestamp': datetime.utcnow().isoformat()
        }
        
        return jsonify(response)
        
    except Exception as e:
        current_app.logger.error(f"Error in explain_code: {str(e)}")
        return jsonify({'error': 'Failed to generate explanation'}), 500

@api_bp.route('/free-models', methods=['GET'])
def get_free_models():
    """
    Get list of available free AI models for code analysis
    """
    try:
        models = free_ai_service.get_huggingface_model_suggestions()
        
        response = {
            'recommended_models': models,
            'currently_used': {
                'similarity_model': 'microsoft/unixcoder-base',
                'sentence_model': 'all-mpnet-base-v2',
                'local_llm': 'distilgpt2'
            },
            'benefits': [
                'Completely free to use',
                'No API limits or costs',
                'Can run offline',
                'Privacy-friendly (no data sent to external servers)',
                'Customizable and fine-tunable'
            ]
        }
        
        return jsonify(response)
        
    except Exception as e:
        current_app.logger.error(f"Error in get_free_models: {str(e)}")
        return jsonify({'error': 'Failed to get model information'}), 500

@api_bp.route('/statistics', methods=['GET'])
def get_statistics():
    """
    Get API usage statistics
    """
    # This would typically come from a database
    stats = {
        'total_analyses': 0,
        'languages_analyzed': {},
        'average_similarity_score': 0.0,
        'most_common_matches': []
    }
    return jsonify(stats)

@api_bp.route('/analyze-enhanced', methods=['POST'])
def analyze_code_enhanced():
    """
    Enhanced code analysis using Cohere AI for better semantic understanding
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        # Validate input
        validation_result = validate_code_input(data)
        if not validation_result['valid']:
            return jsonify({'error': validation_result['message']}), 400
        
        code_content = data.get('code')
        language = data.get('language', 'auto')
        check_database = data.get('checkDatabase', True)
        use_cohere = data.get('useCohere', True)
        
        # Analyze code structure and extract features
        analysis_result = code_analyzer.analyze(code_content, language)
        
        # Perform enhanced similarity detection with timeout handling
        try:
            if use_cohere:
                similarity_results = similarity_detector.find_similar_code_with_cohere(
                    code_content, 
                    language, 
                    check_database=check_database
                )
                
                # Get comprehensive Cohere analysis with timeout
                cohere_analysis = similarity_detector.get_cohere_code_analysis(code_content)
            else:
                # Fallback to traditional similarity detection
                similarity_results = similarity_detector.find_similar_code(
                    code_content, 
                    language, 
                    check_database=check_database
                )
                cohere_analysis = {'note': 'Cohere analysis disabled for this request'}
        except Exception as analysis_error:
            # Fallback if AI analysis fails
            current_app.logger.warning(f"AI analysis failed, falling back: {analysis_error}")
            similarity_results = similarity_detector.find_similar_code(
                code_content, 
                language, 
                check_database=check_database
            )
            cohere_analysis = {'error': f'AI analysis failed: {str(analysis_error)}', 'fallback_used': True}
        
        # Prepare enhanced response
        response = {
            'analysis': analysis_result,
            'similarity': similarity_results,
            'cohere_analysis': cohere_analysis,
            'timestamp': datetime.utcnow().isoformat(),
            'language': analysis_result.get('detected_language', language),
            'enhanced_features': {
                'semantic_understanding': use_cohere and 'error' not in cohere_analysis,
                'ai_powered_insights': True,
                'pattern_recognition': True
            }
        }
        
        # Convert numpy types to JSON-serializable types
        response = convert_numpy_types(response)
        
        return jsonify(response)
        
    except Exception as e:
        current_app.logger.error(f"Error in analyze_code_enhanced: {str(e)}")
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@api_bp.route('/cohere-analysis', methods=['POST'])
def cohere_analysis():
    """
    Get detailed Cohere AI analysis of code
    """
    try:
        data = request.get_json()
        
        if not data or 'code' not in data:
            return jsonify({'error': 'Code content is required'}), 400
        
        code_content = data.get('code')
        analysis_type = data.get('type', 'all')  # 'intent', 'patterns', 'classification', or 'all'
        
        # Get Cohere analysis
        cohere_analysis = similarity_detector.get_cohere_code_analysis(code_content)
        
        if 'error' in cohere_analysis:
            return jsonify({
                'error': 'Cohere service not available',
                'fallback_message': 'Please ensure Cohere API key is configured correctly'
            }), 503
        
        # Filter results based on requested analysis type
        if analysis_type != 'all':
            filtered_analysis = {}
            if analysis_type == 'intent' and 'intent_analysis' in cohere_analysis:
                filtered_analysis['intent_analysis'] = cohere_analysis['intent_analysis']
            elif analysis_type == 'patterns' and 'pattern_analysis' in cohere_analysis:
                filtered_analysis['pattern_analysis'] = cohere_analysis['pattern_analysis']
            elif analysis_type == 'classification' and 'classification' in cohere_analysis:
                filtered_analysis['classification'] = cohere_analysis['classification']
            
            cohere_analysis = filtered_analysis if filtered_analysis else cohere_analysis
        
        response = {
            'analysis': cohere_analysis,
            'timestamp': datetime.utcnow().isoformat(),
            'analysis_type': analysis_type,
            'powered_by': 'Cohere AI'
        }
        
        return jsonify(response)
        
    except Exception as e:
        current_app.logger.error(f"Error in cohere_analysis: {str(e)}")
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

@api_bp.route('/compare-with-cohere', methods=['POST'])
def compare_with_cohere():
    """
    Compare two code snippets using Cohere AI
    """
    try:
        data = request.get_json()
        
        if not data or 'code1' not in data or 'code2' not in data:
            return jsonify({'error': 'Both code1 and code2 are required'}), 400
        
        code1 = data.get('code1')
        code2 = data.get('code2')
        
        from services.cohere_service import CohereService
        cohere_service = CohereService()
        
        if not cohere_service.is_available():
            return jsonify({
                'error': 'Cohere service not available',
                'fallback_message': 'Please ensure Cohere API key is configured correctly'
            }), 503
        
        # Calculate similarity using Cohere
        similarity_score = cohere_service.calculate_similarity(code1, code2)
        
        if similarity_score is None:
            return jsonify({'error': 'Failed to calculate similarity'}), 500
        
        # Get analysis for both codes
        analysis1 = cohere_service.analyze_code_intent(code1)
        analysis2 = cohere_service.analyze_code_intent(code2)
        
        response = {
            'similarity_score': similarity_score,
            'similarity_percentage': f"{similarity_score * 100:.1f}%",
            'analysis': {
                'code1_analysis': analysis1,
                'code2_analysis': analysis2
            },
            'interpretation': {
                'level': 'very_high' if similarity_score > 0.85 else 
                        'high' if similarity_score > 0.7 else
                        'medium' if similarity_score > 0.5 else
                        'low',
                'description': f"The codes show {similarity_score * 100:.1f}% semantic similarity"
            },
            'timestamp': datetime.utcnow().isoformat(),
            'powered_by': 'Cohere AI'
        }
        
        return jsonify(response)
        
    except Exception as e:
        current_app.logger.error(f"Error in compare_with_cohere: {str(e)}")
        return jsonify({'error': f'Comparison failed: {str(e)}'}), 500

@api_bp.route('/batch-analyze', methods=['POST'])
def batch_analyze():
    """
    Analyze multiple code snippets in batch
    """
    try:
        data = request.get_json()
        
        if not data or 'codes' not in data or not isinstance(data['codes'], list):
            return jsonify({'error': 'Array of code snippets required'}), 400
        
        codes = data['codes']
        language = data.get('language', 'auto')
        
        if len(codes) > 20:  # Limit batch size
            return jsonify({'error': 'Maximum 20 code snippets allowed per batch'}), 400
        
        results = []
        for i, code in enumerate(codes):
            try:
                analysis = code_analyzer.analyze(code, language)
                results.append({
                    'index': i,
                    'analysis': analysis,
                    'status': 'success'
                })
            except Exception as e:
                results.append({
                    'index': i,
                    'error': str(e),
                    'status': 'failed'
                })
        
        # Calculate cross-similarities
        similarities = []
        for i in range(len(codes)):
            for j in range(i + 1, len(codes)):
                try:
                    similarity = similarity_detector.calculate_similarity(codes[i], codes[j], language)
                    similarities.append({
                        'code1_index': i,
                        'code2_index': j,
                        'similarity_score': similarity
                    })
                except Exception as e:
                    similarities.append({
                        'code1_index': i,
                        'code2_index': j,
                        'error': str(e)
                    })
        
        response = {
            'results': results,
            'cross_similarities': similarities,
            'timestamp': datetime.utcnow().isoformat(),
            'total_analyzed': len(codes)
        }
        
        return jsonify(response)
        
    except Exception as e:
        current_app.logger.error(f"Error in batch_analyze: {str(e)}")
        return jsonify({'error': 'Batch analysis failed'}), 500
