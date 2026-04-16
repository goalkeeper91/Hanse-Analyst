import { render, screen, fireEvent } from '@testing-library/react';
import { expect, test, vi } from 'vitest';
import App from './App';
import axios from 'axios';

// Mock axios
vi.mock('axios');

test('renders header with application title', () => {
  render(<App />);
  const titleElement = screen.getByText(/Hanse-Analyst/i);
  expect(titleElement).toBeInTheDocument();
});

test('renders privacy indicator', () => {
  render(<App />);
  const privacyElement = screen.getByText(/100% Datenschutz/i);
  expect(privacyElement).toBeInTheDocument();
});

test('shows upload section', () => {
  render(<App />);
  const uploadTitle = screen.getByText(/Dokument hochladen/i);
  expect(uploadTitle).toBeInTheDocument();
});

test('updates question input value', () => {
  render(<App />);
  const input = screen.getByPlaceholderText(/Stellen Sie eine Frage.../i);
  fireEvent.change(input, { target: { value: 'Was ist das Thema?' } });
  expect(input.value).toBe('Was ist das Thema?');
});

test('calls axios on question submit', async () => {
  axios.post.mockResolvedValue({ data: { answer: 'KI Test Antwort' } });

  render(<App />);
  const input = screen.getByPlaceholderText(/Stellen Sie eine Frage.../i);
  const button = screen.getByText(/Senden/i);

  fireEvent.change(input, { target: { value: 'Was ist das Thema?' } });
  fireEvent.click(button);

  expect(axios.post).toHaveBeenCalled();
});
