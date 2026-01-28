"""
Verification script for Normalization and Strict Matching (v2.1).
Tests:
1. "JavaScript" does NOT trigger "Java" (Strict Ratio)
2. "Java/C++" triggers "Java" AND "C++" (Slash Splitting)
3. Noise Reduction (re-verification)
"""
from app.services.skill_extractor import SkillExtractor
import logging

logging.basicConfig(level=logging.INFO)

def test_strict_provenance():
    extractor = SkillExtractor()
    
    print("\n=== Test 1: Substring / Phantom Matching ===")
    # Text contains ONLY JavaScript. Should NOT match Java.
    text_js = """
    Skills
    JavaScript, TypeScript, React
    """
    skills_js = extractor.extract(text_js)
    print(f"Input: 'JavaScript, TypeScript, React'")
    print(f"Extracted: {skills_js}")
    
    if "Java" in skills_js:
        print("[!] FAILED: Extracted 'Java' from 'JavaScript' (Substring match issue)")
    else:
        print("[✓] PASSED: 'Java' correctly NOT extracted")

    if "Script" in skills_js:
         print("[!] FAILED: Extracted 'Script' from 'TypeScript'")
    else:
         print("[✓] PASSED: 'Script' correctly NOT extracted/ignored")

    print("\n=== Test 2: Normalization (Slash Splitting) ===")
    text_slash = """
    Skills
    Java/C++, CI/CD, TCP/IP
    """
    skills_slash = extractor.extract(text_slash)
    print(f"Input: 'Java/C++, CI/CD, TCP/IP'")
    print(f"Extracted: {skills_slash}")
    
    expected_slash = ["Java", "C++", "CI/CD", "TCP/IP"]
    # Note: "CI/CD" might be extracted as "CI/CD" or split into "CI", "CD"?
    # If "CI/CD" is in taxonomy (it is), it should match "CI/CD" exact first (or n-gram).
    # If "Java/C++" isn't in taxonomy, it splits.
    
    missing_slash = [s for s in expected_slash if s not in skills_slash]
    if missing_slash:
        # Check if CI/CD was split
        print(f"[!] Warning: Missing: {missing_slash}")
        if "CI" in skills_slash and "CD" in skills_slash:
            print("    (But CI and CD were found separately)")
    else:
        print("[✓] PASSED: All slash-separated skills found")

    print("\n=== Test 3: Re-verify Noise Reduction ===")
    text_noise = """
    Experience
    I have advanced control over the project timeline and high ROI.
    I understood the blockchain of events.
    """
    skills_noise = extractor.extract(text_noise)
    print(f"Extracted: {skills_noise}")
    
    keywords = ["ROI", "Blockchain", "Control Theory"]
    found = [k for k in keywords if k in skills_noise]
    if found:
        print(f"[!] FAILED: Noise found: {found}")
    else:
        print("[✓] PASSED: Noise filtering intact")

if __name__ == "__main__":
    test_strict_provenance()
