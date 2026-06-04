"""
Career Predictor - Hybrid XGBoost + Gemini LLM Career Prediction
Handles loading and using the XGBoost model for career predictions,
then refines results using Gemini for contextual accuracy.
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


# Career categories based on the dataset - must match train_model.py categories
CAREER_CATEGORIES = [
    "Software Engineer",
    "Data Scientist",
    "Data Analyst",
    "Web Developer",
    "Mobile App Developer",
    "Network Engineer",
    "Database Administrator",
    "DevOps Engineer",
    "Cybersecurity Analyst",
    "Product Manager",
    "Project Manager",
    "UI/UX Designer",
    "Quality Assurance Engineer",
    "Teacher/Educator",
    "Financial Analyst",
    "Marketing Specialist",
    "HR Manager",
    "IT Consultant",   
    "Research Scientist",
    "Healthcare Professional",
    "Mechanical Engineer",
    "Civil Engineer",
    "Electrical Engineer",
    "Legal Professional",
    "Business Manager"
]


class CareerPredictor:
    """
    Career prediction using a hybrid approach:
    
    1. XGBoost model provides fast initial predictions with probability scores.
    2. Gemini LLM refines and re-ranks using full profile context.
    3. Rule-based weighted matching as final fallback.
    """
    
    def __init__(self):
        self.model = None
        self.model_loaded = False
        self.label_encoder = None
        self.feature_columns = None
        self.encoders = None  # Additional encoders (gender, course, skills, interests)
        self.career_data: Optional[pd.DataFrame] = None
        self.skill_career_map = self._build_skill_career_map()
        self._education_career_boost = self._build_education_boost_map()
        self._specialization_career_map = self._build_specialization_map()
        
    def _build_skill_career_map(self) -> Dict[str, List[Tuple[str, float]]]:
        """Build mapping of skills to careers with relevance weights.
        
        Each skill maps to a list of (career, weight) tuples.
        Weight reflects how strongly the skill indicates that career:
        - 3.0 = primary/defining skill for the career
        - 2.0 = important skill
        - 1.0 = useful but not defining
        """
        return {
            # Programming & Tech Skills
            "python": [("Data Scientist", 3.0), ("Software Engineer", 2.0), ("Data Analyst", 2.0), ("Research Scientist", 2.0)],
            "java": [("Software Engineer", 3.0), ("Mobile App Developer", 2.0), ("DevOps Engineer", 1.0)],
            "javascript": [("Web Developer", 3.0), ("Software Engineer", 2.0), ("Mobile App Developer", 1.0)],
            "typescript": [("Web Developer", 3.0), ("Software Engineer", 2.0)],
            "sql": [("Data Analyst", 3.0), ("Database Administrator", 3.0), ("Data Scientist", 2.0), ("Software Engineer", 1.0)],
            "c++": [("Software Engineer", 3.0), ("Electrical Engineer", 2.0), ("Research Scientist", 1.0)],
            "c": [("Software Engineer", 2.0), ("Electrical Engineer", 2.0), ("Mechanical Engineer", 1.0)],
            "c#": [("Software Engineer", 3.0), ("Web Developer", 1.0)],
            "r": [("Data Scientist", 3.0), ("Data Analyst", 2.0), ("Research Scientist", 2.0)],
            "machine learning": [("Data Scientist", 3.0), ("Research Scientist", 2.0), ("Software Engineer", 1.0)],
            "deep learning": [("Data Scientist", 3.0), ("Research Scientist", 2.0)],
            "artificial intelligence": [("Data Scientist", 3.0), ("Research Scientist", 2.0), ("Software Engineer", 1.0)],
            "ai": [("Data Scientist", 3.0), ("Research Scientist", 2.0), ("Software Engineer", 1.0)],
            "cloud computing": [("DevOps Engineer", 3.0), ("Software Engineer", 1.0)],
            "aws": [("DevOps Engineer", 3.0), ("Software Engineer", 1.0)],
            "azure": [("DevOps Engineer", 3.0), ("Software Engineer", 1.0)],
            "gcp": [("DevOps Engineer", 3.0), ("Software Engineer", 1.0)],
            "docker": [("DevOps Engineer", 3.0), ("Software Engineer", 1.0)],
            "kubernetes": [("DevOps Engineer", 3.0), ("Software Engineer", 1.0)],
            "linux": [("DevOps Engineer", 2.0), ("Network Engineer", 2.0), ("Cybersecurity Analyst", 1.0), ("Software Engineer", 1.0)],
            "networking": [("Network Engineer", 3.0), ("Cybersecurity Analyst", 2.0)],
            "cybersecurity": [("Cybersecurity Analyst", 3.0), ("Network Engineer", 1.0)],
            "ethical hacking": [("Cybersecurity Analyst", 3.0)],
            "penetration testing": [("Cybersecurity Analyst", 3.0)],
            "html": [("Web Developer", 2.0), ("UI/UX Designer", 1.0)],
            "css": [("Web Developer", 2.0), ("UI/UX Designer", 1.0)],
            "react": [("Web Developer", 3.0), ("Software Engineer", 2.0), ("Mobile App Developer", 1.0)],
            "angular": [("Web Developer", 3.0), ("Software Engineer", 2.0)],
            "vue": [("Web Developer", 3.0), ("Software Engineer", 1.0)],
            "node.js": [("Web Developer", 3.0), ("Software Engineer", 2.0)],
            "node": [("Web Developer", 3.0), ("Software Engineer", 2.0)],
            "express": [("Web Developer", 2.0), ("Software Engineer", 1.0)],
            "mern": [("Web Developer", 3.0), ("Software Engineer", 2.0)],
            "mean": [("Web Developer", 3.0), ("Software Engineer", 2.0)],
            "next.js": [("Web Developer", 3.0), ("Software Engineer", 2.0)],
            "nextjs": [("Web Developer", 3.0), ("Software Engineer", 2.0)],
            "django": [("Web Developer", 3.0), ("Software Engineer", 2.0)],
            "flask": [("Web Developer", 2.0), ("Software Engineer", 2.0)],
            "spring": [("Software Engineer", 3.0)],
            "spring boot": [("Software Engineer", 3.0)],
            "flutter": [("Mobile App Developer", 3.0), ("Software Engineer", 1.0)],
            "kotlin": [("Mobile App Developer", 3.0), ("Software Engineer", 2.0)],
            "swift": [("Mobile App Developer", 3.0), ("Software Engineer", 1.0)],
            "react native": [("Mobile App Developer", 3.0), ("Web Developer", 1.0)],
            "android": [("Mobile App Developer", 3.0)],
            "ios": [("Mobile App Developer", 3.0)],
            "database": [("Database Administrator", 3.0), ("Data Analyst", 1.0), ("Software Engineer", 1.0)],
            "mongodb": [("Database Administrator", 2.0), ("Web Developer", 2.0), ("Software Engineer", 1.0)],
            "postgresql": [("Database Administrator", 3.0), ("Software Engineer", 1.0)],
            "mysql": [("Database Administrator", 3.0), ("Software Engineer", 1.0)],
            "oracle": [("Database Administrator", 3.0)],
            "excel": [("Data Analyst", 2.0), ("Financial Analyst", 2.0), ("Business Manager", 1.0)],
            "tableau": [("Data Analyst", 3.0), ("Data Scientist", 1.0)],
            "power bi": [("Data Analyst", 3.0), ("Financial Analyst", 1.0)],
            "data visualization": [("Data Analyst", 3.0), ("Data Scientist", 2.0)],
            "statistics": [("Data Scientist", 3.0), ("Data Analyst", 2.0), ("Research Scientist", 2.0)],
            "git": [("Software Engineer", 1.0), ("DevOps Engineer", 1.0), ("Web Developer", 1.0)],
            "github": [("Software Engineer", 1.0), ("DevOps Engineer", 1.0)],
            "figma": [("UI/UX Designer", 3.0), ("Web Developer", 1.0)],
            "sketch": [("UI/UX Designer", 3.0)],
            "adobe xd": [("UI/UX Designer", 3.0)],
            "photoshop": [("UI/UX Designer", 2.0)],
            "illustrator": [("UI/UX Designer", 2.0)],
            "autocad": [("Civil Engineer", 3.0), ("Mechanical Engineer", 3.0)],
            "solidworks": [("Mechanical Engineer", 3.0)],
            "catia": [("Mechanical Engineer", 3.0)],
            "matlab": [("Electrical Engineer", 3.0), ("Research Scientist", 2.0), ("Mechanical Engineer", 2.0)],
            "testing": [("Quality Assurance Engineer", 3.0), ("Software Engineer", 1.0)],
            "selenium": [("Quality Assurance Engineer", 3.0)],
            "cypress": [("Quality Assurance Engineer", 3.0)],
            "jest": [("Quality Assurance Engineer", 2.0), ("Web Developer", 1.0)],
            "ci/cd": [("DevOps Engineer", 3.0), ("Software Engineer", 1.0)],
            "jenkins": [("DevOps Engineer", 3.0)],
            "terraform": [("DevOps Engineer", 3.0)],
            "ansible": [("DevOps Engineer", 3.0)],
            
            # Soft/Business Skills
            "communication": [("Business Manager", 2.0), ("Project Manager", 2.0), ("Product Manager", 2.0), ("Marketing Specialist", 1.0), ("HR Manager", 1.0)],
            "leadership": [("Project Manager", 3.0), ("Product Manager", 2.0), ("Business Manager", 2.0)],
            "analytical thinking": [("Data Analyst", 2.0), ("Data Scientist", 2.0), ("Financial Analyst", 2.0)],
            "analytical": [("Data Analyst", 2.0), ("Financial Analyst", 2.0), ("Data Scientist", 1.0)],
            "problem solving": [("Software Engineer", 1.0), ("Data Scientist", 1.0), ("Business Manager", 1.0)],
            "critical thinking": [("Data Analyst", 1.0), ("Research Scientist", 2.0), ("IT Consultant", 1.0)],
            "project management": [("Project Manager", 3.0), ("Product Manager", 2.0), ("Business Manager", 1.0)],
            "business knowledge": [("Business Manager", 3.0), ("Product Manager", 2.0), ("Marketing Specialist", 1.0)],
            "presentation": [("Business Manager", 1.0), ("IT Consultant", 2.0), ("Product Manager", 1.0)],
            "negotiation": [("Marketing Specialist", 2.0), ("Business Manager", 2.0), ("HR Manager", 1.0)],
            "teamwork": [("Project Manager", 1.0), ("Software Engineer", 1.0)],
            "writing": [("IT Consultant", 1.0), ("Product Manager", 1.0), ("Marketing Specialist", 2.0)],
            "public speaking": [("Teacher/Educator", 2.0), ("Business Manager", 1.0), ("Marketing Specialist", 1.0)],
            "legal research": [("Legal Professional", 3.0), ("Research Scientist", 1.0)],
            "legal writing": [("Legal Professional", 3.0)],
            "legal compliance": [("Legal Professional", 3.0), ("HR Manager", 1.0)],
            "law": [("Legal Professional", 3.0)],
            "legal": [("Legal Professional", 3.0)],
            "litigation & legal service": [("Legal Professional", 3.0)],
            "litigation": [("Legal Professional", 3.0)],
            "legal advice": [("Legal Professional", 3.0)],
            "civil law": [("Legal Professional", 3.0)],
            "criminal law": [("Legal Professional", 3.0)],
            "corporate law": [("Legal Professional", 3.0), ("Business Manager", 1.0)],
            "company law": [("Legal Professional", 3.0), ("Financial Analyst", 1.0)],
            "contract management": [("Legal Professional", 2.0), ("Project Manager", 1.0)],
            
            # Design Skills
            "design": [("UI/UX Designer", 2.0), ("Web Developer", 1.0)],
            "ui/ux": [("UI/UX Designer", 3.0), ("Web Developer", 1.0)],
            "ui design": [("UI/UX Designer", 3.0)],
            "ux design": [("UI/UX Designer", 3.0)],
            "ux research": [("UI/UX Designer", 3.0), ("Product Manager", 1.0)],
            "graphic design": [("UI/UX Designer", 2.0)],
            "creative": [("UI/UX Designer", 1.0), ("Marketing Specialist", 1.0)],
            "prototyping": [("UI/UX Designer", 3.0), ("Product Manager", 1.0)],
            "wireframing": [("UI/UX Designer", 3.0)],
            
            # Domain Skills
            "finance": [("Financial Analyst", 3.0), ("Business Manager", 1.0)],
            "accounting": [("Financial Analyst", 3.0), ("Business Manager", 1.0)],
            "financial modeling": [("Financial Analyst", 3.0)],
            "tally": [("Financial Analyst", 2.0)],
            "marketing": [("Marketing Specialist", 3.0), ("Business Manager", 1.0)],
            "digital marketing": [("Marketing Specialist", 3.0)],
            "seo": [("Marketing Specialist", 3.0), ("Web Developer", 1.0)],
            "content writing": [("Marketing Specialist", 2.0)],
            "social media": [("Marketing Specialist", 2.0)],
            "sales": [("Marketing Specialist", 2.0), ("Business Manager", 2.0)],
            "hr": [("HR Manager", 3.0)],
            "human resources": [("HR Manager", 3.0)],
            "recruitment": [("HR Manager", 3.0)],
            "people management": [("HR Manager", 2.0), ("Business Manager", 1.0)],
            "teaching": [("Teacher/Educator", 3.0)],
            "education": [("Teacher/Educator", 2.0)],
            "pedagogy": [("Teacher/Educator", 3.0)],
            "curriculum": [("Teacher/Educator", 3.0)],
            "medical": [("Healthcare Professional", 3.0)],
            "healthcare": [("Healthcare Professional", 3.0)],
            "nursing": [("Healthcare Professional", 3.0)],
            "pharmacy": [("Healthcare Professional", 3.0)],
            "research": [("Research Scientist", 3.0), ("Data Scientist", 1.0)],
            "data analysis": [("Data Analyst", 3.0), ("Data Scientist", 2.0)],
            "data science": [("Data Scientist", 3.0), ("Data Analyst", 1.0)],
            "agile": [("Project Manager", 2.0), ("Product Manager", 2.0), ("Software Engineer", 1.0)],
            "scrum": [("Project Manager", 3.0), ("Product Manager", 1.0)],
        }
    
    def _build_education_boost_map(self) -> Dict[str, List[Tuple[str, float]]]:
        """Map education keywords to career boosts.
        
        If a user's UG course or specialization contains these keywords,
        the corresponding careers get a significant score boost.
        """
        return {
            # Engineering
            "computer science": [("Software Engineer", 5.0), ("Web Developer", 3.0), ("Data Scientist", 3.0), ("Mobile App Developer", 2.0), ("DevOps Engineer", 2.0)],
            "computer engineering": [("Software Engineer", 5.0), ("Network Engineer", 3.0), ("DevOps Engineer", 2.0)],
            "information technology": [("Software Engineer", 4.0), ("Web Developer", 3.0), ("Network Engineer", 2.0), ("IT Consultant", 3.0)],
            "it": [("Software Engineer", 3.0), ("Web Developer", 2.0), ("IT Consultant", 2.0)],
            "software": [("Software Engineer", 5.0), ("Web Developer", 3.0)],
            "electronics": [("Electrical Engineer", 5.0), ("Software Engineer", 1.0)],
            "electrical": [("Electrical Engineer", 5.0)],
            "mechanical": [("Mechanical Engineer", 5.0)],
            "civil": [("Civil Engineer", 5.0)],
            "bca": [("Software Engineer", 4.0), ("Web Developer", 3.0), ("Mobile App Developer", 2.0)],
            "bsc csit": [("Software Engineer", 5.0), ("Data Scientist", 3.0), ("Web Developer", 3.0)],
            "csit": [("Software Engineer", 5.0), ("Data Scientist", 3.0), ("Web Developer", 3.0)],
            "b.e": [("Software Engineer", 3.0), ("Mechanical Engineer", 2.0), ("Civil Engineer", 2.0), ("Electrical Engineer", 2.0)],
            "b.tech": [("Software Engineer", 3.0), ("Mechanical Engineer", 2.0), ("Civil Engineer", 2.0), ("Electrical Engineer", 2.0)],
            "bsc": [("Research Scientist", 2.0), ("Data Analyst", 1.0)],
            "mca": [("Software Engineer", 4.0), ("Web Developer", 3.0)],
            
            # Business & Management
            "mba": [("Business Manager", 5.0), ("Marketing Specialist", 3.0), ("HR Manager", 3.0), ("Financial Analyst", 2.0), ("Product Manager", 3.0)],
            "bba": [("Business Manager", 4.0), ("Marketing Specialist", 3.0), ("HR Manager", 2.0)],
            "commerce": [("Financial Analyst", 4.0), ("Business Manager", 3.0)],
            "bcom": [("Financial Analyst", 4.0), ("Business Manager", 3.0)],
            "economics": [("Financial Analyst", 4.0), ("Data Analyst", 2.0), ("Business Manager", 2.0)],
            "finance": [("Financial Analyst", 5.0), ("Business Manager", 2.0)],
            "marketing": [("Marketing Specialist", 5.0), ("Business Manager", 2.0)],
            "human resource": [("HR Manager", 5.0)],
            
            # Science & Research
            "physics": [("Research Scientist", 4.0), ("Data Scientist", 2.0)],
            "mathematics": [("Data Scientist", 4.0), ("Research Scientist", 3.0), ("Financial Analyst", 2.0)],
            "statistics": [("Data Scientist", 5.0), ("Data Analyst", 4.0), ("Research Scientist", 2.0)],
            "biology": [("Healthcare Professional", 3.0), ("Research Scientist", 3.0)],
            "chemistry": [("Research Scientist", 4.0), ("Healthcare Professional", 1.0)],
            "data science": [("Data Scientist", 5.0), ("Data Analyst", 3.0)],
            
            # Health
            "mbbs": [("Healthcare Professional", 5.0)],
            "nursing": [("Healthcare Professional", 5.0)],
            "pharmacy": [("Healthcare Professional", 5.0)],
            "public health": [("Healthcare Professional", 4.0)],
            
            # Arts & Education
            "education": [("Teacher/Educator", 5.0)],
            "b.ed": [("Teacher/Educator", 5.0)],
            "bed": [("Teacher/Educator", 5.0)],
            "psychology": [("HR Manager", 3.0), ("Teacher/Educator", 2.0), ("Research Scientist", 1.0)],
            "design": [("UI/UX Designer", 5.0), ("Web Developer", 2.0)],
            "fine arts": [("UI/UX Designer", 4.0)],

            # Law
            "law": [("Legal Professional", 5.0)],
            "llb": [("Legal Professional", 5.0)],
            "llm": [("Legal Professional", 5.0)],
            "ballb": [("Legal Professional", 5.0)],
            "ba llb": [("Legal Professional", 5.0)],
            "criminal law": [("Legal Professional", 5.0)],
            "criminal justice": [("Legal Professional", 5.0)],
            "corporate law": [("Legal Professional", 5.0), ("Business Manager", 1.0)],
            "company law": [("Legal Professional", 5.0), ("Financial Analyst", 1.0)],
        }
    
    def _build_specialization_map(self) -> Dict[str, List[Tuple[str, float]]]:
        """Map specialization keywords to direct career matches."""
        return {
            "web development": [("Web Developer", 5.0), ("Software Engineer", 2.0)],
            "mobile development": [("Mobile App Developer", 5.0)],
            "android development": [("Mobile App Developer", 5.0)],
            "ios development": [("Mobile App Developer", 5.0)],
            "data science": [("Data Scientist", 5.0), ("Data Analyst", 2.0)],
            "machine learning": [("Data Scientist", 5.0), ("Research Scientist", 2.0)],
            "artificial intelligence": [("Data Scientist", 5.0), ("Research Scientist", 3.0)],
            "cybersecurity": [("Cybersecurity Analyst", 5.0)],
            "network security": [("Cybersecurity Analyst", 5.0), ("Network Engineer", 2.0)],
            "cloud computing": [("DevOps Engineer", 5.0)],
            "devops": [("DevOps Engineer", 5.0)],
            "database management": [("Database Administrator", 5.0)],
            "ui/ux": [("UI/UX Designer", 5.0)],
            "user experience": [("UI/UX Designer", 5.0)],
            "product management": [("Product Manager", 5.0)],
            "project management": [("Project Manager", 5.0)],
            "digital marketing": [("Marketing Specialist", 5.0)],
            "financial analysis": [("Financial Analyst", 5.0)],
            "human resources": [("HR Manager", 5.0)],
            "law": [("Legal Professional", 5.0)],
            "criminal law": [("Legal Professional", 5.0)],
            "corporate law": [("Legal Professional", 5.0)],
            "civil law": [("Legal Professional", 5.0)],
            "legal studies": [("Legal Professional", 5.0)],
            "criminal justice": [("Legal Professional", 5.0)],
            "structural engineering": [("Civil Engineer", 5.0)],
            "power systems": [("Electrical Engineer", 5.0)],
            "thermodynamics": [("Mechanical Engineer", 5.0)],
            "quality assurance": [("Quality Assurance Engineer", 5.0)],
            "software testing": [("Quality Assurance Engineer", 5.0)],
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
    

    # ------------------------------------------------------------------
    # PUBLIC PREDICTION API
    # ------------------------------------------------------------------

    def predict(
        self,
        user_profile: UserProfile,
        top_n: int = 5
    ) -> List[PredictedCareer]:
        """
        Predict top careers for user profile (synchronous, no LLM).
        
        Uses XGBoost if loaded, otherwise weighted rule-based matching.
        This is the fast path — for LLM-refined results, use predict_with_llm().
        
        Args:
            user_profile: User's profile data
            top_n: Number of top careers to return
            
        Returns:
            List of PredictedCareer objects
        """
        # Use XGBoost if model is loaded
        if self.model_loaded and self.model is not None:
            return self._predict_with_model(user_profile, top_n)
        
        # Otherwise use weighted rule-based matching
        return self._predict_rule_based(user_profile, top_n)

    async def predict_with_llm(
        self,
        user_profile: UserProfile,
        top_n: int = 5
    ) -> List[PredictedCareer]:
        """
        Predict careers using Gemini LLM refinement over XGBoost results.
        
        Pipeline:
        1. Get XGBoost predictions (fast)
        2. Send profile + XGBoost hints to Gemini for re-ranking
        3. Fall back to rule-based if both fail
        
        Args:
            user_profile: User's profile data
            top_n: Number of top careers to return
            
        Returns:
            List of PredictedCareer objects, refined by LLM
        """
        # Step 1: Get XGBoost / rule-based predictions as hints
        raw_predictions = self.predict(user_profile, top_n=5)
        xgboost_hints = [
            {"career": p.career, "confidence": p.confidence}
            for p in raw_predictions
        ]
        
        # Step 2: Try LLM refinement
        try:
            from app.services.gemini_service import gemini_service
            from app.prompts.career_prediction_prompts import (
                CAREER_PREDICTION_SYSTEM_PROMPT,
                get_career_prediction_prompt,
            )
            
            prompt = get_career_prediction_prompt(
                education_level=user_profile.education_level.value,
                ug_course=user_profile.ug_course or "",
                specialization=user_profile.specialization or "",
                skills=user_profile.skills,
                interests=user_profile.interests,
                cgpa=user_profile.cgpa,
                certifications=user_profile.certifications,
                gender=user_profile.gender or "",
                preferences=user_profile.preferences or "",
                xgboost_suggestions=xgboost_hints,
            )
            
            response = await gemini_service.generate(
                prompt=prompt,
                system_prompt=CAREER_PREDICTION_SYSTEM_PROMPT,
                temperature=0.3,   # Low temp for deterministic reasoning
                max_tokens=1024,
            )
            
            parsed = gemini_service.parse_json_response(response)
            llm_predictions = self._parse_llm_predictions(parsed, top_n)
            
            if llm_predictions:
                logger.info("Career prediction refined by LLM successfully")
                return llm_predictions
                
        except Exception as e:
            logger.warning(f"LLM career refinement failed, using model/rule predictions: {e}")
        
        # Step 3: Fall back to raw predictions
        return raw_predictions[:top_n]

    def _parse_llm_predictions(
        self,
        parsed: Dict[str, Any],
        top_n: int
    ) -> List[PredictedCareer]:
        """Parse career predictions from LLM JSON response."""
        predictions_data = parsed.get("predictions", [])
        
        if not predictions_data:
            return []
        
        predictions = []
        for p in predictions_data[:top_n]:
            career = p.get("career", "")
            confidence = p.get("confidence", 0.5)
            description = p.get("description", "")
            
            # Validate career is in our allowed list (fuzzy match)
            matched_career = self._fuzzy_match_career(career)
            if matched_career:
                predictions.append(PredictedCareer(
                    career=matched_career,
                    confidence=round(min(max(float(confidence), 0.0), 1.0), 2),
                    description=description or self._get_career_description(matched_career)
                ))
        
        return predictions
    
    def _fuzzy_match_career(self, career_name: str) -> Optional[str]:
        """Match a career name to our allowed categories."""
        if not career_name:
            return None
            
        career_lower = career_name.lower().strip()
        
        # Exact match
        for cat in CAREER_CATEGORIES:
            if cat.lower() == career_lower:
                return cat
        
        # Partial match
        for cat in CAREER_CATEGORIES:
            if career_lower in cat.lower() or cat.lower() in career_lower:
                return cat
        
        return None

    # ------------------------------------------------------------------
    # XGBOOST MODEL PREDICTION
    # ------------------------------------------------------------------

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

            rule_predictions = self._predict_rule_based(user_profile, top_n=top_n)
            if (
                predictions
                and rule_predictions
                and predictions[0].career != rule_predictions[0].career
                and predictions[0].confidence < 0.60
                and rule_predictions[0].confidence >= 0.85
            ):
                logger.info(
                    "XGBoost prediction was low-confidence (%s, %.2f); using rule-based top career %s",
                    predictions[0].career,
                    predictions[0].confidence,
                    rule_predictions[0].career,
                )
                return rule_predictions

            return predictions
            
        except Exception as e:
            logger.error(f"Model prediction failed: {e}")
            return self._predict_rule_based(user_profile, top_n)
    

    # ------------------------------------------------------------------
    # WEIGHTED RULE-BASED PREDICTION (IMPROVED FALLBACK)
    # ------------------------------------------------------------------

    def _predict_rule_based(
        self,
        user_profile: UserProfile,
        top_n: int
    ) -> List[PredictedCareer]:
        """Predict using weighted rule-based skill/interest/education matching."""
        
        career_scores: Dict[str, float] = {cat: 0.0 for cat in CAREER_CATEGORIES}
        
        # --- 1. Score based on skills (highest weight) ---
        user_skills = [s.lower().strip() for s in user_profile.skills]
        for user_skill in user_skills:
            for map_skill, career_weights in self.skill_career_map.items():
                if self._skill_matches(user_skill, map_skill):
                    for career, weight in career_weights:
                        career_scores[career] += weight
        
        # --- 2. Score based on interests ---
        user_interests = [i.lower().strip() for i in user_profile.interests]
        for user_interest in user_interests:
            for map_skill, career_weights in self.skill_career_map.items():
                if self._skill_matches(user_interest, map_skill):
                    for career, weight in career_weights:
                        # Interests get 60% weight compared to skills
                        career_scores[career] += weight * 0.6
        
        # --- 3. Education-based boosting (strong signal) ---
        education_text = " ".join(filter(None, [
            user_profile.ug_course,
            user_profile.specialization,
            user_profile.education_level.value if user_profile.education_level else ""
        ])).lower()
        
        for edu_keyword, career_boosts in self._education_career_boost.items():
            if edu_keyword in education_text:
                for career, boost in career_boosts:
                    career_scores[career] += boost
        
        # --- 4. Specialization direct matching (strongest signal) ---
        if user_profile.specialization:
            spec_lower = user_profile.specialization.lower().strip()
            for spec_keyword, career_boosts in self._specialization_career_map.items():
                if spec_keyword in spec_lower or spec_lower in spec_keyword:
                    for career, boost in career_boosts:
                        career_scores[career] += boost
        
        # --- 5. Filter out zero scores and sort ---
        scored_careers = {k: v for k, v in career_scores.items() if v > 0}
        
        if not scored_careers:
            return self._get_default_predictions()

        # Normalize scores to 0.0-0.95 range
        max_score = max(scored_careers.values())
        
        sorted_careers = sorted(
            scored_careers.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        predictions = []
        for career, score in sorted_careers[:top_n]:
            # Scale to 0.30 - 0.95 range
            confidence = 0.30 + (score / max_score) * 0.65
            predictions.append(PredictedCareer(
                career=career,
                confidence=round(confidence, 2),
                description=self._get_career_description(career)
            ))
        
        return predictions
    
    def _skill_matches(self, user_input: str, map_key: str) -> bool:
        """Check if a user skill/interest matches a map key using word-boundary matching.
        
        This prevents false positives like "java" matching "javascript".
        """
        user_input = user_input.strip().lower()
        map_key = map_key.strip().lower()
        
        # Exact match
        if user_input == map_key:
            return True
        
        # Check if map_key appears as a whole word in user_input
        # Use word boundary regex to prevent "java" matching "javascript"
        pattern = r'\b' + re.escape(map_key) + r'\b'
        if re.search(pattern, user_input):
            return True
        
        # Check reverse — user_input as whole word in map_key
        # (e.g., user says "ml" and map has "machine learning" — this won't match,
        #  which is correct since "ml" is ambiguous)
        
        return False

    def _safe_feature_name(self, prefix: str, value: str, max_length: int = 45) -> str:
        """Create stable feature names shared with the training pipeline."""
        cleaned = re.sub(r"[^a-z0-9]+", "_", str(value).lower()).strip("_")
        return f"{prefix}_{cleaned[:max_length]}"

    def _get_default_predictions(self) -> List[PredictedCareer]:
        """Return safe default predictions when no signals are available."""
        return [
            PredictedCareer(
                career="Software Engineer",
                confidence=0.50,
                description="Design, develop, and maintain software applications — one of the most versatile and in-demand career paths"
            ),
            PredictedCareer(
                career="Data Analyst",
                confidence=0.40,
                description="Interpret data and turn it into actionable insights for businesses"
            ),
            PredictedCareer(
                career="Business Manager",
                confidence=0.35,
                description="Lead business operations, manage teams, and drive growth"
            ),
            PredictedCareer(
                career="IT Consultant",
                confidence=0.30,
                description="Advise organizations on technology solutions and strategy"
            ),
            PredictedCareer(
                career="Web Developer",
                confidence=0.30,
                description="Build and maintain websites and web applications"
            ),
        ]


    # ------------------------------------------------------------------
    # FEATURE EXTRACTION (FIXED)
    # ------------------------------------------------------------------

    def _extract_features(self, user_profile: UserProfile) -> List[float]:
        """Extract features from user profile matching training feature columns.
        
        Fixed issues:
        - Uses word-boundary matching for skills/interests (no false positives)
        - Better handling of unknown gender/course values
        - Consistent CGPA normalization
        """
        if not self.feature_columns or not self.encoders:
            # Fallback for when encoders aren't available
            return self._extract_basic_features(user_profile)
        
        # Initialize feature dict with zeros
        feature_dict = {col: 0 for col in self.feature_columns}
        
        # Gender encoding — safe mapping with fallback
        gender_map = {"male": 0, "female": 1, "other": 2}
        user_gender = (user_profile.gender or "male").lower().strip()
        if 'gender_encoded' in feature_dict:
            feature_dict['gender_encoded'] = gender_map.get(user_gender, 0)
        
        # UG Course encoding — improved fuzzy matching
        if 'ug_course_encoded' in feature_dict:
            le_course = self.encoders.get('le_course')
            if le_course and user_profile.ug_course:
                feature_dict['ug_course_encoded'] = self._encode_course(
                    user_profile.ug_course, le_course
                )
        
        # CGPA (always normalize to 0-1 range consistently)
        if 'cgpa' in feature_dict:
            cgpa = user_profile.cgpa or 70
            # Training script divides by 100, so we do the same
            feature_dict['cgpa'] = min(cgpa / 100.0, 1.0)
        
        # Has certification
        if 'has_certification' in feature_dict:
            feature_dict['has_certification'] = 1 if user_profile.certifications else 0
        
        # Is working — default to 0 (student)
        if 'is_working' in feature_dict:
            feature_dict['is_working'] = 0
        
        # Skills encoding — FIXED: use word-boundary matching
        top_skills = self.encoders.get('top_skills', [])
        user_skills_lower = [s.lower().strip() for s in user_profile.skills]
        
        for skill in top_skills:
            safe_name = f"skill_{skill.replace(' ', '_').replace('-', '_')[:30]}"
            if safe_name in feature_dict:
                has_skill = any(
                    self._skill_matches(us, skill) for us in user_skills_lower
                )
                feature_dict[safe_name] = 1 if has_skill else 0
        
        # Interests encoding — FIXED: use word-boundary matching
        top_interests = self.encoders.get('top_interests', [])
        user_interests_lower = [i.lower().strip() for i in user_profile.interests]
        
        for interest in top_interests:
            safe_name = f"interest_{interest.replace(' ', '_').replace('-', '_')[:30]}"
            if safe_name in feature_dict:
                has_interest = any(
                    self._skill_matches(ui, interest) for ui in user_interests_lower
                )
                feature_dict[safe_name] = 1 if has_interest else 0

        # Deterministic recommendation scores are high-signal features for the
        # XGBoost model and keep inference aligned with the training pipeline.
        rule_score_features = [
            column for column in self.feature_columns
            if isinstance(column, str) and column.startswith("rule_score_")
        ]
        if rule_score_features:
            rule_predictions = self._predict_rule_based(user_profile, top_n=len(CAREER_CATEGORIES))
            rule_scores = {prediction.career: prediction.confidence for prediction in rule_predictions}
            for career in CAREER_CATEGORIES:
                feature_name = self._safe_feature_name("rule_score", career)
                if feature_name in feature_dict:
                    feature_dict[feature_name] = rule_scores.get(career, 0.0)
        
        # Return features in correct column order
        return [feature_dict[col] for col in self.feature_columns]

    def _encode_course(self, user_course: str, le_course) -> int:
        """Encode user's UG course to match the training label encoder.
        
        Tries exact match first, then progressively fuzzier matching.
        """
        try:
            course = user_course.strip()
            classes_list = list(le_course.classes_)
            classes_lower = [str(c).lower() for c in classes_list]
            course_lower = course.lower()
            
            # 1. Exact match
            if course in classes_list:
                return classes_list.index(course)
            
            # 2. Case-insensitive exact match
            if course_lower in classes_lower:
                return classes_lower.index(course_lower)
            
            # 3. Containment match — but only if it's a meaningful match
            #    (avoid matching "B" in "B.Sc" for input "BCA")
            best_match_idx = -1
            best_match_len = 0
            for i, cls_lower in enumerate(classes_lower):
                # Check if user input contains a training class or vice versa
                if len(cls_lower) >= 3 and cls_lower in course_lower:
                    if len(cls_lower) > best_match_len:
                        best_match_len = len(cls_lower)
                        best_match_idx = i
                elif len(course_lower) >= 3 and course_lower in cls_lower:
                    if len(course_lower) > best_match_len:
                        best_match_len = len(course_lower)
                        best_match_idx = i
            
            if best_match_idx >= 0:
                return best_match_idx
            
            # 4. No match — return 0 (will use other features for prediction)
            return 0
            
        except Exception:
            return 0
    
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
    

    # ------------------------------------------------------------------
    # CAREER DESCRIPTIONS & INSIGHTS
    # ------------------------------------------------------------------

    def _get_career_description(self, career: str) -> str:
        """Get brief description for a career."""
        descriptions = {
            "Software Engineer": "Design, develop, and maintain software applications",
            "Data Scientist": "Analyze complex data to help businesses make decisions",
            "Data Analyst": "Interpret data and turn it into actionable insights",
            "Web Developer": "Build and maintain websites and web applications",
            "Mobile App Developer": "Build mobile apps for Android and iOS",
            "DevOps Engineer": "Bridge development and operations for faster delivery",
            "Cybersecurity Analyst": "Protect systems from security threats",
            "Database Administrator": "Manage and optimize database systems",
            "Network Engineer": "Design and manage computer networks",
            "Product Manager": "Lead product development and strategy",
            "Project Manager": "Lead and coordinate project teams",
            "UI/UX Designer": "Design user interfaces and experiences",
            "Quality Assurance Engineer": "Test and ensure software quality",
            "Teacher/Educator": "Educate and mentor students",
            "Financial Analyst": "Analyze financial data and advise on investments",
            "Marketing Specialist": "Plan and execute marketing strategies",
            "HR Manager": "Manage recruitment and employee relations",
            "IT Consultant": "Advise organizations on technology solutions",
            "Research Scientist": "Conduct research and develop new technologies",
            "Healthcare Professional": "Provide medical care and health services",
            "Mechanical Engineer": "Design and build mechanical systems",
            "Civil Engineer": "Design and oversee construction projects",
            "Electrical Engineer": "Design and develop electrical systems",
            "Legal Professional": "Provide legal advice, research, representation, and compliance support",
            "Business Manager": "Lead business operations and teams"
        }
        return descriptions.get(career, f"Build a career in {career}")
    
    def get_career_insights(self, career: str) -> Dict[str, Any]:
        """Get insights about a specific career from the dataset."""
        if self.career_data is None:
            self.load_career_data()
        
        if self.career_data is None:
            return {}
        
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
            "Data Analyst": ["SQL", "Excel", "Python", "Tableau/Power BI", "Statistics"],
            "Web Developer": ["JavaScript", "HTML", "CSS", "React", "Node.js"],
            "Mobile App Developer": ["Flutter", "React Native", "Java/Kotlin", "Swift", "UI Design"],
            "DevOps Engineer": ["Docker", "Kubernetes", "CI/CD", "Linux", "Cloud (AWS/Azure)"],
            "Cybersecurity Analyst": ["Network Security", "Ethical Hacking", "Linux", "Firewalls", "Risk Assessment"],
            "Database Administrator": ["SQL", "PostgreSQL/MySQL", "Database Design", "Performance Tuning", "Backup Management"],
            "Network Engineer": ["Networking Protocols", "Linux", "Cisco", "Firewalls", "Troubleshooting"],
            "Product Manager": ["Product Strategy", "User Research", "Agile", "Data Analysis", "Communication"],
            "Project Manager": ["Project Planning", "Agile/Scrum", "Risk Management", "Leadership", "Communication"],
            "UI/UX Designer": ["Figma", "User Research", "Prototyping", "Visual Design", "Wireframing"],
            "Quality Assurance Engineer": ["Testing", "Selenium", "Test Automation", "Bug Tracking", "SQL"],
            "Teacher/Educator": ["Subject Expertise", "Communication", "Pedagogy", "Curriculum Design", "Patience"],
            "Financial Analyst": ["Excel", "Financial Modeling", "Accounting", "Data Analysis", "Risk Assessment"],
            "Marketing Specialist": ["Digital Marketing", "SEO/SEM", "Content Strategy", "Analytics", "Social Media"],
            "HR Manager": ["Recruitment", "Employee Relations", "Labor Law", "Communication", "Conflict Resolution"],
            "IT Consultant": ["Business Analysis", "Technical Knowledge", "Communication", "Problem Solving", "Project Management"],
            "Research Scientist": ["Research Methods", "Data Analysis", "Technical Writing", "Statistics", "Critical Thinking"],
            "Healthcare Professional": ["Medical Knowledge", "Patient Care", "Communication", "Empathy", "Attention to Detail"],
            "Mechanical Engineer": ["AutoCAD", "SolidWorks", "Thermodynamics", "Material Science", "Manufacturing"],
            "Civil Engineer": ["AutoCAD", "Structural Analysis", "Construction Management", "Surveying", "Project Planning"],
            "Electrical Engineer": ["Circuit Design", "MATLAB", "Embedded Systems", "Power Systems", "Electronics"],
            "Legal Professional": ["Legal Research", "Legal Writing", "Criminal/Civil Law", "Case Analysis", "Advocacy"],
            "Business Manager": ["Leadership", "Strategic Planning", "Financial Management", "Communication", "Decision Making"],
        }
        return career_skills.get(career, ["Technical Skills", "Problem Solving", "Communication"])


# Singleton instance
career_predictor = CareerPredictor()
