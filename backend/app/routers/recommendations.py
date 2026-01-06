"""
Recommendations Router - Full Career Guidance Endpoints
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
import json
import logging

from app.models.schemas import (
    FullRecommendationRequest,
    FullRecommendationResponse,
    CareerPredictionRequest,
    ErrorResponse
)
from app.models.career_predictor import career_predictor
from app.services.recommendation_service import recommendation_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/recommendations", tags=["Full Recommendations"])


@router.post(
    "/full",
    response_model=FullRecommendationResponse,
    responses={500: {"model": ErrorResponse}}
)
async def get_full_recommendation(request: FullRecommendationRequest):
    """
    Get complete career guidance including:
    
    1. **Career Prediction** - Top careers based on profile
    2. **Career Roadmap** - Step-by-step learning path
    3. **College Recommendations** - Best colleges in Nepal
    4. **Summary & Next Steps** - Actionable guidance
    
    This is the main endpoint for complete career assessment.
    """
    try:
        # Step 1: Predict careers
        predicted_careers = career_predictor.predict(
            user_profile=request.user_profile,
            top_n=5
        )
        
        if not predicted_careers:
            raise HTTPException(
                status_code=400,
                detail="Could not generate career predictions. Please provide more information."
            )
        
        # Step 2: Generate full recommendation
        recommendation = await recommendation_service.generate_full_recommendation(
            predicted_careers=predicted_careers,
            request=request
        )
        
        return recommendation
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Full recommendation failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate recommendations: {str(e)}"
        )


@router.post("/quick")
async def get_quick_recommendation(request: CareerPredictionRequest):
    """
    Get quick career recommendation without full roadmap/college details.
    
    Faster response for initial career suggestions.
    """
    try:
        # Get career predictions
        predictions = career_predictor.predict(
            user_profile=request.user_profile,
            top_n=3
        )
        
        # Get basic insights for top career
        top_career = predictions[0].career if predictions else "Software Developer"
        insights = career_predictor.get_career_insights(top_career)
        
        return {
            "predictions": [p.model_dump() for p in predictions],
            "top_career": top_career,
            "insights": insights,
            "message": "Use /recommendations/full for complete guidance including roadmap and colleges"
        }
        
    except Exception as e:
        logger.error(f"Quick recommendation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/stream")
async def stream_recommendation(request: FullRecommendationRequest):
    """
    Stream the full recommendation generation.
    
    Returns Server-Sent Events (SSE) with progress updates.
    """
    async def generate():
        try:
            # Step 1: Career Prediction
            yield f"data: {json.dumps({'step': 'predicting', 'message': 'Analyzing your profile...'})}\n\n"
            
            predictions = career_predictor.predict(
                user_profile=request.user_profile,
                top_n=5
            )
            
            yield f"data: {json.dumps({'step': 'predicted', 'careers': [p.model_dump() for p in predictions]})}\n\n"
            
            # Step 2: Generate Roadmap
            yield f"data: {json.dumps({'step': 'roadmap', 'message': 'Generating career roadmap...'})}\n\n"
            
            # Step 3: College Recommendations
            yield f"data: {json.dumps({'step': 'colleges', 'message': 'Finding best colleges...'})}\n\n"
            
            # Step 4: Full recommendation
            recommendation = await recommendation_service.generate_full_recommendation(
                predicted_careers=predictions,
                request=request
            )
            
            yield f"data: {json.dumps({'step': 'complete', 'data': recommendation.model_dump()})}\n\n"
            yield "data: [DONE]\n\n"
            
        except Exception as e:
            logger.error(f"Stream recommendation failed: {e}")
            yield f"data: {json.dumps({'step': 'error', 'error': str(e)})}\n\n"
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive"
        }
    )
