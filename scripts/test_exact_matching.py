"""
Test exact matching logic
"""

# Simulate the exact matching logic
resume_skills = ["Docker", "Express.js", "Git", "MongoDB", "Node.js", "PostgreSQL", "AWS", "Microsoft Azure"]
target_skills = ["Docker", "Express.js", "Git", "MongoDB", "Node.js", "PostgreSQL", "Cloud Basics", "Django"]

# Phase 1: Exact matching
resume_skills_lower = {s.lower(): s for s in resume_skills}
target_skills_lower = {s.lower(): s for s in target_skills}

exact_matches = set(resume_skills_lower.keys()) & set(target_skills_lower.keys())

print(f"Resume skills: {len(resume_skills)}")
print(f"Target skills: {len(target_skills)}")
print(f"\nExact matches: {len(exact_matches)}")
print(f"Matched skills: {sorted(exact_matches)}")

unmatched = [target_skills_lower[s] for s in target_skills_lower.keys() if s not in exact_matches]
print(f"\nUnmatched (need semantic check): {len(unmatched)}")
print(f"Skills: {unmatched}")

print(f"\nMatch percentage: {len(exact_matches) / len(target_skills) * 100:.1f}%")
