import sys
from unittest.mock import MagicMock

# Mock sentence-transformers before import
sys.modules["sentence_transformers"] = MagicMock()

import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app
from app.services.generator import GeneratorService

client = TestClient(app)

@pytest.fixture
def mock_groq():
    with patch("app.services.generator.Groq") as mock:
        yield mock

def test_generate_skills_list(mock_groq):
    service = GeneratorService()
    
    # Mock LLM response with JSON
    mock_completion = MagicMock()
    mock_completion.choices[0].message.content = '["Python", "SQL"]'
    service.client.chat.completions.create.return_value = mock_completion
    
    result = service.generate_skills_list("Data Engineer", "Senior")
    assert result == ["Python", "SQL"]
    
def test_generate_skills_api(mock_groq):
    with patch("app.main.analyzer.generator.generate_skills_list") as mock_gen:
        mock_gen.return_value = ["Skill A", "Skill B"]
        
        response = client.post("/api/v1/generate-skills", json={"role": "Tester", "experience_level": "Mid-Level"})
        
        assert response.status_code == 200
        assert response.json() == {"skills": ["Skill A", "Skill B"]}
