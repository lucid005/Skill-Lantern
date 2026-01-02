"""
Skill Lantern - ML-based Career Predictor

Uses XGBoost model trained on career data for improved predictions.
Falls back gracefully if model is not available.
"""

import joblib
import numpy as np
from typing import Dict, List, Optional
from pathlib import Path


class MLPredictor:
    """
    Machine Learning based career prediction using XGBoost.
    
    This predictor uses a trained model to predict career matches.
    If no model is available, it gracefully indicates unavailability.
    """
    
    def __init__(self, model_path: str = None):
        """
        Initialize the ML predictor.
        
        Args:
            model_path: Path to the trained model file
        """
        if model_path is None:
            model_path = Path(__file__).parent.parent / "models" / "trained" / "career_model.joblib"
        
        self.model_path = Path(model_path)
        self.model = None
        self.label_encoder = None
        self.feature_names = None
        self.scaler = None
        
        self._load_model()
    
    def _load_model(self):
        """Load the trained model and associated components"""
        try:
            if self.model_path.exists():
                model_data = joblib.load(self.model_path)
                
                self.model = model_data.get('model')
                self.label_encoder = model_data.get('label_encoder')
                self.feature_names = model_data.get('feature_names')
                self.scaler = model_data.get('scaler')
                
                print(f"✅ ML Model loaded from {self.model_path}")
            else:
                print(f"⚠️ No trained model found at {self.model_path}")
                print("   Run training first: python -m training.train_xgboost")
        
        except Exception as e:
            print(f"⚠️ Error loading model: {e}")
            self.model = None
    
    def is_model_loaded(self) -> bool:
        """Check if model is loaded and ready"""
        return self.model is not None
    
    def predict(self, user_profile: Dict, top_k: int = 5) -> List[Dict]:
        """
        Predict top careers for a user profile.
        
        Args:
            user_profile: User's data (scores, skills, interests)
            top_k: Number of top predictions to return
            
        Returns:
            List of predicted careers with confidence scores
        """
        if not self.is_model_loaded():
            return []
        
        try:
            # Prepare features
            features = self._prepare_features(user_profile)
            
            # Scale features if scaler is available
            if self.scaler is not None:
                features = self.scaler.transform([features])[0]
            
            # Get prediction probabilities
            features_array = np.array([features])
            probabilities = self.model.predict_proba(features_array)[0]
            
            # Get top K predictions
            top_indices = np.argsort(probabilities)[-top_k:][::-1]
            
            predictions = []
            for idx in top_indices:
                career_label = self.label_encoder.inverse_transform([idx])[0]
                confidence = float(probabilities[idx])
                
                predictions.append({
                    'career_id': career_label.lower().replace(' ', '_'),
                    'career_name': career_label,
                    'confidence': round(confidence, 4),
                    'match_score': round(confidence * 100, 2),
                })
            
            return predictions
            
        except Exception as e:
            print(f"⚠️ Prediction error: {e}")
            return []
    
    def _prepare_features(self, user_profile: Dict) -> List[float]:
        """
        Prepare feature vector from user profile.
        
        Args:
            user_profile: Raw user data
            
        Returns:
            Feature vector matching training data format
        """
        if self.feature_names is None:
            # Use default feature order if not loaded
            self.feature_names = self._get_default_feature_names()
        
        features = []
        
        for feature_name in self.feature_names:
            value = 0.0
            
            # Academic scores
            if feature_name == 'math_score':
                value = user_profile.get('math_score', 0) / 100.0
            elif feature_name == 'science_score':
                value = user_profile.get('science_score', 0) / 100.0
            elif feature_name == 'english_score':
                value = user_profile.get('english_score', 0) / 100.0
            elif feature_name == 'gpa':
                value = user_profile.get('gpa', 0) / 4.0
            
            # Skills
            elif feature_name.startswith('skill_'):
                skill_name = feature_name.replace('skill_', '')
                skills = user_profile.get('skills', {})
                value = skills.get(skill_name, 0) / 5.0
            
            # Interests
            elif feature_name.startswith('interest_'):
                interest_name = feature_name.replace('interest_', '')
                interests = user_profile.get('interests', {})
                value = interests.get(interest_name, 0) / 5.0
            
            # Direct skill/interest match (without prefix)
            else:
                skills = user_profile.get('skills', {})
                interests = user_profile.get('interests', {})
                
                if feature_name in skills:
                    value = skills[feature_name] / 5.0
                elif feature_name in interests:
                    value = interests[feature_name] / 5.0
            
            features.append(value)
        
        return features
    
    def _get_default_feature_names(self) -> List[str]:
        """Get default feature names if not loaded from model"""
        return [
            'math_score',
            'science_score',
            'english_score',
            'gpa',
            'skill_programming',
            'skill_communication',
            'skill_analytical_thinking',
            'skill_problem_solving',
            'skill_creativity',
            'skill_leadership',
            'skill_teamwork',
            'skill_attention_to_detail',
            'skill_time_management',
            'skill_stress_management',
            'skill_empathy',
            'skill_technical_skills',
            'skill_presentation',
            'skill_project_management',
            'skill_dedication',
            'skill_integrity',
            'skill_patience',
            'interest_technology',
            'interest_engineering',
            'interest_healthcare',
            'interest_business',
            'interest_arts',
            'interest_education',
            'interest_research',
            'interest_helping_others',
            'interest_finance',
            'interest_law',
        ]
    
    def get_feature_importance(self) -> Optional[Dict[str, float]]:
        """
        Get feature importance from the trained model.
        
        Returns:
            Dictionary mapping feature names to importance scores
        """
        if not self.is_model_loaded() or self.feature_names is None:
            return None
        
        try:
            importances = self.model.feature_importances_
            
            importance_dict = {}
            for name, importance in zip(self.feature_names, importances):
                importance_dict[name] = float(importance)
            
            # Sort by importance
            sorted_importance = dict(
                sorted(importance_dict.items(), key=lambda x: x[1], reverse=True)
            )
            
            return sorted_importance
            
        except Exception as e:
            print(f"⚠️ Error getting feature importance: {e}")
            return None


# For testing
if __name__ == "__main__":
    predictor = MLPredictor()
    
    if predictor.is_model_loaded():
        test_user = {
            'math_score': 85,
            'science_score': 90,
            'english_score': 75,
            'gpa': 3.7,
            'skills': {
                'programming': 4,
                'analytical_thinking': 5,
                'communication': 3,
                'problem_solving': 4,
            },
            'interests': {
                'technology': 5,
                'engineering': 4,
                'research': 4,
            }
        }
        
        print("\n🤖 ML Model Predictions:")
        print("=" * 60)
        
        for pred in predictor.predict(test_user, top_k=5):
            print(f"\n📌 {pred['career_name']}")
            print(f"   Confidence: {pred['confidence']:.2%}")
    else:
        print("\n⚠️ No trained model available.")
        print("Run training: python -m training.train_xgboost")
