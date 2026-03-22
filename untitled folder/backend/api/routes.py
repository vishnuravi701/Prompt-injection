"""
API Routes - Analysis and testing endpoints
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import logging
from typing import Optional

from backend.services.model_service import get_model_service
from backend.services.gemini_service import get_gemini_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["Analysis"])


# Request/Response Models
class AnalyzePromptRequest(BaseModel):
    prompt: str
    system_instruction: Optional[str] = None


class AnalyzeResponse(BaseModel):
    is_injection: bool
    confidence: float
    risk_score: float
    explanation: str
    model_status: str
    attack_type: str
    llm_response: str
    llm_warning: Optional[str] = None
    api_success: bool
    api_error: Optional[str] = None


class TestVulnerabilityRequest(BaseModel):
    prompt: str
    system_instruction: str = None


class TestVulnerabilityResponse(BaseModel):
    success: bool
    response: str
    vulnerability_detected: bool
    analysis: str
    error: Optional[str] = None


class FixSuggestionsResponse(BaseModel):
    success: bool
    fixes: list
    improved_prompt: str
    explanation: str
    error: Optional[str] = None


# Endpoints

@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_prompt(request: AnalyzePromptRequest):
    """
    Stage 1: Detect prompt injection locally. Stage 2: Conditionally call LLM API.
    """
    try:
        if not request.prompt or len(request.prompt.strip()) == 0:
            raise HTTPException(status_code=400, detail="Prompt cannot be empty")

        model_service = get_model_service()
        detection = model_service.predict(request.prompt)

        attack_type = "prompt_injection" if detection["is_injection"] else "safe"
        llm_warning = None
        if detection["is_injection"]:
            llm_warning = "injection detected — showing simulated + sanitized response"

        gemini_service = get_gemini_service()
        llm_result = gemini_service.generate_llm_response(
            user_prompt=request.prompt,
            is_injection=detection["is_injection"],
            attack_type=attack_type,
            confidence=detection["confidence"],
            system_instruction=request.system_instruction
        )

        api_success = llm_result.get("success", False)
        api_error = llm_result.get("error")
        llm_response_value = llm_result.get("response", "")

        if not api_success and "API_KEY_INVALID" in str(api_error):
            llm_warning = "Invalid Gemini API key. Please check your GEMINI_API_KEY in the .env file and ensure it's a valid Google AI API key with Generative AI API enabled."
            llm_response_value = "Stage 2 failed due to invalid API key. Prompt injection result is available from Stage 1."
            api_success = False
        elif not api_success and "not found" in str(api_error).lower():
            llm_warning = "Gemini model not available. The API key may not have access to the requested model, or the model name may be incorrect."
            llm_response_value = "Stage 2 failed due to model availability. Prompt injection result is available from Stage 1."
            api_success = False
        elif not api_success and api_error == "Gemini API not configured":
            llm_warning = "Gemini API not configured; set GEMINI_API_KEY in backend .env to enable Stage 2 external response."
            llm_response_value = "Stage 2 skipped due to missing Gemini API key. Prompt injection result is available from Stage 1."
            api_success = False
        elif not api_success:
            llm_warning = f"Gemini API error: {api_error}"
            llm_response_value = "Stage 2 failed with API error. Prompt injection result is available from Stage 1."
            api_success = False

        return AnalyzeResponse(
            is_injection=detection["is_injection"],
            confidence=detection["confidence"],
            risk_score=detection["risk_score"],
            explanation=detection["explanation"],
            model_status=detection["model_status"],
            attack_type=attack_type,
            llm_response=llm_response_value,
            llm_warning=llm_warning,
            api_success=api_success,
            api_error=api_error
        )

    except HTTPException:
        raise
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
