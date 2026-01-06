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
    
    return f"""Career Chosen: {career_name}

Roadmap Summary:
{roadmap_summary}

College Recommendations:
{college_summary}

Task:
Create a final user-facing career recommendation summary that includes:
1. Why this career suits {name_str}
2. Key skills to focus on
3. Education pathway in Nepal
4. Next 3 immediate actions

Tone:
- Encouraging
- Clear
- Practical

Output Format (respond in valid JSON):
{{
    "career_fit_explanation": "Explanation of why this career is a good fit",
    "key_skills": ["skill1", "skill2", "skill3"],
    "education_pathway": "Summary of educational steps in Nepal",
    "immediate_actions": [
        "Action 1: Description",
        "Action 2: Description",
        "Action 3: Description"
    ],
    "motivation_message": "An encouraging closing message"
}}"""
