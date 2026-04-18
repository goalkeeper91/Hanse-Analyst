import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Upload, MessageSquare, FileText, ShieldCheck, List, FileSearch } from 'lucide-react';

function App() {
  const [documents, setDocuments] = useState([]);
  const [selectedDoc, setSelectedDoc] = useState(null);
  const [question, setQuestion] = useState('');
  const [chat, setChat] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchDocuments();
  }, []);

  const fetchDocuments = async () => {
    try {
      const response = await axios.get('http://localhost:8000/documents');
      setDocuments(response.data || []);
    } catch (error) {
      console.error('Fehler beim Laden der Dokumente:', error);
    }
  };

  const handleFileUpload = async (e) => {
    const selectedFiles = Array.from(e.target.files);
    if (selectedFiles.length === 0) return;

    const formData = new FormData();
    selectedFiles.forEach(file => formData.append('files', file));

    setLoading(true);
    try {
      await axios.post('http://localhost:8000/upload', formData);
      await fetchDocuments();
    } catch (error) {
      console.error('Upload Fehler:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAsk = async () => {
    if (!question || !selectedDoc) return;
    setLoading(true);

    try {
      const response = await axios.post(`http://localhost:8000/ask/${selectedDoc.id}?question=${encodeURIComponent(question)}`);
      setChat(prev => [...prev, { q: question, a: response.data.answer }]);
      setQuestion('');
    } catch (error) {
      console.error('KI Fehler:', error);
    } finally {
      setLoading(false);
    }
  };

  const getTypeBadge = (type) => {
    switch (type) {
      case 'Rechnung': return <span className="bg-green-100 text-green-800 text-xs font-medium px-2.5 py-0.5 rounded-full border border-green-400">Rechnung</span>;
      case 'Vertrag': return <span className="bg-blue-100 text-blue-800 text-xs font-medium px-2.5 py-0.5 rounded-full border border-blue-400">Vertrag</span>;
      default: return <span className="bg-gray-100 text-gray-800 text-xs font-medium px-2.5 py-0.5 rounded-full border border-gray-400">Sonstiges</span>;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 font-sans flex flex-col">
      <header className="bg-white border-b border-gray-200 p-4 shadow-sm">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="bg-blue-900 p-2 rounded-lg">
              <FileSearch className="text-white w-6 h-6" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-blue-900 leading-tight">Hanse-Analyst</h1>
              <p className="text-xs text-gray-500 uppercase tracking-wider font-semibold">Intelligente Dokumenten-KI</p>
            </div>
          </div>
          <div className="flex items-center space-x-4">
            <div className="hidden md:flex items-center text-green-600 bg-green-50 px-4 py-2 rounded-full border border-green-100">
              <ShieldCheck className="mr-2 w-4 h-4" />
              <span className="text-xs font-bold uppercase">100% DSGVO-Konform (Lokal)</span>
            </div>
            <label className="cursor-pointer bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition flex items-center shadow-md text-sm font-semibold">
              <Upload className="mr-2 w-4 h-4" /> Dokumente hochladen
              <input type="file" multiple accept=".pdf" onChange={handleFileUpload} className="hidden" aria-label="Dokument-Upload" />
            </label>
          </div>
        </div>
      </header>

      <main className="flex-1 flex overflow-hidden">
        <aside className="w-80 bg-white border-r border-gray-200 flex flex-col">
          <div className="p-4 border-b border-gray-100 bg-gray-50/50">
            <h2 className="text-sm font-bold text-gray-400 uppercase tracking-widest flex items-center">
              <List className="w-4 h-4 mr-2" /> Ihre Dokumente
            </h2>
          </div>
          <div className="flex-1 overflow-y-auto">
            {documents.length === 0 && !loading && (
              <p className="p-4 text-xs text-gray-400 italic">Keine Dokumente gefunden.</p>
            )}
            {documents.map((doc) => (
              <div
                key={doc.id}
                onClick={() => { setSelectedDoc(doc); setChat([]); }}
                className={`p-4 cursor-pointer border-b border-gray-50 transition-colors hover:bg-blue-50/50 ${selectedDoc?.id === doc.id ? 'bg-blue-50 border-r-4 border-r-blue-600' : ''}`}
                data-testid={`doc-item-${doc.id}`}
              >
                <div className="flex items-center justify-between mb-2">
                  <p className="text-sm font-bold text-gray-800 truncate pr-2">{doc.filename}</p>
                  {getTypeBadge(doc.doc_type)}
                </div>
                <p className="text-xs text-gray-500 line-clamp-2">{doc.summary}</p>
              </div>
            ))}
          </div>
        </aside>

        {selectedDoc ? (
          <div className="flex-1 flex">
            <div className="flex-1 p-6 overflow-y-auto border-r border-gray-200">
              <div className="mb-6 bg-white p-6 rounded-xl shadow-sm border border-gray-200">
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-xl font-bold text-gray-900 flex items-center">
                    <FileText className="mr-2 text-blue-600" /> Dokumenten-Vorschau
                  </h2>
                  {getTypeBadge(selectedDoc.doc_type)}
                </div>
                <div className="bg-gray-50 p-4 rounded-lg border border-gray-100">
                  <h3 className="text-xs font-bold text-gray-400 uppercase mb-2">KI-Zusammenfassung</h3>
                  <p className="text-sm text-gray-700 leading-relaxed">{selectedDoc.summary}</p>
                </div>
                <div className="mt-6">
                  <h3 className="text-xs font-bold text-gray-400 uppercase mb-2">Text-Inhalt</h3>
                  <div className="text-sm text-gray-600 bg-gray-50 p-4 rounded-lg border border-dashed border-gray-300 font-mono whitespace-pre-wrap max-h-96 overflow-y-auto">
                    {selectedDoc.content}
                  </div>
                </div>
              </div>
            </div>

            <div className="w-[450px] bg-white flex flex-col shadow-xl">
              <div className="p-4 border-b border-gray-200 bg-gray-50/80">
                <h2 className="font-bold text-gray-800 flex items-center">
                  <MessageSquare className="mr-2 text-blue-600 w-5 h-5" /> Chat-Assistent
                </h2>
                <p className="text-[10px] text-gray-400 uppercase font-bold tracking-tight">Analyse von: {selectedDoc.filename}</p>
              </div>

              <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50/30">
                {chat.map((msg, i) => (
                  <div key={i}>
                    <div className="bg-blue-900 text-white p-3 rounded-t-lg rounded-bl-lg ml-8 text-sm shadow-sm mb-2">
                      <p className="font-bold text-[10px] uppercase opacity-70 mb-1 text-blue-200">Frage</p>
                      {msg.q}
                    </div>
                    <div className="bg-white border border-gray-200 p-4 rounded-t-lg rounded-br-lg mr-8 text-sm shadow-sm">
                      <p className="font-bold text-[10px] uppercase text-blue-600 mb-2 tracking-widest">Antwort</p>
                      <p className="text-gray-700 leading-relaxed">{msg.a}</p>
                    </div>
                  </div>
                ))}
                {loading && (
                  <div className="flex items-center space-x-2 text-blue-600 animate-pulse p-4">
                    <div className="w-2 h-2 bg-blue-600 rounded-full"></div>
                    <div className="w-2 h-2 bg-blue-600 rounded-full"></div>
                    <div className="w-2 h-2 bg-blue-600 rounded-full"></div>
                  </div>
                )}
              </div>

              <div className="p-4 border-t border-gray-200 bg-white">
                <div className="relative flex gap-2">
                  <input
                    type="text"
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                    placeholder="Frage stellen..."
                    className="flex-1 p-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 shadow-inner text-sm"
                    onKeyPress={(e) => e.key === 'Enter' && handleAsk()}
                  />
                  <button
                    onClick={handleAsk}
                    disabled={loading || !question}
                    aria-label="Senden"
                    className="bg-blue-600 text-white p-3 rounded-xl hover:bg-blue-700 disabled:opacity-50 shadow-md"
                  >
                    <MessageSquare className="w-4 h-4" />
                  </button>
                </div>
              </div>
            </div>
          </div>
        ) : (
          <div className="flex-1 flex items-center justify-center bg-gray-50 text-gray-400">
            Wählen Sie ein Dokument aus.
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
