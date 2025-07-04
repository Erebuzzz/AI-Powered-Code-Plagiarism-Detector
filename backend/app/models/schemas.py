from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime

class CodeSubmission(BaseModel):
    content: str
    language: str
    filename: str
    
class SimilarityScore(BaseModel):
    structural_similarity: float
    semantic_similarity: float
    overall_similarity: float
    
class ComparisonResult(BaseModel):
    submission1: CodeSubmission
    submission2: CodeSubmission
    similarity_score: SimilarityScore
    similar_blocks: List[Dict]
    analysis_time: float
    timestamp: datetime
    
class UploadResponse(BaseModel):
    message: str
    files: List[Dict]
    count: int
