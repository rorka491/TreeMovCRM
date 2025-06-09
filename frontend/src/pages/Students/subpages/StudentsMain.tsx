import { FilterBar } from '../../../components/page/FilterBar'
import { api } from '../../../api'
import { StudentsTable } from '../components/StudentsTable'
import { useEffect, useState } from 'react'

export function StudentsMain() {
    const [filterData, setFilterData] = useState([
        {
            id: 'group',
            label: 'Группа',
            options: ['A', 'B'],
            multiple: true,
        },
        {
            id: 'student',
            label: 'Ученик',
            options: ['Иванов'],
            multiple: true,
        },
        {
            id: 'filters',
            label: 'Фильтр',
            options: ['Активные', 'Неактивные'],
        },
        {
            id: 'exportTypes',
            label: 'Экспорт',
            options: ['xlsx', 'csv', 'pdf'],
            default: 'xlsx',
        },
    ])

    useEffect(() => {
        ;(async () => {
            filterData[0].options = await api.students.getAllGroups()
            filterData[1].options = (await api.students.getAll()).map(
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
