import ollama
import os
import asyncio
import json
from .order_service import OrderService

class AIService:
    def __init__(self, model: str = "llama3"):
        self.model = model
        self.host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        self.client = ollama.AsyncClient(host=self.host)
        self.order_service = OrderService()

    async def classify_and_summarize(self, context: str):
        """
        Classifies the document type and provides a summary.
        Returns a JSON-formatted string with keys: 'type' and 'summary'.
        """
        prompt = f"""
        Analysiere den folgenden Dokumententext und gib das Ergebnis NUR als JSON zurück.
        Struktur: {{
            "type": "Rechnung" oder "Vertrag" oder "Sonstiges", 
            "summary": "Kurze Zusammenfassung",
            "order_id": "Gefundene Bestellnummer (z.B. PO-123) oder null",
            "total_amount": "Gefundener Gesamtbetrag als Zahl oder null"
        }}
        
        Text: {context[:4000]}
        """
        try:
            response = await self.client.generate(model=self.model, prompt=prompt, format="json")
            data = json.loads(response['response'])
            
            # Falls es eine Rechnung ist, führen wir die Rechnungseingangskontrolle durch
            if data.get("type") == "Rechnung" and data.get("order_id") and data.get("total_amount"):
                try:
                    amount = float(data["total_amount"])
                    is_valid, message = self.order_service.verify_order(
                        data["order_id"], 
                        amount
                    )
                    data["verification_status"] = "valid" if is_valid else "invalid"
                    data["verification_message"] = message
                except (ValueError, TypeError):
                    data["verification_status"] = "invalid"
                    data["verification_message"] = "Ungültiger Betrag im Dokument gefunden."
            else:
                data["verification_status"] = "n/a"
                data["verification_message"] = "Keine Rechnungseingangskontrolle möglich."
                
            return data
        except Exception:
            return {
                "type": "Sonstiges", 
                "summary": "Konnte nicht klassifiziert werden (KI-Fehler).", 
                "verification_status": "error",
                "verification_message": "Fehler bei der KI-Analyse."
            }

    async def analyze_document(self, context: str, question: str) -> str:
        prompt = f"Nutze den Kontext: {context[:8000]}\nFrage: {question}\nAntwort:"
        try:
            response = await self.client.generate(model=self.model, prompt=prompt)
            return response['response']
        except Exception as e:
            return f"Fehler: {str(e)}"
