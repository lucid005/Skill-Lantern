"""
Skill Lantern - Rule-Based Career Matcher

This module provides explainable career matching based on predefined rules.
No training data required - works immediately with career definitions.
"""

import yaml
from typing import Dict, List, Optional
from pathlib import Path


class CareerMatcher:
    """
    Rule-based career matching system.
    
    Provides fast, explainable career recommendations based on:
    - Academic performance
    - Skills match
    - Interest alignment
    - GPA requirements
    """
    
    def __init__(self, config_path: str = None):
        """
        Initialize the career matcher.
        
        Args:
            config_path: Path to careers.yaml configuration file
        """
        if config_path is None:
            # Default path relative to project root
            config_path = Path(__file__).parent.parent / "config" / "careers.yaml"
        
        self.config_path = Path(config_path)
        self.careers = {}
        self.features = {}
        
        self._load_careers()
    
    def _load_careers(self):
        """Load career definitions from YAML config"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            self.careers = config.get('careers', {})
            self.features = config.get('features', {})
            
            print(f"✅ Loaded {len(self.careers)} career profiles")
            
        except FileNotFoundError:
            print(f"⚠️ Career config not found at {self.config_path}")
            self._load_default_careers()
        except Exception as e:
            print(f"⚠️ Error loading careers: {e}")
            self._load_default_careers()
    
    def _load_default_careers(self):
        """Load minimal default careers if config not found"""
        self.careers = {
            'software_engineer': {
                'name': 'Software Engineer',
                'description': 'Designs and builds software applications',
                'category': 'Technology',
                'required_skills': {'programming': 4, 'analytical_thinking': 4, 'problem_solving': 4},
                'required_interests': {'technology': 4, 'engineering': 3},
                'academic_weights': {'math': 0.4, 'science': 0.3, 'english': 0.3},
                'min_gpa': 3.0,
            }
        }
        self.features = {
            'skills': ['programming', 'communication', 'analytical_thinking', 'problem_solving'],
            'interests': ['technology', 'engineering', 'healthcare', 'business', 'arts'],
        }
    
    def calculate_match_score(self, user_profile: Dict, career_id: str) -> Dict:
        """
        Calculate how well a user matches a specific career.
        
        Args:
            user_profile: User's academic scores, skills, and interests
            career_id: Career identifier
            
        Returns:
            Dictionary with match score, breakdown, and explanations
        """
        if career_id not in self.careers:
            return None
        
        career = self.careers[career_id]
        scores = {}
        explanations = []
        
        # === 1. Academic Score (0-30 points) ===
        academic_score = 0
        weights = career.get('academic_weights', {'math': 0.33, 'science': 0.33, 'english': 0.34})
        
        math_contribution = (user_profile.get('math_score', 0) / 100) * weights.get('math', 0.33) * 30
        science_contribution = (user_profile.get('science_score', 0) / 100) * weights.get('science', 0.33) * 30
        english_contribution = (user_profile.get('english_score', 0) / 100) * weights.get('english', 0.34) * 30
        
        academic_score = math_contribution + science_contribution + english_contribution
        scores['academic'] = round(academic_score, 2)
        
        if academic_score >= 24:
            explanations.append(f"✅ Strong academic fit ({academic_score:.1f}/30)")
        elif academic_score >= 18:
            explanations.append(f"📊 Good academic foundation ({academic_score:.1f}/30)")
        else:
            explanations.append(f"⚠️ Academic improvement needed ({academic_score:.1f}/30)")
        
        # === 2. Skills Match (0-40 points) ===
        skill_score = 0
        skill_matches = []
        skill_gaps = []
        required_skills = career.get('required_skills', {})
        user_skills = user_profile.get('skills', {})
        
        for skill, required_level in required_skills.items():
            user_level = user_skills.get(skill, 0)
            
            if user_level >= required_level:
                # Full points for meeting or exceeding requirement
                contribution = (user_level / 5.0) * (40 / len(required_skills))
                skill_score += contribution
                skill_matches.append(f"{skill.replace('_', ' ').title()} ({user_level}/5)")
            elif user_level > 0:
                # Partial points for having some skill
                contribution = (user_level / required_level) * (40 / len(required_skills)) * 0.5
                skill_score += contribution
                skill_gaps.append(f"{skill.replace('_', ' ').title()} (need {required_level}, have {user_level})")
            else:
                skill_gaps.append(f"{skill.replace('_', ' ').title()} (need {required_level})")
        
        scores['skills'] = round(min(skill_score, 40), 2)
        
        if skill_matches:
            explanations.append(f"💪 Matching skills: {', '.join(skill_matches[:3])}")
        if skill_gaps and len(skill_gaps) <= 2:
            explanations.append(f"📈 Skills to develop: {', '.join(skill_gaps)}")
        
        # === 3. Interest Alignment (0-30 points) ===
        interest_score = 0
        interest_matches = []
        required_interests = career.get('required_interests', {})
        user_interests = user_profile.get('interests', {})
        
        for interest, required_level in required_interests.items():
            user_level = user_interests.get(interest, 0)
            
            if user_level >= required_level:
                contribution = (user_level / 5.0) * (30 / len(required_interests))
                interest_score += contribution
                interest_matches.append(f"{interest.replace('_', ' ').title()}")
            elif user_level > 0:
                contribution = (user_level / required_level) * (30 / len(required_interests)) * 0.5
                interest_score += contribution
        
        scores['interests'] = round(min(interest_score, 30), 2)
        
        if interest_matches:
            explanations.append(f"❤️ Strong interests: {', '.join(interest_matches)}")
        
        # === Calculate Total Score ===
        total_score = scores['academic'] + scores['skills'] + scores['interests']
        
        # === GPA Penalty/Bonus ===
        min_gpa = career.get('min_gpa', 2.5)
        user_gpa = user_profile.get('gpa', 0)
        
        if user_gpa < min_gpa:
            penalty = (min_gpa - user_gpa) * 5
            total_score -= penalty
            explanations.append(f"⚠️ GPA below recommended ({user_gpa:.1f} < {min_gpa})")
        elif user_gpa >= min_gpa + 0.5:
            bonus = 3
            total_score += bonus
            explanations.append(f"🌟 Excellent GPA ({user_gpa:.1f})")
        
        # Ensure score is in valid range
        total_score = max(0, min(100, total_score))
        
        return {
            'career_id': career_id,
            'career_name': career.get('name', career_id),
            'category': career.get('category', 'General'),
            'description': career.get('description', ''),
            'match_score': round(total_score, 2),
            'confidence': round(total_score / 100, 3),
            'score_breakdown': scores,
            'explanations': explanations,
        }
    
    def get_top_careers(self, user_profile: Dict, top_k: int = 5) -> List[Dict]:
        """
        Get top K career matches for a user profile.
        
        Args:
            user_profile: User's data (scores, skills, interests)
            top_k: Number of top careers to return
            
        Returns:
            List of career matches sorted by score
        """
        all_matches = []
        
        for career_id in self.careers.keys():
            match = self.calculate_match_score(user_profile, career_id)
            if match:
                all_matches.append(match)
        
        # Sort by match score (descending)
        all_matches.sort(key=lambda x: x['match_score'], reverse=True)
        
        return all_matches[:top_k]
    
    def get_all_careers(self) -> List[Dict]:
        """Get list of all available careers"""
        careers_list = []
        
        for career_id, career_data in self.careers.items():
            careers_list.append({
                'career_id': career_id,
                'name': career_data.get('name', career_id),
                'category': career_data.get('category', 'General'),
                'description': career_data.get('description', ''),
            })
        
        return careers_list
    
    def get_career_details(self, career_id: str) -> Optional[Dict]:
        """Get detailed information about a specific career"""
        if career_id not in self.careers:
            return None
        
        career = self.careers[career_id]
        
        return {
            'career_id': career_id,
            **career,
        }
    
    def get_categories(self) -> List[str]:
        """Get list of all career categories"""
        categories = set()
        
        for career in self.careers.values():
            category = career.get('category', 'General')
            categories.add(category)
        
        return sorted(list(categories))
    
    def get_features(self) -> Dict:
        """Get list of all skills and interests"""
        return {
            'skills': self.features.get('skills', []),
            'interests': self.features.get('interests', []),
            'academic_subjects': self.features.get('academic_subjects', ['math', 'science', 'english']),
        }
    
    def explain_match(self, user_profile: Dict, career_id: str) -> Dict:
        """
        Get detailed explanation for a career match.
        
        Args:
            user_profile: User's data
            career_id: Career to explain
            
        Returns:
            Detailed explanation of the match
        """
        match = self.calculate_match_score(user_profile, career_id)
        
        if not match:
            return {"error": "Career not found"}
        
        career = self.careers.get(career_id, {})
        
        # Build detailed explanation
        explanation = {
            "career": match['career_name'],
            "overall_match": f"{match['match_score']:.1f}%",
            "summary": self._generate_summary(match),
            "breakdown": {
                "academic_fit": {
                    "score": f"{match['score_breakdown']['academic']:.1f}/30",
                    "explanation": self._explain_academic(user_profile, career),
                },
                "skills_fit": {
                    "score": f"{match['score_breakdown']['skills']:.1f}/40",
                    "matching": self._get_matching_skills(user_profile, career),
                    "gaps": self._get_skill_gaps(user_profile, career),
                },
                "interests_fit": {
                    "score": f"{match['score_breakdown']['interests']:.1f}/30",
                    "matching": self._get_matching_interests(user_profile, career),
                },
            },
            "recommendations": self._generate_recommendations(user_profile, career),
        }
        
        return explanation
    
    def _generate_summary(self, match: Dict) -> str:
        """Generate a summary statement based on match score"""
        score = match['match_score']
        name = match['career_name']
        
        if score >= 80:
            return f"Excellent match! {name} aligns very well with your profile."
        elif score >= 65:
            return f"Good match! {name} is a strong option for you with some areas to develop."
        elif score >= 50:
            return f"Moderate match. {name} is possible but may require significant skill development."
        else:
            return f"Lower match. {name} may not be the best fit based on your current profile."
    
    def _explain_academic(self, user_profile: Dict, career: Dict) -> str:
        """Explain academic fit"""
        weights = career.get('academic_weights', {})
        primary_subject = max(weights, key=weights.get) if weights else 'math'
        
        return f"This career emphasizes {primary_subject} skills. Your scores align {'well' if user_profile.get(f'{primary_subject}_score', 0) >= 70 else 'moderately'} with requirements."
    
    def _get_matching_skills(self, user_profile: Dict, career: Dict) -> List[str]:
        """Get list of skills that match requirements"""
        matching = []
        required = career.get('required_skills', {})
        user_skills = user_profile.get('skills', {})
        
        for skill, required_level in required.items():
            if user_skills.get(skill, 0) >= required_level:
                matching.append(skill.replace('_', ' ').title())
        
        return matching
    
    def _get_skill_gaps(self, user_profile: Dict, career: Dict) -> List[Dict]:
        """Get list of skills that need improvement"""
        gaps = []
        required = career.get('required_skills', {})
        user_skills = user_profile.get('skills', {})
        
        for skill, required_level in required.items():
            user_level = user_skills.get(skill, 0)
            if user_level < required_level:
                gaps.append({
                    'skill': skill.replace('_', ' ').title(),
                    'current': user_level,
                    'required': required_level,
                    'gap': required_level - user_level,
                })
        
        return gaps
    
    def _get_matching_interests(self, user_profile: Dict, career: Dict) -> List[str]:
        """Get list of interests that match"""
        matching = []
        required = career.get('required_interests', {})
        user_interests = user_profile.get('interests', {})
        
        for interest, required_level in required.items():
            if user_interests.get(interest, 0) >= required_level:
                matching.append(interest.replace('_', ' ').title())
        
        return matching
    
    def _generate_recommendations(self, user_profile: Dict, career: Dict) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # Check skill gaps
        gaps = self._get_skill_gaps(user_profile, career)
        for gap in gaps[:2]:  # Top 2 skill gaps
            recommendations.append(f"Develop your {gap['skill']} skills (currently {gap['current']}/5, need {gap['required']}/5)")
        
        # Check GPA
        min_gpa = career.get('min_gpa', 2.5)
        if user_profile.get('gpa', 0) < min_gpa:
            recommendations.append(f"Focus on improving your GPA to at least {min_gpa}")
        
        # Add general recommendation
        if not recommendations:
            recommendations.append("Continue building your profile - you're on the right track!")
        
        return recommendations


# For testing
if __name__ == "__main__":
    matcher = CareerMatcher()
    
    # Test user profile
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
            'creativity': 3,
        },
        'interests': {
            'technology': 5,
            'engineering': 4,
            'research': 4,
            'business': 2,
        }
    }
    
    print("\n🎯 Top Career Matches:")
    print("=" * 60)
    
    for match in matcher.get_top_careers(test_user, top_k=5):
        print(f"\n📌 {match['career_name']}")
        print(f"   Score: {match['match_score']}/100")
        print(f"   Category: {match['category']}")
        for exp in match['explanations']:
            print(f"   {exp}")
