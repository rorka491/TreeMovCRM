import React from 'react';
import Base from './components/base/base';

import { 
  Route,
  BrowserRouter as Router, 
  Routes 
} from 'react-router-dom';

function App() {
  return (
    <Router>
      <Routes>
        <Route path='/*' element={<Base />} />
        <Route path="/schedules/by-teacher/" element={<ScheduleByTeacher />} />
        <Route path="/schedules/by-group/" element={<ScheduleByGroup />} />
        <Route path="/schedules/by-classroom/" element={<ScheduleByClassroom />} />
      </Routes>
    </Router>
  );
}

export default App;