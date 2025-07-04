import sys
import os

# Add the project root to sys.path to ensure imports work
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

try:
    from app.main import app
    from fastapi.middleware.cors import CORSMiddleware

    # Configure CORS for Render deployment
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["https://ai-plagiarism-detector-web.onrender.com", "http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # No need for Mangum with Render (that's for AWS Lambda/Vercel)
    # Just use the app directly
    
except Exception as import_error:
    # Create a simple FastAPI app for diagnostics if imports fail
    from fastapi import FastAPI
    
    app = FastAPI(title="Backup API")
    
    @app.get("/")
    def read_root():
        return {"message": "Import error in Render deployment", "error": "Application initialization failed"}
    
    @app.get("/debug")
    def debug():
        return {
            "sys.path": sys.path,
            "cwd": os.getcwd(),
            "listdir": os.listdir("."),
            "env": dict(os.environ)
        }