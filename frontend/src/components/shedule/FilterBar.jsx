import React from 'react';
import Calendar from '../other/Calendar'; 


const FilterBar = () => {
  return (
    
    <div className="flex items-center space-x-4 mt-5 mb-6 bg-white p-4 rounded-[12.5px]">
      {/* Преподаватель */}
      <div>
        <label htmlFor="teacher-select" className="block text-sm font-medium text-black">
          Преподаватель
        </label>
        <select
          id="teacher-select"
          className="mt-1 block w-[200px] h-[37px] py-1.5 px-2 border border-gray-300 bg-white rounded-xl shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
        >
          <option value="">Все преподаватели</option>
        </select>
      </div>

      {/* Группа */}
      <div>
        <label htmlFor="group-select" className="block text-sm font-medium text-black">
          Группа
        </label>
        <select
          id="group-select"
          className="mt-1 block w-[200px] h-[37px] py-1.5 px-2 border border-gray-300 bg-white rounded-xl shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
        >
          <option value="">Все группы</option>
        </select>
      </div>

      {/* Предмет */}
      <div>
        <label htmlFor="subject-select" className="block text-sm font-medium text-black">
          Предмет
        </label>
        <select
          id="subject-select"
          className="mt-1 block w-[200px] h-[37px] py-1.5 px-2 border border-gray-300 bg-white rounded-xl shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
        >
          <option value="">Все предметы</option>
        </select>
      </div>

      {/* Календарь */}
      <div>
        <label htmlFor="date-input" className="block text-sm font-medium text-black">
          Дата
        </label>
        {/*<Calendar />*/}


        <input
          type="date"
          id="date-input"
          className="mt-1 block w-[200px] h-[37px] py-1.5 px-2 border border-gray-300 bg-white rounded-xl shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
        />
        


      </div>

      {/* Кнопка экспорта */}
      <button
        type="button"
        className="ml-auto self-end w-[200px] h-[37px] py-1.5 px-2 bg-white text-[#7816db] border border-[#7816db] 
                   rounded-xl flex items-center justify-center gap-2 text-sm font-semibold 
                   hover:bg-[#7816db] hover:text-white transition-colors"
      >
        
        Экспорт в xlsx
      </button>
    </div>
  );
};

export default FilterBar;