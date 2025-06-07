// Calendar.jsx
import React, { useState } from 'react';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import './css/Calendar.css';

const Calendar = () => {
  const [startDate, setStartDate] = useState(new Date());

  return (
    <DatePicker
      selected={startDate}
      onChange={(date) => setStartDate(date)}
      dateFormat="dd.MM.yyyy"
      className="w-[200px] py-1.5 px-2 border border-[#7816db] bg-white text-black rounded-xl text-sm font-semibold focus:outline-none"
      calendarClassName="custom-calendar"
    />
  );
};

export default Calendar;
