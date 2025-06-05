import React, { useState } from 'react';
import './Calendar.css';

const Calendar = ({ onDateSelect }) => {
  const [currentDate, setCurrentDate] = useState(new Date());
  const [selectedDate, setSelectedDate] = useState(null);

  const months = [
    'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
    'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'
  ];

  const dayHeaders = ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ', 'ВС'];

  // Проверка на високосный год
  const isLeapYear = (year) => {
    return (year % 4 === 0 && year % 100 !== 0) || year % 400 === 0;
  };

  // Получение количества дней в месяце
  const getDaysInMonth = (year, month) => {
    const daysInMonth = [
      31, isLeapYear(year) ? 29 : 28, 31, 30, 31, 30,
      31, 31, 30, 31, 30, 31
    ];
    return daysInMonth[month];
  };

  // Определение дня недели для 1-го числа месяца
  const getFirstDayOfMonth = (year, month) => {
    const date = new Date(year, month, 1);
    return date.getDay() === 0 ? 6 : date.getDay() - 1;
  };

  // Генерация календаря на месяц
  const generateCalendar = (year, month) => {
    const daysInMonth = getDaysInMonth(year, month);
    const firstDay = getFirstDayOfMonth(year, month);
    const weeks = [];
    let week = Array(7).fill(null);

    let day = 1;
    // Заполняем первую неделю
    for (let i = 0; i < 7; i++) {
      if (i >= firstDay && day <= daysInMonth) {
        week[i] = day++;
      }
    }
    weeks.push(week);

    // Заполняем остальные недели
    while (day <= daysInMonth) {
      week = Array(7).fill(null);
      for (let i = 0; i < 7 && day <= daysInMonth; i++) {
        week[i] = day++;
      }
      weeks.push(week);
    }

    return weeks;
  };

  // Переключение на предыдущий месяц
  const handlePrevMonth = () => {
    const newDate = new Date(currentDate);
    newDate.setMonth(newDate.getMonth() - 1);
    if (newDate.getFullYear() >= 0) {
      setCurrentDate(newDate);
    }
  };

  // Переключение на следующий месяц
  const handleNextMonth = () => {
    const newDate = new Date(currentDate);
    newDate.setMonth(newDate.getMonth() + 1);
    if (newDate.getFullYear() <= 9999) {
      setCurrentDate(newDate);
    }
  };

  // Изменение года
  const handleYearChange = (e) => {
    const year = parseInt(e.target.value);
    if (year >= 0 && year <= 9999) {
      const newDate = new Date(currentDate);
      newDate.setFullYear(year);
      setCurrentDate(newDate);
    }
  };

  // Изменение месяца
  const handleMonthChange = (e) => {
    const month = parseInt(e.target.value);
    const newDate = new Date(currentDate);
    newDate.setMonth(month);
    setCurrentDate(newDate);
  };

  // Выбор даты
  const handleDateClick = (day) => {
    if (day) {
      const newSelectedDate = new Date(
        currentDate.getFullYear(),
        currentDate.getMonth(),
        day
      );
      setSelectedDate(newSelectedDate);
      if (onDateSelect) {
        onDateSelect(newSelectedDate);
      }
    }
  };

  // Рендер календаря
  const renderCalendar = () => {
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth();
    const weeks = generateCalendar(year, month);

    return weeks.map((week, weekIndex) => (
      <tr key={weekIndex}>
        {week.map((day, dayIndex) => {
          const isSelected = selectedDate && 
            selectedDate.getDate() === day &&
            selectedDate.getMonth() === month &&
            selectedDate.getFullYear() === year;

          const isCurrentDay = new Date().getDate() === day &&
            new Date().getMonth() === month &&
            new Date().getFullYear() === year;

          return (
            <td
              key={dayIndex}
              className={`${day ? 'active' : ''} ${isSelected ? 'selected' : ''} ${isCurrentDay ? 'current' : ''}`}
              onClick={() => handleDateClick(day)}
            >
              {day || ''}
            </td>
          );
        })}
      </tr>
    ));
  };

  return (
    <div className="calendar">
      <div className="calendar-header">
        <button 
          onClick={handlePrevMonth} 
          disabled={currentDate.getFullYear() === 0 && currentDate.getMonth() === 0}
        >
          &lt;
        </button>
        
        <select 
          value={currentDate.getMonth()} 
          onChange={handleMonthChange}
          className="month-select"
        >
          {months.map((month, index) => (
            <option key={index} value={index}>{month}</option>
          ))}
        </select>
        
        <input
          type="number"
          min="0"
          max="9999"
          value={currentDate.getFullYear()}
          onChange={handleYearChange}
          className="year-input"
        />
        
        <button 
          onClick={handleNextMonth} 
          disabled={currentDate.getFullYear() === 9999 && currentDate.getMonth() === 11}
        >
          &gt;
        </button>
      </div>

      <table className="calendar-table">
        <thead>
          <tr>
            {dayHeaders.map((day, index) => (
              <th key={index}>{day}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {renderCalendar()}
        </tbody>
      </table>

      {selectedDate && (
        <div className="selected-date">
          Выбранная дата: {selectedDate.toLocaleDateString('ru-RU')}
        </div>
      )}
    </div>
  );
};

export default Calendar;
