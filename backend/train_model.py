"""
XGBoost Career Prediction Model Training Script
Trains a model on the career_recommender.csv dataset and saves it for use in the API.

Usage:
    python train_model.py
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder, MultiLabelBinarizer
from sklearn.metrics import (
    accuracy_score, 
    classification_report, 
    confusion_matrix,
    top_k_accuracy_score
)
import xgboost as xgb
import joblib
import os
import re
from collections import Counter

# Paths
DATA_PATH = "app/data/career_recommender.csv"
MODEL_PATH = "app/models/xgboost_model.pkl"
LABEL_ENCODER_PATH = "app/models/label_encoder.pkl"
FEATURE_COLUMNS_PATH = "app/models/feature_columns.pkl"


def load_and_preprocess_data(filepath: str) -> pd.DataFrame:
    """Load and clean the career recommendation dataset."""
    print("=" * 60)
    print("📊 LOADING AND PREPROCESSING DATA")
    print("=" * 60)
    
    df = pd.read_csv(filepath)
    print(f"✅ Loaded {len(df)} records from {filepath}")
    
    # Clean column names
    df.columns = df.columns.str.strip()
    
    # Display column info
    print(f"\n📋 Columns in dataset:")
    for col in df.columns:
        print(f"   - {col}")
    
    return df


def extract_job_title(df: pd.DataFrame) -> pd.Series:
    """Extract and clean job titles from the dataset."""
    # The job title column
    job_col = "If yes, then what is/was your first Job title in your current field of work? If not applicable, write NA."
    
    if job_col not in df.columns:
        # Try to find similar column
        for col in df.columns:
            if "Job title" in col or "job title" in col:
                job_col = col
                break
    
    jobs = df[job_col].fillna("Unknown").astype(str)
    
    # Clean job titles
    jobs = jobs.str.strip()
    jobs = jobs.replace({"NA": "Student/Unemployed", "N/A": "Student/Unemployed", 
                         "na": "Student/Unemployed", "Student (Unemployed)": "Student/Unemployed",
                         "": "Student/Unemployed"})
    
    return jobs


def categorize_career(job_title: str) -> str:
    """Map job titles to standardized career categories."""
    job_lower = str(job_title).lower().strip()
    
    # Career category mappings
    categories = {
        "Software Engineer": ["software engineer", "software developer", "programmer", 
                             "developer", "coding", "software", "full stack", "backend", 
                             "frontend", "web developer", "application developer"],
        "Data Scientist": ["data scientist", "machine learning", "ml engineer", 
                          "ai engineer", "deep learning", "artificial intelligence"],
        "Data Analyst": ["data analyst", "business analyst", "analytics", 
                        "data analysis", "bi analyst", "reporting analyst"],
        "DevOps Engineer": ["devops", "site reliability", "sre", "infrastructure",
                           "cloud engineer", "platform engineer"],
        "Network Engineer": ["network engineer", "network administrator", 
                            "system administrator", "it administrator", "network"],
        "Database Administrator": ["database", "dba", "sql developer", "data engineer"],
        "Cybersecurity Analyst": ["security", "cybersecurity", "infosec", 
                                  "penetration tester", "security analyst"],
        "Product Manager": ["product manager", "product owner", "pm", "product"],
        "Project Manager": ["project manager", "program manager", "scrum master"],
        "UI/UX Designer": ["ui", "ux", "designer", "user experience", "user interface",
                          "graphic designer", "visual designer"],
        "Quality Assurance": ["qa", "quality assurance", "tester", "testing", "sdet"],
        "Teacher/Educator": ["teacher", "professor", "lecturer", "educator", 
                            "teaching", "academic", "faculty"],
        "Finance/Accounting": ["accountant", "finance", "financial", "auditor", 
                              "banking", "investment", "chartered accountant"],
        "Sales/Marketing": ["sales", "marketing", "business development", 
                           "account manager", "digital marketing", "brand"],
        "HR/Recruiter": ["hr", "human resource", "recruiter", "talent acquisition",
                        "people operations"],
        "Consultant": ["consultant", "consulting", "advisory", "advisor"],
        "Research": ["researcher", "research", "scientist", "r&d"],
        "Healthcare": ["doctor", "nurse", "medical", "healthcare", "pharmacist",
                      "physician", "hospital"],
        "Engineering": ["engineer", "mechanical", "civil", "electrical", 
                       "electronics", "chemical", "design engineer"],
        "Management": ["manager", "director", "head", "lead", "chief", "vp", 
                      "executive", "ceo", "cto"],
    }
    
    # Check each category
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in job_lower:
                return category
    
    # Default category
    if "student" in job_lower or "unemployed" in job_lower or job_lower == "na":
        return "Student/Entry-Level"
    
    return "Other"


def encode_skills(df: pd.DataFrame) -> pd.DataFrame:
    """Encode skills column into binary features."""
    skills_col = "What are your skills ? (Select multiple if necessary)"
    
    if skills_col not in df.columns:
        for col in df.columns:
            if "skills" in col.lower():
                skills_col = col
                break
    
    # Split skills by common delimiters
    def parse_skills(skill_str):
        if pd.isna(skill_str) or str(skill_str).strip().upper() == "NO":
            return []
        skills = re.split(r'[;,\n]', str(skill_str))
        return [s.strip().lower() for s in skills if s.strip() and len(s.strip()) > 1]
    
    df['skills_list'] = df[skills_col].apply(parse_skills)
    
    # Get all unique skills
    all_skills = []
    for skills in df['skills_list']:
        all_skills.extend(skills)
    
    # Get top 50 most common skills
    skill_counts = Counter(all_skills)
    top_skills = [skill for skill, count in skill_counts.most_common(50)]
    
    print(f"\n🛠️ Top 20 skills found:")
    for skill, count in skill_counts.most_common(20):
        print(f"   - {skill}: {count}")
    
    # Create binary columns for top skills
    for skill in top_skills:
        safe_name = f"skill_{skill.replace(' ', '_').replace('-', '_')[:30]}"
        df[safe_name] = df['skills_list'].apply(lambda x: 1 if skill in x else 0)
    
    return df, top_skills


def encode_interests(df: pd.DataFrame) -> pd.DataFrame:
    """Encode interests column."""
    interests_col = "What are your interests?"
    
    if interests_col not in df.columns:
        for col in df.columns:
            if "interest" in col.lower():
                interests_col = col
                break
    
    def parse_interests(interest_str):
        if pd.isna(interest_str):
            return []
        interests = re.split(r'[;,\n]', str(interest_str))
        return [i.strip().lower() for i in interests if i.strip()]
    
    df['interests_list'] = df[interests_col].apply(parse_interests)
    
    # Get all unique interests
    all_interests = []
    for interests in df['interests_list']:
        all_interests.extend(interests)
    
    # Top interests
    interest_counts = Counter(all_interests)
    top_interests = [interest for interest, count in interest_counts.most_common(30)]
    
    print(f"\n💡 Top 15 interests found:")
    for interest, count in interest_counts.most_common(15):
        print(f"   - {interest}: {count}")
    
    # Create binary columns
    for interest in top_interests:
        safe_name = f"interest_{interest.replace(' ', '_').replace('-', '_')[:30]}"
        df[safe_name] = df['interests_list'].apply(lambda x: 1 if interest in x else 0)
    
    return df, top_interests


def prepare_features(df: pd.DataFrame) -> tuple:
    """Prepare all features for training."""
    print("\n" + "=" * 60)
    print("🔧 FEATURE ENGINEERING")
    print("=" * 60)
    
    # Extract target variable (career)
    df['job_title'] = extract_job_title(df)
    df['career_category'] = df['job_title'].apply(categorize_career)
    
    # Print career distribution
    print("\n📈 Career Category Distribution:")
    career_dist = df['career_category'].value_counts()
    for career, count in career_dist.items():
        print(f"   - {career}: {count} ({count/len(df)*100:.1f}%)")
    
    # Encode categorical features
    le_gender = LabelEncoder()
    df['gender_encoded'] = le_gender.fit_transform(df['What is your gender?'].fillna('Unknown'))
    
    # UG Course encoding
    le_course = LabelEncoder()
    df['ug_course_encoded'] = le_course.fit_transform(
        df['What was your course in UG?'].fillna('Unknown').astype(str)
    )
    
    # CGPA
    cgpa_col = [c for c in df.columns if 'CGPA' in c or 'Percentage' in c][0]
    df['cgpa'] = pd.to_numeric(df[cgpa_col], errors='coerce').fillna(70) / 100
    
    # Certifications
    cert_col = "Did you do any certification courses additionally?"
    df['has_certification'] = df[cert_col].apply(
        lambda x: 1 if str(x).lower().strip() == 'yes' else 0
    )
    
    # Working status
    work_col = "Are you working?"
    df['is_working'] = df[work_col].apply(
        lambda x: 1 if str(x).lower().strip() == 'yes' else 0
    )
    
    # Encode skills and interests
    df, top_skills = encode_skills(df)
    df, top_interests = encode_interests(df)
    
    # Collect feature columns
    feature_cols = ['gender_encoded', 'ug_course_encoded', 'cgpa', 
                   'has_certification', 'is_working']
    
    # Add skill columns
    skill_cols = [c for c in df.columns if c.startswith('skill_')]
    feature_cols.extend(skill_cols)
    
    # Add interest columns  
    interest_cols = [c for c in df.columns if c.startswith('interest_')]
    feature_cols.extend(interest_cols)
    
    print(f"\n📊 Total features: {len(feature_cols)}")
    
    # Prepare X and y
    X = df[feature_cols].values
    
    # Encode target
    le_career = LabelEncoder()
    y = le_career.fit_transform(df['career_category'])
    
    print(f"📋 Target classes: {len(le_career.classes_)}")
    for i, cls in enumerate(le_career.classes_):
        print(f"   {i}: {cls}")
    
    return X, y, feature_cols, le_career, le_gender, le_course, top_skills, top_interests


def train_model(X: np.ndarray, y: np.ndarray, feature_cols: list):
    """Train the XGBoost model."""
    print("\n" + "=" * 60)
    print("🚀 TRAINING XGBOOST MODEL")
    print("=" * 60)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"\n📊 Dataset Split:")
    print(f"   - Training samples: {len(X_train)}")
    print(f"   - Testing samples: {len(X_test)}")
    
    # Create XGBoost classifier
    model = xgb.XGBClassifier(
        n_estimators=200,
        max_depth=6,
        learning_rate=0.1,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        n_jobs=-1,
        objective='multi:softprob',
        eval_metric='mlogloss',
        use_label_encoder=False
    )
    
    print("\n⏳ Training model...")
    model.fit(
        X_train, y_train,
        eval_set=[(X_test, y_test)],
        verbose=False
    )
    
    return model, X_train, X_test, y_train, y_test


def evaluate_model(model, X_test, y_test, le_career):
    """Evaluate the trained model and print metrics."""
    print("\n" + "=" * 60)
    print("📊 MODEL EVALUATION METRICS")
    print("=" * 60)
    
    # Predictions
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)
    
    # Accuracy
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\n🎯 Overall Accuracy: {accuracy * 100:.2f}%")
    
    # Top-k Accuracy
    if len(le_career.classes_) > 2:
        top_3_acc = top_k_accuracy_score(y_test, y_pred_proba, k=3)
        top_5_acc = top_k_accuracy_score(y_test, y_pred_proba, k=min(5, len(le_career.classes_)))
        print(f"🎯 Top-3 Accuracy: {top_3_acc * 100:.2f}%")
        print(f"🎯 Top-5 Accuracy: {top_5_acc * 100:.2f}%")
    
    # Classification Report
    print("\n📋 Classification Report:")
    print("-" * 60)
    report = classification_report(
        y_test, y_pred, 
        target_names=le_career.classes_,
        zero_division=0
    )
    print(report)
    
    # Feature Importance
    print("\n🔝 Top 15 Most Important Features:")
    print("-" * 40)
    importance = model.feature_importances_
    indices = np.argsort(importance)[::-1][:15]
    
    for i, idx in enumerate(indices):
        print(f"   {i+1}. Feature {idx}: {importance[idx]:.4f}")
    
    return accuracy


def cross_validate_model(X, y):
    """Perform cross-validation."""
    print("\n" + "=" * 60)
    print("🔄 CROSS-VALIDATION (5-Fold)")
    print("=" * 60)
    
    model = xgb.XGBClassifier(
        n_estimators=100,
        max_depth=6,
        learning_rate=0.1,
        random_state=42,
        n_jobs=-1,
        use_label_encoder=False,
        eval_metric='mlogloss'
    )
    
    scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')
    
    print(f"\n📊 Cross-Validation Scores:")
    for i, score in enumerate(scores, 1):
        print(f"   Fold {i}: {score * 100:.2f}%")
    
    print(f"\n🎯 Mean CV Accuracy: {scores.mean() * 100:.2f}% (+/- {scores.std() * 2 * 100:.2f}%)")
    
    return scores.mean()


def save_model(model, le_career, feature_cols, le_gender=None, le_course=None, top_skills=None, top_interests=None):
    """Save the trained model and encoders."""
    print("\n" + "=" * 60)
    print("💾 SAVING MODEL")
    print("=" * 60)
    
    # Create directory if needed
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    
    # Save model
    joblib.dump(model, MODEL_PATH)
    print(f"✅ Model saved to: {MODEL_PATH}")
    
    # Save label encoder
    joblib.dump(le_career, LABEL_ENCODER_PATH)
    print(f"✅ Label encoder saved to: {LABEL_ENCODER_PATH}")
    
    # Save feature columns
    joblib.dump(feature_cols, FEATURE_COLUMNS_PATH)
    print(f"✅ Feature columns saved to: {FEATURE_COLUMNS_PATH}")
    
    # Save additional encoders for inference
    encoders_path = os.path.join(os.path.dirname(MODEL_PATH), "encoders.pkl")
    encoders = {
        'le_gender': le_gender,
        'le_course': le_course,
        'top_skills': top_skills,
        'top_interests': top_interests
    }
    joblib.dump(encoders, encoders_path)
    print(f"✅ Additional encoders saved to: {encoders_path}")
    
    # Print model size
    model_size = os.path.getsize(MODEL_PATH) / 1024
    print(f"\n📦 Model size: {model_size:.2f} KB")


def main():
    """Main training pipeline."""
    print("\n" + "=" * 60)
    print("🎓 SKILL LANTERN - CAREER PREDICTION MODEL TRAINING")
    print("=" * 60)
    
    # Load data
    df = load_and_preprocess_data(DATA_PATH)
    
    # Prepare features
    X, y, feature_cols, le_career, le_gender, le_course, top_skills, top_interests = prepare_features(df)
    
    # Cross-validation
    cv_accuracy = cross_validate_model(X, y)
    
    # Train final model
    model, X_train, X_test, y_train, y_test = train_model(X, y, feature_cols)
    
    # Evaluate
    test_accuracy = evaluate_model(model, X_test, y_test, le_career)
    
    # Save
    save_model(model, le_career, feature_cols, le_gender, le_course, top_skills, top_interests)
    
    print("\n" + "=" * 60)
    print("✨ TRAINING COMPLETE!")
    print("=" * 60)
    print(f"""
📊 Summary:
   - Training samples: {len(X_train)}
   - Test samples: {len(X_test)}
   - Features: {len(feature_cols)}
   - Career categories: {len(le_career.classes_)}
   - Cross-validation accuracy: {cv_accuracy * 100:.2f}%
   - Test accuracy: {test_accuracy * 100:.2f}%
   - Model saved to: {MODEL_PATH}

🚀 The model is now ready to use!
   Restart the FastAPI server to load the new model.
""")


if __name__ == "__main__":
    main()
