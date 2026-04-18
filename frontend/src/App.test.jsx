import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { expect, test, vi, beforeEach } from 'vitest';
import App from './App';
import axios from 'axios';

// Mock axios
vi.mock('axios');

const mockDocs = [
  { id: 1, filename: 'rechnung.pdf', doc_type: 'Rechnung', summary: 'Eine Testrechnung', content: 'Inhalt 1' },
];

beforeEach(() => {
  vi.clearAllMocks();
  // Standard-Mock für das Laden der Dokumente beim Start
  axios.get.mockResolvedValue({ data: mockDocs });
});

test('renders header with application title', async () => {
  render(<App />);
  const title = await screen.findByText(/Hanse-Analyst/i);
  expect(title).toBeInTheDocument();
});

test('loads and displays documents in sidebar', async () => {
  render(<App />);
  const docItem = await screen.findByText('rechnung.pdf');
  expect(docItem).toBeInTheDocument();
});

test('selects a document and shows preview', async () => {
  render(<App />);

  // Warten bis die Sidebar geladen ist
  const docItem = await screen.findByText('rechnung.pdf');
  fireEvent.click(docItem);

  // Prüfen ob die Vorschau-Sektion erscheint
  const previewHeader = await screen.findByText(/Dokumenten-Vorschau/i);
  expect(previewHeader).toBeInTheDocument();

  // Da der Text zweimal vorkommt (Sidebar & Vorschau), nutzen wir getAllByText
  const summaries = await screen.findAllByText('Eine Testrechnung');
  expect(summaries.length).toBeGreaterThanOrEqual(1);
});

test('sends a question and displays answer', async () => {
  axios.post.mockResolvedValue({ data: { answer: 'KI Test Antwort' } });

  render(<App />);

  // 1. Dokument auswählen
  const docItem = await screen.findByText('rechnung.pdf');
  fireEvent.click(docItem);

  // 2. Frage stellen
  const input = await screen.findByPlaceholderText(/Frage stellen.../i);
  fireEvent.change(input, { target: { value: 'Was ist das?' } });

  const sendButton = screen.getByLabelText('Senden');
  fireEvent.click(sendButton);

  // 3. Auf Antwort warten (Asynchron)
  const answer = await screen.findByText('KI Test Antwort');
  expect(answer).toBeInTheDocument();
});

test('triggers upload on file change', async () => {
  axios.post.mockResolvedValue({ data: [] });

  render(<App />);

  const fileInput = screen.getByLabelText('Dokument-Upload');
  const file = new File(['test'], 'test.pdf', { type: 'application/pdf' });

  fireEvent.change(fileInput, { target: { files: [file] } });

  await waitFor(() => {
    expect(axios.post).toHaveBeenCalledWith(
      expect.stringContaining('/upload'),
      expect.any(FormData)
    );
  });
});
