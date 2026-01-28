import time
from app.services.generator import GeneratorService

def test_latency():
    service = GeneratorService()
    role = "Data Scientist"
    print(f"Testing generation for: {role}")
    
    start = time.time()
    try:
        result = service.generate_job_description(role)
        duration = time.time() - start
        print(f"Success! Time taken: {duration:.2f} seconds")
        print(f"Preview: {result[:100]}...")
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    test_latency()
