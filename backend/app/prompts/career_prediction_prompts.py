"""
Prompt Templates for LLM-Powered Career Prediction

These prompts are used to refine XGBoost predictions using Gemini.
The LLM receives the user's full profile context plus the model's
raw suggestions, and produces re-ranked, well-reasoned career predictions.
"""

CAREER_PREDICTION_SYSTEM_PROMPT = """You are an expert career counselor with deep knowledge of career paths, required skills, and education-to-career mapping.

Your task is to predict the most suitable careers for a student based on their profile.

RULES:
1. You MUST return EXACTLY 5 career predictions ranked by suitability.
2. Each prediction MUST have a confidence score between 0.0 and 1.0.
3. Confidence scores should reflect genuine suitability — do NOT inflate scores.
4. The top prediction's confidence should be between 0.50 and 0.95.
5. Consider the FULL profile holistically: skills + interests + education + specialization work together.
6. If skills clearly point to a technical career but interests are different, weight skills more heavily for career prediction.
7. Specialization and UG course are STRONG signals — a Computer Science student is very likely headed for a tech career.
8. Do NOT suggest careers that require skills or education the student clearly lacks.
9. Provide a brief, specific description explaining WHY each career fits this particular student.
10. Always respond in valid JSON format — no markdown, no explanation outside JSON.

CAREER CATEGORIES (choose ONLY from these):
- Software Engineer
- Data Scientist
- Data Analyst
- Web Developer
- Mobile App Developer
- DevOps Engineer
- Network Engineer
- Database Administrator
- Cybersecurity Analyst
- Product Manager
- Project Manager
- UI/UX Designer
- Quality Assurance Engineer
- Teacher/Educator
- Financial Analyst
- Marketing Specialist
- HR Manager
- IT Consultant
- Research Scientist
- Healthcare Professional
- Mechanical Engineer
- Civil Engineer
- Electrical Engineer
- Legal Professional
- Business Manager"""


def get_career_prediction_prompt(
    education_level: str,
    ug_course: str,
    specialization: str,
    skills: list,
    interests: list,
    cgpa: float,
    certifications: list,
    gender: str,
    preferences: str,
    xgboost_suggestions: list,
) -> str:
    """Generate the user prompt for career prediction.

    Args:
        education_level: Student's current education level
        ug_course: Undergraduate course/degree
        specialization: Major subject or specialization
        skills: List of student's skills
        interests: List of student's interests
        cgpa: CGPA or percentage
        certifications: List of certifications
        gender: Student's gender
        preferences: Any career preferences stated
        xgboost_suggestions: Top predictions from XGBoost model (list of dicts with career, confidence)
    """
    skills_str = ", ".join(skills) if skills else "Not specified"
    interests_str = ", ".join(interests) if interests else "Not specified"
    certs_str = ", ".join(certifications) if certifications else "None"
    prefs_str = preferences if preferences else "No specific preferences"
    cgpa_str = f"{cgpa}" if cgpa else "Not provided"
    ug_str = ug_course if ug_course else "Not specified"
    spec_str = specialization if specialization else "Not specified"
    gender_str = gender if gender else "Not specified"

    # Format XGBoost suggestions if available
    if xgboost_suggestions:
        model_hints = "\n".join(
            f"  {i+1}. {s['career']} (model confidence: {s['confidence']:.2f})"
            for i, s in enumerate(xgboost_suggestions[:5])
        )
        model_section = f"""
ML Model Suggestions (from XGBoost — use as hints, NOT as ground truth):
{model_hints}

IMPORTANT: The ML model may be wrong. Use these as reference points but make your own judgment based on the full profile. You may reorder them, replace some, or disagree entirely."""
    else:
        model_section = "\nNo ML model suggestions available — predict purely from the profile."

    return f"""STUDENT PROFILE:
- Education Level: {education_level}
- UG Course/Degree: {ug_str}
- Specialization/Major: {spec_str}
- Skills: {skills_str}
- Interests: {interests_str}
- CGPA/Percentage: {cgpa_str}
- Certifications: {certs_str}
- Gender: {gender_str}
- Career Preferences: {prefs_str}
- Location: Nepal
{model_section}

Based on this complete profile, predict the 5 most suitable careers.

Respond in JSON:
{{
  "predictions": [
    {{
      "career": "Career Name (from allowed list)",
      "confidence": 0.85,
      "description": "1-2 sentence explanation of why this career fits THIS student specifically"
    }}
  ]
}}"""
