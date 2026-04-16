import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_ask_question_without_upload():
    # Attempting to ask a question before uploading should return 400
    response = client.post("/ask?question=Was steht im Dokument?")
    assert response.status_code == 400
    assert "Bitte laden Sie zuerst eine PDF hoch" in response.json()["detail"]

def test_upload_non_pdf():
    # Uploading a non-pdf file
    files = {'file': ('test.txt', b'some text content', 'text/plain')}
    response = client.post("/upload", files=files)
    assert response.status_code == 400
    assert "Nur PDF-Dateien sind erlaubt" in response.json()["detail"]
