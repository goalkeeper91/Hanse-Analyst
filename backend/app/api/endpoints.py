from fastapi import APIRouter, UploadFile, File, HTTPException
from ..services.pdf_service import PDFService
from ..services.ai_service import AIService

router = APIRouter()
pdf_service = PDFService()
ai_service = AIService()

# In-memory storage for the current document context (for demo purposes)
document_store = {"context": ""}

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Nur PDF-Dateien sind erlaubt.")
    
    try:
        content = await file.read()
        text = await pdf_service.extract_text(content)
        
        if not text.strip():
            raise HTTPException(status_code=400, detail="Die PDF scheint keinen lesbaren Text zu enthalten.")
            
        document_store["context"] = text
        
        # Generiere eine erste Übersicht mittels KI
        overview = await ai_service.get_overview(text)
        
        return {
            "filename": file.filename, 
            "status": "processed",
            "overview": overview
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Serverfehler beim Verarbeiten der PDF: {str(e)}")

@router.post("/ask")
async def ask_question(question: str):
    if not document_store["context"]:
        raise HTTPException(status_code=400, detail="Bitte laden Sie zuerst eine PDF hoch.")
    
    answer = await ai_service.analyze_document(document_store["context"], question)
    return {"answer": answer}
