import React, { useEffect, useState } from 'react';
import logo from '../../assets/logo/Logo.svg';
import { Link, useParams, useLocation } from 'react-router-dom';
import { NavLink } from 'react-router-dom';



const Sidebar = ({ isVisible, setIsVisible, setSection }) => {
  const location = useLocation();


  const links = [
    { path: '/api/analytics', label: 'Аналитика' },
    { path: '/api/schedule', label: 'Расписание' },
    { path: '/api/empoloyers', label: 'Сотрудники' },
    { path: '/api/students', label: 'Ученики' },
    { path: '/api/financial_reporting', label: 'Финансовая отчётность' },
    { path: '/api/settings', label: 'Настройки' }
  ];


  useEffect(() => {
    const currentLink = links.find(link => location.pathname.startsWith(link.path));
    if (currentLink) {
      setSection(currentLink.label);
    }
  }, [location.pathname, setSection]);

  return (
    <div className="relative">
      <aside
        id="sidebar"
        className={`w-80 h-screen text-white flex flex-col justify-between transition-transform duration-300 bg-[#7816db] ease-in-out top-0 left-0 ${
          isVisible ? '' : 'hidden'
        }`}
      >
        <div>
          <div className="flex items-center justify-center gap-2 px-6 py-6">
            <div className="rounded-full p-2">
              <img src={logo} alt="TreeMov" />
            </div>
          </div>

          <nav className="mt-2 mr-12 ml-6">
          <ul className="space-y-1" style={{ fontFamily: 'Arial, Helvetica, sans-serif', fontSize: '14pt', fontWeight: 'bold' }}>
            {links.map(link => (
              <li key={link.path}>
                <Link 
                  to={link.path} 
                  onClick={() => setSection(link.label)}
                  className={`block px-6 py-3 rounded-lg hover:bg-purple-600 ${location.pathname === link.path ? 'bg-[#4b0096]' : ''}`}
                >
                  {link.label}
                </Link>
              </li>
            ))}
          </ul>
          </nav>
        </div>

        <div className="px-6 py-4 flex justify-center items-center" style={{ backgroundColor: '#2f213E' }}>
          <button className="flex items-center gap-2 text-white hover:text-gray-300">
            <span style={{ fontFamily: 'Arial, Helvetica, sans-serif', fontSize: '14pt', fontWeight: 'bold' }}>Выйти</span>
          </button>
        </div>

        <button
          id="hideBtn"
          onClick={() => setIsVisible(false)}
          className="absolute top-1/2 right-0 transform -translate-y-1/2 bg-gray-100 text-white p-2 rounded-l-[15px] h-[130px]"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="w-6 h-16" viewBox="0 0 24 24" fill="none" stroke="black" strokeWidth="3">
            <path strokeLinecap="round" strokeLinejoin="round" d="M15 19l-7-7 7-7" />
          </svg>
        </button>

      </aside>

      {!isVisible && (
        <button
          id="showBtn"
          onClick={() => setIsVisible(true)}
          className="fixed top-1/2 left-0 transform -translate-y-1/2 bg-[#7816db] text-white p-2 rounded-r-[15px] h-[130px]"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="w-6 h-16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3">
            <path strokeLinecap="round" strokeLinejoin="round" d="M9 5l7 7-7 7" />
          </svg>
        </button>
      )}
    </div>
  );
};

export default Sidebar;
