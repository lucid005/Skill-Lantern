"""
Career Router - Career Prediction Endpoints
"""

from fastapi import APIRouter, HTTPException
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
async def predict_career(request: CareerPredictionRequest):
    """
    Predict suitable careers based on user profile.
    
    Uses XGBoost model (if available) or rule-based matching
    to suggest top careers based on skills, interests, and education.
    """
    try:
        # Get predictions
        predictions = career_predictor.predict(
            user_profile=request.user_profile,
            top_n=5
        )
        
        # Build user profile summary
        profile_summary = {
            "education": request.user_profile.education_level.value,
            "skills_count": len(request.user_profile.skills),
            "interests_count": len(request.user_profile.interests),
            "specialization": request.user_profile.specialization
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
