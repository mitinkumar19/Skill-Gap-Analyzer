"""
RAG Verifier Service - AI-powered skill verification for borderline cases
"""
from app.services.generator import GeneratorService
import json
import logging
from typing import Dict, List

logger = logging.getLogger(__name__)

class RAGVerifier:
    def __init__(self, generator: GeneratorService):
        self.generator = generator
    
    def verify_skill(
        self, 
        required_skill: str, 
        resume_context: str,
        similarity_score: float
    ) -> Dict:
        """
        Verify if resume demonstrates required skill using AI.
        
        Args:
            required_skill: The skill to verify
            resume_context: Relevant resume text (from vector search)
            similarity_score: Cosine similarity score for context
            
        Returns:
            {
                "decision": "COVERED" | "MISSING" | "PARTIAL",
                "confidence": 0.0-1.0,
                "reasoning": "explanation",
                "evidence": "quote from resume" | None
            }
        """
        if not self.generator.client:
            # Fallback to threshold if AI unavailable
            logger.warning("AI not available, using threshold fallback")
            return self._threshold_fallback(similarity_score)
        
        prompt = f"""You are an expert technical recruiter analyzing resume-job fit.

Required Skill: {required_skill}

Resume Evidence (Similarity Score: {similarity_score:.2f}):
{resume_context}

Task: Determine if the resume demonstrates this required skill.

Consider:
1. Does the candidate have hands-on experience with this skill?
2. Is the skill mentioned directly or through equivalent terms?
3. Is the experience level sufficient (not just hobby/tutorial use)?
4. Are similar but DIFFERENT skills being confused? Examples:
   - Docker ≠ Kubernetes (both containers, different purposes)
   - AWS ≠ Azure (both cloud, different platforms)
   - REST ≠ GraphQL (both APIs, different protocols)
   - React ≠ Angular (both frameworks, different libraries)

Respond ONLY with valid JSON (no markdown, no extra text):
{{
    "decision": "COVERED",
    "confidence": 0.85,
    "reasoning": "Brief 1-2 sentence explanation",
    "evidence": "Direct quote from resume if COVERED, null otherwise"
}}

Decision must be either "COVERED" or "MISSING" (no PARTIAL).
"""
        
        try:
            response = self.generator.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
                temperature=0.3,  # Lower for consistent decisions
                response_format={"type": "json_object"}
            )
            
            content = response.choices[0].message.content
            result = json.loads(content)
            
            # Validate response
            if "decision" not in result:
                logger.error("Invalid AI response - missing decision field")
                return self._threshold_fallback(similarity_score)
            
            # Normalize decision
            result["decision"] = result["decision"].upper()
            if result["decision"] not in ["COVERED", "MISSING", "PARTIAL"]:
                logger.warning(f"Unexpected decision: {result['decision']}, defaulting to threshold")
                return self._threshold_fallback(similarity_score)
            
            # Ensure confidence is present
            if "confidence" not in result:
                result["confidence"] = 0.7
            
            # Ensure reasoning is present
            if "reasoning" not in result:
                result["reasoning"] = "AI verification completed"
            
            logger.info(f"✓ RAG verified '{required_skill}': {result['decision']} (confidence: {result['confidence']:.2f})")
            return result
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse AI response as JSON: {e}")
            return self._threshold_fallback(similarity_score)
        except Exception as e:
            logger.error(f"RAG verification failed: {e}")
            return self._threshold_fallback(similarity_score)
    
    def _threshold_fallback(self, score: float) -> Dict:
        """Fallback to threshold-based decision if AI fails"""
        threshold = 0.5
        decision = "COVERED" if score >= threshold else "MISSING"
        
        # Calculate confidence based on distance from threshold
        distance_from_threshold = abs(score - threshold)
        confidence = min(distance_from_threshold * 2, 1.0)
        
        return {
            "decision": decision,
            "confidence": round(confidence, 2),
            "reasoning": f"Threshold-based decision (score: {score:.2f}, threshold: {threshold})",
            "evidence": None
        }
    
    def batch_verify(
        self, 
        skills: List[str], 
        contexts: List[str],
        scores: List[float]
    ) -> List[Dict]:
        """
        Batch verify multiple skills.
        
        Note: Currently processes sequentially. Could be optimized with async calls.
        """
        results = []
        for skill, context, score in zip(skills, contexts, scores):
            result = self.verify_skill(skill, context, score)
            results.append(result)
        
        return results
