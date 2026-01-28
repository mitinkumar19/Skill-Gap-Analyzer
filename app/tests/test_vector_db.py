import pytest
from unittest.mock import MagicMock, patch
from qdrant_client.http import models
from app.services.vector_db import VectorDBService

@pytest.fixture
def mock_qdrant_client():
    with patch("app.services.vector_db.QdrantClient") as mock:
        yield mock

def test_init_collection(mock_qdrant_client):
    service = VectorDBService()
    # Mock get_collections to return empty list
    service.client.get_collections.return_value.collections = []
    
    service.init_collection(384)
    service.client.create_collection.assert_called_once()

def test_upsert(mock_qdrant_client):
    service = VectorDBService()
    service.upsert("id1", [0.1, 0.2], {"meta": "data"})
    
    service.client.upsert.assert_called_once()
    call_args = service.client.upsert.call_args
    assert call_args.kwargs['collection_name'] == "skills_jobs"
    points = call_args.kwargs['points']
    assert len(points) == 1
    # Check if PointStruct is used (or just check attributes if it's a mock)
    # Since we use models.PointStruct in the real code, we expect it to be passed.

def test_search_uses_query_points(mock_qdrant_client):
    service = VectorDBService()
    
    # Mock query_points response
    mock_point = MagicMock()
    mock_point.id = 1
    mock_point.score = 0.9
    mock_point.payload = {"text": "skill"}
    
    mock_response = MagicMock()
    mock_response.points = [mock_point]
    
    service.client.query_points.return_value = mock_response
    
    results = service.search([0.1, 0.1])
    
    service.client.query_points.assert_called_once()
    assert len(results) == 1
    assert results[0]['id'] == 1
    assert results[0]['score'] == 0.9
