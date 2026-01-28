from app.services.embedder import EmbeddingService
from app.services.vector_db import VectorDBService
from app.services.generator import GeneratorService
from app.services.parser import ParsingService
from app.services.job_database import JobDatabaseService
from app.services.rag_verifier import RAGVerifier
import logging
from qdrant_client.http import models
from typing import List, Dict

logger = logging.getLogger(__name__)

class GapAnalyzer:
    # Hybrid RAG thresholds
    CLEAR_MATCH_THRESHOLD = 0.7  # High confidence match - fast path
    CLEAR_MISS_THRESHOLD = 0.3   # High confidence miss - fast path
    # Between 0.3-0.7 = borderline, needs AI verification
    
    def __init__(self):
        self.embedder = EmbeddingService()
        self.vector_db = VectorDBService()  # Now uses persistent storage
        self.generator = GeneratorService()
        self.job_db = JobDatabaseService()
        self.rag_verifier = RAGVerifier(self.generator)
        
        # Initialize DB with correct dim
        self.vector_db.init_collection(self.embedder.get_dimension())
        
        logger.info(f"GapAnalyzer initialized with hybrid RAG (thresholds: {self.CLEAR_MATCH_THRESHOLD}/{self.CLEAR_MISS_THRESHOLD})")
        logger.info(f"Job database available: {self.job_db.is_available()}")
    
    def get_required_skills(self, role: str, experience_level: str = "Mid-Level") -> List[str]:
        """
        Get required skills for a role - database first, AI fallback
        
        Args:
            role: Job title (e.g., "Backend Developer")
            experience_level: Experience level (Fresher, Junior, Mid-Level, Senior, Lead)
        
        Returns:
            List of required skills
        """
        # Try database first
        if self.job_db.is_available():
            db_skills = self.job_db.get_skills_for_role(role, experience_level)
            
            if db_skills and len(db_skills) >= 10:
                # Use the filtered skills directly (respects experience level)
                # Limit to top 30 for consistency
                top_skills = db_skills[:30]
                
                logger.info(f"✓ Using {len(top_skills)} skills from database for '{role}' ({experience_level}) (FREE, instant)")
                return top_skills
            else:
                logger.info(f"Database has insufficient skills for '{role}' ({len(db_skills)} found), falling back to AI")
        else:
            logger.warning("Job database not available, using AI generation")
        
        # Fallback to AI generation
        logger.info(f"Generating skills with AI for '{role}'")
        return self.generator.generate_skills_list(role, experience_level)


    def analyze(self, resume_file_bytes: bytes, job_description: str = None, skills_list: list[str] = None, is_text: bool = False) -> dict:
        """
        Orchestrate the full analysis pipeline.
        
        Args:
            resume_file_bytes: PDF bytes or UTF-8 text (if is_text=True)
            job_description: Optional job description
            skills_list: List of required skills
            is_text: If True, treat resume_file_bytes as text not PDF
        """
        # 1. Parse Resume
        if is_text:
            resume_text = resume_file_bytes.decode('utf-8')
        else:
            resume_text = ParsingService.extract_text_from_pdf(resume_file_bytes)
        
        # Split into chunks - preserve ALL lines for skill matching (don't filter by length!)
        resume_chunks = [line.strip() for line in resume_text.split('\n') if line.strip()]
        
        # 2. Determine Requirements (JD Text vs Skills List)
        jd_chunks = []
        if skills_list and len(skills_list) > 0:
            jd_chunks = skills_list
        elif job_description:
            jd_chunks = [line for line in job_description.split('\n') if len(line) > 10]
        
        # 3. Embed JD chunks to find "Requirements"
        jd_embeddings = self.embedder.encode(jd_chunks)
        
        # 4. Embed Resume chunks
        resume_embeddings = self.embedder.encode(resume_chunks)
        
        # 5. Hybrid RAG Analysis
        # Three-tier approach:
        # 1. Score >= 0.7: Clear match (fast path)
        # 2. Score <= 0.3: Clear miss (fast path)
        # 3. 0.3 < score < 0.7: Borderline (AI verification)
        
        missing_skills = []
        covered_skills = []
        borderline_cases = []
        
        # We index Resume chunks into a temporary collection logic or just manual cosine calc
        # Since VectorDBService is set up for generic storage, let's use manual calc for this request scope
        # Or: Index resume into Vector DB? 
        # Better: Index RESUME chunks. Query with JD chunks.
        
        batch_points = [
            {"id": i, "vector": emb, "payload": {"text": txt}} 
            for i, (emb, txt) in enumerate(zip(resume_embeddings, resume_chunks))
        ]
        
        # Ensure ID format for Qdrant - integer is fine.
        # We need to clear/init a session-specific collection ideally. 
        # For MVP: "resume_session" collection.
        self.vector_db.collection_name = "current_analysis_resume"
        self.vector_db.init_collection(self.embedder.get_dimension())
        
        # Upsert all resume points
        # Qdrant client upsert expects specific format. 
        self.vector_db.client.upsert(
            collection_name="current_analysis_resume",
            points=[
                models.PointStruct(
                    id=p["id"], 
                    vector=p["vector"], 
                    payload=p["payload"]
                )
                for p in batch_points
            ]
        )
        
        # Query for each JD chunk with hybrid decision logic
        for jd_text, jd_emb in zip(jd_chunks, jd_embeddings):
            results = self.vector_db.search(jd_emb, limit=1)
            best_score = results[0]['score'] if results else 0
            context = results[0]['payload']['text'] if results else ""
            
            if best_score >= self.CLEAR_MATCH_THRESHOLD:
                # Path 1: Clear match - fast decision
                covered_skills.append({
                    "skill": jd_text,
                    "score": best_score,
                    "match": context,
                    "confidence": min((best_score - 0.7) / 0.3, 1.0),
                    "reasoning": "Strong similarity match",
                    "verification_method": "threshold"
                })
                
            elif best_score <= self.CLEAR_MISS_THRESHOLD:
                # Path 2: Clear miss - fast decision
                missing_skills.append({
                    "skill": jd_text,
                    "score": best_score,
                    "confidence": min((0.3 - best_score) / 0.3, 1.0),
                    "reasoning": "Low similarity, skill not found in resume",
                    "verification_method": "threshold"
                })
                
            else:
                # Path 3: Borderline - needs AI verification
                borderline_cases.append((jd_text, context, best_score))
        
        # Batch verify borderline cases with AI
        if borderline_cases:
            logger.info(f"Verifying {len(borderline_cases)} borderline skills with hybrid RAG")
            
            for skill, context, score in borderline_cases:
                verification = self.rag_verifier.verify_skill(skill, context, score)
                
                skill_result = {
                    "skill": skill,
                    "score": score,
                    "confidence": verification["confidence"],
                    "reasoning": verification["reasoning"],
                    "verification_method": "rag"
                }
                
                if verification["decision"] == "COVERED":
                    skill_result["match"] = verification.get("evidence") or context
                    covered_skills.append(skill_result)
                else:
                    missing_skills.append(skill_result)
        
        # 6. Generate Roadmap
        # Consolidate missing skills text
        missing_text_list = [m['skill'] for m in missing_skills[:5]] # Top 5 missing
        roadmap = self.generator.generate_roadmap(missing_text_list, "Target Role")
        
        # Calculate verification stats
        total_skills = len(jd_chunks)
        verification_stats = {
            "total_skills": total_skills,
            "clear_matches": sum(1 for s in covered_skills if s.get("verification_method") == "threshold"),
            "clear_misses": sum(1 for s in missing_skills if s.get("verification_method") == "threshold"),
            "ai_verified": len(borderline_cases),
            "fast_path_percentage": round((total_skills - len(borderline_cases)) / total_skills * 100, 1) if total_skills > 0 else 0
        }
        
        logger.info(f"Analysis complete: {len(covered_skills)} covered, {len(missing_skills)} missing")
        logger.info(f"Hybrid RAG stats: {verification_stats['fast_path_percentage']}% fast path, {len(borderline_cases)} AI verified")
        
        return {
            "match_percentage": round(len(covered_skills) / total_skills * 100, 1) if total_skills > 0 else 0,
            "missing_skills": missing_skills,
            "covered_skills": covered_skills,
            "roadmap": roadmap,
            "verification_stats": verification_stats
        }
