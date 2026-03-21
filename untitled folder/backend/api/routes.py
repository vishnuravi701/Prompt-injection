"""
API Routes - Analysis and testing endpoints
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import logging

from backend.services.model_service import get_model_service
from backend.services.gemini_service import get_gemini_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["Analysis"])


# Request/Response Models
class AnalyzePromptRequest(BaseModel):
    prompt: str


class AnalyzeResponse(BaseModel):
    is_injection: bool
    confidence: float
    risk_score: float
    explanation: str
    model_status: str


class TestVulnerabilityRequest(BaseModel):
    prompt: str
    system_instruction: str = None


class TestVulnerabilityResponse(BaseModel):
    success: bool
    response: str
    vulnerability_detected: bool
    analysis: str
    error: str = None


class FixSuggestionsResponse(BaseModel):
    success: bool
    fixes: list
    improved_prompt: str
    explanation: str
    error: str = None


# Endpoints

@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_prompt(request: AnalyzePromptRequest):
    """
    Analyze a prompt to detect potential injection attacks
    """
    try:
        if not request.prompt or len(request.prompt.strip()) == 0:
            raise HTTPException(status_code=400, detail="Prompt cannot be empty")
        
        model_service = get_model_service()
        result = model_service.predict(request.prompt)
        
        return AnalyzeResponse(**result)
    
    except Exception as e:
        logger.error(f"Error analyzing prompt: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/test-vulnerable", response_model=TestVulnerabilityResponse)
async def test_prompt_vulnerability(request: TestVulnerabilityRequest):
    """
    Test a vulnerable prompt with Gemini to see the actual impact
    """
    try:
        if not request.prompt or len(request.prompt.strip()) == 0:
            raise HTTPException(status_code=400, detail="Prompt cannot be empty")
        
        gemini_service = get_gemini_service()
        result = gemini_service.test_prompt_vulnerability(
            prompt=request.prompt,
            system_instruction=request.system_instruction
        )
        
        return TestVulnerabilityResponse(**result)
    
    except Exception as e:
        logger.error(f"Error testing vulnerability: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/fix-prompt", response_model=FixSuggestionsResponse)
async def get_fix_suggestions(request: AnalyzePromptRequest):
    """
    Get suggestions to fix a vulnerable prompt
    """
    try:
        if not request.prompt or len(request.prompt.strip()) == 0:
            raise HTTPException(status_code=400, detail="Prompt cannot be empty")
        
        gemini_service = get_gemini_service()
        result = gemini_service.get_fix_suggestions(request.prompt)
        
        return FixSuggestionsResponse(**result)
    
    except Exception as e:
        logger.error(f"Error getting fix suggestions: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/test-improved-prompt", response_model=TestVulnerabilityResponse)
async def test_improved_prompt(request: TestVulnerabilityRequest):
    """
    Test an improved prompt to verify the fix works
    """
    try:
        if not request.prompt or len(request.prompt.strip()) == 0:
            raise HTTPException(status_code=400, detail="Prompt cannot be empty")
        
        gemini_service = get_gemini_service()
        result = gemini_service.test_prompt_vulnerability(
            prompt=request.prompt,
            system_instruction=request.system_instruction
        )
        
        return TestVulnerabilityResponse(**result)
    
    except Exception as e:
        logger.error(f"Error testing improved prompt: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
