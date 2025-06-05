import React from 'react';
import './App.css';  // Импорт из той же папки
import Calendar from './Calendar/Calendar';  // Путь относительно текущей папки

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