import React, { useState } from 'react';
import axios from 'axios';
import { Upload, MessageSquare, FileText, ShieldCheck } from 'lucide-react';

function App() {
  const [file, setFile] = useState(null);
  const [question, setQuestion] = useState('');
  const [chat, setChat] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleFileUpload = async (e) => {
    const selectedFile = e.target.files[0];
    setFile(selectedFile);

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      await axios.post('http://localhost:8000/upload', formData);
      alert('PDF erfolgreich hochgeladen und lokal verarbeitet.');
    } catch (error) {
      console.error('Upload Fehler:', error);
    }
  };

  const handleAsk = async () => {
    if (!question) return;
    setLoading(true);

    try {
      const response = await axios.post(`http://localhost:8000/ask?question=${encodeURIComponent(question)}`);
      setChat([...chat, { q: question, a: response.data.answer }]);
      setQuestion('');
    } catch (error) {
      console.error('KI Fehler:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-8 font-sans">
      <header className="max-w-4xl mx-auto mb-12 flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-blue-900">Hanse-Analyst</h1>
          <p className="text-gray-600">Lokale KI-Analyse Ihrer Dokumente</p>
        </div>
        <div className="flex items-center text-green-600 bg-green-50 px-4 py-2 rounded-full">
          <ShieldCheck className="mr-2" />
          <span className="text-sm font-semibold">100% Datenschutz</span>
        </div>
      </header>

      <main className="max-w-4xl mx-auto grid grid-cols-1 gap-8">
        {/* Upload Section */}
        <section className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
          <div className="flex items-center mb-4">
            <Upload className="mr-2 text-blue-600" />
            <h2 className="text-xl font-semibold">Dokument hochladen</h2>
          </div>
          <input
            type="file"
            accept=".pdf"
            onChange={handleFileUpload}
            className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
          />
        </section>

        {/* Chat/QA Section */}
        <section className="bg-white p-6 rounded-xl shadow-sm border border-gray-200 flex flex-col h-[500px]">
          <div className="flex items-center mb-4">
            <MessageSquare className="mr-2 text-blue-600" />
            <h2 className="text-xl font-semibold">Fragen zum Dokument</h2>
          </div>

          <div className="flex-1 overflow-y-auto mb-4 p-4 bg-gray-50 rounded-lg">
            {chat.map((msg, i) => (
              <div key={i} className="mb-4">
                <p className="font-bold text-blue-800">Frage: {msg.q}</p>
                <p className="text-gray-700 bg-white p-2 rounded mt-1 shadow-sm">Antwort: {msg.a}</p>
              </div>
            ))}
            {loading && <p className="text-gray-400 italic animate-pulse">KI analysiert...</p>}
          </div>

          <div className="flex gap-2">
            <input
              type="text"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="Stellen Sie eine Frage..."
              className="flex-1 p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              onKeyPress={(e) => e.key === 'Enter' && handleAsk()}
            />
            <button
              onClick={handleAsk}
              className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition"
            >
              Senden
            </button>
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;
