"""
Prompt Templates for Career Roadmap Generation
"""

ROADMAP_SYSTEM_PROMPT = """You are an expert AI career counselor and curriculum planner.
Your task is to generate clear, realistic, and actionable career roadmaps.
You must not invent facts.
You must strictly follow the user context and provided data.
If data is missing, clearly state assumptions.
Use structured formatting.
Always respond in valid JSON format."""


def get_roadmap_user_prompt(
    career_name: str,
    education_level: str,
    skills: list,
    interests: list,
    preferences: str = None
) -> str:
    """Generate user prompt for roadmap generation."""
    
    skills_str = ", ".join(skills[:5]) if skills else "Not specified"
    interests_str = ", ".join(interests[:3]) if interests else "Not specified"
    
    return f"""Career: {career_name}
Education: {education_level} | Skills: {skills_str} | Interests: {interests_str} | Location: Nepal

Create a 3-stage career roadmap (Beginner/Intermediate/Advanced) with skills, free resources, and milestones for each stage. Include tools, job roles, and growth paths. Keep it realistic for Nepal. Use free platforms (YouTube, freeCodeCamp, Coursera).

Respond in JSON:
{{{{
  "overview": "brief overview",
  "stages": [{{{{"level": "Beginner", "duration": "3-6 months", "skills": [], "resources": [], "milestones": []}}}}, ...],
  "tools_and_technologies": [],
  "job_roles": [],
  "growth_paths": []
}}}}"""
