"""
Career listing endpoints
"""

from fastapi import APIRouter, Request
from typing import List, Optional

router = APIRouter()


@router.get("/careers")
async def list_careers(
    request: Request,
    category: Optional[str] = None
):
    """
    Get list of all available careers
    
    Args:
        category: Optional filter by category (Technology, Healthcare, etc.)
    """
    career_matcher = request.app.state.career_matcher
    careers = career_matcher.get_all_careers()
    
    if category:
        careers = [c for c in careers if c.get("category", "").lower() == category.lower()]
    
    return {
        "total": len(careers),
        "careers": careers,
    }


@router.get("/careers/{career_id}")
async def get_career_details(
    request: Request,
    career_id: str
):
    """
    Get detailed information about a specific career
    
    Args:
        career_id: Career identifier (e.g., 'software_engineer')
    """
    career_matcher = request.app.state.career_matcher
    career = career_matcher.get_career_details(career_id)
    
    if not career:
        return {"error": "Career not found"}
    
    return career


@router.get("/careers/categories/list")
async def list_categories(request: Request):
    """Get list of all career categories"""
    career_matcher = request.app.state.career_matcher
    categories = career_matcher.get_categories()
    
    return {
        "categories": categories,
    }


@router.get("/features")
async def list_features(request: Request):
    """Get list of all skills and interests used for matching"""
    career_matcher = request.app.state.career_matcher
    features = career_matcher.get_features()
    
    return features
