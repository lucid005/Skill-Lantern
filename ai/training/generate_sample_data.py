"""
Skill Lantern - Generate Sample Training Data

Creates synthetic training data for initial model development.
Replace with real survey data for production use.
"""

import random
import pandas as pd
import numpy as np
from pathlib import Path


# Career profiles with expected feature ranges
CAREER_PROFILES = {
    'Software Engineer': {
        'academic': {'math': (70, 100), 'science': (65, 100), 'english': (60, 90)},
        'skills': {'programming': (4, 5), 'analytical_thinking': (4, 5), 'problem_solving': (4, 5), 
                   'communication': (2, 4), 'teamwork': (3, 5), 'creativity': (2, 4)},
        'interests': {'technology': (4, 5), 'engineering': (3, 5), 'research': (2, 4), 'business': (1, 3)},
        'gpa_range': (3.0, 4.0),
    },
    'Data Scientist': {
        'academic': {'math': (80, 100), 'science': (75, 100), 'english': (60, 85)},
        'skills': {'programming': (3, 5), 'analytical_thinking': (4, 5), 'problem_solving': (4, 5),
                   'statistics': (4, 5), 'communication': (3, 5)},
        'interests': {'technology': (4, 5), 'research': (4, 5), 'business': (2, 4)},
        'gpa_range': (3.3, 4.0),
    },
    'Doctor': {
        'academic': {'math': (65, 95), 'science': (85, 100), 'english': (60, 90)},
        'skills': {'dedication': (4, 5), 'empathy': (4, 5), 'analytical_thinking': (3, 5),
                   'communication': (4, 5), 'stress_management': (3, 5)},
        'interests': {'healthcare': (4, 5), 'helping_others': (4, 5), 'research': (2, 4)},
        'gpa_range': (3.5, 4.0),
    },
    'Civil Engineer': {
        'academic': {'math': (75, 100), 'science': (70, 100), 'english': (50, 80)},
        'skills': {'analytical_thinking': (4, 5), 'problem_solving': (4, 5), 'technical_drawing': (3, 5),
                   'project_management': (2, 4), 'communication': (2, 4)},
        'interests': {'engineering': (4, 5), 'construction': (4, 5), 'environment': (2, 4)},
        'gpa_range': (2.8, 4.0),
    },
    'Graphic Designer': {
        'academic': {'math': (40, 75), 'science': (40, 75), 'english': (60, 95)},
        'skills': {'creativity': (4, 5), 'technical_skills': (3, 5), 'communication': (3, 5),
                   'attention_to_detail': (4, 5), 'time_management': (2, 4)},
        'interests': {'arts': (4, 5), 'technology': (2, 4), 'business': (1, 3)},
        'gpa_range': (2.3, 3.8),
    },
    'Business Analyst': {
        'academic': {'math': (70, 95), 'science': (55, 85), 'english': (70, 95)},
        'skills': {'analytical_thinking': (4, 5), 'communication': (4, 5), 'problem_solving': (4, 5),
                   'presentation': (3, 5), 'technical_skills': (2, 4)},
        'interests': {'business': (4, 5), 'technology': (3, 5), 'research': (2, 4)},
        'gpa_range': (2.8, 4.0),
    },
    'Accountant': {
        'academic': {'math': (75, 100), 'science': (50, 80), 'english': (60, 90)},
        'skills': {'analytical_thinking': (4, 5), 'attention_to_detail': (5, 5), 'integrity': (4, 5),
                   'communication': (2, 4), 'time_management': (3, 5)},
        'interests': {'business': (3, 5), 'finance': (4, 5), 'law': (2, 4)},
        'gpa_range': (3.0, 4.0),
    },
    'Teacher': {
        'academic': {'math': (55, 90), 'science': (55, 90), 'english': (65, 95)},
        'skills': {'communication': (4, 5), 'patience': (4, 5), 'creativity': (3, 5),
                   'empathy': (4, 5), 'subject_expertise': (3, 5)},
        'interests': {'education': (4, 5), 'helping_others': (4, 5), 'research': (2, 4)},
        'gpa_range': (2.5, 4.0),
    },
    'Marketing Manager': {
        'academic': {'math': (55, 85), 'science': (45, 80), 'english': (70, 100)},
        'skills': {'communication': (4, 5), 'creativity': (4, 5), 'analytical_thinking': (3, 5),
                   'leadership': (3, 5), 'digital_marketing': (3, 5)},
        'interests': {'business': (4, 5), 'arts': (2, 4), 'technology': (2, 4)},
        'gpa_range': (2.5, 3.8),
    },
    'Nurse': {
        'academic': {'math': (50, 80), 'science': (70, 95), 'english': (55, 85)},
        'skills': {'empathy': (4, 5), 'communication': (4, 5), 'stress_management': (3, 5),
                   'attention_to_detail': (4, 5), 'teamwork': (4, 5)},
        'interests': {'healthcare': (4, 5), 'helping_others': (4, 5)},
        'gpa_range': (2.5, 3.8),
    },
}

