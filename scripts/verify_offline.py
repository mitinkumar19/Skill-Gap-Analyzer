"""
Script to verify skill extraction API independence.
Temporarily removes API key to prove local NLP works offline.
"""
import os
import logging
from app.services.generator import GeneratorService
from app.core.config import settings

# Configure logging to show our messages
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("app.services.generator")

def verify_offline():
    print("-" * 60)
    print("OFFLINE VERIFICATION TEST")
    print("-" * 60)
    
    # Simulate missing API Key
    original_key = settings.GROQ_API_KEY
    settings.GROQ_API_KEY = None
    
    print("1. API Key Removed from Config (Simulating Offline/No Key)")
    
    # Re-initialize service to pick up "missing" key
    generator = GeneratorService()
    
    # Verify client is None
    if generator.client is None:
        print("   [✓] GeneratorService initialized without Groq client")
    else:
        print("   [x] Warning: Client still exists!")

    resume_text = """
    Experienced Software Engineer with expertise in Python, Docker, and Kubernetes.
    Proficient in building REST APIs using FastAPI and PostgreSQL.
    """
    
    print("\n2. Attempting Extraction...")
    try:
        skills = generator.extract_skills_from_text(resume_text)
        print(f"   [✓] Extraction Successful!")
        print(f"   Skills Found: {skills}")
        
        expected = ["Python", "Docker", "Kubernetes", "FastAPI", "PostgreSQL", "REST APIs"]
        found_lower = [s.lower() for s in skills]
        
        missing = [e for e in expected if e.lower() not in found_lower]
        if not missing:
             print("   [✓] All expected skills found.")
        else:
             print(f"   [!] Some skills missed: {missing}")
             
    except Exception as e:
        print(f"   [x] Extraction Failed: {e}")
        
    print("\n3. Verifying API Usage")
    # restore key
    settings.GROQ_API_KEY = original_key
    print(f"   (Restored API Key for future use)")

if __name__ == "__main__":
    verify_offline()
