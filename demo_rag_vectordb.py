"""
Live Demonstration: Vector Database & RAG in Skill Gap Analyzer
================================================================

This script demonstrates how the vector database and RAG (Retrieval Augmented Generation)
work in the Skill Gap Analyzer project with real examples.
"""

from app.services.embedder import EmbeddingService
from app.services.vector_db import VectorDBService
from qdrant_client.http import models
import numpy as np

def print_section(title: str):
    """Pretty print section headers"""
    print("\n" + "="*80)
    print(f"🎯 {title}")
    print("="*80)

def print_step(step_num: int, description: str):
    """Pretty print step headers"""
    print(f"\n{'─'*80}")
    print(f"📍 STEP {step_num}: {description}")
    print(f"{'─'*80}")

def demonstrate_embeddings():
    """Demonstrate how text is converted to embeddings"""
    print_section("PART 1: Understanding Embeddings (Text → Numbers)")
    
    embedder = EmbeddingService()
    
    # Example texts
    texts = [
        "Python programming",
        "Python development",
        "JavaScript coding",
        "React framework",
    ]
    
    print(f"\n📝 Converting these texts to embeddings:")
    for i, text in enumerate(texts, 1):
        print(f"   {i}. '{text}'")
    
    # Generate embeddings
    embeddings = embedder.encode(texts)
    
    print(f"\n✨ Embedding Properties:")
    print(f"   • Dimension: {embedder.get_dimension()}D vectors")
    print(f"   • Total embeddings: {len(embeddings)}")
    print(f"\n📊 Sample embedding (first 10 values of '{texts[0]}'):")
    print(f"   {embeddings[0][:10]}")
    
    # Calculate similarity between texts
    print(f"\n🔍 Cosine Similarity Matrix:")
    print(f"   (1.0 = identical, 0.0 = completely different)\n")
    
    # Print header
    print("   " + " "*20, end="")
    for text in texts:
        print(f"{text[:15]:>17}", end="")
    print()
    
    # Calculate and print similarities
    for i, text1 in enumerate(texts):
        print(f"   {text1[:20]:20}", end="")
        for j, text2 in enumerate(texts):
            emb1 = np.array(embeddings[i])
            emb2 = np.array(embeddings[j])
            # Cosine similarity
            similarity = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
            print(f"{similarity:17.4f}", end="")
        print()
    
    print(f"\n💡 Key Insight:")
    print(f"   'Python programming' vs 'Python development' = HIGH similarity (same concept)")
    print(f"   'Python programming' vs 'React framework' = LOW similarity (different concepts)")
    
    return embedder

def demonstrate_vector_db(embedder: EmbeddingService):
    """Demonstrate vector database storage and search"""
    print_section("PART 2: Vector Database Storage & Search")
    
    # Initialize vector DB
    vector_db = VectorDBService(collection_name="demo_resume")
    vector_db.init_collection(embedder.get_dimension())
    
    print_step(1, "Storing Resume Skills in Vector Database")
    
    # Simulate resume content
    resume_skills = [
        "5 years of Python development experience",
        "Built REST APIs using FastAPI and Flask",
        "Experience with React and Vue.js frontend",
        "Docker containerization and deployment",
        "SQL databases including PostgreSQL",
        "Git version control and CI/CD pipelines",
    ]
    
    print("\n📄 Resume Content Being Indexed:")
    for i, skill in enumerate(resume_skills, 1):
        print(f"   {i}. {skill}")
    
    # Embed and store
    resume_embeddings = embedder.encode(resume_skills)
    
    # Upsert into Qdrant
    vector_db.client.upsert(
        collection_name="demo_resume",
        points=[
            models.PointStruct(
                id=i,
                vector=emb,
                payload={"text": text, "type": "resume_skill"}
            )
            for i, (emb, text) in enumerate(zip(resume_embeddings, resume_skills))
        ]
    )
    
    print(f"\n✅ Stored {len(resume_skills)} skills in Qdrant vector database")
    
    return vector_db, resume_skills

