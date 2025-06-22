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
import { StudentProfileEdit } from './pages/Students/subpages/StudentProfileEdit'
import { StudentsGrades } from './pages/Students/subpages/StudentsGrades'
import { StudentsPayments } from './pages/Students/subpages/StudentsPayments'
import SheduleByMonth from './pages/Schedule/subpages/SheduleByMonth'
import SheduleByWeek from './pages/Schedule/subpages/SheduleByWeek'
import ScheduleByDay from './pages/Schedule/subpages/ScheduleByDay'

function App() {
    return (
        <Router>
            <Routes>
                <Route path="*" element={<Base />}>
                    <Route path="schedule" element={<Schedule />}>
                        <Route path="by-month" element={<SheduleByMonth />} />
                        <Route path="by-week" element={<SheduleByWeek />} />
                        <Route path="by-day" element={<ScheduleByDay />} />
                        <Route path="edit" element={<>...</>} />
                        <Route
                            path="*"
                            element={<Navigate to="../by-month" />}
                        />
                    </Route>
                    <Route path="employees" element={<Employees />}>
                        <Route path="main" element={<EmployeesMain />} />
                        <Route path="*" element={<Navigate to="../main" />} />
                    </Route>
                    <Route path="students" element={<StudentsPage />}>
                        <Route path="main" element={<StudentsMain />} />
                        <Route path="grades" element={<StudentsGrades />} />
                        <Route path="payments" element={<StudentsPayments />} />
                        <Route path="profile/:studentId">
                            <Route
                                path="edit"
                                element={<StudentProfileEdit />}
                            />
                            <Route path="*" element={<StudentProfile />} />
                        </Route>
                        <Route path="*" element={<Navigate to="../main" />} />
                    </Route>
                </Route>
                <Route />
            </Routes>
        </Router>
    )
}

export default App
