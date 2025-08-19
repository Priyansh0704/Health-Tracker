import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import { BrowserRouter } from 'react-router-dom'; // <-- Import this

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    {/* 👇 Wrap your App component like this 👇 */}
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </React.StrictMode>
);