def demonstrate_rag_retrieval(embedder: EmbeddingService, vector_db: VectorDBService):
    """Demonstrate RAG: Retrieval for skill matching"""
    print_section("PART 3: RAG - Retrieval Augmented Generation")
    
    print_step(2, "Job Requirements → Semantic Search")
    
    # Job requirements
    job_requirements = [
        "Python expertise required",           # Should MATCH
        "Kubernetes deployment experience",    # Should be MISSING
        "RESTful API development",             # Should MATCH
        "Machine Learning with TensorFlow",    # Should be MISSING
        "Frontend development skills",         # Should MATCH
    ]
    
    print("\n📋 Job Requirements to Check:")
    for i, req in enumerate(job_requirements, 1):
        print(f"   {i}. {req}")
    
    # Embed job requirements
    jd_embeddings = embedder.encode(job_requirements)
    
    print(f"\n🔍 Searching for matches in resume...")
    print(f"\n{'Requirement':<35} {'Match Score':<12} {'Status':<10} Resume Match")
    print("─" * 110)
    
    THRESHOLD = 0.5  # Same as in analyzer.py
    
    missing_skills = []
    covered_skills = []
    
    for req, jd_emb in zip(job_requirements, jd_embeddings):
        # Search in vector DB
        results = vector_db.search(jd_emb, limit=1)
        
        if results:
            best_match = results[0]
            score = best_match['score']
            matched_text = best_match['payload']['text']
            
            # Determine if skill is covered or missing
            if score >= THRESHOLD:
                status = "✅ COVERED"
                covered_skills.append(req)
            else:
                status = "❌ MISSING"
                missing_skills.append(req)
            
            print(f"{req:<35} {score:<12.4f} {status:<10} {matched_text[:50]}")
        else:
            print(f"{req:<35} {'0.0000':<12} {'❌ MISSING':<10} No match found")
            missing_skills.append(req)
    
    print(f"\n📊 Analysis Summary:")
    print(f"   • Total Requirements: {len(job_requirements)}")
    print(f"   • Covered Skills: {len(covered_skills)} ({len(covered_skills)/len(job_requirements)*100:.1f}%)")
    print(f"   • Missing Skills: {len(missing_skills)} ({len(missing_skills)/len(job_requirements)*100:.1f}%)")
    
    print(f"\n❌ Skills Gap Identified:")
    for i, skill in enumerate(missing_skills, 1):
        print(f"   {i}. {skill}")
    
    return missing_skills

def demonstrate_threshold_impact(embedder: EmbeddingService, vector_db: VectorDBService):
    """Show how threshold affects gap detection"""
    print_section("PART 4: Threshold Impact on Gap Detection")
    
    requirement = "API development experience"
    req_embedding = embedder.encode([requirement])[0]
    
    print(f"\n🎯 Testing Requirement: '{requirement}'")
    print(f"\n📊 How different thresholds affect gap detection:\n")
    
    # Search
    results = vector_db.search(req_embedding, limit=3)
    
    print(f"{'Threshold':<12} {'Decision':<15} Best Match (Score)")
    print("─" * 80)
    
    if results:
        best_score = results[0]['score']
        best_match = results[0]['payload']['text']
        
        for threshold in [0.3, 0.5, 0.7, 0.9]:
            if best_score >= threshold:
                decision = "✅ COVERED"
            else:
                decision = "❌ MISSING"
            
            print(f"{threshold:<12} {decision:<15} {best_match[:40]} ({best_score:.4f})")
    
    print(f"\n💡 Key Insight:")
    print(f"   • Lower threshold (0.3) = More lenient (fewer gaps detected)")
    print(f"   • Higher threshold (0.9) = More strict (more gaps detected)")
    print(f"   • Current system uses: 0.5 (balanced approach)")

