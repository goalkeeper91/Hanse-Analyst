import ollama
import os
import asyncio
import json

class AIService:
    def __init__(self, model: str = "llama3"):
        self.model = model
        self.host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        self.client = ollama.AsyncClient(host=self.host)

    async def classify_and_summarize(self, context: str):
        """
        Classifies the document type and provides a summary.
        Returns a JSON-formatted string with keys: 'type' and 'summary'.
        """
        prompt = f"""
        Analysiere den folgenden Dokumententext und gib das Ergebnis NUR als JSON zurück.
        Struktur: {{"type": "Rechnung" oder "Vertrag" oder "Sonstiges", "summary": "Kurze Zusammenfassung"}}
        
        Text: {context[:4000]}
        """
        try:
            response = await self.client.generate(model=self.model, prompt=prompt, format="json")
            data = json.loads(response['response'])
            return data
        except Exception:
            return {"type": "Sonstiges", "summary": "Konnte nicht klassifiziert werden."}

    async def analyze_document(self, context: str, question: str) -> str:
        prompt = f"Nutze den Kontext: {context[:8000]}\nFrage: {question}\nAntwort:"
        try:
            response = await self.client.generate(model=self.model, prompt=prompt)
            return response['response']
        except Exception as e:
            return f"Fehler: {str(e)}"
