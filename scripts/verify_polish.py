"""
Verification script for Post-Processing (v2.2).
Tests:
1. Compound skills split correctly ("Docker, CI/CD" -> "Docker", "CI/CD")
2. Generic abstractions removed ("Cloud" removed if "AWS" present)
3. Deduplication works
"""
from app.services.skill_extractor import SkillExtractor
import logging

logging.basicConfig(level=logging.INFO)

def test_post_processing():
    extractor = SkillExtractor()
    
    print("\n=== Test 1: Compound Splitting ===")
    text_compound = """
    Technical Skills
    Docker, CI/CD, Git/GitHub, JavaScript/TypeScript
    """
    skills = extractor.extract(text_compound)
    print(f"Input: 'Docker, CI/CD, Git/GitHub, JavaScript/TypeScript'")
    print(f"Extracted: {skills}")
    
    # Should have individual skills, not compounds
    expected_individual = ["Docker", "CI/CD", "Git", "GitHub", "JavaScript", "TypeScript"]
    found = [s for s in expected_individual if s in skills]
    
    # Should NOT have compound strings
    bad_compounds = ["Docker, CI/CD", "Git/GitHub", "JavaScript/TypeScript"]
    found_bad = [s for s in bad_compounds if s in skills]
    
    if len(found) >= len(expected_individual) - 1:
        print(f"[✓] PASSED: Individual skills extracted: {found}")
    else:
        print(f"[!] WARNING: Missing some individual skills. Found: {found}")
        
    if found_bad:
        print(f"[!] FAILED: Compound strings still present: {found_bad}")
    else:
        print("[✓] PASSED: No bad compounds in output")

    print("\n=== Test 2: Abstraction Removal ===")
    text_abstraction = """
    Skills
    Cloud, AWS, Azure, APIs, REST APIs, gRPC, CSS, Tailwind CSS
    """
    skills_abs = extractor.extract(text_abstraction)
    print(f"Extracted: {skills_abs}")
    
    # "Cloud" should be removed (AWS/Azure present)
    # "APIs" should be removed (REST APIs/gRPC present)
    # "CSS" should be removed (Tailwind CSS present)
    generics_that_should_be_gone = ["Cloud", "APIs", "CSS"]
    found_generics = [s for s in generics_that_should_be_gone if s in skills_abs]
    
    if found_generics:
        print(f"[!] FAILED: Generic abstractions still present: {found_generics}")
    else:
        print("[✓] PASSED: Generic abstractions correctly removed")
    
    # Specific skills should be present
    specifics = ["AWS", "Azure", "REST APIs", "gRPC", "Tailwind CSS"]
    found_specifics = [s for s in specifics if s in skills_abs]
    print(f"    Specifics kept: {found_specifics}")

    print("\n=== Test 3: Complete Resume Scenario ===")
    text_full = """
    Skills
    Languages: JavaScript, TypeScript, Rust, Python
    Backend: Node.js, Express.js, FastAPI, REST APIs, gRPC, WebSockets
    Databases: PostgreSQL, MongoDB, Redis
    Cloud: AWS, Azure, Docker, CI/CD
    
    Experience
    Built scalable microservices using Node.js and deployed on AWS.
    """
    skills_full = extractor.extract(text_full)
    print(f"Extracted ({len(skills_full)} skills): {skills_full}")
    
    must_have = ["JavaScript", "TypeScript", "Node.js", "PostgreSQL", "AWS", "Docker"]
    must_not_have = ["Cloud", "APIs", "Languages", "Backend"]
    
    missing = [s for s in must_have if s not in skills_full]
    unwanted = [s for s in must_not_have if s in skills_full]
    
    if missing:
        print(f"[!] WARNING: Missing expected skills: {missing}")
    else:
        print("[✓] PASSED: All critical skills found")
        
    if unwanted:
        print(f"[!] WARNING: Unwanted generics still present: {unwanted}")
    else:
        print("[✓] PASSED: Generics/noise correctly removed")

if __name__ == "__main__":
    test_post_processing()
