# Hanse-Analyst

Hanse-Analyst ist eine moderne Fullstack-Demo-Anwendung zur lokalen Analyse von PDF-Dokumenten mittels Künstlicher Intelligenz. Dieses Projekt demonstriert fortgeschrittene Kenntnisse in **Python (FastAPI)**, **React (Vite)** und der Integration **lokaler Large Language Models (LLMs)**.

## Projektziel
Das Tool ermöglicht es Benutzern, PDF-Dokumente hochzuladen, die anschließend vollständig lokal analysiert werden. Die Anwendung bietet eine automatische Zusammenfassung des Inhalts und erlaubt interaktive Fragen zum Dokument, ohne dass Daten die lokale Infrastruktur verlassen.

## Hauptfunktionen
- **PDF-Verarbeitung:** Automatisierte Textextraktion aus PDF-Dateien.
- **Lokale KI-Analyse:** Nutzung von Ollama (z.B. Llama 3) zur Inhaltsanalyse und Beantwortung von Fragen.
- **Modernes UI:** Eine responsive React-Oberfläche, entwickelt mit Vite und Tailwind CSS.
- **Clean Architecture:** Klare Trennung von API-Endpunkten, Services und Frontend-Komponenten.
- **Test-First Ansatz:** Umfassende Unit-Tests für Backend (Pytest) und Frontend (Vitest).

## Datenschutz & Lokale KI (Fokus: Deutsche Unternehmen)
Ein zentraler Aspekt dieses Projekts ist der **Schutz der Privatsphäre**. 
Gerade für deutsche Unternehmen ist Datensicherheit von höchster Bedeutung. Daher arbeitet dieses Tool ausschließlich mit **lokal gehosteten KI-Clients**. 

- **Keine Cloud-Abhängigkeit:** Die Daten verlassen niemals die lokale Infrastruktur.
- **Maximale Datensicherheit:** Sensible Dokumente werden nicht an externe Server oder Drittanbieter übertragen.
- **Compliance:** Unterstützung bei der Einhaltung strenger Datenschutzrichtlinien (DSGVO).

---

## Installation und Ausführung

### Voraussetzungen
- Python 3.9+
- Node.js & npm
- [Ollama](https://ollama.ai/) (installiert und gestartet)
  - Empfohlenes Modell laden: `ollama pull llama3`

### 1. Backend Setup (FastAPI)
Navigieren Sie in den `backend`-Ordner:
```bash
cd backend
# Virtuelle Umgebung erstellen (optional aber empfohlen)
python -m venv venv
source venv/bin/activate  # Unter Windows: venv\Scripts\activate

# Abhängigkeiten installieren
pip install -r requirements.txt

# Server starten
python main.py
```
Das Backend ist nun unter `http://localhost:8000` erreichbar.

### 2. Frontend Setup (React + Vite)
Öffnen Sie ein neues Terminal und navigieren Sie in den `frontend`-Ordner:
```bash
cd frontend
# Abhängigkeiten installieren
npm install

# Entwicklungsserver starten
npm run dev
```
Das Frontend ist nun unter der in der Konsole angegebenen Adresse (meist `http://localhost:5173`) erreichbar.

---

## Testing

### Backend Tests (Pytest)
```bash
cd backend
pytest
```

### Frontend Tests (Vitest)
```bash
cd frontend
npm run test
```

---

*Dieses Projekt dient als technischer Proof-of-Concept.*
