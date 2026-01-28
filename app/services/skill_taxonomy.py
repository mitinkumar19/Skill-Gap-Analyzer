"""
Skill Taxonomy Service - Loads and normalizes skills from job database.
Provides fast lookup with alias mapping and categorization.
"""
import json
import re
import logging
from pathlib import Path
from typing import Dict, List, Set, Optional, Tuple
from functools import lru_cache

logger = logging.getLogger(__name__)


class SkillTaxonomy:
    """
    Skill database loader and normalizer.
    
    Features:
    - Loads 2000+ skills from job_dataset.json
    - Normalizes skill names (case, whitespace, abbreviations)
    - Provides alias mapping (JS → JavaScript, K8s → Kubernetes)
    - Fast O(1) lookup via hash sets
    """
    
    # Common abbreviations and aliases
    SKILL_ALIASES: Dict[str, str] = {
        # JavaScript variants
        "js": "JavaScript",
        "javascript": "JavaScript",
        "es6": "JavaScript",
        "es2015": "JavaScript",
        "ecmascript": "JavaScript",
        
        # TypeScript
        "ts": "TypeScript",
        "typescript": "TypeScript",
        
        # Python
        "python3": "Python",
        "python 3": "Python",
        "py": "Python",
        
        # Kubernetes
        "k8s": "Kubernetes",
        "kube": "Kubernetes",
        
        # Docker
        "containerization": "Docker",
        "containers": "Docker",
        
        # Databases
        "postgres": "PostgreSQL",
        "postgresql": "PostgreSQL",
        "psql": "PostgreSQL",
        "mongo": "MongoDB",
        "mongodb": "MongoDB",
        "mysql": "MySQL",
        "mssql": "SQL Server",
        "sql server": "SQL Server",
        
        # Cloud
        "amazon web services": "AWS",
        "aws": "AWS",
        "google cloud platform": "GCP",
        "google cloud": "GCP",
        "gcp": "GCP",
        "azure": "Azure",
        "microsoft azure": "Azure",
        
        # Frameworks
        "reactjs": "React",
        "react.js": "React",
        "react js": "React",
        "vuejs": "Vue.js",
        "vue": "Vue.js",
        "vue.js": "Vue.js",
        "angularjs": "Angular",
        "angular.js": "Angular",
        "angular": "Angular",
        "nextjs": "Next.js",
        "next.js": "Next.js",
        "nodejs": "Node.js",
        "node.js": "Node.js",
        "node": "Node.js",
        "expressjs": "Express.js",
        "express.js": "Express.js",
        "express": "Express.js",
        "fastapi": "FastAPI",
        "django": "Django",
        "flask": "Flask",
        "spring boot": "Spring Boot",
        "springboot": "Spring Boot",
        
        # APIs
        "rest api": "REST APIs",
        "rest apis": "REST APIs",
        "restful": "REST APIs",
        "restful api": "REST APIs",
        "graphql": "GraphQL",
        
        # ML/AI
        "machine learning": "Machine Learning",
        "ml": "Machine Learning",
        "deep learning": "Deep Learning",
        "dl": "Deep Learning",
        "artificial intelligence": "AI",
        "ai": "AI",
        "natural language processing": "NLP",
        "nlp": "NLP",
        
        # Version Control
        "git": "Git",
        "github": "GitHub",
        "gitlab": "GitLab",
        "bitbucket": "Bitbucket",
        
        # CI/CD
        "ci/cd": "CI/CD",
        "cicd": "CI/CD",
        "continuous integration": "CI/CD",
        "jenkins": "Jenkins",
        "github actions": "GitHub Actions",
        
        # Languages
        "c#": "C#",
        "csharp": "C#",
        "c sharp": "C#",
        "c++": "C++",
        "cpp": "C++",
        "cplusplus": "C++",
        "golang": "Go",
        "go": "Go",
        "rust": "Rust",
        "java": "Java",
        "kotlin": "Kotlin",
        "swift": "Swift",
        "ruby": "Ruby",
        "php": "PHP",
        "r": "R",
        "scala": "Scala",
        
        # Testing
        "unit testing": "Unit Testing",
        "unittest": "Unit Testing",
        "pytest": "Pytest",
        "jest": "Jest",
        "mocha": "Mocha",
        "selenium": "Selenium",
        "cypress": "Cypress",
        
        # Data
        "pandas": "Pandas",
        "numpy": "NumPy",
        "scipy": "SciPy",
        "tensorflow": "TensorFlow",
        "tf": "TensorFlow",
        "pytorch": "PyTorch",
        "torch": "PyTorch",
        "scikit-learn": "Scikit-learn",
        "sklearn": "Scikit-learn",
        
        # DevOps
        "terraform": "Terraform",
        "ansible": "Ansible",
        "puppet": "Puppet",
        "chef": "Chef",
        
        # Messaging
        "kafka": "Apache Kafka",
        "rabbitmq": "RabbitMQ",
        "redis": "Redis",
        
        # Others
        "html5": "HTML",
        "html": "HTML",
        "css3": "CSS",
        "css": "CSS",
        "sass": "SASS",
        "scss": "SASS",
        "less": "LESS",
        "tailwind": "Tailwind CSS",
        "tailwindcss": "Tailwind CSS",
        "bootstrap": "Bootstrap",
        "jquery": "jQuery",
        "webpack": "Webpack",
        "vite": "Vite",
        "babel": "Babel",
        "eslint": "ESLint",
        "prettier": "Prettier",
        "linux": "Linux",
        "unix": "Unix",
        "bash": "Bash",
        "shell": "Shell Scripting",
        "powershell": "PowerShell",
    }
    
    def __init__(self, data_path: str = "data/job_dataset.json"):
        self.data_path = data_path
        self._skills_set: Set[str] = set()
        self._skills_lower_map: Dict[str, str] = {}  # lowercase -> canonical
        self._load_skills()
    
    def _load_skills(self) -> None:
        """Load skills from job dataset and build lookup structures."""
        try:
            path = Path(self.data_path)
            if not path.exists():
                logger.warning(f"Job database not found at {self.data_path}")
                return
            
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Extract all unique skills
            for job in data:
                skills = job.get('Skills', [])
                if isinstance(skills, list):
                    for skill in skills:
                        if isinstance(skill, str) and skill.strip():
                            canonical = skill.strip()
                            self._skills_set.add(canonical)
                            self._skills_lower_map[canonical.lower()] = canonical
            
            # Add aliases to lowercase map
            for alias, canonical in self.SKILL_ALIASES.items():
                self._skills_lower_map[alias.lower()] = canonical
                # Also add the canonical form
                if canonical not in self._skills_set:
                    self._skills_set.add(canonical)
                    self._skills_lower_map[canonical.lower()] = canonical
            
            logger.info(f"Loaded {len(self._skills_set)} unique skills into taxonomy")
            
        except Exception as e:
            logger.error(f"Failed to load skill taxonomy: {e}")
    
    @property
    def skills(self) -> Set[str]:
        """Get all canonical skill names."""
        return self._skills_set.copy()
    
    @property
    def skill_count(self) -> int:
        """Get total number of skills in taxonomy."""
        return len(self._skills_set)
    
    def normalize(self, skill: str) -> Optional[str]:
        """
        Normalize a skill name to its canonical form.
        
        Args:
            skill: Raw skill name (any case, may include aliases)
            
        Returns:
            Canonical skill name if found, None otherwise
        """
        if not skill:
            return None
        
        # Clean and lowercase
        cleaned = skill.strip().lower()
        cleaned = re.sub(r'\s+', ' ', cleaned)  # Normalize whitespace
        
        # Direct lookup
        if cleaned in self._skills_lower_map:
            return self._skills_lower_map[cleaned]
        
        return None
    
    def is_known_skill(self, skill: str) -> bool:
        """Check if a skill exists in the taxonomy."""
        return self.normalize(skill) is not None
    
    def get_canonical(self, skill: str) -> Tuple[str, bool]:
        """
        Get canonical form of skill.
        
        Returns:
            Tuple of (canonical_name, is_known)
            If not known, returns original with is_known=False
        """
        canonical = self.normalize(skill)
        if canonical:
            return (canonical, True)
        return (skill.strip(), False)
    
    @lru_cache(maxsize=1000)
    def search_similar(self, query: str, limit: int = 5) -> List[str]:
        """
        Find similar skills using fuzzy matching.
        Uses rapidfuzz for performance.
        
        Args:
            query: Skill to search for
            limit: Maximum results to return
            
        Returns:
            List of similar skill names
        """
        try:
            from rapidfuzz import fuzz, process
            
            if not query or not self._skills_set:
                return []
            
            # Use rapidfuzz for fast fuzzy matching
            results = process.extract(
                query.strip(),
                list(self._skills_set),
                scorer=fuzz.WRatio,
                limit=limit,
                score_cutoff=70  # Minimum 70% similarity
            )
            
            return [r[0] for r in results]
            
        except ImportError:
            logger.warning("rapidfuzz not installed, fuzzy search disabled")
            return []
        except Exception as e:
            logger.error(f"Fuzzy search failed: {e}")
            return []
