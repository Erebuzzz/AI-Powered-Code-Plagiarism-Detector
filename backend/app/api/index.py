import sys
import os

# Add the project root to sys.path to ensure imports work
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

try:
    from app.main import app
    from fastapi.middleware.cors import CORSMiddleware

    # Configure CORS for Vercel
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["https://ai-plagiarism-detector-web.onrender.com", "http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # This is needed for Vercel serverless functions
    from mangum import Mangum
    handler = Mangum(app)
    
except Exception as e:  # Added "as e" to properly capture the exception
    # Create a simple FastAPI app for diagnostics if imports fail
    from fastapi import FastAPI
    from mangum import Mangum
    
    app = FastAPI(title="Backup API")
    
    @app.get("/")
    def read_root():
        return {"message": "Import error in Vercel deployment", "error": str(e)}
    
    @app.get("/debug")
    def debug():
        return {
            "sys.path": sys.path,
            "cwd": os.getcwd(),
            "listdir": os.listdir("."),
            "env": dict(os.environ)
        }
    
    handler = Mangum(app)