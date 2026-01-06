"""
Pydantic Schemas for Request/Response Models
Defines all data structures used in the API.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum


# ============== Enums ==============

class EducationLevel(str, Enum):
    """Education level options."""
    HIGH_SCHOOL = "high_school"
    PLUS_TWO = "plus_two"
    BACHELORS = "bachelors"
    MASTERS = "masters"
    PHD = "phd"


class DegreeLevel(str, Enum):
    """Degree level for college recommendations."""
    DIPLOMA = "diploma"
    BACHELORS = "bachelors"
    MASTERS = "masters"
    PHD = "phd"


class BudgetRange(str, Enum):
    """Budget range options."""
    LOW = "low"  # < 50,000 NPR
    MEDIUM = "medium"  # 50,000 - 200,000 NPR
    HIGH = "high"  # > 200,000 NPR


# ============== User Profile ==============

class UserProfile(BaseModel):
    """User profile data for career assessment."""
    name: Optional[str] = Field(None, description="User's name")
    gender: Optional[str] = Field(None, description="User's gender")
    education_level: EducationLevel = Field(..., description="Current education level")
    ug_course: Optional[str] = Field(None, description="Undergraduate course/degree")
    specialization: Optional[str] = Field(None, description="Major subject or specialization")
    skills: List[str] = Field(default_factory=list, description="List of skills")
    interests: List[str] = Field(default_factory=list, description="Areas of interest")
    preferences: Optional[str] = Field(None, description="Career preferences")
    cgpa: Optional[float] = Field(None, ge=0, le=100, description="CGPA or percentage")
    certifications: List[str] = Field(default_factory=list, description="Additional certifications")
    location: str = Field(default="Nepal", description="User's location")


# ============== Career Prediction ==============

class CareerPredictionRequest(BaseModel):
    """Request model for career prediction."""
    user_profile: UserProfile


class PredictedCareer(BaseModel):
    """Single career prediction with confidence score."""
    career: str = Field(..., description="Predicted career name")
    confidence: float = Field(..., ge=0, le=1, description="Confidence score 0-1")
    description: Optional[str] = Field(None, description="Brief career description")


class CareerPredictionResponse(BaseModel):
    """Response model for career prediction."""
    predictions: List[PredictedCareer] = Field(..., description="List of predicted careers")
    user_profile_summary: Dict[str, Any] = Field(default_factory=dict)
    message: str = Field(default="Prediction successful")


# ============== Roadmap Generation ==============

class RoadmapRequest(BaseModel):
    """Request model for career roadmap generation."""
    career_name: str = Field(..., description="Target career name")
    user_profile: UserProfile


class RoadmapStage(BaseModel):
    """A single stage in the career roadmap."""
    level: str = Field(..., description="Stage level: Beginner/Intermediate/Advanced")
    duration: str = Field(..., description="Estimated duration e.g., '3-6 months'")
    skills: List[str] = Field(default_factory=list, description="Skills to learn")
    resources: List[str] = Field(default_factory=list, description="Learning resources")
    milestones: List[str] = Field(default_factory=list, description="Key milestones")


class RoadmapResponse(BaseModel):
    """Response model for career roadmap."""
    career: str = Field(..., description="Career name")
    overview: str = Field(..., description="Career overview")
    stages: List[RoadmapStage] = Field(default_factory=list, description="Roadmap stages")
    tools_and_technologies: List[str] = Field(default_factory=list, description="Tools to learn")
    job_roles: List[str] = Field(default_factory=list, description="Entry-level job roles")
    growth_paths: List[str] = Field(default_factory=list, description="Long-term growth paths")
    raw_response: Optional[str] = Field(None, description="Raw LLM response")


# ============== College Recommendations ==============

class CollegeRequest(BaseModel):
    """Request model for college recommendations."""
    career_name: str = Field(..., description="Target career")
    required_courses: List[str] = Field(default_factory=list, description="Required courses/programs")
    preferred_location: Optional[str] = Field(None, description="Preferred location in Nepal")
    budget_range: Optional[BudgetRange] = Field(None, description="Budget range")
    degree_level: DegreeLevel = Field(default=DegreeLevel.BACHELORS)


class CollegeInfo(BaseModel):
    """Information about a single college."""
    name: str = Field(..., description="College name")
    location: str = Field(..., description="College location")
    university: Optional[str] = Field(None, description="Affiliated university")
    programs: List[str] = Field(default_factory=list, description="Relevant programs offered")
    ownership_type: Optional[str] = Field(None, description="Private/Government")
    phone: Optional[str] = Field(None, description="Contact phone")
    email: Optional[str] = Field(None, description="Contact email")
    reason: Optional[str] = Field(None, description="Why this college is recommended")


class CollegeRecommendationResponse(BaseModel):
    """Response model for college recommendations."""
    career: str = Field(..., description="Target career")
    recommendations: List[CollegeInfo] = Field(default_factory=list, description="Recommended colleges")
    alternatives: List[CollegeInfo] = Field(default_factory=list, description="Alternative options")
    notes: Optional[str] = Field(None, description="Additional notes")
    raw_response: Optional[str] = Field(None, description="Raw LLM response")


# ============== Full Recommendation ==============

class FullRecommendationRequest(BaseModel):
    """Request model for complete career guidance."""
    user_profile: UserProfile
    preferred_location: Optional[str] = Field(None, description="Preferred location for college")
    budget_range: Optional[BudgetRange] = Field(None)
    degree_level: DegreeLevel = Field(default=DegreeLevel.BACHELORS)


class FullRecommendationResponse(BaseModel):
    """Complete career guidance response."""
    predicted_careers: List[PredictedCareer] = Field(default_factory=list)
    selected_career: str = Field(..., description="Primary recommended career")
    roadmap: RoadmapResponse
    colleges: CollegeRecommendationResponse
    summary: str = Field(..., description="Final summary and next steps")
    immediate_actions: List[str] = Field(default_factory=list, description="3 immediate next steps")


# ============== Health Check ==============

class HealthResponse(BaseModel):
    """Health check response."""
    status: str = Field(default="healthy")
    ollama_status: str = Field(default="unknown")
    model_loaded: bool = Field(default=False)
    version: str = Field(default="1.0.0")


# ============== Error Response ==============

class ErrorResponse(BaseModel):
    """Standard error response."""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Error details")
    code: Optional[str] = Field(None, description="Error code")
