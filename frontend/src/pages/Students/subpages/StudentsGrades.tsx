import { FilterBar } from '../../../components/page/FilterBar'
import { api } from '../../../api'
import { useEffect, useState } from 'react'
import { Table } from '../../../components/Table'
import { useNavigate } from 'react-router-dom'
import { Student } from '../../../api/fakeApi'
import { Grade } from '../../../api/api'
import { formatDate } from '../../../lib/formatDate'

export function StudentsGrades() {
    const [students, setStudents] = useState<Student[]>([])
    const [grades, setGrades] = useState<Grade[]>([])
    const [loaded, setLoaded] = useState(false)
    const navigate = useNavigate()

    useEffect(() => {
        ;(async () => {
            const students = await api.students.getAll()
            setStudents(students)
            const grades = await api.students.getAllGrades()
            console.log(grades)
            setGrades(grades)
            setLoaded(true)
            filterData[0].options = await api.students.getAllGroups()
            filterData[1].options = students.map((student) => student.fullName)
            setFilterData([...filterData])
        })()
    }, [])

    const [filtersSelected, setFiltersSelected] = useState<{
        [k: string]: any | undefined
    }>({})

    const [filterData, setFilterData] = useState([
        {
            id: 'group',
            label: 'Группа',
            options: ['A', 'B'],
            multiple: true,
            search: true,
            removeButton: true,
        },
        {
            id: 'student',
            label: 'Ученик',
            options: ['Иванов'],
            multiple: true,
            search: true,
            removeButton: true,
        },
        {
            id: 'active',
            label: 'Фильтр',
            options: ['Активные', 'Неактивные'],
            removeButton: true,
        },
        {
            id: 'exportTypes',
            label: 'Экспорт',
            options: ['xlsx', 'csv', 'pdf'],
            default: 'xlsx',
        },
    ])

    console.log(grades)

    return (
        <>
            <FilterBar
                filterData={filterData}
                selectedChange={setFiltersSelected}
            />
            <Table
                data={grades
                    .filter((grade) =>
                        filtersSelected.student &&
                        filtersSelected.student.length > 0
                            ? filtersSelected.student.some(
                                  (fullName) =>
                                      fullName === grade.student.fullName
                              )
                            : true
                    )
                    .filter((grade) =>
                        filtersSelected.active
                            ? (filtersSelected.active === 'Активные' &&
                                  grade.student.subscriptionActive) ||
                              (filtersSelected.active === 'Неактивные' &&
                                  !grade.student.subscriptionActive)
                            : true
                    )
                    .map((grade) => ({
                        ...grade,
                        studentFullName: grade.student.fullName,
                        subject: grade.lesson,
                        date: formatDate(
                            new Date(grade.lesson.date),
                            'HH:MIN DD.MM.YYYY'
                        ),
                        teacherFullName: `${grade.lesson.teacher.employer.surname} ${grade.lesson.teacher.employer.name} ${grade.lesson.teacher.employer.patronymic}`,
                        grade: [
                            'Плохо',
                            'Удовлетворительно',
                            'Хорошо',
                            'Отлично',
                        ][grade.value - 2],
                        comment: grade.comment || 'Нет',
                    }))}
                keys={{
                    studentFullName: 'Ученик',
                    date: 'Дата урока',
                    teacherFullName: 'Преподаватель',
                    grade: 'Оценка',
                    comment: 'Комментарий преподавателя',
                }}
                conditionalClassNames={{
                    grade: (studentGrade) =>
                        ({
                            Отлично: 'text-[#22C55E]',
                            Хорошо: 'text-[#22C55E]',
                            Удовлетворительно: 'text-[#FFAB25]',
                            Плохо: 'text-[#FF1814]',
                        })[studentGrade.grade] ?? '',
                }}
                rowActions={{}}
                showSkeleton={!loaded}
                skeletonAmount={18}
            />
        </>
    )
}
