"""
Skill Lantern - Process Survey Data

Converts raw Google Forms survey data to training format.
"""

import pandas as pd
from pathlib import Path
import sys


# Column mapping from Google Forms to training format
COLUMN_MAPPING = {
    # Academic
    "Mathematics Score (0-100)": "math_score",
    "Science Score (0-100)": "science_score",
    "English Score (0-100)": "english_score",
    "Overall GPA (0-4.0)": "gpa",
    
    # Skills
    "Programming / Coding": "skill_programming",
    "Communication Skills": "skill_communication",
    "Analytical Thinking": "skill_analytical_thinking",
    "Problem Solving": "skill_problem_solving",
    "Creativity": "skill_creativity",
    "Leadership": "skill_leadership",
    "Teamwork": "skill_teamwork",
    "Attention to Detail": "skill_attention_to_detail",
    "Time Management": "skill_time_management",
    "Stress Management": "skill_stress_management",
    "Empathy / Understanding Others": "skill_empathy",
    "Technical / Computer Skills": "skill_technical_skills",
    "Presentation Skills": "skill_presentation",
    "Project Management": "skill_project_management",
    "Dedication / Persistence": "skill_dedication",
    "Integrity / Ethics": "skill_integrity",
    "Patience": "skill_patience",
    
    # Interests
    "Technology & Computers": "interest_technology",
    "Engineering & Building Things": "interest_engineering",
    "Healthcare & Medicine": "interest_healthcare",
    "Business & Entrepreneurship": "interest_business",
    "Arts & Design": "interest_arts",
    "Education & Teaching": "interest_education",
    "Research & Discovery": "interest_research",
    "Helping Others / Social Work": "interest_helping_others",
    "Finance & Money Management": "interest_finance",
    "Law & Legal Matters": "interest_law",
    "Construction & Infrastructure": "interest_construction",
    "Environment & Nature": "interest_environment",
    
    # Target
    "What is your chosen/current career or the career you are pursuing?": "career_label",
}

# Career label normalization
CAREER_NORMALIZATION = {
    "Software Engineer / Developer": "Software Engineer",
    "Data Scientist / Analyst": "Data Scientist",
    "Doctor (MBBS)": "Doctor",
    "Civil Engineer": "Civil Engineer",
    "Graphic Designer": "Graphic Designer",
    "Business Analyst": "Business Analyst",
    "Chartered Accountant (CA)": "Accountant",
    "Teacher / Educator": "Teacher",
    "Marketing Manager": "Marketing Manager",
    "Nurse": "Nurse",
}


def load_survey_data(file_path: Path) -> pd.DataFrame:
    """Load raw survey data from CSV"""
    print(f"Loading survey data from {file_path}...")
    
    df = pd.read_csv(file_path)
    print(f"Loaded {len(df)} responses")
    
    return df


def clean_and_map_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Rename columns to training format"""
    print("Mapping columns...")
    
    # Find matching columns
    rename_map = {}
    for orig_col in df.columns:
        for survey_col, train_col in COLUMN_MAPPING.items():
            if survey_col.lower() in orig_col.lower():
                rename_map[orig_col] = train_col
                break
    
    df = df.rename(columns=rename_map)
    
    # Keep only mapped columns
    valid_cols = list(COLUMN_MAPPING.values())
    existing_cols = [c for c in valid_cols if c in df.columns]
    df = df[existing_cols]
    
    print(f"Mapped {len(existing_cols)} columns")
    
    return df


def normalize_career_labels(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize career labels to standard format"""
    if "career_label" in df.columns:
        df["career_label"] = df["career_label"].map(
            lambda x: CAREER_NORMALIZATION.get(x, x)
        )
    
    return df


def validate_data(df: pd.DataFrame) -> pd.DataFrame:
    """Validate and clean data"""
    print("Validating data...")
    
    initial_count = len(df)
    
    # Remove rows with missing career label
    if "career_label" in df.columns:
        df = df[df["career_label"].notna()]
    
    # Validate score ranges
    for col in ["math_score", "science_score", "english_score"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
            df = df[(df[col] >= 0) & (df[col] <= 100) | df[col].isna()]
    
    # Validate GPA
    if "gpa" in df.columns:
        df["gpa"] = pd.to_numeric(df["gpa"], errors="coerce")
        df = df[(df["gpa"] >= 0) & (df["gpa"] <= 4.0) | df["gpa"].isna()]
    
    # Validate skill/interest ratings (1-5)
    for col in df.columns:
        if col.startswith("skill_") or col.startswith("interest_"):
            df[col] = pd.to_numeric(df[col], errors="coerce")
            df[col] = df[col].clip(1, 5)
    
    # Fill missing values
    df = df.fillna(df.median(numeric_only=True))
    
    final_count = len(df)
    print(f"Validated: {initial_count} -> {final_count} rows ({initial_count - final_count} removed)")
    
    return df


def merge_with_existing(new_df: pd.DataFrame, existing_path: Path) -> pd.DataFrame:
    """Merge new survey data with existing dataset"""
    if existing_path.exists():
        print(f"Merging with existing data from {existing_path}...")
        existing_df = pd.read_csv(existing_path)
        
        # Align columns
        all_cols = list(set(new_df.columns) | set(existing_df.columns))
        
        for col in all_cols:
            if col not in new_df.columns:
                new_df[col] = 0
            if col not in existing_df.columns:
                existing_df[col] = 0
        
        merged_df = pd.concat([existing_df, new_df], ignore_index=True)
        print(f"Merged: {len(existing_df)} existing + {len(new_df)} new = {len(merged_df)} total")
        
        return merged_df
    
    return new_df


def main():
    """Process survey data"""
    print("=" * 60)
    print("🎓 Skill Lantern - Survey Data Processor")
    print("=" * 60)
    
    base_path = Path(__file__).parent.parent
    raw_path = base_path / "data" / "raw" / "survey_data.csv"
    processed_path = base_path / "data" / "processed" / "career_dataset.csv"
    
    if not raw_path.exists():
        print(f"\n❌ Survey data not found: {raw_path}")
        print("\nPlease:")
        print("1. Export your Google Form responses as CSV")
        print("2. Save to: ai/data/raw/survey_data.csv")
        print("3. Run this script again")
        sys.exit(1)
    
    # Process pipeline
    df = load_survey_data(raw_path)
    df = clean_and_map_columns(df)
    df = normalize_career_labels(df)
    df = validate_data(df)
    df = merge_with_existing(df, processed_path)
    
    # Save
    processed_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(processed_path, index=False)
    
    print(f"\n✅ Saved processed data to: {processed_path}")
    print(f"   Total samples: {len(df)}")
    print(f"   Career labels: {df['career_label'].nunique()}")
    
    print("\nCareer distribution:")
    print(df["career_label"].value_counts())
    
    print("\n" + "=" * 60)
    print("✅ Data processing complete!")
    print("\nNext step: Train the model:")
    print("   python -m training.train_xgboost")
    print("=" * 60)


if __name__ == "__main__":
    main()
