import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './components/other/App';  // Обновлённый путь
import './components/other/App.css';      // Обновлённый путь

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);