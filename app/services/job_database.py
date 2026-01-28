"""
Job Database Service - Loads and queries the synthetic job descriptions dataset
"""
import json
import pandas as pd
from typing import List, Dict, Optional
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class JobDatabaseService:
    def __init__(self, data_path: str = "data/job_dataset.json"):
        self.data_path = data_path
        self.df: Optional[pd.DataFrame] = None
        self._load_data()
    
    def _load_data(self):
        """Load job descriptions dataset"""
        try:
            path = Path(self.data_path)
            if not path.exists():
                logger.warning(f"Job database not found at {self.data_path}")
                return
            
            # Try JSON first, then CSV
            if path.suffix == '.json':
                self.df = pd.read_json(self.data_path)
            elif path.suffix == '.csv':
                self.df = pd.read_csv(self.data_path)
            else:
                logger.error(f"Unsupported file format: {path.suffix}")
                return
            
            logger.info(f"Loaded {len(self.df)} job descriptions from database")
            
        except Exception as e:
            logger.error(f"Failed to load job database: {e}")
            self.df = None
    
    def is_available(self) -> bool:
        """Check if database is loaded"""
        return self.df is not None and not self.df.empty
    
    def get_available_roles(self) -> List[str]:
        """Get list of all unique roles in database"""
        if not self.is_available():
            return []
        
        return sorted(self.df['Title'].unique().tolist())
    
    def get_skills_for_role(
        self, 
        role: str, 
        experience_level: Optional[str] = None
    ) -> List[str]:
        """
        Get all skills for a specific role and experience level.
        
        Args:
            role: Job title (e.g., "Backend Developer")
            experience_level: Experience level (Fresher, Entry, Junior, Mid-Level, Senior, Lead, Experienced)
        
        Returns:
            List of unique skills for this role and experience level
        """
        if not self.is_available():
            logger.warning("Database not available")
            return []
        
        # Step 1: Match role name (fuzzy, case-insensitive)
        role_normalized = role.strip()
        role_mask = self.df['Title'].str.contains(role_normalized, case=False, na=False, regex=False)
        
        if role_mask.sum() == 0:
            logger.info(f"No matches found for role: '{role}'")
            return []
        
        # Step 2: Filter by experience level if provided
        if experience_level:
            # Normalize experience level for matching
            exp_normalized = experience_level.strip()
            
            # Map common variations
            exp_mappings = {
                'intern': ['intern', 'fresher', 'entry', 'entry-level', 'trainee'],
                'entry': ['entry', 'fresher', 'entry-level'],
                'junior': ['junior'],
                'mid': ['mid', 'mid-level', 'mid-senior'],
                'senior': ['senior', 'senior-level'],
                'lead': ['lead'],
                'experienced': ['experienced']
            }
            
            # Find matching variations
            exp_lower = exp_normalized.lower()
            search_terms = [exp_normalized]
            
            for key, variations in exp_mappings.items():
                if any(v in exp_lower for v in variations):
                    search_terms.extend(variations)
                    break
            
            # Create experience level mask (OR condition for variations)
            exp_mask = self.df['ExperienceLevel'].str.contains(
                '|'.join(search_terms), case=False, na=False, regex=True
            )
            
            # Combine role and experience masks
            combined_mask = role_mask & exp_mask
            
            if combined_mask.sum() > 0:
                filtered_df = self.df[combined_mask]
                logger.info(f"Found {len(filtered_df)} JDs matching '{role}' + '{experience_level}'")
            else:
                # Fallback: Use all role matches if no experience level match
                filtered_df = self.df[role_mask]
                logger.info(f"No exact experience level match for '{experience_level}', using all {len(filtered_df)} '{role}' JDs")
        else:
            # No experience level specified, use all role matches
            filtered_df = self.df[role_mask]
            logger.info(f"Found {len(filtered_df)} JDs matching '{role}' (all experience levels)")
        
        if filtered_df.empty:
            return []
        
        # Extract all skills
        all_skills = []
        for skills_field in filtered_df['Skills']:
            # Parse skills (could be JSON string or list)
            try:
                if isinstance(skills_field, str):
                    # Try parsing as JSON
                    if skills_field.startswith('['):
                        skills = json.loads(skills_field)
                    else:
                        # Semicolon-separated
                        skills = [s.strip() for s in skills_field.split(';')]
                else:
                    skills = skills_field if isinstance(skills_field, list) else []
                
                all_skills.extend(skills)
            except Exception as e:
                logger.warning(f"Error parsing skills: {e}")
                continue
        
        # Return unique skills
        unique_skills = list(set(all_skills))
        logger.info(f"Extracted {len(unique_skills)} unique skills for '{role}' ({experience_level or 'all levels'})")
        return unique_skills
    
    def get_role_insights(self, role: str) -> Dict:
        """
        Get comprehensive insights for a role
        
        Returns:
            Dictionary with role statistics, top skills, and metadata
        """
        if not self.is_available():
            return {"error": "Database not available"}
        
        mask = self.df['Title'].str.contains(role, case=False, na=False)
        role_df = self.df[mask]
        
        if role_df.empty:
            return {"error": f"Role '{role}' not found"}
        
        # Aggregate skills
        all_skills = []
        all_responsibilities = []
        all_keywords = []
        
        for _, row in role_df.iterrows():
            # Parse skills
            skills = self._parse_field(row.get('Skills', []))
            all_skills.extend(skills)
            
            # Parse responsibilities
            responsibilities = self._parse_field(row.get('Responsibilities', []))
            all_responsibilities.extend(responsibilities)
            
            # Parse keywords
            keywords = self._parse_field(row.get('Keywords', []))
            all_keywords.extend(keywords)
        
        # Skill frequency
        from collections import Counter
        skill_freq = Counter(all_skills)
        
        return {
            "role": role,
            "jd_count": len(role_df),
            "total_unique_skills": len(set(all_skills)),
            "top_skills": [s for s, count in skill_freq.most_common(30)],
            "skill_frequencies": dict(skill_freq.most_common(50)),
            "experience_levels": role_df['ExperienceLevel'].value_counts().to_dict(),
            "avg_skills_per_jd": len(all_skills) / len(role_df) if role_df.empty == False else 0
        }
    
    def _parse_field(self, field) -> List[str]:
        """Parse a field that could be JSON array, semicolon-separated, or list"""
        if isinstance(field, list):
            return field
        
        if isinstance(field, str):
            try:
                # Try JSON parsing
                if field.startswith('['):
                    return json.loads(field)
                else:
                    # Semicolon-separated
                    return [s.strip() for s in field.split(';') if s.strip()]
            except:
                return []
        
        return []
    
    def search_similar_roles(self, role: str, limit: int = 5) -> List[str]:
        """Find similar role titles using fuzzy matching"""
        if not self.is_available():
            return []
        
        from difflib import get_close_matches
        all_roles = self.df['Title'].unique().tolist()
        matches = get_close_matches(role, all_roles, n=limit, cutoff=0.6)
        return matches
