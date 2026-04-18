import pytest
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch, AsyncMock

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

@pytest.mark.asyncio
async def test_get_documents_empty():
    # Test abrufen der Dokumente (SQLite sollte initialisiert sein)
    response = client.get("/documents")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_ask_invalid_id():
    # Test Frage an nicht existierendes Dokument
    response = client.post("/ask/999?question=Test")
    assert response.status_code == 404
    assert "Dokument nicht gefunden" in response.json()["detail"]

@patch('app.services.pdf_service.PDFService.extract_text', new_callable=AsyncMock)
@patch('app.services.ai_service.AIService.classify_and_summarize', new_callable=AsyncMock)
def test_upload_success(mock_classify, mock_extract):
    mock_extract.return_value = "Test Inhalt"
    mock_classify.return_value = {"type": "Rechnung", "summary": "Test Summary"}
    
    files = [
        ('files', ('test.pdf', b'fake-pdf-content', 'application/pdf'))
    ]
    response = client.post("/upload", files=files)
    
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["type"] == "Rechnung"
