# AI-Powered Code Plagiarism Detector - Backend

Flask backend for the AI-Powered Code Plagiarism Detector.

## Features

- RESTful API for code analysis
- Multiple similarity detection algorithms
- Support for 15+ programming languages
- Semantic similarity using transformer models
- Structural and textual analysis
- Real-time code comparison

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Copy environment variables:
```bash
cp .env.example .env
```

5. Run the development server:
```bash
python app.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Health Check
- `GET /health` - Check API status

### Code Analysis
- `POST /api/analyze` - Analyze code for similarities
- `POST /api/upload` - Upload code file for analysis
- `POST /api/compare` - Compare two code snippets
- `GET /api/supported-languages` - Get supported languages
- `GET /api/statistics` - Get usage statistics

## API Usage Examples

### Analyze Code
```bash
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def hello_world():\n    print(\"Hello, World!\")",
    "language": "python",
    "checkDatabase": true
  }'
```

### Compare Two Code Snippets
```bash
curl -X POST http://localhost:5000/api/compare \
  -H "Content-Type: application/json" \
  -d '{
    "code1": "def sort_list(arr):\n    return sorted(arr)",
    "code2": "def sort_array(array):\n    return sorted(array)",
    "language": "python"
  }'
```

## Deployment

### Local Development
The development server runs on port 5000 by default:
```bash
python app.py
```

### Production with Gunicorn
For production deployment (uses PORT environment variable, defaults to 5000):
```bash
# Local production testing
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Cloud deployment (uses $PORT environment variable)
gunicorn -w 4 -b 0.0.0.0:$PORT app:app
```

## Environment Variables

- `SECRET_KEY` - Flask secret key
- `FLASK_ENV` - Environment (development/production)
- `PORT` - Server port (default: 5000 for local, 10000 for Render)
- `SIMILARITY_THRESHOLD` - Minimum similarity threshold
- `MODEL_NAME` - Transformer model name
- `CORS_ORIGINS` - Allowed CORS origins

## Supported Languages

- Python
- JavaScript/TypeScript
- Java
- C/C++
- C#
- PHP
- Ruby
- Go
- Rust
- Swift
- Kotlin
- And more...

## License

MIT License
