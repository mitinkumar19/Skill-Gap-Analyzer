"""
Script to compare Local NLP extraction vs Groq API extraction.
Measures latency and skill overlap.
"""
import time
import logging
import asyncio
from app.services.generator import GeneratorService
from app.services.skill_extractor import SkillExtractor

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

SAMPLE_RESUME = """
John Doe
Senior Full Stack Engineer

Summary
Passionate developer with 6+ years of experience building scalable web applications.
Expertise in Python ecosystem and modern JavaScript frameworks.

Technical Skills
Languages: Python, JavaScript, TypeScript, Go, SQL, HTML/CSS
Backend: FastAPI, Django, Node.js, Express.js
Frontend: React, Next.js, Redux, Tailwind CSS
Database: PostgreSQL, MongoDB, Redis
DevOps: Docker, Kubernetes, AWS (EC2, S3, RDS), Git, CI/CD
Tools: Jira, Slack, VS Code, Postman

Experience
Senior Software Engineer | TechFlow Inc. | 2021 - Present
- Architected and built microservices using FastAPI and Docker
- Migrated legacy monolith to Kubernetes cluster on AWS
- Developed interactive dashboards using React and Recharts
- Optimized database queries in PostgreSQL, reducing load by 40%

Software Engineer | CodeWorks LLC | 2018 - 2021
- Built RESTful APIs using Django Rest Framework
- Implemented frontend features using Vue.js and Vuex
- Collaborated with design team to implement responsive UI
"""

def compare_extraction():
    print("-" * 60)
    print("SKILL EXTRACTION SHOWDOWN: Local NLP vs Groq API")
    print("-" * 60)
    
    generator = GeneratorService()
    
    # 1. Local NLP Extraction
    print("\n1. Running Local NLP Extraction...")
    start_time = time.time()
    local_skills = generator.extract_skills_from_text(SAMPLE_RESUME, use_api=False)
    local_duration = (time.time() - start_time) * 1000
    
    print(f"   Time: {local_duration:.2f} ms")
    print(f"   Skills Found: {len(local_skills)}")
    print(f"   Sample: {local_skills[:10]}...")

    # 2. Groq API Extraction (if key available)
    print("\n2. Running Groq API Extraction...")
    if not generator.client:
        print("   Skipping: No API Key found.")
        api_skills = []
        api_duration = 0
    else:
        try:
            start_time = time.time()
            api_skills = generator.extract_skills_from_text(SAMPLE_RESUME, use_api=True)
            api_duration = (time.time() - start_time) * 1000
            
            print(f"   Time: {api_duration:.2f} ms")
            print(f"   Skills Found: {len(api_skills)}")
            print(f"   Sample: {api_skills[:10]}...")
        except Exception as e:
            print(f"   Failed: {e}")
            api_skills = []
            api_duration = 0

    # 3. Comparison
    print("\n" + "-" * 60)
    print("RESULTS")
    print("-" * 60)
    
    if api_skills:
        speedup = api_duration / local_duration if local_duration > 0 else 0
        print(f"Speedup: Local is {speedup:.1f}x faster")
        
        local_set = set(s.lower() for s in local_skills)
        api_set = set(s.lower() for s in api_skills)
        
        overlap = local_set.intersection(api_set)
        only_local = local_set - api_set
        only_api = api_set - local_set
        
        print(f"\nAgreement: {len(overlap)} skills matching")
        
        if only_local:
            print(f"\nFound ONLY by Local ({len(only_local)}):")
            print(f"{', '.join(sorted(list(only_local)))}")
            
        if only_api:
            print(f"\nFound ONLY by API ({len(only_api)}):")
            print(f"{', '.join(sorted(list(only_api)))}")
    else:
        print("Could not compare (API extraction failed or skipped)")

if __name__ == "__main__":
    compare_extraction()
