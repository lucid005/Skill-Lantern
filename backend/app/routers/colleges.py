"""
Colleges Router - College Recommendation Endpoints
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
import logging

from app.models.schemas import (
    CollegeRequest,
    CollegeRecommendationResponse,
    CollegeInfo,
    ErrorResponse,
    DegreeLevel,
    BudgetRange
)
from app.services.college_service import college_service
from app.services.recommendation_service import recommendation_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/colleges", tags=["College Recommendations"])


@router.post(
    "/recommend",
    response_model=CollegeRecommendationResponse,
    responses={500: {"model": ErrorResponse}}
)
async def recommend_colleges(request: CollegeRequest):
    """
    Get college recommendations based on career and preferences.
    
    Uses Nepal college data and LLM to provide:
    - Top recommended colleges
    - Relevant programs offered
    - Reasons for recommendation
    - Alternative options
    """
    try:
        recommendations = await recommendation_service.get_college_recommendations(request)
        return recommendations
        
    except Exception as e:
        logger.error(f"College recommendation failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get college recommendations: {str(e)}"
        )


@router.get("/list")
async def list_colleges(
    location: Optional[str] = Query(None, description="Filter by location"),
    program: Optional[str] = Query(None, description="Filter by program keyword"),
    university: Optional[str] = Query(None, description="Filter by university"),
    limit: int = Query(50, ge=1, le=200, description="Maximum results")
):
    """
    List colleges with optional filters.
    Returns raw college data from CSV.
    """
    try:
        # Ensure data is loaded
        if not college_service.loaded:
            college_service.load_data()
        
        colleges = college_service.filter_colleges(
            location=location,
            university=university,
            program_keyword=program
        )
        
        # Limit results
        colleges = colleges[:limit]
        
        # Convert to response format
        result = []
        for college in colleges:
            result.append({
                "name": college.get("College", "Unknown"),
                "location": college.get("Location", "N/A"),
                "university": college.get("University", "N/A"),
                "programs": college.get("Course Offered", "")[:500],
                "ownership_type": college.get("Ownership Type", "N/A"),
                "phone": college.get("Phone Number", ""),
                "email": college.get("Email", "")
            })
        
        return {
            "total": len(result),
            "colleges": result
        }
        
    except Exception as e:
        logger.error(f"Failed to list colleges: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/locations", response_model=List[str])
async def get_locations():
    """Get list of unique locations from college data."""
    try:
        if not college_service.loaded:
            college_service.load_data()
        
        return college_service.get_locations()
        
    except Exception as e:
        logger.error(f"Failed to get locations: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/universities", response_model=List[str])
async def get_universities():
    """Get list of universities from college data."""
    try:
        if not college_service.loaded:
            college_service.load_data()
        
        return college_service.get_universities()
        
    except Exception as e:
        logger.error(f"Failed to get universities: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/for-career/{career_name}")
async def get_colleges_for_career(
    career_name: str,
    limit: int = Query(10, ge=1, le=50)
):
    """
    Get colleges offering programs relevant to a specific career.
    """
    try:
        if not college_service.loaded:
            college_service.load_data()
        
        colleges = college_service.get_colleges_for_career(career_name)[:limit]
        
        return {
            "career": career_name,
            "total": len(colleges),
            "colleges": [
                {
                    "name": c.get("College", "Unknown"),
                    "location": c.get("Location", "N/A"),
                    "university": c.get("University", "N/A"),
                    "programs": c.get("Course Offered", "")[:300]
                }
                for c in colleges
            ]
        }
        
    except Exception as e:
        logger.error(f"Failed to get colleges for career: {e}")
        raise HTTPException(status_code=500, detail=str(e))
