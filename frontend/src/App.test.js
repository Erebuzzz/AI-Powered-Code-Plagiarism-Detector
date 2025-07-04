import { render, screen } from '@testing-library/react';
import App from './App';

test('renders app header', () => {
  render(<App />);
  const headerElement = screen.getByText(/AI Code Plagiarism Detector/i);
  expect(headerElement).toBeInTheDocument();
});