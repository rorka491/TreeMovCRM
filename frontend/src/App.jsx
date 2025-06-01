import Base from './components/base/base';
import ScheduleByTeacher from './components/shedule/ScheduleByTeacher';
// import ScheduleByGroup from './components/shedule/ScheduleByGroup';
// import ScheduleByClassroom from './components/shedule/ScheduleByClassroom';
import Login from './pages/login'
import { 
  Route,
  BrowserRouter as Router, 
  Routes 
} from 'react-router-dom';
import React, { useState } from 'react';

function App() {
  // const [user, setUser] = useState(null);

  // if (!user) return <Login setUser={setUser} />;

  return (
    <Router>
      <Routes>
        <Route path='/*' element={<Base />} />
        <Route path="/schedules/by-teacher/" element={<ScheduleByTeacher />} />

      </Routes>
    </Router>
  );
}

export default App;