import ollama
import os
import asyncio

class AIService:
    def __init__(self, model: str = "llama3"):
        self.model = model
        # Explizite Definition des lokalen Ollama-Hosts.
        self.host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        # Wir nutzen den AsyncClient für bessere Performance in FastAPI
        self.client = ollama.AsyncClient(host=self.host)

    async def analyze_document(self, context: str, question: str) -> str:
        """
        Analysiert den Dokumentenkontext und beantwortet eine spezifische Frage 
        über den lokalen Async-LLM-Client.
        """
        prompt = f"""
        Du bist ein Experte für Dokumentenanalyse. Nutze den folgenden Kontext, um die Frage präzise zu beantworten.
        WICHTIG: Antworte nur basierend auf dem bereitgestellten Kontext. 
        Falls die Antwort nicht im Kontext zu finden ist, sage das bitte höflich.
        
        Kontext:
        {context[:8000]}
        
        Frage: {question}
        
        Antwort:
        """
        
        try:
            # await ist notwendig, da wir den AsyncClient nutzen
            response = await self.client.generate(model=self.model, prompt=prompt)
            return response['response']
        except Exception as e:
            return (f"Fehler bei der lokalen KI-Verarbeitung (Host: {self.host}): {str(e)}. "
                    "Stellen Sie sicher, dass Ollama lokal gestartet wurde und das Modell geladen ist.")

    async def get_overview(self, context: str) -> str:
        """
        Generiert eine allgemeine Zusammenfassung des Dokumentinhalts lokal.
        """
        prompt = f"""
        Fasse den wesentlichen Inhalt dieses Dokuments kurz und präzise auf Deutsch zusammen. 
        Konzentriere dich auf die Kernaussagen:

        {context[:8000]}
        """
        try:
            response = await self.client.generate(model=self.model, prompt=prompt)
            return response['response']
        except Exception as e:
            return f"Fehler bei der lokalen Zusammenfassung: {str(e)}"
