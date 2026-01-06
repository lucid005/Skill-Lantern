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
    
    skills_str = ", ".join(skills) if skills else "Not specified"
    interests_str = ", ".join(interests) if interests else "Not specified"
    preferences_str = preferences if preferences else "Not specified"
    
    return f"""Career Title: {career_name}

User Profile:
- Education Level: {education_level}
- Skills: {skills_str}
- Interests: {interests_str}
- Preferences: {preferences_str}
- Location: Nepal

Task:
Create a complete career roadmap for the given career.

Roadmap Requirements:
1. Beginner → Intermediate → Advanced stages
2. Skills to learn at each stage
3. Recommended tools & technologies
4. Estimated learning timeline
5. Entry-level job roles
6. Long-term career growth paths

Constraints:
- Keep recommendations realistic for Nepal
- Do not suggest paid foreign universities
- Prefer online learning platforms (Coursera, edX, freeCodeCamp, YouTube)
- Output must be structured and easy to read

Output Format (respond in valid JSON):
{{
    "overview": "Brief career overview",
    "stages": [
        {{
            "level": "Beginner",
            "duration": "3-6 months",
            "skills": ["skill1", "skill2"],
            "resources": ["resource1", "resource2"],
            "milestones": ["milestone1", "milestone2"]
        }},
        {{
            "level": "Intermediate",
            "duration": "6-12 months",
            "skills": ["skill1", "skill2"],
            "resources": ["resource1", "resource2"],
            "milestones": ["milestone1", "milestone2"]
        }},
        {{
            "level": "Advanced",
            "duration": "12-24 months",
            "skills": ["skill1", "skill2"],
            "resources": ["resource1", "resource2"],
            "milestones": ["milestone1", "milestone2"]
        }}
    ],
    "tools_and_technologies": ["tool1", "tool2"],
    "job_roles": ["role1", "role2"],
    "growth_paths": ["path1", "path2"]
}}"""
