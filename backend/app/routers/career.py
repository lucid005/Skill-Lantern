"""
Career Router - Career Prediction Endpoints
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List
import logging

from app.models.schemas import (
    CareerPredictionRequest,
    CareerPredictionResponse,
    PredictedCareer,
    ErrorResponse
)
from app.models.career_predictor import career_predictor

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/career", tags=["Career Prediction"])


@router.post(
    "/predict",
    response_model=CareerPredictionResponse,
    responses={500: {"model": ErrorResponse}}
)
async def predict_career(
    request: CareerPredictionRequest,
    use_llm: bool = Query(
        default=True,
        description="Use Gemini LLM to refine predictions (slower but more accurate)"
    )
):
    """
    Predict suitable careers based on user profile.
    
    Uses a hybrid approach:
    1. XGBoost model (if available) or weighted rule-based matching for fast initial predictions
    2. Gemini LLM refinement for contextual accuracy (when use_llm=true)
    
    Set use_llm=false for instant predictions without LLM (less accurate).
    """
    try:
        # Get predictions — use LLM refinement if requested
        if use_llm:
            predictions = await career_predictor.predict_with_llm(
                user_profile=request.user_profile,
                top_n=5
            )
        else:
            predictions = career_predictor.predict(
                user_profile=request.user_profile,
                top_n=5
            )
        
        # Build user profile summary
        profile_summary = {
            "education": request.user_profile.education_level.value,
            "skills_count": len(request.user_profile.skills),
            "interests_count": len(request.user_profile.interests),
            "specialization": request.user_profile.specialization,
            "prediction_method": "hybrid_llm" if use_llm else "model_only"
        }
        
        return CareerPredictionResponse(
            predictions=predictions,
            user_profile_summary=profile_summary,
            message="Career predictions generated successfully"
        )
        
    except Exception as e:
        logger.error(f"Career prediction failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate career predictions: {str(e)}"
        )


@router.get("/categories", response_model=List[str])
async def get_career_categories():
    """Get list of all available career categories."""
    from app.models.career_predictor import CAREER_CATEGORIES
    return CAREER_CATEGORIES


@router.get("/insights/{career_name}")
async def get_career_insights(career_name: str):
    """Get insights about a specific career."""
    try:
        insights = career_predictor.get_career_insights(career_name)
        return insights
    except Exception as e:
        logger.error(f"Failed to get career insights: {e}")
        raise HTTPException(status_code=500, detail=str(e))
