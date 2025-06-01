import { useParams } from 'react-router-dom';
import Sidebar from './Sidebar'
import Frame1 from './frame1'; 
import SchedulePage from '../shedule/SchedulePage';
import React, { useEffect, useState } from 'react';





const Base = () => {
    const [isSidebarVisible, setIsSidebarVisible] = useState(true);
    const [section, setSection] = useState("Расписание");




    useEffect(() => {
      fetch('http://localhost:8000/api/schedules/')
        .then((res) => {
          return res.json();
        })
        .then((data) => setSchedules(data))
        .catch((err) => console.error("Ошибка при загрузке:", err));
    }, []);

    return (
        <div className="flex h-screen">
        <Sidebar 
            isVisible={isSidebarVisible} 
            setIsVisible={setIsSidebarVisible} 
            setSection={setSection}
        />
        <div className="flex-1 flex flex-col items-center justify-start px-10 py-4 h-screen overflow-y-auto">
          <div className="space-y-4 w-full max-w-[1800px]">
            <Frame1 path={section}/>    
            

            <div className="mt-2">
                {section === 'Расписание' && <SchedulePage />}
            </div>
          </div>
        </div>
        </div>
    )
}

export default Base;