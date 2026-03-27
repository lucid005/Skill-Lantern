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
        # Map careers to relevant program keywords - MUST match actual career categories
        career_to_programs = {
            "software engineer": ["computer science", "information technology", "software", "bca", "bsc csit", "computer application", "computer engineering"],
            "data scientist": ["data science", "computer science", "statistics", "mathematics", "machine learning", "bsc csit", "information technology"],
            "data analyst": ["data science", "computer science", "statistics", "mathematics", "information technology", "bsc csit", "bca"],
            "web developer": ["computer science", "information technology", "bca", "software", "computer application", "bsc csit"],
            "mobile app developer": ["computer science", "information technology", "software", "bca", "bsc csit", "computer application"],
            "network engineer": ["computer science", "information technology", "networking", "electronics", "computer engineering"],
            "database administrator": ["computer science", "information technology", "bca", "bsc csit", "data"],
            "devops engineer": ["computer science", "information technology", "software", "bsc csit", "computer engineering"],
            "cybersecurity analyst": ["cybersecurity", "computer science", "information technology", "information security", "computer engineering"],
            "product manager": ["business", "management", "bba", "mba", "information technology", "computer science"],
            "project manager": ["business", "management", "bba", "mba", "project management"],
            "ui/ux designer": ["design", "fine arts", "multimedia", "computer application", "information technology", "bca"],
            "quality assurance engineer": ["computer science", "information technology", "software", "bca", "bsc csit"],
            "teacher/educator": ["education", "bed", "med", "bachelor of education", "master of education"],
            "financial analyst": ["accounting", "commerce", "bba", "bbs", "finance", "mba", "bcom"],
            "marketing specialist": ["marketing", "business", "management", "bba", "mba", "bbs"],
            "hr manager": ["business", "management", "bba", "mba", "human resource"],
            "it consultant": ["computer science", "information technology", "management", "bca", "mba", "bsc csit"],
            "research scientist": ["science", "research", "physics", "chemistry", "biology", "biotechnology", "mathematics"],
            "healthcare professional": ["mbbs", "medicine", "medical", "health science", "nursing", "pharmacy"],
            "mechanical engineer": ["mechanical engineering", "automobile"],
            "civil engineer": ["civil engineering", "construction"],
            "electrical engineer": ["electrical", "electronics", "electronics and communication"],
            "business manager": ["business", "management", "bba", "mba", "bbm", "bbs"],
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
    
    def format_colleges_for_prompt(self, colleges: List[Dict[str, Any]], max_colleges: int = 8) -> str:
        """
        Format college data for LLM prompt (compact format to reduce tokens).
        
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
            name = college.get('College', 'Unknown')
            loc = college.get('Location', 'N/A')
            programs = college.get('Course Offered', 'N/A')[:150]
            uni = college.get('University', '')
            formatted.append(f"{i}. {name} | {loc} | {uni} | Programs: {programs}")
        
        return "\n".join(formatted)


# Singleton instance
college_service = CollegeService()
