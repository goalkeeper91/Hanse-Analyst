import pytest
from unittest.mock import patch, MagicMock
from app.services.ai_service import AIService

@pytest.fixture
def ai_service():
    return AIService(model="test-model")

@pytest.mark.asyncio
async def test_get_overview_error_handling(ai_service):
    # Test how service handles ollama errors
    with patch('ollama.generate') as mock_generate:
        mock_generate.side_effect = Exception("Connection Error")
        result = await ai_service.get_overview("Some context")
        assert "Fehler bei der Zusammenfassung" in result

@pytest.mark.asyncio
async def test_analyze_document_success(ai_service):
    with patch('ollama.generate') as mock_generate:
        mock_generate.return_value = {'response': 'Dies ist eine KI-Antwort.'}
        result = await ai_service.analyze_document("Kontext", "Frage")
        assert result == "Dies ist eine KI-Antwort."
