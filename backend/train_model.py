"""
XGBoost Career Prediction Model Training Script
Trains a model on the career_recommender.csv dataset and saves it for use in the API.

Usage:
    python train_model.py
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

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

from app.models.career_predictor import CAREER_CATEGORIES, CareerPredictor
from app.models.schemas import EducationLevel, UserProfile

try:
    sys.stdout.reconfigure(encoding="utf-8")
except AttributeError:
    pass

# Paths
DATA_PATH = "app/data/career_recommender.csv"
MODEL_PATH = "app/models/xgboost_model.pkl"
LABEL_ENCODER_PATH = "app/models/label_encoder.pkl"
FEATURE_COLUMNS_PATH = "app/models/feature_columns.pkl"
ENCODERS_PATH = "app/models/encoders.pkl"
EVALUATION_PATH = "app/data/model_evaluation.json"


def safe_feature_name(prefix: str, value: str, max_length: int = 45) -> str:
    """Create stable feature names shared by training and inference."""
    cleaned = re.sub(r"[^a-z0-9]+", "_", str(value).lower()).strip("_")
    return f"{prefix}_{cleaned[:max_length]}"


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
    
    # Skip students/unemployed/NA - these are not useful career categories
    if not job_lower or job_lower in ["na", "n/a", "unknown", "student/unemployed", "student (unemployed)"]:
        return None  # Will be filtered out
    if job_lower.startswith("student") or job_lower == "unemployed":
        return None
    
    # Career category mappings - ordered from most specific to least specific
    categories = {
        "Legal Professional": ["lawyer", "legal", "litigation", "advocate",
                               "attorney", "counsel", "company secretary",
                               "ipr", "criminal law", "corporate law",
                               "disputes lawyer"],
        "Software Engineer": ["software engineer", "software developer", "programmer", 
                             "software", "full stack", "backend developer", 
                             "frontend developer", "web developer", "application developer",
                             "computer software"],
        "Data Scientist": ["data scientist", "machine learning", "ml engineer", 
                          "ai engineer", "deep learning", "artificial intelligence",
                          "data science"],
        "Data Analyst": ["data analyst", "business analyst", "analytics", 
                        "data analysis", "bi analyst", "reporting analyst",
                        "data engineer"],
        "Web Developer": ["web developer", "frontend", "react developer",
                         "angular developer", "web designer", "web application"],
        "Mobile App Developer": ["mobile", "android", "ios developer", "flutter",
                                "react native", "app developer"],
        "DevOps Engineer": ["devops", "site reliability", "sre", "infrastructure",
                           "cloud engineer", "platform engineer"],
        "Network Engineer": ["network engineer", "network administrator", 
                            "system administrator", "it administrator",
                            "network analyst"],
        "Database Administrator": ["database", "dba", "sql developer"],
        "Cybersecurity Analyst": ["security", "cybersecurity", "infosec", 
                                  "penetration tester", "security analyst",
                                  "ethical hacking"],
        "Product Manager": ["product manager", "product owner", "product lead"],
        "Project Manager": ["project manager", "program manager", "scrum master",
                           "project lead"],
        "UI/UX Designer": ["ui", "ux", "user experience", "user interface",
                          "graphic designer", "visual designer", "designer"],
        "Quality Assurance Engineer": ["qa", "quality assurance", "tester", "testing", "sdet"],
        "Teacher/Educator": ["teacher", "professor", "lecturer", "educator", 
                            "teaching", "academic", "faculty", "assistant professor"],
        "Financial Analyst": ["accountant", "finance", "financial", "auditor", 
                              "banking", "investment", "chartered accountant",
                              "tele-caller"],
        "Marketing Specialist": ["sales", "marketing", "business development", 
                           "account manager", "digital marketing", "brand",
                           "relationships manager"],
        "HR Manager": ["hr", "human resource", "recruiter", "talent acquisition",
                        "people operations"],
        "IT Consultant": ["consultant", "consulting", "advisory", "advisor"],
        "Research Scientist": ["researcher", "research", "scientist", "r&d"],
        "Healthcare Professional": ["doctor", "nurse", "medical", "healthcare", "pharmacist",
                      "physician", "hospital"],
        "Mechanical Engineer": ["mechanical", "design engineer", "automobile",
                               "plant", "mine engineer"],
        "Civil Engineer": ["civil", "structural", "construction"],
        "Electrical Engineer": ["electrical", "electronics", "embedded",
                               "instrumentation"],
        "Business Manager": ["manager", "director", "head", "lead", "chief", "vp", 
                      "executive", "ceo", "cto"],
    }
    
    # Check each category - more specific matches first
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in job_lower:
                return category
    
    # If no match found, try to infer from broader context
    if "engineer" in job_lower:
        return "Software Engineer"
    if "developer" in job_lower or "coding" in job_lower:
        return "Software Engineer"
    if "analyst" in job_lower:
        return "Data Analyst"
    
    return None  # Will be filtered out - no guessing


def parse_multi_value(value) -> list:
    """Parse semicolon/comma/newline separated survey values."""
    if pd.isna(value):
        return []
    text = str(value).strip()
    if not text or text.upper() in {"NO", "NA", "N/A"}:
        return []
    values = re.split(r'[;,\n]', text)
    return [item.strip() for item in values if item.strip() and len(item.strip()) > 1]


def row_to_user_profile(row: pd.Series) -> UserProfile:
    """Convert a raw survey row into the API's UserProfile shape."""
    cgpa = pd.to_numeric(
        row.get("What was the average CGPA or Percentage obtained in under graduation?", None),
        errors="coerce"
    )
    cgpa_value = float(cgpa) if pd.notna(cgpa) else None

    return UserProfile(
        education_level=EducationLevel.BACHELORS,
        gender=str(row.get("What is your gender?", "") or "").strip() or None,
        ug_course=str(row.get("What was your course in UG?", "") or "").strip() or None,
        specialization=str(row.get("What is your UG specialization? Major Subject (Eg; Mathematics)", "") or "").strip() or None,
        skills=parse_multi_value(row.get("What are your skills ? (Select multiple if necessary)", "")),
        interests=parse_multi_value(row.get("What are your interests?", "")),
        cgpa=cgpa_value,
        certifications=parse_multi_value(row.get("If yes, please specify your certificate course title.", "")),
        location="Nepal",
    )


