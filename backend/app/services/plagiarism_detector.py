import asyncio
import time
from typing import Dict, List
from datetime import datetime
from app.models.schemas import CodeSubmission, ComparisonResult, SimilarityScore
from app.services.code_processor import CodeProcessor
from app.services.ai_analyzer import AIAnalyzer

class PlagiarismDetector:
    """Main plagiarism detection service"""
    
    def __init__(self):
        self.code_processor = CodeProcessor()
        self.ai_analyzer = AIAnalyzer()
    
    async def compare_code(self, submission1: CodeSubmission, submission2: CodeSubmission) -> ComparisonResult:
        """Compare two code submissions for plagiarism"""
        start_time = time.time()
        
        # Preprocess both code snippets
        processed_code1 = self.code_processor.preprocess_code(
            submission1.content, 
            submission1.language
        )
        processed_code2 = self.code_processor.preprocess_code(
            submission2.content, 
            submission2.language
        )
        
        # Calculate structural similarity
        structural_sim = self.code_processor.calculate_structural_similarity(
            processed_code1, 
            processed_code2
        )
        
        # Calculate semantic similarity using AI
        semantic_sim = await self.ai_analyzer.calculate_semantic_similarity(
            processed_code1, 
            processed_code2, 
            submission1.language
        )
        
        # Calculate overall similarity
        overall_sim = (structural_sim + semantic_sim) / 2
        
        # Find similar blocks
        similar_blocks = self._find_similar_blocks(
            submission1.content, 
            submission2.content
        )
        
        # Create similarity score
        similarity_score = SimilarityScore(
            structural_similarity=structural_sim,
            semantic_similarity=semantic_sim,
            overall_similarity=overall_sim
        )
        
        analysis_time = time.time() - start_time
        
        return ComparisonResult(
            submission1=submission1,
            submission2=submission2,
            similarity_score=similarity_score,
            similar_blocks=similar_blocks,
            analysis_time=analysis_time,
            timestamp=datetime.now()
        )
    
    def _find_similar_blocks(self, code1: str, code2: str) -> List[Dict]:
        """Find similar code blocks between two snippets"""
        # This is a simplified implementation
        # In practice, you'd use more sophisticated algorithms
        similar_blocks = []
        
        lines1 = code1.split('\n')
        lines2 = code2.split('\n')
        
        # Find common subsequences
        for i, line1 in enumerate(lines1):
            for j, line2 in enumerate(lines2):
                if line1.strip() == line2.strip() and len(line1.strip()) > 10:
                    similar_blocks.append({
                        'line1': i + 1,
                        'line2': j + 1,
                        'content': line1.strip(),
                        'similarity': 1.0
                    })
        
        return similar_blocks
    
    async def batch_compare(self, submissions: List[CodeSubmission]) -> List[ComparisonResult]:
        """Compare multiple submissions for plagiarism"""
        results = []
        
        for i in range(len(submissions)):
            for j in range(i + 1, len(submissions)):
                result = await self.compare_code(submissions[i], submissions[j])
                results.append(result)
        
        return results
