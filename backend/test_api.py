"""Test the LLM hybrid prediction via API."""
import requests
import json
import time

BASE = "http://127.0.0.1:8000/api/career/predict"

profiles = [
    {
        "label": "CS/ML Student (BCA)",
        "user_profile": {
            "education_level": "bachelors",
            "ug_course": "BCA",
            "specialization": "Computer Science",
            "skills": ["Python", "Machine Learning", "SQL", "Data Visualization"],
            "interests": ["Artificial Intelligence", "Data Analysis"],
            "cgpa": 78.0,
            "location": "Nepal",
        },
    },
    {
        "label": "MBA Marketing Student",
        "user_profile": {
            "education_level": "masters",
            "ug_course": "MBA",
            "specialization": "Marketing",
            "skills": ["Digital Marketing", "SEO", "Content Writing", "Social Media"],
            "interests": ["Sales", "Brand Management"],
            "cgpa": 72.0,
            "location": "Nepal",
        },
    },
    {
        "label": "Design Student (Figma/UI)",
        "user_profile": {
            "education_level": "bachelors",
            "ug_course": "B.Sc",
            "specialization": "Design",
            "skills": ["Figma", "UI Design", "Prototyping", "CSS", "HTML"],
            "interests": ["User Experience", "Visual Design"],
            "cgpa": 80.0,
            "location": "Nepal",
        },
    },
]

for prof in profiles:
    label = prof.pop("label")
    print(f"\n=== {label} ===")
    try:
        r = requests.post(BASE, json=prof, timeout=30)
        data = r.json()
        method = data.get("user_profile_summary", {}).get("prediction_method", "unknown")
        print(f"  Method: {method}")
        for i, p in enumerate(data["predictions"]):
            desc = p.get("description", "")
            print(f"  {i+1}. {p['career']} ({p['confidence']:.2f}) — {desc[:80]}")
    except Exception as e:
        print(f"  ERROR: {e}")
    time.sleep(6)  # Respect rate limits
