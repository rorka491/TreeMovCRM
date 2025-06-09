import Login from './pages/login'
import {
    Route,
    BrowserRouter as Router,
    Routes,
    Navigate,
} from 'react-router-dom'
import ScheduleByClassroom from './pages/Schedule/subpages/ScheduleByClassroom'
import ScheduleByGroup from './pages/Schedule/subpages/ScheduleByGroup'
import ScheduleByTeacher from './pages/Schedule/subpages/ScheduleByTeacher'
import Schedule from './pages/Schedule'
import Base from './components/page-defaults/Base'
import Employees from './pages/Employees'
import EmployeesMain from './pages/Employees/subpages/EmployeesMain'
import { StudentsPage } from './pages/Students'
import { StudentsMain } from './pages/Students/subpages/StudentsMain'
import { StudentProfile } from './pages/Students/subpages/StudentProfile'

function App() {
    return (
        <Router>
            <Routes>
                <Route path="*" element={<Base />}>
                    <Route path="schedule" element={<Schedule />}>
                        <Route
                            path="by-teacher"
                            element={<ScheduleByTeacher />}
                        />
                        <Route path="by-group" element={<ScheduleByGroup />} />
                        <Route
                            path="by-classroom"
                            element={<ScheduleByClassroom />}
                        />
                        <Route path="edit" element={<>...</>} />
                        <Route
                            path="*"
                            element={<Navigate to="../by-teacher" />}
                        />
                    </Route>
                    <Route path="employees" element={<Employees />}>
                        <Route path="main" element={<EmployeesMain />} />
                        <Route path="*" element={<Navigate to="../main" />} />
                    </Route>
                    <Route path="students" element={<StudentsPage />}>
                        <Route path="main" element={<StudentsMain />} />
                        <Route
                            path="profile/:studentId"
                            element={<StudentProfile />}
                        />
                        <Route path="*" element={<Navigate to="../main" />} />
                    </Route>
                </Route>
                <Route />
            </Routes>
        </Router>
    )
}

export default App
