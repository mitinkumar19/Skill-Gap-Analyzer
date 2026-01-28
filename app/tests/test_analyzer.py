import pytest
from unittest.mock import MagicMock, patch
from app.services.analyzer import GapAnalyzer
from qdrant_client.http import models

@pytest.fixture
def mock_services():
    with patch("app.services.analyzer.EmbeddingService") as mock_embedder, \
         patch("app.services.analyzer.VectorDBService") as mock_vdb, \
         patch("app.services.analyzer.GeneratorService") as mock_gen, \
         patch("app.services.analyzer.ParsingService") as mock_parser:
        
        # Setup common mock behaviors
        mock_embedder.return_value.encode.return_value = [[0.1]*384]
        mock_embedder.return_value.get_dimension.return_value = 384
        
        mock_parser.extract_text_from_pdf.return_value = "Resume content line.\nAnother line."
        
        mock_vdb_instance = mock_vdb.return_value
        mock_vdb_instance.search.return_value = [{"id": 1, "score": 0.9, "payload": {"text": "match"}}]
        
        yield mock_embedder, mock_vdb, mock_gen, mock_parser

def test_analyze_flow(mock_services):
    mock_embedder, mock_vdb, mock_gen, mock_parser = mock_services
    
    analyzer = GapAnalyzer()
    
    # Run analyze
    result = analyzer.analyze(b"pdf_bytes", "Job Description\nRequirement line.")
    
    # Verify upsert used PointStruct
    # analyzer.py accesses self.vector_db.client.upsert directly
    upsert_call = analyzer.vector_db.client.upsert.call_args
    assert upsert_call is not None
    
    points = upsert_call.kwargs['points']
    assert len(points) > 0
    # Check if the first point is likely a PointStruct (has .id attribute or is instance)
    first_point = points[0]
    
    # In the fix, we wrap it in models.PointStruct
    assert isinstance(first_point, models.PointStruct) 
    assert first_point.id == 0

    # Check result structure
    assert "match_percentage" in result
    assert "missing_skills" in result