def demonstrate_semantic_understanding():
    """Show semantic understanding capabilities"""
    print_section("PART 5: Semantic Understanding - Why This Beats Keyword Matching")
    
    embedder = EmbeddingService()
    
    test_cases = [
        {
            "resume": "Experienced in building RESTful web services with FastAPI",
            "requirement": "REST API development",
            "should_match": True
        },
        {
            "resume": "Proficient in React.js and Next.js for frontend",
            "requirement": "React development experience",
            "should_match": True
        },
        {
            "resume": "Used Docker for containerization",
            "requirement": "Experience with Kubernetes orchestration",
            "should_match": False  # Similar but not same
        },
        {
            "resume": "SQL database design with PostgreSQL",
            "requirement": "Machine learning expertise",
            "should_match": False
        }
    ]
    
    print(f"\n🧠 Testing Semantic Understanding:\n")
    
    for i, test in enumerate(test_cases, 1):
        resume_emb = embedder.encode([test['resume']])[0]
        req_emb = embedder.encode([test['requirement']])[0]
        
        # Calculate cosine similarity
        resume_vec = np.array(resume_emb)
        req_vec = np.array(req_emb)
        similarity = np.dot(resume_vec, req_vec) / (np.linalg.norm(resume_vec) * np.linalg.norm(req_vec))
        
        print(f"Test Case {i}:")
        print(f"   Resume: '{test['resume']}'")
        print(f"   Requirement: '{test['requirement']}'")
        print(f"   Similarity Score: {similarity:.4f}")
        print(f"   Expected: {'Should MATCH' if test['should_match'] else 'Should NOT match'}")
        
        threshold = 0.5
        actual_match = similarity >= threshold
        expected_match = test['should_match']
        
        if actual_match == expected_match:
            print(f"   Result: ✅ CORRECT - {'Matched' if actual_match else 'Not matched'}")
        else:
            print(f"   Result: ⚠️ UNEXPECTED - {'Matched' if actual_match else 'Not matched'}")
        
        print()

def main():
    """Run the complete demonstration"""
    print("\n" + "🚀" * 40)
    print("  LIVE DEMONSTRATION: Vector DB & RAG in Skill Gap Analyzer")
    print("🚀" * 40)
    
    print("""
This demonstration will show you:
1. How text is converted to embeddings (numerical vectors)
2. How embeddings are stored in Qdrant vector database
3. How semantic search retrieves relevant skills (RAG retrieval)
4. How threshold affects gap detection
5. Why semantic matching beats keyword search
    """)
    
    input("Press Enter to start the demonstration...")
    
    # Part 1: Embeddings
    embedder = demonstrate_embeddings()
    input("\n\nPress Enter to continue to Vector Database demonstration...")
    
    # Part 2: Vector DB
    vector_db, resume_skills = demonstrate_vector_db(embedder)
    input("\n\nPress Enter to continue to RAG Retrieval demonstration...")
    
    # Part 3: RAG Retrieval
    missing_skills = demonstrate_rag_retrieval(embedder, vector_db)
    input("\n\nPress Enter to see Threshold Impact...")
    
    # Part 4: Threshold Impact
    demonstrate_threshold_impact(embedder, vector_db)
    input("\n\nPress Enter to see Semantic Understanding examples...")
    
    # Part 5: Semantic Understanding
    demonstrate_semantic_understanding()
    
    print_section("🎉 Demonstration Complete!")
    print("""
Key Takeaways:
1. ✅ Embeddings convert text into 384-dimensional vectors that capture semantic meaning
2. ✅ Qdrant stores these vectors and enables fast similarity search using cosine distance
3. ✅ RAG retrieval finds the most relevant resume content for each job requirement
4. ✅ Threshold (0.5) determines whether a skill is covered or missing
5. ✅ Semantic matching finds skills even when worded differently (unlike keyword search)

This is exactly how your Skill Gap Analyzer works! 🚀
    """)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Demonstration interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
