import ollama
from typing import List, Dict

class AIService:
    def __init__(self, model: str = "llama3"):
        self.model = model

    async def analyze_document(self, context: str, question: str) -> str:
        """
        Analyzes the document context and answers a specific question using a local LLM.
        """
        prompt = f"""
        Du bist ein Experte für Dokumentenanalyse. Nutze den folgenden Kontext, um die Frage präzise zu beantworten.
        Falls die Antwort nicht im Kontext zu finden ist, sage das bitte höflich.
        
        Kontext:
        {context[:4000]} # Limiting context for basic demo
        
        Frage: {question}
        
        Antwort:
        """
        
        try:
            response = ollama.generate(model=self.model, prompt=prompt)
            return response['response']
        except Exception as e:
            return f"Fehler bei der lokalen KI-Verarbeitung: {str(e)}. Stellen Sie sicher, dass Ollama läuft."

    async def get_overview(self, context: str) -> str:
        """
        Generates a general overview of the document content.
        """
        prompt = f"Fasse den wesentlichen Inhalt dieses Dokuments kurz und präzise auf Deutsch zusammen:\n\n{context[:4000]}"
        try:
            response = ollama.generate(model=self.model, prompt=prompt)
            return response['response']
        except Exception as e:
            return f"Fehler bei der Zusammenfassung: {str(e)}"
