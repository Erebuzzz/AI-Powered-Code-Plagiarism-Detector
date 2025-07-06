from typing import Dict, Any

def validate_code_input(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate code input data
    """
    result = {'valid': True, 'message': ''}
    
    if 'code' not in data:
        return {'valid': False, 'message': 'Code field is required'}
    
    code = data['code']
    
    if not isinstance(code, str):
        return {'valid': False, 'message': 'Code must be a string'}
    
    if not code.strip():
        return {'valid': False, 'message': 'Code cannot be empty'}
    
    if len(code) > 100000:  # 100KB limit
        return {'valid': False, 'message': 'Code is too large (max 100KB)'}
    
    # Check for minimum meaningful content
    meaningful_lines = [line.strip() for line in code.split('\n') if line.strip() and not line.strip().startswith('#')]
    if len(meaningful_lines) < 3:
        return {'valid': False, 'message': 'Code must contain at least 3 meaningful lines'}
    
    return result

def allowed_file(filename: str) -> bool:
    """
    Check if file type is allowed
    """
    allowed_extensions = {
        '.py', '.js', '.jsx', '.ts', '.tsx', '.java', '.cpp', '.cc', '.cxx', 
        '.c', '.cs', '.php', '.rb', '.go', '.rs', '.swift', '.kt', '.scala',
        '.r', '.m', '.pl', '.sh', '.sql', '.html', '.css', '.xml', '.json'
    }
    
    return any(filename.lower().endswith(ext) for ext in allowed_extensions)

def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename for safe storage
    """
    import re
    # Remove or replace dangerous characters
    sanitized = re.sub(r'[^\w\-_\.]', '_', filename)
    # Limit length
    if len(sanitized) > 255:
        name, ext = sanitized.rsplit('.', 1)
        sanitized = name[:255-len(ext)-1] + '.' + ext
    
    return sanitized

def get_file_language(filename: str) -> str:
    """
    Determine programming language from file extension
    """
    extension_map = {
        '.py': 'python',
        '.js': 'javascript',
        '.jsx': 'javascript',
        '.ts': 'typescript',
        '.tsx': 'typescript',
        '.java': 'java',
        '.cpp': 'cpp',
        '.cc': 'cpp',
        '.cxx': 'cpp',
        '.c': 'c',
        '.cs': 'csharp',
        '.php': 'php',
        '.rb': 'ruby',
        '.go': 'go',
        '.rs': 'rust',
        '.swift': 'swift',
        '.kt': 'kotlin',
        '.scala': 'scala',
        '.r': 'r',
        '.m': 'matlab',
        '.pl': 'perl',
        '.sh': 'bash',
        '.sql': 'sql'
    }
    
    for ext, lang in extension_map.items():
        if filename.lower().endswith(ext):
            return lang
    
    return 'unknown'
