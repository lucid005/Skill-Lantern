"""
Career Predictor - XGBoost Model for Career Prediction
Handles loading and using the XGBoost model for career predictions.
"""

import pandas as pd
import numpy as np
from typing import List, Optional, Dict, Any, Tuple
from pathlib import Path
import logging
import re

from app.config import settings
from app.models.schemas import UserProfile, PredictedCareer

logger = logging.getLogger(__name__)


# Career categories based on the dataset
CAREER_CATEGORIES = [
    "Software Engineer",
    "Data Scientist",
    "Data Analyst",
    "Web Developer",
    "Network Engineer",
    "Database Administrator",
    "System Administrator",
    "DevOps Engineer",
    "Machine Learning Engineer",
    "Business Analyst",
    "Product Manager",
    "Project Manager",
    "UI/UX Designer",
    "Cybersecurity Analyst",
    "Cloud Engineer",
    "Mobile App Developer",
    "Quality Assurance Engineer",
    "Technical Writer",
    "IT Consultant",
    "AI Researcher"
]


class CareerPredictor:
    """
    Career prediction using XGBoost model with fallback to rule-based matching.
    
    Uses trained XGBoost model for predictions when available,
    falls back to skill/interest matching otherwise.
    """
    
    def __init__(self):
        self.model = None
        self.model_loaded = False
        self.label_encoder = None
        self.feature_columns = None
        self.encoders = None  # Additional encoders (gender, course, skills, interests)
        self.career_data: Optional[pd.DataFrame] = None
        self.skill_career_map = self._build_skill_career_map()
        
    def _build_skill_career_map(self) -> Dict[str, List[str]]:
        """Build mapping of skills to careers."""
        return {
            # Programming & Tech Skills
            "python": ["Data Scientist", "Machine Learning Engineer", "Software Engineer", "Data Analyst", "AI Researcher"],
            "java": ["Software Engineer", "Mobile App Developer", "Backend Developer", "DevOps Engineer"],
            "javascript": ["Web Developer", "Frontend Developer", "Full Stack Developer", "Mobile App Developer"],
            "sql": ["Data Analyst", "Database Administrator", "Data Scientist", "Business Analyst"],
            "c++": ["Software Engineer", "System Programmer", "Game Developer", "Embedded Systems Engineer"],
            "r": ["Data Scientist", "Data Analyst", "Statistician", "AI Researcher"],
            "machine learning": ["Machine Learning Engineer", "Data Scientist", "AI Researcher"],
            "deep learning": ["Machine Learning Engineer", "AI Researcher", "Data Scientist"],
            "ai": ["AI Researcher", "Machine Learning Engineer", "Data Scientist"],
            "cloud computing": ["Cloud Engineer", "DevOps Engineer", "System Administrator"],
            "aws": ["Cloud Engineer", "DevOps Engineer", "Solutions Architect"],
            "docker": ["DevOps Engineer", "Cloud Engineer", "Software Engineer"],
            "kubernetes": ["DevOps Engineer", "Cloud Engineer", "Site Reliability Engineer"],
            "linux": ["System Administrator", "DevOps Engineer", "Network Engineer"],
            "networking": ["Network Engineer", "System Administrator", "Cybersecurity Analyst"],
            "cybersecurity": ["Cybersecurity Analyst", "Security Engineer", "Penetration Tester"],
            "html": ["Web Developer", "Frontend Developer", "UI/UX Designer"],
            "css": ["Web Developer", "Frontend Developer", "UI/UX Designer"],
            "react": ["Frontend Developer", "Web Developer", "Full Stack Developer"],
            "node": ["Backend Developer", "Full Stack Developer", "Web Developer"],
            "database": ["Database Administrator", "Data Engineer", "Backend Developer"],
            "excel": ["Data Analyst", "Business Analyst", "Financial Analyst"],
            "tableau": ["Data Analyst", "Business Analyst", "Data Scientist"],
            "power bi": ["Data Analyst", "Business Analyst", "Data Scientist"],
            "git": ["Software Engineer", "DevOps Engineer", "Web Developer"],
            
            # Business & Soft Skills
            "communication": ["Business Analyst", "Project Manager", "Product Manager", "Consultant"],
            "leadership": ["Project Manager", "Product Manager", "Team Lead", "Manager"],
            "analytical": ["Data Analyst", "Business Analyst", "Data Scientist", "Research Analyst"],
            "problem solving": ["Software Engineer", "Data Scientist", "Business Analyst", "Consultant"],
            "critical thinking": ["Business Analyst", "Data Analyst", "Research Analyst", "Consultant"],
            "project management": ["Project Manager", "Product Manager", "Program Manager"],
            "business knowledge": ["Business Analyst", "Product Manager", "Management Consultant"],
            "presentation": ["Business Analyst", "Consultant", "Product Manager", "Sales"],
            "negotiation": ["Sales Manager", "Business Development", "Project Manager"],
            
            # Design Skills
            "design": ["UI/UX Designer", "Graphic Designer", "Product Designer"],
            "ui/ux": ["UI/UX Designer", "Product Designer", "Frontend Developer"],
            "creative": ["UI/UX Designer", "Graphic Designer", "Content Creator"],
            
            # Domain Skills
            "finance": ["Financial Analyst", "Business Analyst", "Accountant", "Risk Analyst"],
            "accounting": ["Accountant", "Financial Analyst", "Auditor"],
            "marketing": ["Digital Marketing", "Marketing Manager", "Brand Manager"],
            "sales": ["Sales Manager", "Business Development", "Account Manager"],
            "hr": ["HR Manager", "Recruiter", "HR Analyst"],
            "healthcare": ["Healthcare Analyst", "Medical Researcher", "Health Informatics"],
        }
    
    def load_career_data(self, csv_path: str = None) -> bool:
        """Load career recommendation dataset."""
        try:
            path = csv_path or settings.careers_csv_path
            
            if not Path(path).exists():
                logger.warning(f"Career data CSV not found at: {path}")
                return False
            
            self.career_data = pd.read_csv(path)
            self.career_data.columns = self.career_data.columns.str.strip()
            logger.info(f"Loaded {len(self.career_data)} career records")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load career data: {e}")
            return False
    
    def load_model(self, model_path: str = None) -> bool:
        """
        Load XGBoost model, label encoder, and feature columns.
        Returns False if model not found (uses rule-based matching instead).
        """
        try:
            import joblib
            
            model_dir = Path(model_path or settings.model_path).parent
            model_file = model_path or settings.model_path
            label_encoder_path = model_dir / "label_encoder.pkl"
            feature_columns_path = model_dir / "feature_columns.pkl"
            
            if not Path(model_file).exists():
                logger.info("XGBoost model not found, using rule-based prediction")
                return False
            
            # Load model
            self.model = joblib.load(model_file)
            logger.info("XGBoost model loaded successfully")
            
            # Load label encoder
            if label_encoder_path.exists():
                self.label_encoder = joblib.load(label_encoder_path)
                logger.info(f"Label encoder loaded with {len(self.label_encoder.classes_)} classes")
            
            # Load feature columns
            if feature_columns_path.exists():
                self.feature_columns = joblib.load(feature_columns_path)
                logger.info(f"Feature columns loaded: {len(self.feature_columns)} features")
            
            # Load additional encoders
            encoders_path = model_dir / "encoders.pkl"
            if encoders_path.exists():
                self.encoders = joblib.load(encoders_path)
                logger.info("Additional encoders loaded (gender, course, skills, interests)")
            
            self.model_loaded = True
            return True
            
        except Exception as e:
            logger.warning(f"Failed to load XGBoost model: {e}")
            return False
    
    def predict(
        self,
        user_profile: UserProfile,
        top_n: int = 3
    ) -> List[PredictedCareer]:
        """
        Predict top careers for user profile.
        
        Args:
            user_profile: User's profile data
            top_n: Number of top careers to return
            
        Returns:
            List of PredictedCareer objects
        """
        # Use XGBoost if model is loaded
        if self.model_loaded and self.model is not None:
            return self._predict_with_model(user_profile, top_n)
        
        # Otherwise use rule-based matching
        return self._predict_rule_based(user_profile, top_n)
    
    def _predict_with_model(
        self,
        user_profile: UserProfile,
        top_n: int
    ) -> List[PredictedCareer]:
        """Predict using XGBoost model with label encoder."""
        try:
            # Prepare features from user profile
            features = self._extract_features(user_profile)
            
            # Create feature DataFrame with correct column order
            if self.feature_columns is not None:
                feature_df = pd.DataFrame([features], columns=self.feature_columns)
            else:
                feature_df = pd.DataFrame([features])
            
            # Get prediction probabilities
            proba = self.model.predict_proba(feature_df)[0]
            
            # Get top N predictions
            top_indices = np.argsort(proba)[-top_n:][::-1]
            
            predictions = []
            for idx in top_indices:
                # Use label encoder to get actual career names
                if self.label_encoder is not None and idx < len(self.label_encoder.classes_):
                    career = self.label_encoder.classes_[idx]
                elif idx < len(CAREER_CATEGORIES):
                    career = CAREER_CATEGORIES[idx]
                else:
                    career = f"Career {idx}"
                    
                predictions.append(PredictedCareer(
                    career=career,
                    confidence=float(proba[idx]),
                    description=self._get_career_description(career)
                ))
            
            return predictions
            
        except Exception as e:
            logger.error(f"Model prediction failed: {e}")
            return self._predict_rule_based(user_profile, top_n)
    
    def _predict_rule_based(
        self,
        user_profile: UserProfile,
        top_n: int
    ) -> List[PredictedCareer]:
        """Predict using rule-based skill matching."""
        
        # Combine skills and interests for matching
        user_keywords = []
        user_keywords.extend([s.lower() for s in user_profile.skills])
        user_keywords.extend([i.lower() for i in user_profile.interests])
        if user_profile.specialization:
            user_keywords.extend(user_profile.specialization.lower().split())
        if user_profile.ug_course:
            user_keywords.extend(user_profile.ug_course.lower().split())
        
        # Count career matches
        career_scores: Dict[str, float] = {}
        
        for keyword in user_keywords:
            keyword_clean = keyword.strip().lower()
            
            # Check skill-career map
            for skill, careers in self.skill_career_map.items():
                if skill in keyword_clean or keyword_clean in skill:
                    for career in careers:
                        career_scores[career] = career_scores.get(career, 0) + 1
        
        # Normalize scores
        max_score = max(career_scores.values()) if career_scores else 1
        
        # Sort by score
        sorted_careers = sorted(
            career_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        # Build predictions
        predictions = []
        for career, score in sorted_careers[:top_n]:
            confidence = min(score / max_score, 0.95)  # Cap at 95%
            predictions.append(PredictedCareer(
                career=career,
                confidence=round(confidence, 2),
                description=self._get_career_description(career)
            ))
        
        # If no matches, return default suggestions
        if not predictions:
            predictions = [
                PredictedCareer(
                    career="Software Developer",
                    confidence=0.6,
                    description="Build software applications and systems"
                ),
                PredictedCareer(
                    career="Business Analyst",
                    confidence=0.5,
                    description="Analyze business needs and propose solutions"
                ),
                PredictedCareer(
                    career="Data Analyst",
                    confidence=0.4,
                    description="Analyze data to derive insights"
                )
            ]
        
        return predictions
    
    def _extract_features(self, user_profile: UserProfile) -> List[float]:
        """Extract features from user profile matching training feature columns."""
        if not self.feature_columns or not self.encoders:
            # Fallback for when encoders aren't available
            return self._extract_basic_features(user_profile)
        
        # Initialize feature dict with zeros
        feature_dict = {col: 0 for col in self.feature_columns}
        
        # Gender encoding
        gender_map = {"male": 0, "female": 1, "other": 2}
        user_gender = getattr(user_profile, 'gender', 'male')
        if 'gender_encoded' in feature_dict:
            feature_dict['gender_encoded'] = gender_map.get(str(user_gender).lower(), 0)
        
        # UG Course encoding - try to find best match
        if 'ug_course_encoded' in feature_dict:
            le_course = self.encoders.get('le_course')
            if le_course and user_profile.ug_course:
                try:
                    # Try direct match
                    course = user_profile.ug_course
                    if course in le_course.classes_:
                        feature_dict['ug_course_encoded'] = list(le_course.classes_).index(course)
                    else:
                        # Try fuzzy match
                        course_lower = course.lower()
                        for i, cls in enumerate(le_course.classes_):
                            if course_lower in str(cls).lower() or str(cls).lower() in course_lower:
                                feature_dict['ug_course_encoded'] = i
                                break
                except:
                    feature_dict['ug_course_encoded'] = 0
        
        # CGPA (normalized 0-1)
        if 'cgpa' in feature_dict:
            cgpa = user_profile.cgpa or 70
            feature_dict['cgpa'] = cgpa / 100 if cgpa > 4 else cgpa / 4
        
        # Has certification
        if 'has_certification' in feature_dict:
            feature_dict['has_certification'] = 1 if user_profile.certifications else 0
        
        # Is working
        if 'is_working' in feature_dict:
            # Assume not working if not specified
            feature_dict['is_working'] = 0
        
        # Skills encoding - match user skills to training skill columns
        top_skills = self.encoders.get('top_skills', [])
        user_skills_lower = [s.lower().strip() for s in user_profile.skills]
        
        for skill in top_skills:
            safe_name = f"skill_{skill.replace(' ', '_').replace('-', '_')[:30]}"
            if safe_name in feature_dict:
                # Check if user has this skill (fuzzy match)
                has_skill = any(skill in us or us in skill for us in user_skills_lower)
                feature_dict[safe_name] = 1 if has_skill else 0
        
        # Interests encoding - match user interests to training interest columns
        top_interests = self.encoders.get('top_interests', [])
        user_interests_lower = [i.lower().strip() for i in user_profile.interests]
        
        for interest in top_interests:
            safe_name = f"interest_{interest.replace(' ', '_').replace('-', '_')[:30]}"
            if safe_name in feature_dict:
                # Check if user has this interest (fuzzy match)
                has_interest = any(interest in ui or ui in interest for ui in user_interests_lower)
                feature_dict[safe_name] = 1 if has_interest else 0
        
        # Return features in correct column order
        return [feature_dict[col] for col in self.feature_columns]
    
    def _extract_basic_features(self, user_profile: UserProfile) -> List[float]:
        """Basic feature extraction fallback when encoders not available."""
        features = []
        
        # Education level encoding
        education_map = {
            "high_school": 0, "plus_two": 1, "bachelors": 2, "masters": 3, "phd": 4
        }
        features.append(education_map.get(user_profile.education_level.value, 2))
        
        # CGPA normalized
        features.append(user_profile.cgpa / 100 if user_profile.cgpa else 0.7)
        
        # Number of skills
        features.append(len(user_profile.skills))
        
        # Number of certifications
        features.append(len(user_profile.certifications))
        
        return features
    
    def _get_career_description(self, career: str) -> str:
        """Get brief description for a career."""
        descriptions = {
            "Software Engineer": "Design, develop, and maintain software applications",
            "Data Scientist": "Analyze complex data to help businesses make decisions",
            "Data Analyst": "Interpret data and turn it into actionable insights",
            "Web Developer": "Build and maintain websites and web applications",
            "Machine Learning Engineer": "Build and deploy machine learning models",
            "DevOps Engineer": "Bridge development and operations for faster delivery",
            "Cloud Engineer": "Design and manage cloud infrastructure",
            "Business Analyst": "Analyze business needs and propose solutions",
            "Product Manager": "Lead product development and strategy",
            "UI/UX Designer": "Design user interfaces and experiences",
            "Cybersecurity Analyst": "Protect systems from security threats",
            "Database Administrator": "Manage and optimize database systems",
            "Network Engineer": "Design and manage computer networks",
            "Project Manager": "Lead and coordinate project teams",
            "AI Researcher": "Research and develop AI technologies"
        }
        return descriptions.get(career, f"Build a career in {career}")
    
    def get_career_insights(self, career: str) -> Dict[str, Any]:
        """Get insights about a specific career from the dataset."""
        if self.career_data is None:
            self.load_career_data()
        
        if self.career_data is None:
            return {}
        
        # Search for matching records
        career_lower = career.lower()
        # This would search the actual career column if available
        
        return {
            "career": career,
            "description": self._get_career_description(career),
            "common_skills": self._get_common_skills_for_career(career),
            "growth_outlook": "Positive"
        }
    
    def _get_common_skills_for_career(self, career: str) -> List[str]:
        """Get common skills for a career."""
        career_skills = {
            "Software Engineer": ["Python", "Java", "Git", "Problem Solving", "Data Structures"],
            "Data Scientist": ["Python", "Machine Learning", "Statistics", "SQL", "Data Visualization"],
            "Web Developer": ["JavaScript", "HTML", "CSS", "React", "Node.js"],
            "DevOps Engineer": ["Docker", "Kubernetes", "CI/CD", "Linux", "Cloud"],
            "Business Analyst": ["Excel", "SQL", "Communication", "Requirements Analysis", "Presentation"]
        }
        return career_skills.get(career, ["Technical Skills", "Problem Solving", "Communication"])


# Singleton instance
career_predictor = CareerPredictor()
