"""
Recommendation Service - Full Career Guidance Orchestration
Combines all services to provide complete career recommendations.
"""

from typing import Optional, Dict, Any, List
import logging

from app.services.ollama_service import ollama_service
from app.services.college_service import college_service
from app.services.roadmap_service import roadmap_service
from app.prompts.college_prompts import COLLEGE_SYSTEM_PROMPT, get_college_user_prompt
from app.prompts.summary_prompts import SUMMARY_SYSTEM_PROMPT, get_summary_user_prompt
from app.models.schemas import (
    UserProfile, 
    FullRecommendationRequest,
    FullRecommendationResponse,
    PredictedCareer,
    RoadmapResponse,
    CollegeRecommendationResponse,
    CollegeInfo,
    CollegeRequest,
    BudgetRange,
    DegreeLevel
)

logger = logging.getLogger(__name__)


class RecommendationService:
    """Service for generating complete career recommendations."""
    
    def __init__(self):
        self.ollama = ollama_service
        self.college_svc = college_service
        self.roadmap_svc = roadmap_service
    
    async def get_college_recommendations(
        self,
        request: CollegeRequest
    ) -> CollegeRecommendationResponse:
        """
        Get college recommendations for a career.
        
        Args:
            request: College recommendation request
            
        Returns:
            CollegeRecommendationResponse with recommendations
        """
        try:
            # Ensure college data is loaded
            if not self.college_svc.loaded:
                self.college_svc.load_data()
            
            # Get relevant colleges
            colleges = self.college_svc.get_colleges_for_career(request.career_name)
            
            # Filter by location if specified
            if request.preferred_location:
                colleges = [c for c in colleges 
                           if request.preferred_location.lower() in c.get("Location", "").lower()]
            
            # If too few colleges after filtering, get all relevant
            if len(colleges) < 3:
                colleges = self.college_svc.get_colleges_for_career(request.career_name)
            
            if not colleges:
                return CollegeRecommendationResponse(
                    career=request.career_name,
                    recommendations=[],
                    notes="No colleges found matching the criteria. Please try with broader search terms."
                )
            
            # Format colleges for LLM prompt
            formatted_colleges = self.college_svc.format_colleges_for_prompt(colleges)
            
            # Generate LLM recommendations
            user_prompt = get_college_user_prompt(
                career_name=request.career_name,
                required_courses=request.required_courses,
                preferred_location=request.preferred_location or "Any",
                budget_range=request.budget_range.value if request.budget_range else "Flexible",
                degree_level=request.degree_level.value if request.degree_level else "bachelors",
                filtered_colleges=formatted_colleges
            )
            
            raw_response = await self.ollama.generate(
                prompt=user_prompt,
                system_prompt=COLLEGE_SYSTEM_PROMPT,
                temperature=0.5
            )
            
            # Parse response
            parsed = self.ollama.parse_json_response(raw_response)
            
            return self._build_college_response(request.career_name, parsed, colleges, raw_response)
            
        except Exception as e:
            logger.error(f"College recommendation failed: {e}")
            # Return basic recommendations from CSV without LLM
            return self._get_fallback_colleges(request.career_name, colleges[:5] if 'colleges' in dir() else [])
    
    def _build_college_response(
        self,
        career_name: str,
        parsed_data: Dict[str, Any],
        all_colleges: List[Dict],
        raw_response: str
    ) -> CollegeRecommendationResponse:
        """Build CollegeRecommendationResponse from parsed data."""
        
        recommendations = []
        for rec in parsed_data.get("recommendations", [])[:5]:
            # Try to find matching college in CSV data
            csv_college = self._find_college_in_data(rec.get("name", ""), all_colleges)
            
            college_info = CollegeInfo(
                name=rec.get("name", "Unknown"),
                location=rec.get("location", csv_college.get("Location", "N/A") if csv_college else "N/A"),
                university=csv_college.get("University") if csv_college else None,
                programs=rec.get("programs", []),
                ownership_type=csv_college.get("Ownership Type") if csv_college else None,
                phone=csv_college.get("Phone Number") if csv_college else None,
                email=csv_college.get("Email") if csv_college else None,
                reason=rec.get("reason", "")
            )
            recommendations.append(college_info)
        
        alternatives = []
        for alt in parsed_data.get("alternatives", [])[:3]:
            csv_college = self._find_college_in_data(alt.get("name", ""), all_colleges)
            
            college_info = CollegeInfo(
                name=alt.get("name", "Unknown"),
                location=alt.get("location", csv_college.get("Location", "N/A") if csv_college else "N/A"),
                programs=alt.get("programs", []),
                reason=alt.get("reason", "")
            )
            alternatives.append(college_info)
        
        return CollegeRecommendationResponse(
            career=career_name,
            recommendations=recommendations,
            alternatives=alternatives,
            notes=parsed_data.get("notes", ""),
            raw_response=raw_response
        )
    
    def _find_college_in_data(self, name: str, colleges: List[Dict]) -> Optional[Dict]:
        """Find a college by name in the CSV data."""
        name_lower = name.lower()
        for college in colleges:
            college_name = college.get("College", "").lower()
            if name_lower in college_name or college_name in name_lower:
                return college
        return None
    
    def _get_fallback_colleges(self, career_name: str, colleges: List[Dict]) -> CollegeRecommendationResponse:
        """Return fallback colleges when LLM fails."""
        recommendations = []
        for college in colleges[:5]:
            recommendations.append(CollegeInfo(
                name=college.get("College", "Unknown"),
                location=college.get("Location", "N/A"),
                university=college.get("University"),
                programs=[college.get("Course Offered", "")[:100]],
                reason="Recommended based on available programs"
            ))
        
        return CollegeRecommendationResponse(
            career=career_name,
            recommendations=recommendations,
            notes="These colleges offer programs relevant to your chosen career."
        )
    
    async def generate_full_recommendation(
        self,
        predicted_careers: List[PredictedCareer],
        request: FullRecommendationRequest
    ) -> FullRecommendationResponse:
        """
        Generate complete career recommendation including roadmap and colleges.
        
        Args:
            predicted_careers: List of careers from XGBoost prediction
            request: Full recommendation request with user profile
            
        Returns:
            FullRecommendationResponse with complete guidance
        """
        try:
            # Select top career
            selected_career = predicted_careers[0].career if predicted_careers else "Software Developer"
            
            # Generate roadmap
            roadmap = await self.roadmap_svc.generate_roadmap(
                career_name=selected_career,
                user_profile=request.user_profile
            )
            
            # Get college recommendations
            college_request = CollegeRequest(
                career_name=selected_career,
                preferred_location=request.preferred_location,
                budget_range=request.budget_range,
                degree_level=request.degree_level
            )
            colleges = await self.get_college_recommendations(college_request)
            
            # Generate final summary
            roadmap_summary = self.roadmap_svc.get_roadmap_summary(roadmap)
            college_summary = self._get_college_summary(colleges)
            
            summary_prompt = get_summary_user_prompt(
                career_name=selected_career,
                user_name=request.user_profile.name,
                roadmap_summary=roadmap_summary,
                college_summary=college_summary
            )
            
            summary_response = await self.ollama.generate(
                prompt=summary_prompt,
                system_prompt=SUMMARY_SYSTEM_PROMPT,
                temperature=0.7
            )
            
            parsed_summary = self.ollama.parse_json_response(summary_response)
            
            return FullRecommendationResponse(
                predicted_careers=predicted_careers,
                selected_career=selected_career,
                roadmap=roadmap,
                colleges=colleges,
                summary=parsed_summary.get("career_fit_explanation", f"You are well-suited for a career as a {selected_career}."),
                immediate_actions=parsed_summary.get("immediate_actions", [
                    "Research the field and required skills",
                    "Start with free online courses",
                    "Connect with professionals in the field"
                ])
            )
            
        except Exception as e:
            logger.error(f"Full recommendation generation failed: {e}")
            raise
    
    def _get_college_summary(self, colleges: CollegeRecommendationResponse) -> str:
        """Get text summary of college recommendations."""
        if not colleges.recommendations:
            return "No specific colleges recommended at this time."
        
        summary_parts = ["Recommended Colleges:"]
        for i, college in enumerate(colleges.recommendations[:3], 1):
            summary_parts.append(f"{i}. {college.name} - {college.location}")
            if college.programs:
                summary_parts.append(f"   Programs: {', '.join(college.programs[:2])}")
        
        return "\n".join(summary_parts)


# Singleton instance
recommendation_service = RecommendationService()
