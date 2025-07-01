import { useState } from 'react'
import CategoryBar from '../../components/page/CategoryBar'
import { Outlet, useMatch, useNavigate } from 'react-router-dom'
import { debounce } from '../../lib/debounce'
import { api } from '../../api'
import { Student } from '../../api/api'

export function StudentsPage() {
    const match = useMatch('/:any/:lastPart/*')
    const navigate = useNavigate()

    const activeSection = match?.params?.lastPart

    const [searchStudents, setSearchStudents] = useState<Student[]>([])

    const onSearchChange = debounce((s: string) => {
        if (s === '') {
            return
        }

        api.students.getSearch(s).then(setSearchStudents)
    }, 400)
    console.log(searchStudents)
    return (
        <section className="flex h-[100%] flex-col gap-y-5">
            {activeSection !== 'profile' && (
                <CategoryBar
                    categories={[
                        { url: 'main', label: 'Основное' },
                        { url: 'grades', label: 'Оценки' },
                        { url: 'payments', label: 'Оплаты' },
                    ]}
                    activeSection={activeSection}
                    searchPlaceholder="Поиск в студентах..."
                    searchOptions={searchStudents.map((student) => ({
                        id: student.id,
                        object: student,
                        title: `${student.fullName} ${student.groups[0]}`,
                        onSelect: () =>
                            navigate('/students/profile/' + student.id),
                    }))}
                    onSearchInputChange={onSearchChange}
                />
            )}

            <Outlet />
        </section>
    )
}
