"""
Prompt Templates for Career Roadmap Generation
"""

ROADMAP_SYSTEM_PROMPT = """You are an expert AI career counselor and curriculum planner.
Your task is to generate clear, realistic, and actionable career roadmaps.
You must not invent facts.
You must strictly follow the user context and provided data.
If data is missing, clearly state assumptions.
Create plans that are specific to the target career, the student's current skills,
their education background, and Nepal's entry-level job market.
Do not produce generic stages such as "learn fundamentals" unless you name the
actual concepts, tools, projects, and milestones for the target career.
Always respond in valid JSON format."""


def get_roadmap_user_prompt(
    career_name: str,
    education_level: str,
    ug_course: str = None,
    specialization: str = None,
    skills: list = None,
    interests: list = None,
    preferences: str = None,
    cgpa: float = None,
    certifications: list = None,
    location: str = "Nepal",
) -> str:
    """Generate user prompt for roadmap generation."""
    
    skills_str = ", ".join(skills) if skills else "Not specified"
    interests_str = ", ".join(interests) if interests else "Not specified"
    certifications_str = ", ".join(certifications) if certifications else "None"
    ug_course_str = ug_course or "Not specified"
    specialization_str = specialization or "Not specified"
    preferences_str = preferences or "Not specified"
    cgpa_str = str(cgpa) if cgpa is not None else "Not provided"
    
    return f"""TARGET CAREER:
- Career: {career_name}

STUDENT PROFILE:
- Education Level: {education_level}
- UG Course/Degree: {ug_course_str}
- Specialization/Major: {specialization_str}
- Current Skills: {skills_str}
- Interests: {interests_str}
- CGPA/Percentage: {cgpa_str}
- Certifications: {certifications_str}
- Preferences: {preferences_str}
- Location: {location}

Create a personalized 3-stage roadmap for this exact student.

Requirements:
1. Use Beginner, Intermediate, and Advanced stages.
2. Each stage must have a realistic duration.
3. Start from the student's existing skills; do not repeat skills they already know unless the milestone advances them.
4. Include 4-7 concrete skills per stage.
5. Include 3-5 specific free or low-cost resources per stage. Prefer named resources such as freeCodeCamp, Kaggle Learn, MDN, Google/Coursera audit courses, YouTube channels, official docs, or local Nepal-relevant communities when appropriate.
6. Include 3-5 measurable milestones per stage, such as projects, portfolio artifacts, internships, certifications, or interview readiness tasks.
7. Keep colleges and long-term roles realistic for Nepal and remote-entry opportunities.
8. Avoid vague phrases like "advanced concepts", "industry tools", or "modern frameworks" unless accompanied by exact examples.

Respond in JSON:
{{{{
  "overview": "brief overview",
  "stages": [{{{{"level": "Beginner", "duration": "3-6 months", "skills": [], "resources": [], "milestones": []}}}}, ...],
  "tools_and_technologies": [],
  "job_roles": [],
  "growth_paths": []
}}}}"""
