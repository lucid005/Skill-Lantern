"""Quick test script for career predictor predictions."""

from app.models.career_predictor import career_predictor
from app.models.schemas import UserProfile, EducationLevel


def test_predictions():
    # Load model
    career_predictor.load_model()

    # Test 1: CS/ML Student
    profile1 = UserProfile(
        education_level=EducationLevel.BACHELORS,
        ug_course="BCA",
        specialization="Computer Science",
        skills=["Python", "Machine Learning", "SQL", "Data Visualization"],
        interests=["Artificial Intelligence", "Data Analysis"],
        cgpa=78.0,
        location="Nepal",
    )
    preds1 = career_predictor.predict(profile1, top_n=5)
    print("\n=== Test 1: CS/ML Student (BCA, Python/ML/SQL) ===")
    for i, p in enumerate(preds1):
        print(f"  {i+1}. {p.career} ({p.confidence:.2f}) - {p.description}")

    # Test 2: MBA Marketing Student
    profile2 = UserProfile(
        education_level=EducationLevel.MASTERS,
        ug_course="MBA",
        specialization="Marketing",
        skills=["Digital Marketing", "SEO", "Content Writing", "Social Media"],
        interests=["Sales", "Brand Management"],
        cgpa=72.0,
        location="Nepal",
    )
    preds2 = career_predictor.predict(profile2, top_n=5)
    print("\n=== Test 2: MBA Marketing Student ===")
    for i, p in enumerate(preds2):
        print(f"  {i+1}. {p.career} ({p.confidence:.2f}) - {p.description}")

    # Test 3: Design Student
    profile3 = UserProfile(
        education_level=EducationLevel.BACHELORS,
        ug_course="B.Sc",
        specialization="Design",
        skills=["Figma", "UI Design", "Prototyping", "CSS", "HTML"],
        interests=["User Experience", "Visual Design"],
        cgpa=80.0,
        location="Nepal",
    )
    preds3 = career_predictor.predict(profile3, top_n=5)
    print("\n=== Test 3: Design Student (Figma/UI) ===")
    for i, p in enumerate(preds3):
        print(f"  {i+1}. {p.career} ({p.confidence:.2f}) - {p.description}")

    # Test 4: Java developer (should NOT get confused with JavaScript)
    profile4 = UserProfile(
        education_level=EducationLevel.BACHELORS,
        ug_course="B.E",
        specialization="Computer Engineering",
        skills=["Java", "Spring Boot", "SQL", "Git"],
        interests=["Software Development", "Backend Systems"],
        cgpa=75.0,
        location="Nepal",
    )
    preds4 = career_predictor.predict(profile4, top_n=5)
    print("\n=== Test 4: Java Backend Developer (Java, NOT JavaScript) ===")
    for i, p in enumerate(preds4):
        print(f"  {i+1}. {p.career} ({p.confidence:.2f}) - {p.description}")

    # Test 5: Healthcare student
    profile5 = UserProfile(
        education_level=EducationLevel.BACHELORS,
        ug_course="MBBS",
        specialization="Medicine",
        skills=["Patient Care", "Communication"],
        interests=["Healthcare", "Medical Research"],
        cgpa=82.0,
        location="Nepal",
    )
    preds5 = career_predictor.predict(profile5, top_n=5)
    print("\n=== Test 5: MBBS/Healthcare Student ===")
    for i, p in enumerate(preds5):
        print(f"  {i+1}. {p.career} ({p.confidence:.2f}) - {p.description}")

    # Test 6: Legal student
    profile6 = UserProfile(
        education_level=EducationLevel.MASTERS,
        ug_course="LLM",
        specialization="Criminal Law",
        skills=["Legal Research", "Legal Writing", "Critical Thinking"],
        interests=["Law", "Research", "Litigation & Legal Service"],
        cgpa=76.0,
        location="Nepal",
    )
    preds6 = career_predictor.predict(profile6, top_n=5)
    print("\n=== Test 6: LLM/Criminal Law Student ===")
    for i, p in enumerate(preds6):
        print(f"  {i+1}. {p.career} ({p.confidence:.2f}) - {p.description}")


if __name__ == "__main__":
    test_predictions()
