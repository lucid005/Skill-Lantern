"""
College Service - CSV Data Handling
Handles loading, parsing, and filtering of Nepal college data.
"""

import pandas as pd
from typing import List, Optional, Dict, Any
from pathlib import Path
import logging
import re

from app.config import settings

logger = logging.getLogger(__name__)


class CollegeService:
    """Service for managing college data from CSV."""
    
    def __init__(self):
        self.colleges_df: Optional[pd.DataFrame] = None
        self.loaded = False
        
    def load_data(self, csv_path: str = None) -> bool:
        """
        Load college data from CSV file.
        
        Args:
            csv_path: Path to CSV file (uses config path if not provided)
            
        Returns:
            True if loaded successfully
        """
        try:
            path = csv_path or settings.colleges_csv_path
            
            # Check if file exists
            if not Path(path).exists():
                logger.error(f"Colleges CSV not found at: {path}")
                return False
            
            # Load CSV
            self.colleges_df = pd.read_csv(path)
            
            # Clean column names
            self.colleges_df.columns = self.colleges_df.columns.str.strip()
            
            # Fill NaN values
            self.colleges_df = self.colleges_df.fillna("")
            
            self.loaded = True
            logger.info(f"Loaded {len(self.colleges_df)} colleges from CSV")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load colleges CSV: {e}")
            return False
    
    def get_all_colleges(self) -> List[Dict[str, Any]]:
        """Get all colleges as list of dictionaries."""
        if not self.loaded:
            self.load_data()
        
        if self.colleges_df is None:
            return []
        
        return self.colleges_df.to_dict(orient="records")
    
    def get_locations(self) -> List[str]:
        """Get unique locations from college data."""
        if not self.loaded:
            self.load_data()
        
        if self.colleges_df is None:
            return []
        
        locations = self.colleges_df["Location"].unique().tolist()
        # Extract city names from location strings
        cities = set()
        for loc in locations:
            if loc:
                # Extract first part before comma or the whole string
                parts = str(loc).split(",")
                if len(parts) > 1:
                    city = parts[-1].strip()  # Usually city is at the end
                else:
                    city = parts[0].strip()
                cities.add(city)
        
        return sorted(list(cities))
    
    def get_universities(self) -> List[str]:
        """Get unique universities."""
        if not self.loaded:
            self.load_data()
        
        if self.colleges_df is None:
            return []
        
        universities = self.colleges_df["University"].unique().tolist()
        return [u for u in universities if u and str(u).strip()]
    
    def filter_colleges(
        self,
        location: Optional[str] = None,
        university: Optional[str] = None,
        ownership_type: Optional[str] = None,
        program_keyword: Optional[str] = None,
        career_keywords: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Filter colleges based on criteria.
        
        Args:
            location: Filter by location (partial match)
            university: Filter by university affiliation
            ownership_type: 'private' or 'constituent'
            program_keyword: Search in course offerings
            career_keywords: List of keywords related to career
            
        Returns:
            Filtered list of colleges
        """
        if not self.loaded:
            self.load_data()
        
        if self.colleges_df is None:
            return []
        
        df = self.colleges_df.copy()
        
        # Filter by location
        if location:
            location_lower = location.lower()
            df = df[df["Location"].str.lower().str.contains(location_lower, na=False)]
        
        # Filter by university
        if university:
            df = df[df["University"].str.lower().str.contains(university.lower(), na=False)]
        
        # Filter by ownership type
        if ownership_type:
            df = df[df["Ownership Type"].str.lower().str.contains(ownership_type.lower(), na=False)]
        
        # Filter by program keyword
        if program_keyword:
            df = df[df["Course Offered"].str.lower().str.contains(program_keyword.lower(), na=False)]
        
        # Filter by career-related keywords
        if career_keywords:
            keyword_pattern = "|".join([re.escape(k.lower()) for k in career_keywords])
            df = df[df["Course Offered"].str.lower().str.contains(keyword_pattern, na=False, regex=True)]
        
        return df.to_dict(orient="records")
    
    def get_colleges_for_career(self, career: str) -> List[Dict[str, Any]]:
        """
        Get colleges offering programs relevant to a career.
        
        Args:
            career: Career name to match
            
        Returns:
            List of relevant colleges
        """
        # Map careers to relevant program keywords
        career_to_programs = {
            "software engineer": ["computer science", "information technology", "software", "bca", "bsc csit", "computer application"],
            "data scientist": ["data science", "computer science", "statistics", "mathematics", "machine learning"],
            "web developer": ["computer", "information technology", "bca", "software", "web"],
            "network engineer": ["computer", "information technology", "networking", "electronics"],
            "database administrator": ["computer", "information technology", "database", "data"],
            "cybersecurity": ["cybersecurity", "ethical hacking", "computer", "information security"],
            "doctor": ["mbbs", "medicine", "medical", "health science"],
            "nurse": ["nursing", "bsc nursing", "health"],
            "pharmacist": ["pharmacy", "pharmaceutical"],
            "civil engineer": ["civil engineering", "construction"],
            "mechanical engineer": ["mechanical engineering"],
            "electrical engineer": ["electrical", "electronics"],
            "accountant": ["accounting", "commerce", "bba", "bbs", "finance"],
            "business analyst": ["business", "management", "bba", "mba"],
            "marketing": ["marketing", "business", "management", "mba"],
            "hotel management": ["hotel", "hospitality", "tourism"],
            "teacher": ["education", "bed", "med"],
            "lawyer": ["law", "llb", "legal"],
            "psychologist": ["psychology", "counseling"],
            "journalist": ["journalism", "mass communication", "media"],
            "graphic designer": ["design", "fine arts", "multimedia"],
            "architect": ["architecture"],
            "agriculture": ["agriculture", "agricultural"],
            "forestry": ["forestry", "environmental"],
            "biotechnology": ["biotechnology", "biomedical"],
        }
        
        career_lower = career.lower()
        
        # Find matching keywords
        keywords = []
        for career_key, programs in career_to_programs.items():
            if career_key in career_lower or career_lower in career_key:
                keywords = programs
                break
        
        # If no specific mapping, use the career name itself
        if not keywords:
            keywords = [career_lower.replace(" ", ""), career_lower]
        
        return self.filter_colleges(career_keywords=keywords)
    
    def format_colleges_for_prompt(self, colleges: List[Dict[str, Any]], max_colleges: int = 15) -> str:
        """
        Format college data for LLM prompt.
        
        Args:
            colleges: List of college dictionaries
            max_colleges: Maximum number of colleges to include
            
        Returns:
            Formatted string for prompt
        """
        if not colleges:
            return "No colleges found matching the criteria."
        
        # Limit number of colleges
        colleges = colleges[:max_colleges]
        
        formatted = []
        for i, college in enumerate(colleges, 1):
            entry = f"""
{i}. {college.get('College', 'Unknown')}
   - Location: {college.get('Location', 'N/A')}
   - University: {college.get('University', 'N/A')}
   - Programs: {college.get('Course Offered', 'N/A')[:300]}...
   - Type: {college.get('Ownership Type', 'N/A')}
   - Contact: {college.get('Phone Number', 'N/A')} | {college.get('Email', 'N/A')}
"""
            formatted.append(entry)
        
        return "\n".join(formatted)


# Singleton instance
college_service = CollegeService()
