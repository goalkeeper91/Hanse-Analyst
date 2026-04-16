import pytest
from unittest.mock import patch, AsyncMock
from app.services.ai_service import AIService

@pytest.fixture
def ai_service():
    # Wir nutzen llama3, um konsistent mit der App zu sein
    return AIService(model="llama3")

@pytest.mark.asyncio
async def test_get_overview_success(ai_service):
    # Mock für den AsyncClient.generate Call
    with patch('ollama.AsyncClient.generate', new_callable=AsyncMock) as mock_gen:
        mock_gen.return_value = {'response': 'Dies ist eine Zusammenfassung.'}
        
        result = await ai_service.get_overview("Test Kontext")
        
        assert result == "Dies ist eine Zusammenfassung."
        mock_gen.assert_called_once()

@pytest.mark.asyncio
async def test_get_overview_error_handling(ai_service):
    with patch('ollama.AsyncClient.generate', new_callable=AsyncMock) as mock_gen:
        mock_gen.side_effect = Exception("Ollama nicht erreichbar")
        
        result = await ai_service.get_overview("Some context")
        assert "Fehler bei der lokalen Zusammenfassung" in result

@pytest.mark.asyncio
async def test_analyze_document_success(ai_service):
    with patch('ollama.AsyncClient.generate', new_callable=AsyncMock) as mock_gen:
        mock_gen.return_value = {'response': 'Dies ist eine KI-Antwort.'}
        
        result = await ai_service.analyze_document("Kontext", "Frage")
        
        assert result == "Dies ist eine KI-Antwort."
        mock_gen.assert_called_once()

@pytest.mark.asyncio
async def test_analyze_document_error_handling(ai_service):
    with patch('ollama.AsyncClient.generate', new_callable=AsyncMock) as mock_gen:
        mock_gen.side_effect = Exception("Modell nicht gefunden")
        
        result = await ai_service.analyze_document("Kontext", "Frage")
        assert "Fehler bei der lokalen KI-Verarbeitung" in result
