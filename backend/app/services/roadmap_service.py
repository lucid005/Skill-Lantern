"""
Roadmap Service - Career Roadmap Generation
Generates career roadmaps using Gemini API.
"""

from typing import Optional, Dict, Any
import logging

from app.services.gemini_service import gemini_service
from app.prompts.roadmap_prompts import ROADMAP_SYSTEM_PROMPT, get_roadmap_user_prompt
from app.models.schemas import UserProfile, RoadmapResponse, RoadmapStage

logger = logging.getLogger(__name__)


class RoadmapService:
    """Service for generating career roadmaps."""
    
    def __init__(self):
        self.llm = gemini_service
        
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
                ug_course=user_profile.ug_course,
                specialization=user_profile.specialization,
                skills=user_profile.skills,
                interests=user_profile.interests,
                preferences=user_profile.preferences,
                cgpa=user_profile.cgpa,
                certifications=user_profile.certifications,
                location=user_profile.location
            )
            
            # Generate response
            raw_response = await self.llm.generate(
                prompt=user_prompt,
                system_prompt=ROADMAP_SYSTEM_PROMPT,
                temperature=0.25,
                max_tokens=1400
            )
            
            # Parse JSON response
            parsed = self.llm.parse_json_response(raw_response)
            
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

    def _get_career_specific_stages(self, career_name: str) -> list:
        """Get deterministic career-specific stages when LLM output is unavailable."""
        career = career_name.lower()
        plans = {
            "software engineer": [
                RoadmapStage(
                    level="Beginner",
                    duration="3-4 months",
                    skills=["Programming fundamentals", "Git and GitHub", "Data structures basics", "HTML/CSS/JavaScript or Python", "Debugging"],
                    resources=["freeCodeCamp Responsive Web Design", "CS50x lectures", "Python official tutorial", "GitHub Skills", "MDN Web Docs"],
                    milestones=["Publish 3 small projects on GitHub", "Solve 50 beginner coding problems", "Build a personal portfolio site"],
                ),
                RoadmapStage(
                    level="Intermediate",
                    duration="5-8 months",
                    skills=["Object-oriented programming", "REST APIs", "Database design with SQL", "Testing basics", "Frontend or backend framework"],
                    resources=["Full Stack Open", "The Odin Project", "PostgreSQL Tutorial", "FastAPI or Django docs", "React docs"],
                    milestones=["Build one full-stack CRUD app", "Add authentication and database persistence", "Write tests for core features"],
                ),
                RoadmapStage(
                    level="Advanced",
                    duration="8-12 months",
                    skills=["System design basics", "Deployment", "CI/CD", "Performance optimization", "Interview preparation"],
                    resources=["System Design Primer", "Docker getting started", "GitHub Actions docs", "LeetCode study plan", "Render/Railway deployment docs"],
                    milestones=["Deploy 2 production-style apps", "Contribute to one open-source issue", "Prepare a resume and apply for internships or junior roles"],
                ),
            ],
            "data scientist": [
                RoadmapStage(
                    level="Beginner",
                    duration="3-4 months",
                    skills=["Python", "Statistics basics", "Pandas", "Data cleaning", "Visualization"],
                    resources=["Kaggle Learn Python", "Kaggle Learn Pandas", "StatQuest YouTube", "freeCodeCamp Data Analysis with Python", "Matplotlib docs"],
                    milestones=["Complete 3 cleaned datasets", "Publish one notebook with charts", "Explain mean, variance, correlation, and regression"],
                ),
                RoadmapStage(
                    level="Intermediate",
                    duration="5-8 months",
                    skills=["Machine learning", "Scikit-learn", "Feature engineering", "Model evaluation", "SQL"],
                    resources=["Google Machine Learning Crash Course", "Kaggle Intro to Machine Learning", "Scikit-learn docs", "Mode SQL Tutorial", "Coursera ML audit content"],
                    milestones=["Train and compare 3 ML models", "Create an end-to-end prediction project", "Write a model evaluation report"],
                ),
                RoadmapStage(
                    level="Advanced",
                    duration="8-12 months",
                    skills=["Deep learning basics", "MLOps basics", "Model deployment", "Experiment tracking", "Portfolio storytelling"],
                    resources=["fast.ai Practical Deep Learning", "TensorFlow tutorials", "MLflow docs", "Hugging Face course", "Streamlit docs"],
                    milestones=["Deploy one ML demo app", "Build a portfolio with 3 polished case studies", "Apply for data internships or junior analyst/scientist roles"],
                ),
            ],
            "web developer": [
                RoadmapStage(
                    level="Beginner",
                    duration="2-4 months",
                    skills=["HTML", "CSS", "JavaScript", "Responsive design", "Git"],
                    resources=["freeCodeCamp Responsive Web Design", "MDN JavaScript Guide", "The Odin Project Foundations", "Kevin Powell CSS YouTube", "GitHub Skills"],
                    milestones=["Build 5 responsive pages", "Publish code on GitHub", "Create a portfolio homepage"],
                ),
                RoadmapStage(
                    level="Intermediate",
                    duration="4-7 months",
                    skills=["React or Next.js", "API integration", "Forms and validation", "Authentication basics", "Database-backed apps"],
                    resources=["React docs", "Next.js Learn", "Supabase docs", "Full Stack Open", "TanStack Query docs"],
                    milestones=["Build a dashboard app", "Connect frontend to an API", "Deploy one full-stack project"],
                ),
                RoadmapStage(
                    level="Advanced",
                    duration="6-10 months",
                    skills=["Performance", "Accessibility", "Testing", "Deployment pipelines", "UI architecture"],
                    resources=["web.dev", "Testing Library docs", "Playwright docs", "Vercel docs", "A11y Project"],
                    milestones=["Improve Lighthouse scores above 90", "Add automated tests", "Apply for frontend internships or freelance projects"],
                ),
            ],
        }
        return plans.get(career_name.lower(), plans.get(career, self._get_default_stages()))
    
    def _get_fallback_roadmap(self, career_name: str) -> RoadmapResponse:
        """Return a fallback roadmap when LLM fails."""
        return RoadmapResponse(
            career=career_name,
            overview=f"A structured path to becoming a {career_name}. This roadmap covers the essential skills and milestones needed to enter this field.",
            stages=self._get_career_specific_stages(career_name),
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
