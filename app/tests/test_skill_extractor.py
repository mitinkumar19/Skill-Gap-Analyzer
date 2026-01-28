"""
Unit tests for SkillExtractor and SkillTaxonomy services.
"""
import pytest
from app.services.skill_taxonomy import SkillTaxonomy
from app.services.skill_extractor import SkillExtractor


class TestSkillTaxonomy:
    """Tests for SkillTaxonomy skill database service."""
    
    @pytest.fixture
    def taxonomy(self):
        return SkillTaxonomy()
    
    def test_load_skills(self, taxonomy):
        """Should load skills from job_dataset.json"""
        assert taxonomy.skill_count > 100, "Should load at least 100 skills"
    
    def test_normalize_exact_match(self, taxonomy):
        """Exact skill names should normalize correctly"""
        # Find a skill that's definitely in the dataset
        sample_skill = list(taxonomy.skills)[0] if taxonomy.skills else None
        if sample_skill:
            result = taxonomy.normalize(sample_skill)
            assert result == sample_skill
    
    def test_normalize_case_insensitive(self, taxonomy):
        """Should handle case variations"""
        result = taxonomy.normalize("python")
        assert result is not None
        assert result.lower() == "python"
    
    def test_normalize_alias(self, taxonomy):
        """Should resolve common aliases"""
        # JS → JavaScript
        result = taxonomy.normalize("js")
        assert result == "JavaScript"
        
        # K8s → Kubernetes
        result = taxonomy.normalize("k8s")
        assert result == "Kubernetes"
    
    def test_is_known_skill(self, taxonomy):
        """Should correctly identify known skills"""
        assert taxonomy.is_known_skill("Python") == True
        assert taxonomy.is_known_skill("xyznotaskill123") == False
    
    def test_search_similar(self, taxonomy):
        """Fuzzy search should find similar skills"""
        results = taxonomy.search_similar("pythn", limit=5)  # Typo
        assert len(results) > 0
        # Should find Python as a close match
        assert any("python" in r.lower() for r in results)


class TestSkillExtractor:
    """Tests for SkillExtractor hybrid NLP pipeline."""
    
    @pytest.fixture
    def extractor(self):
        return SkillExtractor()
    
    def test_extract_empty_text(self, extractor):
        """Should handle empty text gracefully"""
        assert extractor.extract("") == []
        assert extractor.extract("   ") == []
        assert extractor.extract(None) == []
    
    def test_extract_exact_skills(self, extractor):
        """Should extract exact skill names"""
        text = "Experienced in Python, JavaScript, and Docker"
        skills = extractor.extract(text)
        
        assert "Python" in skills
        assert "JavaScript" in skills
        assert "Docker" in skills
    
    def test_extract_multi_word_skills(self, extractor):
        """Should extract multi-word skills"""
        text = "Strong experience with Machine Learning and REST APIs"
        skills = extractor.extract(text)
        
        # Should find multi-word skills
        skill_str = " ".join(skills).lower()
        assert "machine learning" in skill_str or "ml" in skill_str
    
    def test_extract_abbreviations(self, extractor):
        """Should resolve skill abbreviations to canonical names"""
        text = "Proficient in JS, TS, and K8s deployment"
        skills = extractor.extract(text)
        
        # Abbreviations should be resolved
        assert "JavaScript" in skills or "TypeScript" in skills or "Kubernetes" in skills
    
    def test_extract_from_resume_context(self, extractor):
        """Should extract skills from realistic resume text"""
        resume_text = """
        Software Engineer with 5 years of experience.
        
        Technical Skills:
        - Python, FastAPI, Django
        - React, TypeScript, Node.js
        - PostgreSQL, MongoDB, Redis
        - Docker, Kubernetes, AWS
        - Git, CI/CD, Jenkins
        
        Experience:
        - Built REST APIs using Python and FastAPI
        - Developed frontend applications with React and TypeScript
        - Deployed microservices on AWS EKS with Docker containers
        """
        
        skills = extractor.extract(resume_text)
        
        # Should find many relevant skills
        assert len(skills) >= 5, f"Expected at least 5 skills, got {len(skills)}: {skills}"
        
        # Check for specific important skills
        skills_lower = [s.lower() for s in skills]
        assert any("python" in s for s in skills_lower)
        assert any("react" in s for s in skills_lower)
    
    def test_extract_case_variations(self, extractor):
        """Should handle various case styles"""
        text = "Experience with PYTHON, javascript, and PostgreSQL"
        skills = extractor.extract(text)
        
        # Should normalize to canonical case
        assert len(skills) >= 2
    
    def test_no_false_positives_common_words(self, extractor):
        """Should not extract common words as skills"""
        text = "I have experience working on various projects with different teams"
        skills = extractor.extract(text)
        
        # Common words should not be extracted as skills
        common_words = {"experience", "working", "various", "projects", "different", "teams"}
        for skill in skills:
            assert skill.lower() not in common_words, f"'{skill}' should not be extracted as a skill"
    
    def test_cached_extraction(self, extractor):
        """Cached extraction should return same results"""
        text = "Skills: Python, Java, Docker"
        
        result1 = extractor.extract_cached(text)
        result2 = extractor.extract_cached(text)
        
        assert result1 == result2
    
    def test_skill_suggestions(self, extractor):
        """Should provide skill autocomplete suggestions"""
        suggestions = extractor.get_skill_suggestions("python", limit=5)
        
        # Should return some suggestions (may be empty if no close matches)
        # The main test is that it doesn't crash and returns a list
        assert isinstance(suggestions, list)


class TestIntegration:
    """Integration tests for the full NLP pipeline."""
    
    def test_full_pipeline_real_resume(self):
        """Test extraction on realistic resume content"""
        extractor = SkillExtractor()
        
        resume = """
        John Doe
        Senior Software Engineer
        
        Summary:
        Innovative software engineer with 8+ years of experience in building 
        scalable web applications using modern technologies.
        
        Skills:
        Python, JavaScript, TypeScript, Go, SQL
        React, Next.js, Node.js, FastAPI, Django
        PostgreSQL, MongoDB, Redis, Elasticsearch
        AWS (EC2, S3, Lambda, RDS), Docker, Kubernetes
        Git, GitHub Actions, Jenkins, Terraform
        
        Experience:
        ABC Tech (2020-Present) - Senior Engineer
        - Architected microservices system handling 1M+ requests/day
        - Led migration from monolith to Kubernetes-based architecture
        - Implemented CI/CD pipelines using GitHub Actions
        
        XYZ Corp (2017-2020) - Software Engineer
        - Built React frontend with TypeScript
        - Developed REST APIs with Python/FastAPI
        - Managed PostgreSQL and MongoDB databases
        """
        
        skills = extractor.extract(resume)
        
        # Should extract a good number of skills
        assert len(skills) >= 10, f"Expected 10+ skills, got {len(skills)}"
        
        # Key skills that must be found
        skills_found = set(s.lower() for s in skills)
        expected_skills = {"python", "javascript", "react", "docker"}
        
        for expected in expected_skills:
            assert any(expected in s for s in skills_found), f"Missing expected skill: {expected}"
