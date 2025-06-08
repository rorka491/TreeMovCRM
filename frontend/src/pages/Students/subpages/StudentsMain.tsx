import { FilterBar } from '../../../components/page/FilterBar'
import { api } from '../../../api'
import { StudentsTable } from '../components/StudentsTable'
import { useEffect, useState } from 'react'

export function StudentsMain() {
    const [filterData, setFilterData] = useState([
        {
            id: 'group',
            label: 'Группа',
            data: ['A', 'B'],
            multiple: true,
        },
        {
            id: 'student',
            label: 'Ученик',
            data: ['Иванов'],
            multiple: true,
        },
        {
            id: 'filters',
            label: 'Фильтр',
            data: ['Активные', 'Неактивные'],
        },
        {
            id: 'exportTypes',
            label: 'Экспорт',
            data: ['xlsx', 'csv', 'pdf'],
            default: 'xlsx',
        },
    ])

    useEffect(() => {
        ;(async () => {
            filterData[0].data = await api.students.getAllGroups()
            filterData[1].data = (await api.students.getAll()).map(
                (student) => student.fullName
            )
            setFilterData([...filterData])
        })()
    }, [])

    return (
        <>
            <FilterBar filterData={filterData} />
            <StudentsTable />
        </>
    )
}
