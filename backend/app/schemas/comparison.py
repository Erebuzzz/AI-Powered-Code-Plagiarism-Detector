from pydantic import BaseModel
from typing import Dict, Any, Optional
from datetime import datetime

class ComparisonRequest(BaseModel):
    code1: str
    code2: str
    language1: str
    language2: str

class ComparisonResponse(BaseModel):
    comparison_id: int
    similarity_score: float
    is_plagiarized: bool
    explanation: str
    lexical_similarity: float
    analysis: Dict[str, Any]

class FileUploadResponse(BaseModel):
    comparison_id: int
    message: str

class ComparisonHistory(BaseModel):
    id: int
    file1_name: str
    file2_name: str
    similarity_score: float
    is_plagiarized: bool
    created_at: datetime