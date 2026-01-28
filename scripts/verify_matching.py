"""
Script to analyze fuzzy matching behavior and reproduction "Composite Line Explosion".
Tests WRatio vs Ratio for common false positives.
"""
from rapidfuzz import fuzz

def analyze_matching():
    test_cases = [
        # Candidate (from text), Target (from dictionary)
        ("Java", "JavaScript"),
        ("Script", "TypeScript"),
        (".NET", "ASP.NET Core"),
        ("Flow", "TensorFlow"),
        ("Vision", "Computer Vision"),
        ("React", "React Native"),
        ("C", "C++"),
        ("Advanced", "Advanced Systems"), # Noise matching
    ]
    
    print(f"{'Candidate':<10} | {'Target':<20} | {'WRatio':<6} | {'Ratio':<6} | {'Outcome'}")
    print("-" * 65)
    
    for cand, target in test_cases:
        w_score = fuzz.WRatio(cand, target)
        r_score = fuzz.ratio(cand, target)
        
        # User threshold is 90
        w_pass = "FAIL" if w_score >= 90 else "PASS"
        r_pass = "PASS" # Ratio usually handles this well
        
        # In this context, "FAIL" means it matched when it shouldn't have (False Positive)
        # We want strict matching, so partials should ideally be low score if they are distinct concepts
        # But "Java" and "JavaScript" are distinct. 
        
        print(f"{cand:<10} | {target:<20} | {w_score:<6.1f} | {r_score:<6.1f} | {w_pass}")

if __name__ == "__main__":
    analyze_matching()
