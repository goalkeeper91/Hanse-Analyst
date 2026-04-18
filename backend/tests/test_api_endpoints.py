import pytest
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch, AsyncMock

# Wir nutzen den TestClient als Context Manager, um Lifespan Events zu triggern
def test_health_check():
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}

def test_get_documents_empty():
    with TestClient(app) as client:
        response = client.get("/documents")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

def test_ask_invalid_id():
    with TestClient(app) as client:
        response = client.post("/ask/999?question=Test")
        assert response.status_code == 404

@patch('app.services.pdf_service.PDFService.extract_text', new_callable=AsyncMock)
@patch('app.services.ai_service.AIService.classify_and_summarize', new_callable=AsyncMock)
def test_upload_success(mock_classify, mock_extract):
    mock_extract.return_value = "Test Inhalt"
    mock_classify.return_value = {
        "type": "Rechnung", 
        "summary": "Test Summary",
        "verification_status": "valid",
        "verification_message": "Ok"
    }
    
    with TestClient(app) as client:
        files = [
            ('files', ('test.pdf', b'fake-pdf-content', 'application/pdf'))
        ]
        response = client.post("/upload", files=files)
        
        assert response.status_code == 200
        json_resp = response.json()
        assert len(json_resp) >= 1
        assert json_resp[0]["type"] == "Rechnung"
