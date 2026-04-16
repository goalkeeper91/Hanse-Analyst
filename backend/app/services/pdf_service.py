import pypdf
from io import BytesIO

class PDFService:
    @staticmethod
    async def extract_text(file_content: bytes) -> str:
        """
        Extracts text from a PDF file byte stream.
        """
        try:
            pdf_reader = pypdf.PdfReader(BytesIO(file_content))
            text = ""
            for page in pdf_reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
            return text
        except Exception as e:
            return f"Fehler bei der PDF-Textextraktion: {str(e)}"

    @staticmethod
    def get_summary(text: str) -> str:
        """
        Provides a basic structural overview of the text before AI processing.
        """
        if not text:
            return "Kein Text zum Analysieren gefunden."
        lines = text.strip().split('\n')
        words = text.split()
        return f"Das Dokument enthält ca. {len(lines)} Zeilen und {len(words)} Wörter."
