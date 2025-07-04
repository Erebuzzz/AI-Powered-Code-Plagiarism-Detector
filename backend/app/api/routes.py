from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
from typing import List, Optional
from app.services.plagiarism_detector import PlagiarismDetector
from app.services.code_processor import CodeProcessor
from app.models.schemas import ComparisonResult, CodeSubmission
import tempfile
import os

router = APIRouter()

@router.post("/upload", response_model=dict)
async def upload_code(
    files: List[UploadFile] = File(...),
    language: str = Form(...)
):
    """Upload code files for plagiarism detection"""
    try:
        code_processor = CodeProcessor()
        uploaded_files = []
        
        for file in files:
            # Validate file size
            content = await file.read()
            if len(content) > 1024 * 1024:  # 1MB limit
                raise HTTPException(status_code=413, detail="File too large")
            
            # Process the file
            processed_content = code_processor.preprocess_code(content.decode('utf-8'), language)
            
            uploaded_files.append({
                "filename": file.filename,
                "content": processed_content,
                "language": language,
                "size": len(content)
            })
        
        return {
            "message": "Files uploaded successfully",
            "files": uploaded_files,
            "count": len(uploaded_files)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/compare", response_model=ComparisonResult)
async def compare_code(
    code1: str = Form(...),
    code2: str = Form(...),
    language: str = Form(...),
    filename1: str = Form("file1.py"),
    filename2: str = Form("file2.py")
):
    """Compare two code snippets for plagiarism"""
    try:
        detector = PlagiarismDetector()
        
        # Create code submissions
        submission1 = CodeSubmission(
            content=code1,
            language=language,
            filename=filename1
        )
        submission2 = CodeSubmission(
            content=code2,
            language=language,
            filename=filename2
        )
        
        # Perform comparison
        result = await detector.compare_code(submission1, submission2)
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/report/{comparison_id}")
async def get_report(comparison_id: str):
    """Generate and download comparison report"""
    try:
        # This would typically retrieve from database
        # For now, return a placeholder
        return {
            "comparison_id": comparison_id,
            "report_url": f"/reports/{comparison_id}.pdf",
            "generated_at": "2024-01-01T00:00:00Z"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/languages")
async def get_supported_languages():
    """Get list of supported programming languages"""
    return {
        "languages": [
            {"code": "python", "name": "Python"},
            {"code": "javascript", "name": "JavaScript"},
            {"code": "java", "name": "Java"},
            {"code": "cpp", "name": "C++"},
            {"code": "c", "name": "C"},
            {"code": "csharp", "name": "C#"}
        ]
    }
