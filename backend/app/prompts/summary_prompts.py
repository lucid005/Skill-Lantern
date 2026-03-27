"""
Prompt Templates for Final Career Summary
"""

SUMMARY_SYSTEM_PROMPT = """You are a professional AI career guidance assistant.
Your role is to provide structured, motivational, and accurate guidance.
You must not hallucinate data.
Always respond in valid JSON format."""


def get_summary_user_prompt(
    career_name: str,
    user_name: str,
    roadmap_summary: str,
    college_summary: str
) -> str:
    """Generate user prompt for final career summary."""
    
    name_str = user_name if user_name else "the student"
    
    return f"""Career: {career_name} | Student: {name_str}
Roadmap: {roadmap_summary}
Colleges: {college_summary}

Write a short encouraging career summary: why this career fits, 3 key skills, education pathway in Nepal, and 3 immediate action steps.

Respond in JSON:
{{{{
  "career_fit_explanation": "",
  "key_skills": [],
  "education_pathway": "",
  "immediate_actions": [],
  "motivation_message": ""
}}}}"""
