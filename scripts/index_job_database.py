"""
Indexing Script - Index job descriptions into Qdrant vector database
Run this once after adding the job_dataset.json file
"""
import sys
from pathlib import Path

# Add parent directory to Python path so we can import from app
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

import json
import pandas as pd
from app.services.embedder import EmbeddingService
from app.services.vector_db import VectorDBService
from app.services.job_database import JobDatabaseService
from qdrant_client.http import models
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def index_job_skills():
    """
    One-time indexing of all skills from job descriptions database
    into persistent Qdrant vector storage
    """
    logger.info("="*80)
    logger.info("Starting Job Skills Indexing")
    logger.info("="*80)
    
    # Load services
    job_db = JobDatabaseService()
    embedder = EmbeddingService()
    vector_db = VectorDBService(collection_name="job_skills_library")
    
    if not job_db.is_available():
        logger.error("Job database not found! Please add data/job_dataset.json")
        return
    
    # Initialize collection
    logger.info(f"Creating collection with {embedder.get_dimension()}D vectors")
    vector_db.init_collection(embedder.get_dimension())
    
    # Prepare all skills for indexing
    all_points = []
    skill_index = 0
    
    df = job_db.df
    logger.info(f"Processing {len(df)} job descriptions...")
    
    for idx, row in df.iterrows():
        job_id = row['JobID']
        title = row['Title']
        experience = row['ExperienceLevel']
        
        # Parse skills
        skills = job_db._parse_field(row.get('Skills', []))
        
        if not skills:
            continue
        
        # Process each skill
        for skill in skills:
            if not skill or len(skill.strip()) == 0:
                continue
            
            try:
                # Generate embedding
                embedding = embedder.encode([skill])[0]
                
                all_points.append({
                    "id": skill_index,
                    "vector": embedding,
                    "payload": {
                        "skill": skill,
                        "role": title,
                        "experience_level": experience,
                        "job_id": job_id,
                        "source": "database"
                    }
                })
                
                skill_index += 1
                
                # Progress update every 100 skills
                if skill_index % 100 == 0:
                    logger.info(f"Processed {skill_index} skills...")
                    
            except Exception as e:
                logger.warning(f"Failed to embed skill '{skill}': {e}")
                continue
    
    logger.info(f"Total skills to index: {len(all_points)}")
    
    # Batch upsert (efficient)
    logger.info("Upserting to Qdrant...")
    batch_size = 100
    
    for i in range(0, len(all_points), batch_size):
        batch = all_points[i:i+batch_size]
        
        vector_db.client.upsert(
            collection_name="job_skills_library",
            points=[
                models.PointStruct(
                    id=p["id"],
                    vector=p["vector"],
                    payload=p["payload"]
                )
                for p in batch
            ]
        )
        
        logger.info(f"Indexed {min(i+batch_size, len(all_points))}/{len(all_points)} skills")
    
    logger.info("="*80)
    logger.info(f"✓ Successfully indexed {len(all_points)} skills from {len(df)} job descriptions")
    logger.info(f"Collection: job_skills_library")
    logger.info(f"Storage: ./qdrant_data/")
    logger.info("="*80)
    
    # Verify indexing
    logger.info("Verifying index...")
    test_query = "Python programming"
    test_embedding = embedder.encode([test_query])[0]
    
    results = vector_db.search(test_embedding, limit=5)
    logger.info(f"Test query '{test_query}' returned {len(results)} results:")
    for i, result in enumerate(results[:3], 1):
        logger.info(f"  {i}. {result['payload']['skill']} (role: {result['payload']['role']}, score: {result['score']:.3f})")
    
    logger.info("\n✓ Indexing complete! The vector database is ready to use.")

if __name__ == "__main__":
    index_job_skills()
