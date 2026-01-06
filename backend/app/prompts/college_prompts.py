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
    location_str = preferred_location if preferred_location else "Any location in Nepal"
    budget_str = budget_range if budget_range else "Flexible"
    
    return f"""Target Career: {career_name}
Required Course(s): {courses_str}

User Preferences:
- Location: {location_str}
- Budget: {budget_str}
- Degree Level: {degree_level}

Available Colleges Data:
{filtered_colleges}

Task:
Based on the user's career goal and preferences:
1. Recommend the best-matched colleges from the provided data
2. Explain why each college is suitable
3. Mention offered programs relevant to the career
4. Suggest alternative colleges if budget/location is restrictive

Constraints:
- Use ONLY the provided colleges data
- No assumptions or invented data
- Keep explanations concise and factual

Output Format (respond in valid JSON):
{{
    "recommendations": [
        {{
            "name": "College Name",
            "location": "Location",
            "programs": ["Program 1", "Program 2"],
            "reason": "Why this college is suitable"
        }}
    ],
    "alternatives": [
        {{
            "name": "Alternative College Name",
            "location": "Location",
            "programs": ["Program 1"],
            "reason": "Why this is a good alternative"
        }}
    ],
    "notes": "Any additional notes or considerations"
}}"""
