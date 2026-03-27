"""
Prompt Templates for College Recommendations
"""

COLLEGE_SYSTEM_PROMPT = """You are an AI education advisor specializing in Nepal's higher education system.
You must recommend colleges strictly from the provided list.
Do not add or invent institutions.
Explain recommendations logically.
Always respond in valid JSON format."""


def get_college_user_prompt(
    career_name: str,
    required_courses: list,
    preferred_location: str,
    budget_range: str,
    degree_level: str,
    filtered_colleges: str
) -> str:
    """Generate user prompt for college recommendations."""
    
    courses_str = ", ".join(required_courses) if required_courses else "Related to " + career_name
    location_str = preferred_location if preferred_location else "Any"
    budget_str = budget_range if budget_range else "Flexible"
    
    return f"""Career: {career_name} | Courses: {courses_str} | Location: {location_str} | Budget: {budget_str} | Degree: {degree_level}

Colleges:
{filtered_colleges}

Pick top 3-5 best colleges from above for this career. For each, give name, location, relevant programs, and a short reason. Also suggest 1-2 alternatives. Use ONLY colleges listed above.

Respond in JSON:
{{{{
  "recommendations": [{{{{"name": "", "location": "", "programs": [], "reason": ""}}}}],
  "alternatives": [{{{{"name": "", "location": "", "programs": [], "reason": ""}}}}],
  "notes": ""
}}}}"""
