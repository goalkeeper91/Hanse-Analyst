from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.database import AsyncSessionLocal, Document
from app.services.pdf_service import PDFService
from app.services.ai_service import AIService

router = APIRouter()
pdf_service = PDFService()
ai_service = AIService()

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

@router.post("/upload")
async def upload_documents(files: List[UploadFile] = File(...), db: AsyncSession = Depends(get_db)):
    results = []
    for file in files:
        if not file.filename.endswith('.pdf'):
            continue
            
        try:
            content = await file.read()
            text = await pdf_service.extract_text(content)
            
            # AI Classification & Summary
            ai_data = await ai_service.classify_and_summarize(text)
            
            doc = Document(
                filename=file.filename,
                content=text,
                doc_type=ai_data.get("type", "Sonstiges"),
                summary=ai_data.get("summary", "")
            )
            db.add(doc)
            await db.commit()
            await db.refresh(doc)
            
            results.append({
                "id": doc.id,
                "filename": doc.filename,
                "type": doc.doc_type,
                "summary": doc.summary
            })
        except Exception as e:
            print(f"Fehler beim Verarbeiten von {file.filename}: {e}")
            await db.rollback()
            
    return results

@router.get("/documents")
async def get_documents(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(Document))
        docs = result.scalars().all()
        return docs
    except Exception as e:
        print(f"DB Fehler: {e}")
        raise HTTPException(status_code=500, detail="Datenbank konnte nicht gelesen werden.")

@router.post("/ask/{doc_id}")
async def ask_question(doc_id: int, question: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Document).where(Document.id == doc_id))
    doc = result.scalar_one_or_none()
    if not doc:
        raise HTTPException(status_code=404, detail="Dokument nicht gefunden")
    
    answer = await ai_service.analyze_document(doc.content, question)
    return {"answer": answer}
