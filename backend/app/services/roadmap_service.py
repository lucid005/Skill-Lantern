"""
Roadmap Service - Career Roadmap Generation
Generates career roadmaps using Ollama/LLaMA.
"""

from typing import Optional, Dict, Any
import logging

from app.services.ollama_service import ollama_service
from app.prompts.roadmap_prompts import ROADMAP_SYSTEM_PROMPT, get_roadmap_user_prompt
from app.models.schemas import UserProfile, RoadmapResponse, RoadmapStage

logger = logging.getLogger(__name__)


class RoadmapService:
    """Service for generating career roadmaps."""
    
    def __init__(self):
        self.ollama = ollama_service
        
    async def generate_roadmap(
        self,
        career_name: str,
        user_profile: UserProfile
    ) -> RoadmapResponse:
        """
        Generate a career roadmap using LLM.
        
        Args:
            career_name: Target career
            user_profile: User's profile data
            
        Returns:
            RoadmapResponse with structured roadmap
        """
        try:
            # Build prompt
            user_prompt = get_roadmap_user_prompt(
                career_name=career_name,
                education_level=user_profile.education_level.value,
                skills=user_profile.skills,
                interests=user_profile.interests,
                preferences=user_profile.preferences
            )
            
            # Generate response
            raw_response = await self.ollama.generate(
                prompt=user_prompt,
                system_prompt=ROADMAP_SYSTEM_PROMPT,
                temperature=0.7
            )
            
            # Parse JSON response
            parsed = self.ollama.parse_json_response(raw_response)
            
            # Build structured response
            return self._build_roadmap_response(career_name, parsed, raw_response)
            
        except Exception as e:
            logger.error(f"Roadmap generation failed: {e}")
            # Return fallback response
            return self._get_fallback_roadmap(career_name)
    
    def _build_roadmap_response(
        self,
        career_name: str,
        parsed_data: Dict[str, Any],
        raw_response: str
    ) -> RoadmapResponse:
        """Build RoadmapResponse from parsed LLM data."""
        
        # Extract stages
        stages = []
        for stage_data in parsed_data.get("stages", []):
            stage = RoadmapStage(
                level=stage_data.get("level", "Unknown"),
                duration=stage_data.get("duration", "N/A"),
                skills=stage_data.get("skills", []),
                resources=stage_data.get("resources", []),
                milestones=stage_data.get("milestones", [])
            )
            stages.append(stage)
        
        # If no stages parsed, create default
        if not stages:
            stages = self._get_default_stages()
        
        return RoadmapResponse(
            career=career_name,
            overview=parsed_data.get("overview", f"Career path for {career_name}"),
            stages=stages,
            tools_and_technologies=parsed_data.get("tools_and_technologies", []),
            job_roles=parsed_data.get("job_roles", []),
            growth_paths=parsed_data.get("growth_paths", []),
            raw_response=raw_response
        )
    
    def _get_default_stages(self) -> list:
        """Get default stages if LLM response is invalid."""
        return [
            RoadmapStage(
                level="Beginner",
                duration="3-6 months",
                skills=["Fundamentals", "Basic concepts"],
                resources=["YouTube tutorials", "freeCodeCamp", "Coursera free courses"],
                milestones=["Complete basic course", "Build first project"]
            ),
            RoadmapStage(
                level="Intermediate",
                duration="6-12 months",
                skills=["Advanced concepts", "Practical applications"],
                resources=["edX courses", "Documentation", "Practice projects"],
                milestones=["Build portfolio projects", "Contribute to open source"]
            ),
            RoadmapStage(
                level="Advanced",
                duration="12-24 months",
                skills=["Expert-level skills", "Industry practices"],
                resources=["Specialization courses", "Industry certifications"],
                milestones=["Get internship", "Land first job"]
            )
        ]
    
    def _get_fallback_roadmap(self, career_name: str) -> RoadmapResponse:
        """Return a fallback roadmap when LLM fails."""
        return RoadmapResponse(
            career=career_name,
            overview=f"A structured path to becoming a {career_name}. This roadmap covers the essential skills and milestones needed to enter this field.",
            stages=self._get_default_stages(),
            tools_and_technologies=["Industry-standard tools", "Modern frameworks"],
            job_roles=["Entry-level positions", "Junior roles", "Associate roles"],
            growth_paths=["Senior positions", "Team lead", "Management track", "Specialist track"]
        )
    
    def get_roadmap_summary(self, roadmap: RoadmapResponse) -> str:
        """Get a text summary of the roadmap for the final summary prompt."""
        summary_parts = [f"Career: {roadmap.career}"]
        summary_parts.append(f"Overview: {roadmap.overview[:200]}...")
        
        for stage in roadmap.stages:
            summary_parts.append(f"\n{stage.level} ({stage.duration}):")
            summary_parts.append(f"  Skills: {', '.join(stage.skills[:5])}")
        
        summary_parts.append(f"\nKey Tools: {', '.join(roadmap.tools_and_technologies[:5])}")
        summary_parts.append(f"Entry Roles: {', '.join(roadmap.job_roles[:3])}")
        
        return "\n".join(summary_parts)


# Singleton instance
roadmap_service = RoadmapService()
