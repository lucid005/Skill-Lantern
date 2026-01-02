"""
Career prediction endpoints
"""

from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, List, Optional

router = APIRouter()


class UserProfile(BaseModel):
    """User profile data for career prediction"""
    
    # Academic scores (0-100)
    math_score: float = Field(..., ge=0, le=100, description="Math score (0-100)")
    science_score: float = Field(..., ge=0, le=100, description="Science score (0-100)")
    english_score: float = Field(..., ge=0, le=100, description="English score (0-100)")
    
    # GPA (0-4.0)
    gpa: float = Field(..., ge=0, le=4.0, description="GPA (0-4.0)")
    
    # Skills (1-5 scale)
    skills: Dict[str, int] = Field(
        ...,
        description="Skills with ratings (1-5). e.g., {'programming': 4, 'communication': 3}"
    )
    
    # Interests (1-5 scale)
    interests: Dict[str, int] = Field(
        ...,
        description="Interests with ratings (1-5). e.g., {'technology': 5, 'arts': 2}"
    )
    
    # Optional additional info
    academic_level: Optional[str] = Field(
        default="undergraduate",
        description="Academic level: 'high_school', 'undergraduate', 'graduate'"
    )
    
    certifications: Optional[List[str]] = Field(
        default=[],
        description="List of certifications"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "math_score": 85,
                "science_score": 90,
                "english_score": 75,
                "gpa": 3.7,
                "skills": {
                    "programming": 4,
                    "analytical_thinking": 5,
                    "communication": 3,
                    "problem_solving": 4,
                    "creativity": 3
                },
                "interests": {
                    "technology": 5,
                    "engineering": 4,
                    "research": 4,
                    "business": 2
                },
                "academic_level": "undergraduate",
                "certifications": ["Python Basics"]
            }
        }


class PredictionRequest(BaseModel):
    """Request body for career prediction"""
    user_profile: UserProfile
    top_k: int = Field(default=5, ge=1, le=10, description="Number of top careers to return")
    include_details: bool = Field(default=True, description="Include detailed career information")
    use_ml_model: bool = Field(default=True, description="Use ML model if available")


class CareerMatch(BaseModel):
    """Single career match result"""
    career_id: str
    career_name: str
    match_score: float
    confidence: float
    category: str
    explanations: List[str]
    score_breakdown: Dict[str, float]


class PredictionResponse(BaseModel):
    """Response for career prediction"""
    success: bool
    total_matches: int
    method_used: str  # 'rule_based', 'ml_model', or 'hybrid'
    recommendations: List[Dict]


@router.post("/predict", response_model=PredictionResponse)
async def predict_careers(
    request: Request,
    prediction_request: PredictionRequest
):
    """
    Get career recommendations based on user profile
    
    This endpoint uses a hybrid approach:
    1. Rule-based matching for explainability
    2. ML model (XGBoost) for improved accuracy (if available)
    """
    try:
        career_matcher = request.app.state.career_matcher
        ml_predictor = request.app.state.ml_predictor
        
        user_profile = prediction_request.user_profile.model_dump()
        top_k = prediction_request.top_k
        
        # Get rule-based recommendations (always available)
        rule_based_results = career_matcher.get_top_careers(user_profile, top_k)
        method_used = "rule_based"
        
        # Try ML model if requested and available
        if prediction_request.use_ml_model and ml_predictor.is_model_loaded():
            try:
                ml_results = ml_predictor.predict(user_profile, top_k)
                
                # Combine results (hybrid approach)
                recommendations = combine_predictions(rule_based_results, ml_results)
                method_used = "hybrid"
            except Exception as e:
                print(f"ML prediction failed, using rule-based: {e}")
                recommendations = rule_based_results
        else:
            recommendations = rule_based_results
        
        # Add detailed career info if requested
        if prediction_request.include_details:
            for rec in recommendations:
                career_id = rec.get("career_id")
                if career_id:
                    details = career_matcher.get_career_details(career_id)
                    if details:
                        rec["nepal_info"] = details.get("nepal_info", {})
        
        return PredictionResponse(
            success=True,
            total_matches=len(recommendations),
            method_used=method_used,
            recommendations=recommendations,
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/predict/explain")
async def explain_prediction(
    request: Request,
    prediction_request: PredictionRequest,
    career_id: str
):
    """
    Get detailed explanation for why a specific career was recommended
    """
    career_matcher = request.app.state.career_matcher
    user_profile = prediction_request.user_profile.model_dump()
    
    explanation = career_matcher.explain_match(user_profile, career_id)
    
    return {
        "career_id": career_id,
        "explanation": explanation,
    }


def combine_predictions(
    rule_based: List[Dict],
    ml_based: List[Dict],
    rule_weight: float = 0.4,
    ml_weight: float = 0.6
) -> List[Dict]:
    """
    Combine rule-based and ML predictions using weighted scoring
    
    Args:
        rule_based: Results from rule-based matcher
        ml_based: Results from ML model
        rule_weight: Weight for rule-based scores
        ml_weight: Weight for ML scores
    
    Returns:
        Combined and re-ranked predictions
    """
    combined = {}
    
    # Add rule-based scores
    for rec in rule_based:
        career_id = rec.get("career_id")
        if career_id:
            combined[career_id] = {
                **rec,
                "rule_score": rec.get("match_score", 0),
                "ml_score": 0,
                "combined_score": rec.get("match_score", 0) * rule_weight,
            }
    
    # Add ML scores
    for rec in ml_based:
        career_id = rec.get("career_id")
        if career_id:
            if career_id in combined:
                combined[career_id]["ml_score"] = rec.get("confidence", 0) * 100
                combined[career_id]["combined_score"] += rec.get("confidence", 0) * 100 * ml_weight
            else:
                combined[career_id] = {
                    **rec,
                    "rule_score": 0,
                    "ml_score": rec.get("confidence", 0) * 100,
                    "combined_score": rec.get("confidence", 0) * 100 * ml_weight,
                }
    
    # Sort by combined score
    sorted_careers = sorted(
        combined.values(),
        key=lambda x: x["combined_score"],
        reverse=True
    )
    
    # Update match_score to combined score
    for career in sorted_careers:
        career["match_score"] = round(career["combined_score"], 2)
    
    return sorted_careers
