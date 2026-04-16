import ollama
from typing import List, Dict
import os

class AIService:
    def __init__(self, model: str = "llama3"):
        self.model = model
        # Explizite Definition des lokalen Ollama-Hosts für maximale Transparenz und Sicherheit.
        # Standardmäßig läuft Ollama lokal auf Port 11434.
        self.host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        self.client = ollama.Client(host=self.host)

    async def analyze_document(self, context: str, question: str) -> str:
        """
        Analysiert den Dokumentenkontext und beantwortet eine spezifische Frage 
        ausschließlich über den lokalen LLM-Client.
        """
        prompt = f"""
        Du bist ein Experte für Dokumentenanalyse. Nutze den folgenden Kontext, um die Frage präzise zu beantworten.
        WICHTIG: Antworte nur basierend auf dem bereitgestellten Kontext. 
        Falls die Antwort nicht im Kontext zu finden ist, sage das bitte höflich.
        
        Kontext:
        {context[:8000]} # Erhöhter Kontext für bessere Analyse
        
        Frage: {question}
        
        Antwort:
        """
        
        try:
            # Nutzung des explizit lokalen Clients
            response = self.client.generate(model=self.model, prompt=prompt)
            return response['response']
        except Exception as e:
            return (f"Fehler bei der lokalen KI-Verarbeitung (Host: {self.host}): {str(e)}. "
                    "Stellen Sie sicher, dass Ollama lokal gestartet wurde.")

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
            response = self.client.generate(model=self.model, prompt=prompt)
            return response['response']
        except Exception as e:
            return f"Fehler bei der lokalen Zusammenfassung: {str(e)}"
