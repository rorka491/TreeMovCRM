import { useState } from 'react';
import CategoryBar from './CategoryBar';
import ScheduleByTeacher from './ScheduleByTeacher';
import ScheduleByGroup from './ScheduleByGroup'
import ScheduleByClassroom from './ScheduleByClassroom'


function SchedulePage() {
    const [activeSection, setActiveSection] = useState('teacher');

    return (
        <div>
            <CategoryBar activeSection={activeSection} setActiveSection={setActiveSection} />

            <div className="mt-4">
                {activeSection === 'teacher' && <ScheduleByTeacher/>}
                {activeSection === 'group' && <ScheduleByGroup/>}
                {activeSection === 'classroom' && <ScheduleByClassroom/>}
                {activeSection === 'edit' && '...'}
            </div>
        </div>
    );
}

export default SchedulePage;
