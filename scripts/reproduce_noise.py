"""
Verification script for noise reduction in SkillExtractor v2.
Tests if hallucinations are filtered out using strict rules.
"""
from app.services.skill_extractor import SkillExtractor
import logging

# Enable debug logging to see scoring decisions
logging.basicConfig(level=logging.INFO)

def test_noise_reduction():
    extractor = SkillExtractor()
    
    # Text with potential triggers for false positives
    # "control" -> Control Theory? (Should be rejected - no anchor/wrong section)
    # "physics" -> Game Physics? (Should be rejected)
    # "blockchain" -> (Mentally, not technically)
    # "SEO" -> (Optimization context, not skill)
    
    # We structure it to test Segmentation + Anchoring
    text = """
    John Doe
    Backend Engineer
    
    Summary
    I have advanced control over the project timeline.
    I ensure high roi for the company.
    I understood the blockchain of events in the system.
    
    Experience
    - Worked on a system that is like a game engine for finance.
    - Handled massive traffic load using Redis and Python.
    - Optimized database queries for better performance.
    
    Technical Skills
    Python, Redis, Docker, Kubernetes
    """
    
    print("\n--- Extraction Results (v2) ---")
    skills = extractor.extract(text)
    print(f"Extracted: {skills}")
    
    # Check for likely false positives
    likely_noise = ["ROI", "Blockchain", "Game Engine", "Control Theory", "SEO"]
    
    found_noise = [s for s in skills if any(n.lower() in s.lower() for n in likely_noise)]
    
    # Check for valid skills
    valid_expected = ["Python", "Redis", "Docker", "Kubernetes"]
    found_valid = [s for s in skills if s in valid_expected]
    
    print("\n--- Analysis ---")
    if found_noise:
        print(f"[!] FAILED: Found noise: {found_noise}")
    else:
        print("[✓] PASSED: No noise found.")
        
    if len(found_valid) == len(valid_expected):
        print(f"[✓] PASSED: All valid skills found: {found_valid}")
    else:
        print(f"[!] FAILED: Missed valid skills. Found: {found_valid}")

if __name__ == "__main__":
    test_noise_reduction()