def add_rule_based_labels_and_features(df: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    """
    Add recommendation-oriented features from the deterministic rule engine.

    The survey's job-title label is sparse and noisy. For rows without a usable
    job title, the deterministic rules provide weak labels from education,
    skills, and interests so the model learns the recommendation task rather
    than only first-job-title classification.
    """
    predictor = CareerPredictor()
    feature_cols = [safe_feature_name("rule_score", career) for career in CAREER_CATEGORIES]
    fallback_labels = []
    fallback_confidences = []
    rule_feature_rows = []

    for _, row in df.iterrows():
        profile = row_to_user_profile(row)
        predictions = predictor._predict_rule_based(profile, top_n=len(CAREER_CATEGORIES))
        score_by_career = {prediction.career: prediction.confidence for prediction in predictions}
        rule_features = {}

        fallback_labels.append(predictions[0].career if predictions else None)
        fallback_confidences.append(predictions[0].confidence if predictions else 0.0)
        for career in CAREER_CATEGORIES:
            rule_features[safe_feature_name("rule_score", career)] = score_by_career.get(career, 0.0)
        rule_feature_rows.append(rule_features)

    rule_feature_df = pd.DataFrame(rule_feature_rows, index=df.index)
    df = pd.concat([df, rule_feature_df], axis=1)
    df["rule_based_career_category"] = fallback_labels
    df["rule_based_career_confidence"] = fallback_confidences
    return df, feature_cols


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
    skill_features = {
        f"skill_{skill.replace(' ', '_').replace('-', '_')[:30]}": df['skills_list'].apply(lambda x, skill=skill: 1 if skill in x else 0)
        for skill in top_skills
    }
    df = pd.concat([df, pd.DataFrame(skill_features, index=df.index)], axis=1)
    
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
    interest_features = {
        f"interest_{interest.replace(' ', '_').replace('-', '_')[:30]}": df['interests_list'].apply(lambda x, interest=interest: 1 if interest in x else 0)
        for interest in top_interests
    }
    df = pd.concat([df, pd.DataFrame(interest_features, index=df.index)], axis=1)
    
    return df, top_interests


def prepare_features(df: pd.DataFrame) -> tuple:
    """Prepare all features for training."""
    print("\n" + "=" * 60)
    print("🔧 FEATURE ENGINEERING")
    print("=" * 60)
    
    # Extract target variable (career)
    df['job_title'] = extract_job_title(df)
    df['career_category'] = df['job_title'].apply(categorize_career)
    df, rule_feature_cols = add_rule_based_labels_and_features(df)
    df['career_category'] = df['career_category'].fillna(df['rule_based_career_category'])

    weak_label_count = int(df["job_title"].apply(categorize_career).isna().sum())
    print(f"\n🔁 Added {weak_label_count} weak recommendation labels for rows without usable job titles")
    
    # Remove rows where both job-title and rule-based labeling failed.
    before_count = len(df)
    df = df[df['career_category'].notna()].reset_index(drop=True)
    removed_count = before_count - len(df)
    print(f"\n🗑️ Removed {removed_count} rows with no usable career label")
    print(f"📊 Remaining records: {len(df)}")
    
    # Remove career categories with fewer than 3 samples (can't train reliably)
    MIN_SAMPLES = 3
    career_counts = df['career_category'].value_counts()
    rare_careers = career_counts[career_counts < MIN_SAMPLES].index.tolist()
    if rare_careers:
        print(f"\n⚠️ Removing {len(rare_careers)} rare categories (< {MIN_SAMPLES} samples): {rare_careers}")
        df = df[~df['career_category'].isin(rare_careers)].reset_index(drop=True)
        print(f"📊 Remaining records after filtering rare categories: {len(df)}")
    
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

    # Add deterministic recommendation signals as model features.
    feature_cols.extend(rule_feature_cols)
    
    print(f"\n📊 Total features: {len(feature_cols)}")
    
    # Prepare X and y
    X = df[feature_cols].values
    
    # Encode target
    le_career = LabelEncoder()
    y = le_career.fit_transform(df['career_category'])
    
    print(f"📋 Target classes: {len(le_career.classes_)}")
    for i, cls in enumerate(le_career.classes_):
        print(f"   {i}: {cls}")
    
    metadata = {
        "source_rows": int(before_count),
        "usable_rows": int(len(df)),
        "removed_rows": int(removed_count),
        "career_distribution": {
            career: int(count) for career, count in df["career_category"].value_counts().items()
        },
    }

    return X, y, feature_cols, le_career, le_gender, le_course, top_skills, top_interests, metadata


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
    
    # Create XGBoost classifier with improved hyperparameters
    n_classes = len(np.unique(y_train))
    model = xgb.XGBClassifier(
        n_estimators=350,
        max_depth=5,
        learning_rate=0.05,
        subsample=0.9,
        colsample_bytree=0.9,
        min_child_weight=2,
        gamma=0.05,
        reg_alpha=0.05,
        reg_lambda=1.5,
        random_state=42,
        n_jobs=-1,
        objective='multi:softprob',
        num_class=n_classes,
        eval_metric='mlogloss',
    )
    
    print("\n⏳ Training model...")
    model.fit(
        X_train, y_train,
        eval_set=[(X_test, y_test)],
        verbose=False
    )
    
    return model, X_train, X_test, y_train, y_test


def evaluate_model(model, X_test, y_test, le_career, feature_cols):
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

    labels = list(range(len(le_career.classes_)))
    top_3_acc = None
    top_5_acc = None
    
    # Top-k Accuracy
    if len(le_career.classes_) > 2:
        top_3_acc = top_k_accuracy_score(y_test, y_pred_proba, k=3, labels=labels)
        top_5_acc = top_k_accuracy_score(
            y_test,
            y_pred_proba,
            k=min(5, len(le_career.classes_)),
            labels=labels
        )
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

    report_dict = classification_report(
        y_test,
        y_pred,
        labels=labels,
        target_names=le_career.classes_,
        zero_division=0,
        output_dict=True,
    )
    
    # Feature Importance
    print("\n🔝 Top 15 Most Important Features:")
    print("-" * 40)
    importance = model.feature_importances_
    indices = np.argsort(importance)[::-1][:15]
    
    top_features = []
    for i, idx in enumerate(indices):
        feature_name = feature_cols[idx] if idx < len(feature_cols) else f"feature_{idx}"
        top_features.append({
            "rank": i + 1,
            "feature": feature_name,
            "importance": float(importance[idx]),
        })
        print(f"   {i+1}. {feature_name}: {importance[idx]:.4f}")

    return {
        "accuracy": float(accuracy),
        "top_3_accuracy": float(top_3_acc) if top_3_acc is not None else None,
        "top_5_accuracy": float(top_5_acc) if top_5_acc is not None else None,
        "classification_report": report_dict,
        "top_features": top_features,
    }


def cross_validate_model(X, y):
    """Perform cross-validation."""
    print("\n" + "=" * 60)
    print("🔄 CROSS-VALIDATION (5-Fold)")
    print("=" * 60)
    
    min_class_count = min(Counter(y).values())
    folds = min(5, min_class_count)
    if folds < 2:
        print("\n⚠️ Skipping cross-validation because at least one class has fewer than 2 samples.")
        return None

    model = xgb.XGBClassifier(
        n_estimators=100,
        max_depth=5,
        learning_rate=0.1,
        random_state=42,
        n_jobs=-1,
        objective='multi:softprob',
        num_class=len(np.unique(y)),
        eval_metric='mlogloss',
    )
    
    scores = cross_val_score(model, X, y, cv=folds, scoring='accuracy')
    
    print(f"\n📊 Cross-Validation Scores:")
    for i, score in enumerate(scores, 1):
        print(f"   Fold {i}: {score * 100:.2f}%")
    
    print(f"\n🎯 Mean CV Accuracy ({folds}-fold): {scores.mean() * 100:.2f}% (+/- {scores.std() * 2 * 100:.2f}%)")
    
    return {
        "folds": int(folds),
        "scores": [float(score) for score in scores],
        "mean_accuracy": float(scores.mean()),
        "std_accuracy": float(scores.std()),
    }


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
    encoders = {
        'le_gender': le_gender,
        'le_course': le_course,
        'top_skills': top_skills,
        'top_interests': top_interests
    }
    joblib.dump(encoders, ENCODERS_PATH)
    print(f"✅ Additional encoders saved to: {ENCODERS_PATH}")
    
    # Print model size
    model_size = os.path.getsize(MODEL_PATH) / 1024
    print(f"\n📦 Model size: {model_size:.2f} KB")


def evaluate_viva_profiles() -> list:
    """Evaluate the saved model on representative, explainable demo profiles."""
    from app.models.career_predictor import CareerPredictor
    from app.models.schemas import UserProfile, EducationLevel

    predictor = CareerPredictor()
    predictor.load_model()

    profiles = [
        {
            "label": "CS/ML student",
            "expected": "Data Scientist",
            "profile": UserProfile(
                education_level=EducationLevel.BACHELORS,
                ug_course="BCA",
                specialization="Computer Science",
                skills=["Python", "Machine Learning", "SQL", "Data Visualization"],
                interests=["Artificial Intelligence", "Data Analysis"],
                cgpa=78.0,
                location="Nepal",
            ),
        },
        {
            "label": "MBA marketing student",
            "expected": "Marketing Specialist",
            "profile": UserProfile(
                education_level=EducationLevel.MASTERS,
                ug_course="MBA",
                specialization="Marketing",
                skills=["Digital Marketing", "SEO", "Content Writing", "Social Media"],
                interests=["Sales", "Brand Management"],
                cgpa=72.0,
                location="Nepal",
            ),
        },
        {
            "label": "UI/UX design student",
            "expected": "UI/UX Designer",
            "profile": UserProfile(
                education_level=EducationLevel.BACHELORS,
                ug_course="B.Des",
                specialization="Design",
                skills=["Figma", "UI Design", "Prototyping", "CSS", "HTML"],
                interests=["User Experience", "Visual Design"],
                cgpa=80.0,
                location="Nepal",
            ),
        },
        {
            "label": "Java backend developer",
            "expected": "Software Engineer",
            "profile": UserProfile(
                education_level=EducationLevel.BACHELORS,
                ug_course="B.E",
                specialization="Computer Engineering",
                skills=["Java", "Spring Boot", "SQL", "Git"],
                interests=["Software Development", "Backend Systems"],
                cgpa=75.0,
                location="Nepal",
            ),
        },
        {
            "label": "Healthcare student",
            "expected": "Healthcare Professional",
            "profile": UserProfile(
                education_level=EducationLevel.BACHELORS,
                ug_course="MBBS",
                specialization="Medicine",
                skills=["Patient Care", "Communication"],
                interests=["Healthcare", "Medical Research"],
                cgpa=82.0,
                location="Nepal",
            ),
        },
        {
            "label": "LLM criminal law student",
            "expected": "Legal Professional",
            "profile": UserProfile(
                education_level=EducationLevel.MASTERS,
                ug_course="LLM",
                specialization="Criminal Law",
                skills=["Legal Research", "Legal Writing", "Critical Thinking"],
                interests=["Law", "Research", "Litigation & Legal Service"],
                cgpa=76.0,
                location="Nepal",
            ),
        },
    ]

    results = []
    print("\n" + "=" * 60)
    print("🧪 REPRESENTATIVE PROFILE CHECKS")
    print("=" * 60)
    for item in profiles:
        predictions = predictor.predict(item["profile"], top_n=5)
        top = predictions[0].career if predictions else None
        passed = top == item["expected"]
        print(f"\n{item['label']} -> expected: {item['expected']} | top: {top} | {'PASS' if passed else 'REVIEW'}")
        for index, prediction in enumerate(predictions, 1):
            print(f"  {index}. {prediction.career} ({prediction.confidence:.3f})")

        results.append({
            "label": item["label"],
            "expected_top": item["expected"],
            "actual_top": top,
            "passed": passed,
            "predictions": [prediction.model_dump() for prediction in predictions],
        })

    return results


def save_evaluation_report(report: dict) -> None:
    """Persist metrics for viva/reporting and future comparison."""
    Path(EVALUATION_PATH).parent.mkdir(parents=True, exist_ok=True)
    with open(EVALUATION_PATH, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=2)
    print(f"\n✅ Evaluation report saved to: {EVALUATION_PATH}")


def main():
    """Main training pipeline."""
    print("\n" + "=" * 60)
    print("🎓 SKILL LANTERN - CAREER PREDICTION MODEL TRAINING")
    print("=" * 60)
    
    # Load data
    df = load_and_preprocess_data(DATA_PATH)
    
    # Prepare features
    X, y, feature_cols, le_career, le_gender, le_course, top_skills, top_interests, dataset_metadata = prepare_features(df)
    
    # Cross-validation
    cv_results = cross_validate_model(X, y)
    
    # Train final model
    model, X_train, X_test, y_train, y_test = train_model(X, y, feature_cols)
    
    # Evaluate
    test_results = evaluate_model(model, X_test, y_test, le_career, feature_cols)
    
    # Save
    save_model(model, le_career, feature_cols, le_gender, le_course, top_skills, top_interests)

    representative_results = evaluate_viva_profiles()
    evaluation_report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "data_path": DATA_PATH,
        "model_path": MODEL_PATH,
        "dataset": dataset_metadata,
        "feature_count": len(feature_cols),
        "target_classes": list(le_career.classes_),
        "cross_validation": cv_results,
        "holdout": test_results,
        "representative_profiles": representative_results,
    }
    save_evaluation_report(evaluation_report)

    cv_summary = (
        f"{cv_results['mean_accuracy'] * 100:.2f}%"
        if cv_results
        else "not available"
    )
    
    print("\n" + "=" * 60)
    print("✨ TRAINING COMPLETE!")
    print("=" * 60)
    print(f"""
📊 Summary:
   - Training samples: {len(X_train)}
   - Test samples: {len(X_test)}
   - Features: {len(feature_cols)}
   - Career categories: {len(le_career.classes_)}
   - Cross-validation accuracy: {cv_summary}
   - Test accuracy: {test_results['accuracy'] * 100:.2f}%
   - Top-3 accuracy: {test_results['top_3_accuracy'] * 100:.2f}%
   - Top-5 accuracy: {test_results['top_5_accuracy'] * 100:.2f}%
   - Model saved to: {MODEL_PATH}
   - Evaluation saved to: {EVALUATION_PATH}

🚀 The model is now ready to use!
   Restart the FastAPI server to load the new model.
""")


if __name__ == "__main__":
    main()