# All possible skills and interests
ALL_SKILLS = [
    'programming', 'communication', 'analytical_thinking', 'problem_solving',
    'creativity', 'leadership', 'teamwork', 'attention_to_detail', 'time_management',
    'stress_management', 'empathy', 'technical_skills', 'presentation', 'project_management',
    'dedication', 'integrity', 'patience', 'digital_marketing', 'statistics',
    'subject_expertise', 'technical_drawing'
]

ALL_INTERESTS = [
    'technology', 'engineering', 'healthcare', 'business', 'arts',
    'education', 'research', 'helping_others', 'finance', 'law',
    'construction', 'environment'
]


def generate_sample(career: str, profile: dict, add_noise: bool = True) -> dict:
    """Generate a single sample for a career"""
    sample = {}
    
    # Academic scores
    for subject in ['math', 'science', 'english']:
        if subject in profile['academic']:
            low, high = profile['academic'][subject]
        else:
            low, high = 50, 80
        
        score = random.randint(low, high)
        if add_noise:
            score = max(0, min(100, score + random.randint(-10, 10)))
        sample[f'{subject}_score'] = score
    
    # GPA
    gpa_low, gpa_high = profile['gpa_range']
    sample['gpa'] = round(random.uniform(gpa_low, gpa_high), 2)
    
    # Skills
    for skill in ALL_SKILLS:
        if skill in profile.get('skills', {}):
            low, high = profile['skills'][skill]
        else:
            low, high = 1, 3  # Default low range for non-relevant skills
        
        value = random.randint(low, high)
        if add_noise:
            value = max(1, min(5, value + random.choice([-1, 0, 0, 1])))
        sample[f'skill_{skill}'] = value
    
    # Interests
    for interest in ALL_INTERESTS:
        if interest in profile.get('interests', {}):
            low, high = profile['interests'][interest]
        else:
            low, high = 1, 3
        
        value = random.randint(low, high)
        if add_noise:
            value = max(1, min(5, value + random.choice([-1, 0, 0, 1])))
        sample[f'interest_{interest}'] = value
    
    # Label
    sample['career_label'] = career
    
    return sample


def generate_dataset(samples_per_career: int = 100) -> pd.DataFrame:
    """
    Generate complete training dataset.
    
    Args:
        samples_per_career: Number of samples to generate per career
        
    Returns:
        DataFrame with all samples
    """
    all_samples = []
    
    for career, profile in CAREER_PROFILES.items():
        print(f"Generating {samples_per_career} samples for {career}...")
        
        for _ in range(samples_per_career):
            sample = generate_sample(career, profile, add_noise=True)
            all_samples.append(sample)
    
    df = pd.DataFrame(all_samples)
    
    # Shuffle
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    
    return df


def main():
    """Generate and save sample dataset"""
    print("=" * 60)
    print("🎲 Skill Lantern - Sample Data Generator")
    print("=" * 60)
    
    # Output path
    output_dir = Path(__file__).parent.parent / "data" / "processed"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate data
    samples_per_career = 150  # 150 * 10 careers = 1500 total samples
    
    print(f"\n📊 Generating {samples_per_career} samples per career...")
    df = generate_dataset(samples_per_career)
    
    print(f"\n✅ Generated {len(df)} total samples")
    print(f"   Careers: {df['career_label'].nunique()}")
    print(f"   Features: {len(df.columns) - 1}")  # -1 for label
    
    # Save
    output_file = output_dir / "career_dataset.csv"
    df.to_csv(output_file, index=False)
    print(f"\n💾 Saved to: {output_file}")
    
    # Also save a smaller sample for quick testing
    sample_file = output_dir / "career_dataset_sample.csv"
    df.head(100).to_csv(sample_file, index=False)
    print(f"   Sample: {sample_file}")
    
    # Show sample
    print("\n📝 Sample data:")
    print(df[['math_score', 'science_score', 'gpa', 'skill_programming', 'interest_technology', 'career_label']].head(10))
    
    print("\n" + "=" * 60)
    print("✅ Data generation complete!")
    print("\nNext step: Run model training:")
    print("   python -m training.train_xgboost")
    print("=" * 60)


if __name__ == "__main__":
    main()
