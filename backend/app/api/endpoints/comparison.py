from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
import json
import asyncio
import traceback

from app.models.database import get_db, CodeComparison
from app.services.ai_service import ai_service
from app.schemas.comparison import ComparisonRequest, ComparisonResponse, FileUploadResponse
from app.core.config import settings

router = APIRouter()

@router.post("/compare", response_model=ComparisonResponse)
async def compare_code(
    request: ComparisonRequest,
    db: Session = Depends(get_db)
):
    """Compare two code snippets provided directly"""
    
    try:
        # Validate input
        if not request.code1.strip() or not request.code2.strip():
            raise HTTPException(status_code=400, detail="Both code snippets must be provided")
        
        # Validate languages
        if request.language1 not in settings.SUPPORTED_LANGUAGES or request.language2 not in settings.SUPPORTED_LANGUAGES:
            raise HTTPException(status_code=400, detail="Unsupported programming language")
        
        print(f"Comparing code in {request.language1} vs {request.language2}")
        
        # Perform comparison
        similarity_result = ai_service.calculate_similarity(
            request.code1, request.code2, request.language1, request.language2
        )
        
        print(f"Similarity result: {similarity_result}")
        
        # Get AI explanation
        explanation = await ai_service.get_ai_explanation(
            request.code1, request.code2, similarity_result["semantic_similarity"]
        )
        
        # Save to database
        comparison = CodeComparison(
            file1_name="code_snippet_1",
            file1_content=request.code1,
            file1_language=request.language1,
            file2_name="code_snippet_2",
            file2_content=request.code2,
            file2_language=request.language2,
            similarity_score=similarity_result["semantic_similarity"],
            analysis_result=json.dumps({**similarity_result, "explanation": explanation}),
            is_plagiarized=similarity_result["is_plagiarized"]
        )
        
        db.add(comparison)
        db.commit()
        db.refresh(comparison)
        
        return ComparisonResponse(
            comparison_id=comparison.id,
            similarity_score=similarity_result["semantic_similarity"],
            is_plagiarized=similarity_result["is_plagiarized"],
            explanation=explanation,
            lexical_similarity=similarity_result["lexical_similarity"],
            analysis=similarity_result["analysis"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in compare_code: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.post("/upload", response_model=FileUploadResponse)
async def upload_files(
    file1: UploadFile = File(...),
    file2: UploadFile = File(...),
    language1: str = Form(...),
    language2: str = Form(...),
    db: Session = Depends(get_db)
):
    """Upload two files for comparison"""
    
    try:
        # Validate file sizes
        if file1.size and file1.size > settings.MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail="File 1 size too large")
        if file2.size and file2.size > settings.MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail="File 2 size too large")
        
        # Validate languages
        if language1 not in settings.SUPPORTED_LANGUAGES or language2 not in settings.SUPPORTED_LANGUAGES:
            raise HTTPException(status_code=400, detail="Unsupported programming language")
        
        # Read file contents
        content1 = await file1.read()
        content2 = await file2.read()
        
        # Decode contents
        try:
            code1 = content1.decode('utf-8')
            code2 = content2.decode('utf-8')
        except UnicodeDecodeError:
            raise HTTPException(status_code=400, detail="Invalid file encoding. Please upload text files.")
        
        # Perform comparison
        similarity_result = ai_service.calculate_similarity(code1, code2, language1, language2)
        
        # Get AI explanation
        explanation = await ai_service.get_ai_explanation(code1, code2, similarity_result["semantic_similarity"])
        
        # Save to database
        comparison = CodeComparison(
            file1_name=file1.filename or "uploaded_file_1",
            file1_content=code1,
            file1_language=language1,
            file2_name=file2.filename or "uploaded_file_2",
            file2_content=code2,
            file2_language=language2,
            similarity_score=similarity_result["semantic_similarity"],
            analysis_result=json.dumps({**similarity_result, "explanation": explanation}),
            is_plagiarized=similarity_result["is_plagiarized"]
        )
        
        db.add(comparison)
        db.commit()
        db.refresh(comparison)
        
        return FileUploadResponse(
            comparison_id=comparison.id,
            message="Files uploaded and analyzed successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in upload_files: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/report/{comparison_id}")
async def get_comparison_report(
    comparison_id: int,
    db: Session = Depends(get_db)
):
    """Get detailed comparison report"""
    
    try:
        comparison = db.query(CodeComparison).filter(CodeComparison.id == comparison_id).first()
        if not comparison:
            raise HTTPException(status_code=404, detail="Comparison not found")
        
        analysis_result = json.loads(comparison.analysis_result)
        
        return {
            "comparison_id": comparison.id,
            "file1_name": comparison.file1_name,
            "file2_name": comparison.file2_name,
            "similarity_score": comparison.similarity_score,
            "is_plagiarized": comparison.is_plagiarized,
            "created_at": comparison.created_at,
            "analysis": analysis_result,
            "code1": comparison.file1_content,
            "code2": comparison.file2_content,
            "language1": comparison.file1_language,
            "language2": comparison.file2_language
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in get_comparison_report: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/history")
async def get_comparison_history(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get recent comparison history"""
    
    try:
        comparisons = db.query(CodeComparison).order_by(CodeComparison.created_at.desc()).limit(limit).all()
        
        return [
            {
                "id": comp.id,
                "file1_name": comp.file1_name,
                "file2_name": comp.file2_name,
                "similarity_score": comp.similarity_score,
                "is_plagiarized": comp.is_plagiarized,
                "created_at": comp.created_at
            }
            for comp in comparisons
        ]
    except Exception as e:
        print(f"Error in get_comparison_history: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")