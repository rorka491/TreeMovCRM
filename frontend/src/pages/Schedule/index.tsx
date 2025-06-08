import { Outlet, useMatch } from 'react-router-dom'
import CategoryBar from '../../components/page/CategoryBar'

export function Schedule() {
    const match = useMatch('/schedule/:lastPart')
    const activeSection = match?.params?.lastPart ?? 'by-teacher'

    return (
        <section>
            <CategoryBar
                activeSection={activeSection}
                categories={[
                    { url: 'by-teacher', label: 'По преподавателям' },
                    { url: 'by-group', label: 'По группам' },
                    { url: 'by-classroom', label: 'По аудиториям' },
                    { url: 'edit', label: 'Редактировать расписание' },
                ]}
            />

            <div className="mt-4">
                <Outlet />
            </div>
        </section>
    )
}

export default Schedule
