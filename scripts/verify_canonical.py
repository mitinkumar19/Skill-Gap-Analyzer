"""
Verification script for Canonical Normalization (v2.3).
Tests the exact example from the user's requirements.
"""
from app.services.skill_extractor import SkillExtractor
import logging

logging.basicConfig(level=logging.INFO)

def test_canonical_normalization():
    extractor = SkillExtractor()
    
    print("\n=== Test 1: User's Exact Example ===")
    text = """
    Skills
    Git, Git/GitHub, GitHub, JavaScript/TypeScript
    """
    skills = extractor.extract(text)
    print(f"Input: 'Git, Git/GitHub, GitHub, JavaScript/TypeScript'")
    print(f"Output: {skills}")
    
    expected = ["Git", "GitHub", "JavaScript", "TypeScript"]
    missing = [s for s in expected if s not in skills]
    extra = [s for s in skills if s not in expected]
    
    if not missing and not extra:
        print("[✓] PASSED: Exact match with expected output!")
    else:
        if missing:
            print(f"[!] Missing: {missing}")
        if extra:
            print(f"[!] Extra: {extra}")
    
    print("\n=== Test 2: No Duplicates ===")
    text2 = """
    Skills
    Node.js, NodeJS, node, Express.js, expressjs
    """
    skills2 = extractor.extract(text2)
    print(f"Output: {skills2}")
    
    # Should normalize to Node.js and Express.js only
    if "Node.js" in skills2 and skills2.count("Node.js") == 1:
        print("[✓] PASSED: Node.js appears once")
    else:
        print("[!] FAILED: Node.js duplicated or missing")
        
    if "Express.js" in skills2 and skills2.count("Express.js") == 1:
        print("[✓] PASSED: Express.js appears once")
    else:
        print("[!] FAILED: Express.js duplicated or missing")

    print("\n=== Test 3: Backend Concepts ===")
    text3 = """
    Skills
    WebSockets, Event-Driven, Authentication, Unit Testing, Scalability
    """
    skills3 = extractor.extract(text3)
    print(f"Output: {skills3}")
    
    expected3 = ["WebSockets", "Event-Driven Systems", "Authentication & Authorization", "Unit Testing", "Scalability"]
    found = [s for s in expected3 if s in skills3]
    print(f"Found backend concepts: {found}")
    
    print("\n=== Test 4: Full Resume Scenario ===")
    text4 = """
    Skills
    Languages: JavaScript, TypeScript, Rust, Python
    Backend: Node.js, Express.js, FastAPI, REST APIs, gRPC, WebSockets
    Databases: PostgreSQL, MongoDB, Redis
    Cloud: AWS, Azure, Docker, CI/CD
    Concepts: Event-Driven, Scalability, Unit Testing
    """
    skills4 = extractor.extract(text4)
    print(f"Output ({len(skills4)} skills): {skills4}")
    
    must_have = ["JavaScript", "TypeScript", "Node.js", "REST APIs", "AWS", "Docker", "CI/CD", "WebSockets"]
    must_not_have = ["Cloud", "APIs", "Languages", "Backend", "Concepts"]
    
    m = [s for s in must_have if s not in skills4]
    u = [s for s in must_not_have if s in skills4]
    
    if m:
        print(f"[!] Missing: {m}")
    else:
        print("[✓] All critical skills present")
        
    if u:
        print(f"[!] Unwanted: {u}")
    else:
        print("[✓] No generic abstractions")

if __name__ == "__main__":
    test_canonical_normalization()
