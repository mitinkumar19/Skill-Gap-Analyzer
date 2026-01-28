from groq import Groq
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# Lazy import for skill extractor to avoid circular imports
_skill_extractor = None

def _get_skill_extractor():
    """Lazy load SkillExtractor to avoid startup overhead."""
    global _skill_extractor
    if _skill_extractor is None:
        from app.services.skill_extractor import SkillExtractor
        _skill_extractor = SkillExtractor()
    return _skill_extractor

class GeneratorService:
    def __init__(self):
        self.api_key = settings.GROQ_API_KEY
        self.client = None
        if self.api_key:
            try:
                self.client = Groq(api_key=self.api_key)
            except Exception as e:
                logger.error(f"Failed to initialize Groq client: {e}")
        else:
            logger.warning("GROQ_API_KEY not set. AI Features will be disabled.")

    def generate_roadmap(self, missing_skills: list[str], role: str) -> str:
        """
        Generate a learning roadmap for the missing skills.
        """
        if not self.client:
            return "AI Generation is disabled (No API Key). Please set GROQ_API_KEY."
        
        prompt = f"""
        You are an expert Career Coach and Technical Mentor.
        
        Target Role: {role}
        Missing Skills Identification: {', '.join(missing_skills)}
        
        Create a personalized "Skill Bridge" learning path for this candidate.
        For each missing skill:
        1. Explain WHY it is critical for a {role}.
        2. Recommend 1 specific high-quality resource (Course, Doc, or Project Idea).
        3. Estimate time to learn.
        
        Format as Markdown. Be encouraging but technical and precise.
        """
        
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model="llama-3.3-70b-versatile", # Using a supported strong model
                temperature=0.5,
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            logger.error(f"Generation failed: {e}")
            return f"Error generating roadmap: {str(e)}"

    

    def generate_skills_list(self, role: str, experience_level: str = "Mid-Level") -> list[str]:
        """
        Generate a list of technical skills for a given role and experience level.
        """
        if not self.client:
            return ["AI Generation Disabled"]
        
        prompt = f"""
        List the key technical skills required for the role: "{role}" at the "{experience_level}" level.

        Rules:
        1. Return ONLY technical skills (programming languages, frameworks, tools, technologies, platforms)
        2. NO soft skills (exclude communication, leadership, teamwork, problem-solving, etc.)
        3. Return ALL required technical skills for this role and level (do not limit to top 10).
        4. Adjust difficulty based on experience level
        5. Return as a JSON array of strings only, no other text

        Example output format:
        ["Python", "SQL", "Docker", "Kubernetes", "AWS", "REST APIs", "Git", "PostgreSQL"]

        Now list the technical skills for "{role}" at "{experience_level}" level.
        """
        
        try:
            logger.info(f"Generating skills list for: {role}")
            chat_completion = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
                temperature=0.5,
                response_format={"type": "json_object"}
            )
            content = chat_completion.choices[0].message.content
            
            import json
            data = json.loads(content)
            
            # Extract list from potential behaviors
            if isinstance(data, list):
                return data
            if isinstance(data, dict):
                # Common pattern: {"skills": [...]}
                for key in data:
                    if isinstance(data[key], list):
                        return data[key]
            
            return ["Error: AI returned unexpected format"]
            
        except Exception as e:
            logger.error(f"Skills Generation failed: {e}")
            return [f"Error: {str(e)}"]

    def extract_skills_from_text(self, text: str, use_api: bool = False) -> list[str]:
        """
        Extract technical skills from a given text (Resume).
        
        Uses local NLP pipeline by default for:
        - Faster processing (~50-100ms vs 500-2000ms API)
        - No rate limits
        - Offline capability
        
        Args:
            text: Resume or document text
            use_api: If True, use Groq API instead of local NLP (optional fallback)
        
        Returns:
            List of extracted skill names
        """
        if not text or not text.strip():
            return []
        
        # Default: Use local NLP pipeline
        if not use_api:
            try:
                extractor = _get_skill_extractor()
                skills = extractor.extract(text)
                logger.info(f"Local NLP extracted {len(skills)} skills")
                return skills
            except Exception as e:
                logger.warning(f"Local NLP extraction failed, falling back to API: {e}")
                # Fall through to API fallback
        
        # API fallback (if requested or local NLP failed)
        return self._extract_skills_via_api(text)
    
    def _extract_skills_via_api(self, text: str) -> list[str]:
        """
        Extract skills using Groq API (fallback method).
        
        Kept for backward compatibility and edge cases.
        """
        if not self.client:
            logger.warning("API extraction requested but Groq client not available")
            return []
        
        prompt = f"""
        Analyze the following Resume Text and extract all Technical Skills, Tools, Languages, and Frameworks mentioned.
        
        Resume Text:
        {text[:4000]}... (truncated)
        
        Return strictly a JSON list of strings. Do not include any other text.
        Example: ["Python", "FastAPI", "React", "AWS", "Docker"]
        """
        
        try:
            logger.info("Extracting skills via Groq API...")
            chat_completion = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            content = chat_completion.choices[0].message.content
            
            import json
            data = json.loads(content)
            
            # Extract list
            if isinstance(data, list):
                return data
            if isinstance(data, dict):
                for key in data:
                    if isinstance(data[key], list):
                        return data[key]
            
            return []
            
        except Exception as e:
            logger.error(f"API skill extraction failed: {e}")
            return []
