import React, { useEffect, useState, useRef } from 'react';
import unknown_photo from '../../assets/images/unknown.png';

const Frame1 = ({ path }) => {
  const [profile, setProfile] = useState({
    profilePhoto: null,
    username: 'Admin',
  });

  const [isOpen, setIsOpen] = useState(false);
  const menuRef = useRef(null);

  useEffect(() => {
    const handleClickOutside = (e) => {
      if (menuRef.current && !menuRef.current.contains(e.target)) {
        setIsOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  return (
    <div className="flex justify-between items-center py-4 bg-opacity-100 relative">
      <h1 className="text-[24pt] font-semibold text-black">{path}</h1>

      <div
        ref={menuRef}
        className="w-fit bg-white rounded-[12px] border-none flex items-center gap-2 px-4 py-2 cursor-pointer relative"
        onClick={() => setIsOpen(prev => !prev)}
      >
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
             strokeWidth="1.5" stroke="currentColor" className="size-6">
          <path strokeLinecap="round" strokeLinejoin="round"
                d="M14.857 17.082a23.848 23.848 0 0 0 5.454-1.31A8.967 8.967 0 0 1 18 9.75V9A6 6 0 0 0 6 9v.75a8.967 8.967 0 0 1-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 0 1-5.714 0" />
        </svg>

        {profile.profilePhoto ? (
          <img src={profile.profilePhoto} alt="Avatar" className="w-10 h-10 rounded-full object-cover" />
        ) : (
          <img src={unknown_photo} alt="Avatar" className="w-10 h-10 rounded-full object-cover" />
        )}

        <p>{profile.username}</p>

        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
             strokeWidth="1.5" stroke="currentColor" className="size-6">
          <path strokeLinecap="round" strokeLinejoin="round" d="m19.5 8.25-7.5 7.5-7.5-7.5" />
        </svg>

        {isOpen && (
          <div className="absolute right-0 top-[60px] w-48 bg-white border rounded-lg shadow-lg z-50">
            <ul className="py-2">
              <li className="px-4 py-2 hover:bg-gray-100 cursor-pointer">Профиль</li>
              <li className="px-4 py-2 hover:bg-gray-100 cursor-pointer">Настройки</li>
              <li className="px-4 py-2 hover:bg-gray-100 cursor-pointer text-red-500">Выйти</li>
            </ul>
          </div>
        )}
      </div>
    </div>
  );
};

export default Frame1;
  