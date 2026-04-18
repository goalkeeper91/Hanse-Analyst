import pytest
from unittest.mock import patch, AsyncMock
from app.services.ai_service import AIService
import json

@pytest.fixture
def ai_service():
    return AIService(model="llama3")

@pytest.mark.asyncio
async def test_classify_and_summarize_success(ai_service):
    with patch('ollama.AsyncClient.generate', new_callable=AsyncMock) as mock_gen:
        mock_gen.return_value = {
            'response': json.dumps({"type": "Rechnung", "summary": "Test Rechnung"})
        }
        
        result = await ai_service.classify_and_summarize("Test Kontext")
        
        assert result["type"] == "Rechnung"
        assert result["summary"] == "Test Rechnung"
        mock_gen.assert_called_once()

@pytest.mark.asyncio
async def test_classify_and_summarize_fallback(ai_service):
    with patch('ollama.AsyncClient.generate', new_callable=AsyncMock) as mock_gen:
        mock_gen.side_effect = Exception("Parsing Fehler")
        
        result = await ai_service.classify_and_summarize("Test Kontext")
        
        assert result["type"] == "Sonstiges"
        assert "Konnte nicht klassifiziert werden" in result["summary"]

@pytest.mark.asyncio
async def test_analyze_document_success(ai_service):
    with patch('ollama.AsyncClient.generate', new_callable=AsyncMock) as mock_gen:
        mock_gen.return_value = {'response': 'Dies ist eine KI-Antwort.'}
        
        result = await ai_service.analyze_document("Kontext", "Frage")
        
        assert result == "Dies ist eine KI-Antwort."
        mock_gen.assert_called_once()
