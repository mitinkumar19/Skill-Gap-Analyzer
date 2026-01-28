"""
Test script to verify database-first skill generation
"""
import sys
from pathlib import Path

# Add parent directory to Python path
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from app.services.analyzer import GapAnalyzer

def test_skill_generation():
    print("="*80)
    print("Testing Database-First Skill Generation")
    print("="*80)
    
    analyzer = GapAnalyzer()
    
    test_roles = [
        ("Backend Developer", "Mid-Level"),
        ("Frontend Developer", "Senior"),
        ("Data Scientist", "Junior"),
        ("DevOps Engineer", "Experienced"),
    ]
    
    for role, level in test_roles:
        print(f"\n📋 Testing: {role} ({level})")
        print("-" * 80)
        
        skills = analyzer.get_required_skills(role, level)
        
        print(f"✓ Retrieved {len(skills)} skills")
        print(f"Top 10 skills: {skills[:10]}")
    
    print("\n" + "="*80)
    print("✓ Database-first skill generation test complete!")
    print("="*80)

if __name__ == "__main__":
    test_skill_generation()
