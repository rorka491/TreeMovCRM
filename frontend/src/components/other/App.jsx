import React from 'react';
import Calendar from './components/Calendar/Calendar';
import './App.css';

function App() {
  const handleDateSelect = (date) => {
    console.log('Выбрана дата:', date);
  };

  return (
    <div className="app">
      <h1>Мой календарь</h1>
      <Calendar onDateSelect={handleDateSelect} />
    </div>
  );
}

export default App;