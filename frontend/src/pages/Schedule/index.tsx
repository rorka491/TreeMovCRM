import { Outlet } from 'react-router-dom'
import { FilterBar } from '../../components/page/FilterBar'
import { useState } from 'react'
import CalendarBar from '../../components/page/CalendarBar'

export function Schedule() {
    const [currentDate, setCurrentDate] = useState(new Date())
    const [filtersSelected, setFiltersSelected] = useState<{
        [k: string]: any | undefined
    }>({})
    const [filterData, setFilterData] = useState([
        {
            id: 'teacher',
            label: 'Преводователь',
            options: ['Роман', 'Никита', 'Родион'],
            multiple: true,
            search: true,
            removeButton: true,
        },
        {
            id: 'group',
            label: 'Группа',
            options: ['A', 'B'],
            multiple: true,
            search: true,
            removeButton: true,
        },
        {
            id: 'subject',
            label: 'Предмет',
            options: ['Информатика', 'История'],
            multiple: true,
            search: true,
            removeButton: true,
        },
        {
            id: 'data',
            label: 'Дата',
            options: ['11.11.1111', '11.22.3333'],
            search: true,
        },
        {
            id: 'auditorium',
            label: 'Аудитория',
            options: ['600', '1000'],
            multiple: true,
            search: true,
            removeButton: true,
        },
    ])
    return (
        <section className="flex h-[100%] flex-col gap-y-[16px]">
            <FilterBar
                filterData={filterData}
                selectedChange={setFiltersSelected}
            />
            <CalendarBar
                currentDate={currentDate}
                setCurrentDate={setCurrentDate}
            />
            <Outlet context={currentDate} />
        </section>
    )
}

export default Schedule
