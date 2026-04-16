import pytest
from app.services.pdf_service import PDFService

def test_get_summary_with_text():
    text = "Dies ist ein Testdokument.\nEs hat zwei Zeilen."
    summary = PDFService.get_summary(text)
    assert "2 Zeilen" in summary
    assert "8 Wörter" in summary

def test_get_summary_empty():
    summary = PDFService.get_summary("")
    assert "Kein Text zum Analysieren gefunden" in summary

@pytest.mark.asyncio
async def test_extract_text_empty_bytes():
    # Test how the service handles empty bytes (should fail gracefully)
    result = await PDFService.extract_text(b"")
    assert "Fehler bei der PDF-Textextraktion" in result
