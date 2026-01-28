
import pytest
from unittest.mock import MagicMock, patch
import sys

# Mock modules that might cause import errors or heavy loading
sys.modules["sentence_transformers"] = MagicMock()
sys.modules["qdrant_client"] = MagicMock()
sys.modules["app.services.embedder"] = MagicMock()
sys.modules["app.services.vector_db"] = MagicMock()
sys.modules["app.services.parser"] = MagicMock()

# Now import the service under test
# We might need to mock config if it's used at import time
with patch.dict("os.environ", {"GROQ_API_KEY": "fake-key"}):
    from app.services.generator import GeneratorService

@pytest.fixture
def mock_groq():
    with patch("app.services.generator.Groq") as mock:
        yield mock

def test_generate_skills_list_structure(mock_groq):
    """Test that the service correctly formats the prompt and handles response."""
    service = GeneratorService()
    
    # Mock LLM response
    mock_completion = MagicMock()
    mock_completion.choices[0].message.content = '["Python", "SQL"]'
    service.client.chat.completions.create.return_value = mock_completion
    
    # Call the method
    role = "Data Engineer"
    level = "Senior"
    result = service.generate_skills_list(role, level)
    
    # Assertions
    assert result == ["Python", "SQL"]
    
    # Verify the prompt contained the experience level
    call_args = service.client.chat.completions.create.call_args
    assert call_args is not None
    messages = call_args.kwargs['messages']
    prompt_content = messages[0]['content']
    
    assert f'"{role}"' in prompt_content
    assert f'"{level}"' in prompt_content
    assert "technical skills" in prompt_content
