import { filter, FilterBar } from '../../../components/page/FilterBar'
import { api } from '../../../api'
import { useEffect, useState } from 'react'
import { Table } from '../../../components/Table'
import { useNavigate } from 'react-router-dom'
import { Student } from '../../../api/fakeApi'

export function StudentsMain() {
    const [students, setStudents] = useState<Student[]>([])
    const [loaded, setLoaded] = useState(false)
    const navigate = useNavigate()

    useEffect(() => {
        ;(async () => {
            const students = await api.students.getAll()
            setStudents(students)
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
            id: 'groups',
            label: 'Группа',
            options: ['A', 'B'],
            multiple: true,
            search: true,
            removeButton: true,
        },
        {
            id: 'fullName',
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

    return (
        <>
            <FilterBar
                filterData={filterData}
                selectedChange={setFiltersSelected}
            />
            <Table
                data={filter(
                    students,
                    {
                        groups: {
                            type: 'array-vs-array',
                        },
                        fullName: {
                            type: 'includes',
                        },
                        subscriptionActive: {
                            type: 'equal',
                            filterId: 'active',
                            mapValue: (val) =>
                                val ? 'Активные' : 'Неактивные',
                        },
                    },
                    filtersSelected
                )}
                keys={{
                    fullName: 'Ученик',
                    dateOfBirth: 'Дата рождения',
                    groups: 'Группа',
                    phone: {
                        type: 'map',
                        str: 'Телефон',
                        f: (student) => student.phone ?? 'Нету',
                    },
                    email: {
                        type: 'map',
                        str: 'Почта',
                        f: (student) => student.email ?? 'Нету',
                    },
                }}
                rowActions={{
                    Открыть: (student) =>
                        navigate('/students/profile/' + student.id),
                    Изменить: (student) =>
                        navigate('/students/profile/' + student.id + '/edit'),
                    Удалить: () => {
                        //TODO!
                    },
                }}
                showSkeleton={!loaded}
                skeletonAmount={18}
            />
        </>
    )
}
